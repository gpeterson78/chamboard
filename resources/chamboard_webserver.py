import http.server
import json
import os
from urllib.parse import parse_qs

# Paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
COMMENTS_FILE = os.path.join(BASE_DIR, "data", "comments.json")
CONFIG_FILE = os.path.join(BASE_DIR, "data", "config.json")

# Ensure necessary directories exist
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)

class ChamboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/comments":
            self.send_json_comments()
        elif self.path == "/config":
            self.send_json_config()
        else:
            # Serve static files from DOCS_DIR
            self.path = os.path.join(DOCS_DIR, self.path.lstrip("/"))
            super().do_GET()

    def do_POST(self):
        if self.path == "/update_config":
            self.handle_update_config()
        elif self.path == "/add_comment":
            self.handle_add_comment()
        else:
            self.send_error(404, "Endpoint not found")

    def send_json_comments(self):
        """Serve the last 6 comments."""
        comments = self.load_json_file(COMMENTS_FILE, {"comments": []})
        self.respond_with_json({"comments": comments["comments"][-6:]})

    def send_json_config(self):
        """Serve the configuration file."""
        config = self.load_json_file(CONFIG_FILE, {"url": "http://default-url.com"})
        self.respond_with_json(config)

    def handle_update_config(self):
        """Update the configuration file."""
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        self.save_json_file(CONFIG_FILE, post_data)
        self.respond_with_json({"success": True, "message": "Configuration updated"})

    def handle_add_comment(self):
        """Add a new comment to the comments file."""
        content_length = int(self.headers["Content-Length"])
        post_data = json.loads(self.rfile.read(content_length))
        comments = self.load_json_file(COMMENTS_FILE, {"comments": []})

        new_comment = {
            "author": post_data.get("author", "Unknown"),
            "text": post_data.get("text", ""),
            "timestamp": post_data.get("timestamp", "")
        }
        comments["comments"].append(new_comment)
        comments["comments"] = comments["comments"][-6:]  # Keep only last 6
        self.save_json_file(COMMENTS_FILE, comments)

        self.respond_with_json({"success": True, "message": "Comment added"})

    def respond_with_json(self, data):
        """Helper to send JSON responses."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def load_json_file(self, path, default):
        """Load a JSON file or return default if it doesn't exist."""
        if os.path.exists(path):
            with open(path, "r") as file:
                return json.load(file)
        return default

    def save_json_file(self, path, data):
        """Save data to a JSON file."""
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    PORT = 8080
    os.chdir(DOCS_DIR)  # Serve static files from DOCS_DIR
    server = http.server.HTTPServer(("0.0.0.0", PORT), ChamboardHandler)
    print(f"Serving at http://localhost:{PORT}")
    server.serve_forever()
