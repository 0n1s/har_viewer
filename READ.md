# HAR Analyzer

## Description

HAR Analyzer is a Flask-based web application designed to parse, filter, and analyze HTTP Archive (HAR) files. This tool provides an interactive UI where users can upload a HAR file, apply multiple filters to extract relevant network request details, and view the results in a structured format. Users can also expand individual requests to see complete request and response data.

## Features

- **Upload HAR Files**: Supports `.har` file uploads for analysis.
- **Advanced Filtering**: Filter requests by:
  - HTTP Method (GET, POST, PUT, DELETE, etc.)
  - URL matching (full or partial)
  - HTTP Status Codes (200, 404, etc.)
  - Request time (min/max response time in milliseconds)
  - Cookies
  - Headers
  - Query Parameters
- **Expandable Results Table**: Click on any request to expand and view the full request and response data.
- **Download Filtered Results**: Save filtered HAR data as JSON for further analysis.

## Installation

### Prerequisites

Ensure you have Python installed (>=3.8). You will also need Flask and other dependencies installed.

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/har-analyzer.git
   cd har-analyzer
   ```

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```sh
   flask run
   ```
   The app will be available at: `http://127.0.0.1:5000`

## Usage

1. Open the web app in your browser.
2. Upload a `.har` file.
3. Apply filters as needed.
4. Click on a request to expand and view details.
5. Download filtered results if required.

## File Structure

```
├── app.py               # Flask backend
├── templates
│   ├── index.html       # Frontend UI
├── static
│   ├── style.css        # Styles (if any)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
```

## Contributing

1. Fork the repository.
2. Create a new branch (`feature-xyz`).
3. Commit your changes and push.
4. Submit a Pull Request.

## License

This project is licensed under the MIT License..
