### **Current Site: WordPress API Scraper**

The existing site uses a WordPress API to fetch and display the latest comments. It does so by:

1. **Fetching Comments from WordPress**:
    - The API URL (`scrape_url`) points to the WordPress REST API endpoint (e.g., `https://example.com/wp-json/wp/v2/comments?post=1234`).
    - The API returns comments in JSON format, with fields like:
        - `author_name`: The name of the person who posted the comment.
        - `content.rendered`: The HTML-rendered content of the comment.
        - `date`: The timestamp of when the comment was posted.
2. **Displaying the Last 6 Comments**:
    - The script retrieves the latest comments from the JSON response, sorts them (if needed), and displays the 6 most recent ones.
    - Each comment is rendered into an HTML block that includes:
        - The author’s name.
        - The comment’s content.
        - The date.

---

### **Updated Site: Switchable Backends**

The updated implementation introduces a **configurable backend** to support both:

1. **External WordPress API** (existing functionality).
2. **Internal Message Server** (new functionality hosted by your Chamboard backend).

#### **How It Works**

1. **Configuration via `/config`**:
    - The backend hosts a `/config` endpoint that returns the current configuration in `config.json`.
    - This configuration determines:
        - Whether to use the external WordPress API or the internal server (`use_backend`).
        - The URL of the external WordPress API (`scrape_url`).
        - The URL of the internal backend (`backend_url`).
2. **Dynamic Backend Switching**:
    - The JavaScript fetches the `/config` data to decide which API to use:
        - **External WordPress API**:
            - Uses `scrape_url` to fetch the comments.
        - **Internal API**:
            - Uses `backend_url/comments` to fetch the comments.
3. **Rendering Comments**:
    - Both the external WordPress API and internal API return comments in JSON format.
    - The script dynamically adjusts for field differences between the APIs:
        - WordPress: `author_name`, `content.rendered`, `date`.
        - Internal: `author`, `text`, `timestamp`.
4. **Error Handling**:
    - Displays an error message if fetching data fails (e.g., API unreachable, malformed JSON, etc.).

---

### **Internal Message Server**

The internal API adds the ability to:

1. **Fetch Comments**:
    - The `/comments` endpoint returns comments stored in `comments.json`.
    - The format is:
        ```json
        {
          "comments": [
            {"author": "Alice", "text": "Hello!", "timestamp": "2024-12-17T10:00:00Z"},
            {"author": "Bob", "text": "Welcome!", "timestamp": "2024-12-17T11:00:00Z"}
          ]
        }
        ```
2. **Post New Comments**:
    - The `/add_comment` endpoint accepts POST requests with JSON payloads like:
        ```json
        {
          "author": "Charlie",
          "text": "This is a test message.",
          "timestamp": "2024-12-17T12:00:00Z"
        }
        ```
    - New comments are appended to `comments.json`, and the server ensures only the last 6 comments are kept.

---

### **New Settings Page**

1. **Switch Between Backends**:
    - A checkbox allows you to toggle between the WordPress API (`scrape_url`) and the internal backend (`backend_url`).
2. **Post Messages**:
    - When using the internal backend, additional inputs allow you to post a message (`author`, `text`) to `/add_comment`.
3. **Save Configuration**:
    - The settings page updates `config.json` via `/update_config`, ensuring the configuration persists.

---

### **Final Workflow**

1. **Start with WordPress API**:
    - By default, the site uses the external WordPress API to scrape and display comments.
2. **Switch to Internal API**:
    - Use the settings page to toggle the `use_backend` checkbox, enabling the internal server as the source.
    - Post messages to the internal server and see them displayed on the main page.
3. **Dynamically Display Comments**:
    - The main page automatically adjusts its data source (`scrape_url` or `backend_url`) based on the current configuration.

---

### **Why This is Useful**

- **Flexibility**: You can dynamically switch between external and internal backends without modifying the site’s code.
- **Local Control**: The internal server enables offline functionality and allows posting custom messages.
- **Consistent UI**: The frontend uses the same layout and logic regardless of the data source, ensuring a unified user experience.