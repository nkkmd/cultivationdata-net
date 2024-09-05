# Markdown Viewer: Documentation

## 1. Overview

This Markdown Viewer system is a lightweight solution for dynamically converting specified Markdown files to HTML and displaying them as web pages. It uses URL parameters to specify the Markdown file and employs JavaScript to asynchronously fetch, convert, and display the file.

## 2. System Configuration

The system primarily consists of two files:
1. JavaScript file (md.js): Provides the main functionality.
2. HTML file: Provides the basic page structure and loads the necessary scripts.

Additionally, it uses the external library `marked.js` to convert Markdown to HTML.

## 3. JavaScript File (md.js)

### Key Functions

1. `getMarkdownUrlFromParams()`
   - Purpose: Retrieves the URL of the Markdown file from URL parameters.
   - Operation: Parses URL parameters from `window.location.search` and returns the value of the `md` parameter.

2. `convertMarkdownToHtml(url)`
   - Purpose: Fetches the Markdown file from the specified URL and converts it to HTML.
   - Operation:
     - Uses `fetch` to asynchronously retrieve the Markdown file.
     - If successful, uses `marked.parse()` to convert Markdown to HTML.
     - If an error occurs, outputs the error to the console and returns `null`.

3. `extractH1Content(html)`
   - Purpose: Extracts the content of the first h1 tag from the converted HTML.
   - Operation: Uses DOMParser to parse the HTML and returns the text content of the first h1 tag.

4. `main()`
   - Purpose: Performs the main application processing.
   - Operation:
     - Sets the base URL for Markdown files.
     - Retrieves the Markdown filename from URL parameters.
     - If the parameter doesn't exist, displays an error message and ends processing.
     - Fetches the Markdown, converts it to HTML, and displays it on the page.
     - Extracts the content of the h1 tag and sets it as the page title.
     - If conversion fails, displays an error message.

### Code for JavaScript File (md.js)

```javascript
// Function to get the Markdown file URL from URL parameters
function getMarkdownUrlFromParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('md');
}

// Function to fetch Markdown file and convert it to HTML
async function convertMarkdownToHtml(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdown = await response.text();
        return marked.parse(markdown);
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Function to extract h1 tag content from HTML
function extractH1Content(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const h1 = doc.querySelector('h1');
    return h1 ? h1.textContent : null;
}

// Main processing
async function main() {
    const URL = 'https://raw.githubusercontent.com/username/repository/branch/'; // URL where Markdown files are located
    const mdFile = getMarkdownUrlFromParams();
    const errorElement = document.getElementById('error');
    const contentElement = document.getElementById('content');

    if (!mdFile) {
        errorElement.textContent = 'No Markdown file specified in URL parameters. (?md=sample/file.md)';
        return;
    }

    const html = await convertMarkdownToHtml(`${URL}${mdFile}`);
    if (html) {
        contentElement.innerHTML = html;
        
        // Extract h1 tag content and set as title
        const h1Content = extractH1Content(html);
        if (h1Content) {
            document.title = `${h1Content}`;
        }
    } else {
        errorElement.textContent = 'Conversion failed or file not found.';
    }
}

// Execute on page load
window.onload = main;
```

## 4. HTML File

### Structure Explanation

1. `<head>` section
   - Sets character encoding to UTF-8.
   - Includes a dynamically changeable `<title>` tag.
   - Loads the `marked` library (from CDN) and custom JavaScript file (md.js).

2. `<body>` section
   - `<div id="error">`: Element for displaying error messages.
   - `<div id="content">`: Element for displaying converted Markdown content.

### HTML File Code

```html
<html>
<head>
    <meta charset="UTF-8">
    <title></title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="./md.js"></script>
</head>
<body>
    <div id="error"></div>
    <div id="content"></div>
</body>
</html>
```

## 5. Usage

1. Host the HTML file and JavaScript file (md.js) on a web server.
2. Use the URL parameter `md` to specify the Markdown file you want to display.
   Example: `https://yourserver.com/index.html?md=sample/file.md`
3. When accessing the page, the specified Markdown file will be loaded and displayed as HTML.
4. The first h1 tag in the Markdown will be used as the page title.

## 6. Markdown File Compatibility

While this system is exemplified for displaying Markdown files on GitHub, it can be used with Markdown files from other sources for the following reasons:

1. Generic fetch API: The `convertMarkdownToHtml` function uses the `fetch` API, which can retrieve resources from any URL.

2. Flexible URL configuration: By appropriately setting the `URL` variable in the `main` function, any base URL can be specified.

3. Versatility of marked.js: The `marked` library used supports a wide range of standard Markdown syntax, enabling source-independent conversion.

4. Parameter-based design: The design using URL parameters to specify Markdown files allows flexible handling of any file path or URL.

However, when using Markdown files from different sources, note the following:

- CORS (Cross-Origin Resource Sharing) policy: Proper CORS settings are necessary for fetching files from external sources.
- File structure and URL format: Different platforms or servers may have different file structures or URL formats, which may require adjustments.
- Security: Caution is needed regarding security risks when displaying Markdown files from untrusted sources.

## 7. Important Notes

- Be aware of Cross-Origin Resource Sharing (CORS) restrictions. Appropriate server configuration may be necessary.
- Error handling is implemented, but content may not display due to network issues or file non-existence.
- For security reasons, it is recommended to use Markdown files only from trusted sources.
- Full compatibility is not guaranteed when using different Markdown dialects or extended syntax. Use of standard Markdown syntax is recommended.
- This system provides basic functionality. Additional development is needed for more advanced features (e.g., automatic table of contents generation, styling customization).

---
- Created: 2024-9-5
- Updated: 2024-9-5