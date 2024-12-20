import os
import json
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define paths
BASE_DIR = os.path.expanduser("~/chamboard")
DOCS_DIR = os.path.join(BASE_DIR, "docs")  # Static files like chamboard.jpeg
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")  # Dynamic files and APIs
CONFIG_FILE = os.path.join(RESOURCES_DIR, "config.json")
COMMENTS_FILE = os.path.join(RESOURCES_DIR, "comments.json")

# Serve main.html from RESOURCES_DIR
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_main(path):
    if path == "" or path == "main.html":
        return send_from_directory(RESOURCES_DIR, "main.html")
    elif path == "chamboard.jpeg":
        return send_from_directory(DOCS_DIR, "chamboard.jpeg")
    else:
        return "404: File Not Found", 404

# Serve settings.html from RESOURCES_DIR
@app.route('/settings.html')
def serve_settings():
    return send_from_directory(RESOURCES_DIR, "settings.html")

# API endpoint: Get configuration
@app.route('/config', methods=['GET'])
def get_config():
    with open(CONFIG_FILE, 'r') as f:
        return jsonify(json.load(f))

# API endpoint: Update configuration
@app.route('/update_config', methods=['POST'])
def update_config():
    config = request.json
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    return jsonify({"message": "Configuration updated."})

# API endpoint: Get comments
@app.route('/comments', methods=['GET'])
def get_comments():
    try:
        # Load comments from the local JSON file
        with open(COMMENTS_FILE, 'r') as f:
            comments_data = json.load(f)

        # Format the local comments to match the WordPress API essentials
        formatted_comments = [
            {
                "id": idx,  # Generate a unique ID
                "author_name": comment.get("author", "Anonymous"),
                "content": {"rendered": comment.get("text", "No content")},
                "date": comment.get("timestamp", "Unknown date")
            }
            for idx, comment in enumerate(comments_data.get("comments", []))
        ]

        # Return a flat array of comments
        return jsonify(formatted_comments)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoint: Add a comment
@app.route('/add_comment', methods=['POST'])
def add_comment():
    try:
        new_comment = request.json  # Get JSON payload from the POST request
        if not new_comment:
            return jsonify({"success": False, "message": "No data provided"}), 400

        # Load existing comments
        if os.path.exists(COMMENTS_FILE):
            with open(COMMENTS_FILE, 'r') as f:
                comments_data = json.load(f)
        else:
            comments_data = {"comments": []}

        # Append the new comment
        comments_data["comments"].append(new_comment)

        # Save updated comments back to file
        with open(COMMENTS_FILE, 'w') as f:
            json.dump(comments_data, f, indent=4)

        return jsonify({"success": True, "message": "Comment added successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Add a new API endpoint: Delete the last comment
@app.route('/delete_last_comment', methods=['DELETE'])
def delete_last_comment():
    try:
        # Check if the comments file exists
        if not os.path.exists(COMMENTS_FILE):
            return jsonify({"success": False, "message": "No comments to delete."}), 404

        # Load existing comments
        with open(COMMENTS_FILE, 'r') as f:
            comments_data = json.load(f)

        # Check if there are comments to delete
        if not comments_data.get("comments"):
            return jsonify({"success": False, "message": "No comments to delete."}), 404

        # Remove the last comment
        comments_data["comments"].pop()

        # Save updated comments back to the file
        with open(COMMENTS_FILE, 'w') as f:
            json.dump(comments_data, f, indent=4)

        return jsonify({"success": True, "message": "Last comment deleted successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)