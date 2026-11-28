# Markdown Viewer: Documentation

## 1. Overview

The viewer fetches a Markdown file, converts it to HTML with marked.js, and displays it in a web page. MathJax 3 renders TeX mathematics after the content is inserted. Display equations delimited by `$$ ... $$` are protected before Markdown conversion so that TeX commands, subscripts, and line breaks are preserved.

## 2. System Configuration

- `md-to-web.html`: Page structure, library loading, MathJax configuration, and a content observer.
- `js/md-to-web.js`: URL parameters, fetching, equation protection, Markdown conversion, page title, and breadcrumbs.
- marked.js: Markdown-to-HTML conversion.
- MathJax 3 (`tex-mml-chtml.js`): TeX rendering.

The HTML must provide elements with IDs `header`, `error`, `breadcrumbs`, and `content`. The production page also includes site styling, notices, and a footer, which are omitted from the minimal example below.

## 3. Parameters and Processing

| Parameter | Meaning |
|---|---|
| `md` (required) | Repository-relative Markdown path, such as `AgriculturalManagement/model/sustainable_resource_optimization_model.md`. |
| `bc` (optional) | Breadcrumb category. `agricultural-management` links to `./blog-agricultural-management.html`. |

The current implementation fetches files from `https://raw.githubusercontent.com/nkkmd/cultivationdata-net/main/`. The `md` parameter is a relative path, not an arbitrary external URL. Each path segment is URL-encoded while directory separators are retained.

### Functions

- `getMarkdownUrlFromParams()`: Reads `md`.
- `getBreadcrumbsFromParams()`: Reads `bc`.
- `escapeHtml(text)`: Escapes text for insertion into HTML. This is not a sanitizer for the complete converted Markdown.
- `convertMarkdownToHtml(url)`: Fetches Markdown, temporarily replaces display equations with unique placeholders, calls `marked.parse()`, then restores HTML-escaped equations. Returns `null` on fetch or conversion failure.
- `extractH1Content(html)`: Extracts the first Markdown-derived `h1` text.
- `main()`: Inserts the content, source link, title, and breadcrumbs. Uses the Markdown path as a fallback when there is no `h1`. Runs through a `load` event listener.

### JavaScript: js/md-to-web.js

The following is the deployed script as checked on 2026-11-28; comments are retained in Japanese.

```javascript
// URLパラメーターからMarkdownファイルのパスを取得
function getMarkdownUrlFromParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('md');
}

// URLパラメーターからパンくずリンクの種類を取得
function getBreadcrumbsFromParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('bc');
}

// HTML内のテキストとして使えるようにエスケープ
function escapeHtml(text) {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Markdownを取得し、数式を保護してHTMLに変換
async function convertMarkdownToHtml(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const markdown = await response.text();
        const equations = [];

        // 元の文書に存在しない、一時置換用の識別子を作成
        let placeholderPrefix = 'MATHBLOCKPLACEHOLDER';

        while (markdown.includes(placeholderPrefix)) {
            placeholderPrefix += 'X';
        }

        // $$ ... $$ の内容をMarkdown変換から保護
        const protectedMarkdown = markdown.replace(
            /\$\$[\s\S]*?\$\$/g,
            (equation) => {
                const key =
                    `${placeholderPrefix}${equations.length}END`;

                equations.push(equation);
                return key;
            }
        );

        const html = marked.parse(protectedMarkdown);

        const placeholderPattern = new RegExp(
            `${placeholderPrefix}(\\d+)END`,
            'g'
        );

        // 数式を戻す。数式中の \\ や _ はそのまま維持する
        return html.replace(
            placeholderPattern,
            (_, index) => escapeHtml(equations[Number(index)])
        );
    } catch (error) {
        console.error('Markdown conversion failed:', error);
        return null;
    }
}

// HTMLから最初のh1のテキストを取得
function extractH1Content(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const h1 = doc.querySelector('h1');

    return h1 ? h1.textContent : null;
}

// メイン処理
async function main() {
    const mdFile = getMarkdownUrlFromParams();
    const bcLink = getBreadcrumbsFromParams();

    const errorElement = document.getElementById('error');
    const headerElement = document.getElementById('header');
    const breadcrumbsElement = document.getElementById('breadcrumbs');
    const contentElement = document.getElementById('content');

    if (!mdFile) {
        errorElement.textContent =
            'No Markdown file specified in the URL parameters.';
        return;
    }

    const encodedPath = mdFile
        .split('/')
        .map((part) => encodeURIComponent(part))
        .join('/');

    const markdownUrl =
        `https://raw.githubusercontent.com/nkkmd/cultivationdata-net/main/${encodedPath}`;

    const githubUrl =
        `https://github.com/nkkmd/cultivationdata-net/blob/main/${encodedPath}`;

    const html = await convertMarkdownToHtml(markdownUrl);

    if (html === null) {
        errorElement.textContent =
            'Conversion failed or file not found.';
        return;
    }

    errorElement.textContent = '';

    headerElement.innerHTML =
        `<div>This page displays content loaded from a Markdown file on ` +
        `<a href="${escapeHtml(githubUrl)}" target="_blank" ` +
        `rel="noopener noreferrer">GitHub</a>.</div>`;

    contentElement.innerHTML = html;

    // 最初のh1をページタイトルとパンくずに使用
    const h1Content = extractH1Content(html);
    const pageTitle = h1Content || mdFile;

    document.title = `${pageTitle} - cultivationdata.net`;

    if (bcLink) {
        const blogUrl =
            `./blog-${encodeURIComponent(bcLink)}.html`;

        breadcrumbsElement.innerHTML =
            `<div><small>` +
            `<a href="./">Home</a> &gt; ` +
            `<a href="${escapeHtml(blogUrl)}">Blog</a> &gt; ` +
            `${escapeHtml(pageTitle)}` +
            `</small></div><br />`;
    } else {
        breadcrumbsElement.innerHTML =
            `<div><small>` +
            `<a href="./">Home</a> &gt; ` +
            `${escapeHtml(pageTitle)}` +
            `</small></div><br />`;
    }
}

// ページ読み込み完了後に実行
window.addEventListener('load', main);
```

## 4. HTML and MathJax

Set `window.MathJax` before loading MathJax. The content observer requests typesetting when converted HTML is inserted into `content`. The following minimal example follows the production page's configuration and observer.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown to Web Page - cultivationdata.net</title>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            },
            options: {
                ignoreHtmlClass: 'tex2jax_ignore',
                processHtmlClass: 'tex2jax_process'
            }
        };
    </script>
    <script id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="./js/md-to-web.js"></script>
</head>
<body>
    <div id="header"></div>
    <div id="error"></div>
    <div id="breadcrumbs"></div>
    <div id="content"></div>
    <script>
        const targetNode = document.getElementById('content');
        const observer = new MutationObserver(() => {
            if (window.MathJax && window.MathJax.typesetPromise) {
                MathJax.typesetPromise([targetNode]);
            }
        });
        observer.observe(targetNode, { childList: true });
    </script>
</body>
</html>
```

The script only performs fetching and Markdown conversion; the HTML supplies MathJax rendering. If equations remain as TeX, check that MathJax loaded and typesetting ran after insertion. The observer only calls `typesetPromise()` when it is available; it does not itself wait for initialization or retry a failed request.

## 5. Writing Equations

Use ordinary TeX inside display delimiters. Use `_` for subscripts and two backslashes (`\\`) for a row break in `aligned`. Do not add Markdown escapes inside the protected display equation.

```latex
$$
\begin{aligned}
\text{minimize}_{\mathbf{x}}\quad
& \left(R_1(\mathbf{x}),\ldots,R_n(\mathbf{x})\right) \\
\text{subject to}\quad
& Y(\mathbf{x}) \geq Y_{\min}, \\
& \Pi(\mathbf{x}) \geq \Pi_{\min}, \\
& \mathbf{S}_{t+T}(\mathbf{x}) \succeq \mathbf{S}_t.
\end{aligned}
$$
```

Without protection, Markdown processing can turn two backslashes into one before MathJax sees them. The viewer prevents this by processing in this order:

1. Save each `$$ ... $$` expression and replace it with a placeholder absent from the original text.
2. Convert the remaining Markdown to HTML.
3. Restore equations as HTML-escaped text, preserving their TeX characters.
4. Insert the HTML and let MathJax typeset it.

HTML escaping preserves characters such as `&` as text in the DOM, allowing MathJax to read alignment markers without interpreting them as HTML.

The protection currently covers only `$$ ... $$`. Inline mathematics (`$ ... $`, `\(...\)`) and `\[...\]` are configured in MathJax but are not protected from Markdown conversion. The regular expression is not a full Markdown parser and also matches paired double-dollar delimiters inside code examples; do not assume all combinations of code and math syntax are supported.

## 6. Usage and Troubleshooting

1. Deploy the HTML and `js/md-to-web.js` on the web server.
2. Open a URL such as:
   `https://www.cultivationdata.net/md-to-web.html?md=AgriculturalManagement/model/sustainable_resource_optimization_model.md&bc=agricultural-management`
3. Confirm the content, title, breadcrumbs, and equation rows.
4. After updating JavaScript, use Ctrl+F5 to reload without the usual browser cache. If an old version persists, also check server or CDN caching.

If content is missing, check the browser console and Network panel for JavaScript errors, failed library loads, CORS errors, or missing Markdown files. If only equation line breaks are missing, check that the updated script is loaded and the source contains two backslashes per row break.

## 7. Compatibility and Limits

The base URLs in `main()` must be changed to use another repository or host; the source link must be adjusted as well. External hosts must allow browser fetching through CORS.

Only use trusted Markdown: converted HTML is inserted with `innerHTML`, and equation escaping does not sanitize the rest of the document. Relative links and images are resolved by the browser against the viewer page unless separately rewritten. GitHub-specific syntax and rendering are not guaranteed to match. Library URLs are not fully version-pinned, so library updates can affect behavior.

---

- Created: 2024-09-05
- Updated: 2026-11-28
