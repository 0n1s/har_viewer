from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import re
from io import StringIO

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

data_store = {"entries": []}  # Temporary storage for HAR data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_har():
    global data_store
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        har_data = json.load(file)
        data_store["entries"] = har_data.get("log", {}).get("entries", [])
        return jsonify({
            "message": "HAR file uploaded successfully",
            "total_requests": len(data_store["entries"])
        })
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid HAR file format"}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500


@app.route('/filter', methods=['GET'])
def filter_requests():
    global data_store

    if not data_store["entries"]:
        return jsonify({"error": "No HAR file uploaded"}), 400

    try:
        method = request.args.get('method', '').upper() or None
        url_filter = request.args.get('url', '') or None
        status_code = request.args.get('status_code', '') or None
        min_time = request.args.get('min_time', type=int, default=None)
        max_time = request.args.get('max_time', type=int, default=None)
        request_content = request.args.get('request_content', '') or None
        response_content = request.args.get('response_content', '') or None
        cookie_filter = request.args.get('cookie', '') or None
        header_filter = request.args.get('header', '') or None
        query_param_filter = request.args.get('query_param', '') or None
        min_request_size = request.args.get('min_request_size', type=int, default=None)
        max_request_size = request.args.get('max_request_size', type=int, default=None)
        min_response_size = request.args.get('min_response_size', type=int, default=None)
        max_response_size = request.args.get('max_response_size', type=int, default=None)

        filtered_entries = []

        for entry in data_store["entries"]:
            req_data = entry.get("request", {})
            response = entry.get("response", {})

            if method and req_data.get("method") != method:
                continue
            if url_filter and url_filter not in req_data.get("url", ""):
                continue
            if status_code and str(response.get("status")) != status_code:
                continue
            if min_time and entry.get("time", 0) < min_time:
                continue
            if max_time and entry.get("time", 0) > max_time:
                continue
            if request_content and request_content not in json.dumps(req_data.get("postData", {})):
                continue
            if response_content and response_content not in json.dumps(response.get("content", {})):
                continue
            if cookie_filter:
                cookies = req_data.get("cookies", [])
                if not any(cookie_filter in c.get("name", "") for c in cookies):
                    continue
            if header_filter:
                headers = req_data.get("headers", [])
                if not any(header_filter.lower() in h.get("name", "").lower() for h in headers):
                    continue
            if query_param_filter:
                url_parts = req_data.get("url", "").split('?')
                if len(url_parts) > 1 and query_param_filter not in url_parts[1]:
                    continue
            if min_request_size and req_data.get("bodySize", 0) < min_request_size:
                continue
            if max_request_size and req_data.get("bodySize", 0) > max_request_size:
                continue
            if min_response_size and response.get("bodySize", 0) < min_response_size:
                continue
            if max_response_size and response.get("bodySize", 0) > max_response_size:
                continue

            filtered_entries.append(entry)

        return jsonify({"total_results": len(filtered_entries), "entries": filtered_entries})

    except Exception as e:
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500

@app.route('/download', methods=['GET'])
def download_filtered():
    global data_store
    
    if not data_store["entries"]:
        return jsonify({"error": "No HAR file uploaded"}), 400
    
    output = json.dumps(data_store, indent=4)
    file_stream = StringIO(output)
    return send_file(
        file_stream, as_attachment=True, mimetype="application/json", download_name="filtered_har.json"
    )

if __name__ == '__main__':
    app.run(debug=True)
