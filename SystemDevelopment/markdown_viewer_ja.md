# Markdown Viewer: ドキュメント

## 1. 概要

指定されたMarkdownファイルを取得し、marked.jsでHTMLに変換してWebページとして表示します。コンテンツの挿入後にMathJax 3でTeX数式を描画します。`$$ ... $$` で囲まれた別行立て数式はMarkdown変換前に保護し、TeX命令・下付き・改行を維持します。

## 2. システム構成

- `md-to-web.html`：ページ構造、ライブラリの読み込み、MathJaxの設定、コンテンツの変更監視。
- `js/md-to-web.js`：URLパラメーターの取得、ファイル取得、数式保護、Markdown変換、タイトルとパンくずの設定。
- marked.js：MarkdownからHTMLへの変換。
- MathJax 3（`tex-mml-chtml.js`）：TeX数式の描画。

HTMLには `header`、`error`、`breadcrumbs`、`content` の各IDを持つ要素が必要です。公開ページにあるスタイル、お知らせ、フッターは、以下の最小構成例では省略しています。

## 3. パラメーターと処理

| パラメーター | 意味 |
|---|---|
| `md`（必須） | リポジトリ内のMarkdown相対パス。例：`AgriculturalManagement/model/sustainable_resource_optimization_model.md`。 |
| `bc`（任意） | パンくずの分類。`agricultural-management` を指定すると `./blog-agricultural-management.html` にリンクします。 |

現在の取得元は `https://raw.githubusercontent.com/nkkmd/cultivationdata-net/main/` です。`md` は相対パスであり、任意の外部URLを直接指定するものではありません。ディレクトリ区切りを保ち、パスの各部分をURLエンコードします。

### 主要な関数

- `getMarkdownUrlFromParams()`：`md` を取得します。
- `getBreadcrumbsFromParams()`：`bc` を取得します。
- `escapeHtml(text)`：HTMLに挿入する文字列をエスケープします。変換後のMarkdown全体を無害化する関数ではありません。
- `convertMarkdownToHtml(url)`：Markdownを取得し、別行立て数式を一意な仮の文字列に置換してから `marked.parse()` を実行し、HTMLエスケープした数式を戻します。取得・変換失敗時は `null` を返します。
- `extractH1Content(html)`：Markdown由来の最初の `h1` のテキストを取得します。
- `main()`：本文、取得元リンク、タイトル、パンくずを挿入します。`h1` がない場合はMarkdownのパスをタイトルに使います。`load` イベントリスナーで起動します。

### JavaScript：js/md-to-web.js

以下は2026-11-28に確認した公開中のスクリプトです。

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

## 4. HTMLとMathJax

MathJax本体の読み込み前に `window.MathJax` を設定します。`content` に変換済みHTMLが挿入されると、変更監視から数式の描画を要求します。以下は公開ページの設定と変更監視に合わせた最小構成例です。

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

JavaScriptファイルは取得とMarkdown変換を担当し、MathJaxによる描画はHTML側が担当します。TeXがそのまま表示される場合は、MathJaxの読み込みと、挿入後の描画処理を確認してください。変更監視は `typesetPromise()` が利用できる場合だけ呼び出し、初期化待ちや失敗時の再試行は行いません。

## 5. 数式の書き方と保護処理

別行立て数式には通常のTeX記法を使います。下付きは `_`、`aligned` 内の行区切りはバックスラッシュ2個（`\\`）です。保護対象の数式内にMarkdown用のエスケープを追加する必要はありません。

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

保護せずにMarkdown変換すると、バックスラッシュ2個が1個になり、MathJaxに改行命令が届かなくなる場合があります。そのため、次の順序で処理します。

1. `$$ ... $$` の数式を保存し、元の文書に存在しない仮の文字列へ置換します。
2. 残りのMarkdownをHTMLに変換します。
3. TeXの文字を維持し、HTMLエスケープした数式を戻します。
4. HTMLを挿入し、MathJaxで描画します。

HTMLエスケープにより、整列に使う `&` などをHTMLとして解釈させず、DOM内の文字としてMathJaxへ渡します。

現在の保護対象は `$$ ... $$` だけです。インライン数式（`$ ... $`、`\(...\)`）と `\[...\]` はMathJax側で設定されていますが、Markdown変換からは保護されません。また、正規表現はMarkdown全体の構造を解析しないため、コード例内の対になった二重ドル記号にも一致します。コードと数式のあらゆる組み合わせへの対応を保証するものではありません。

## 6. 使用方法と問題の確認

1. HTMLと `js/md-to-web.js` をWebサーバーに配置します。
2. 次のようなURLを開きます。
   `https://www.cultivationdata.net/md-to-web.html?md=AgriculturalManagement/model/sustainable_resource_optimization_model.md&bc=agricultural-management`
3. 本文、タイトル、パンくず、数式の改行を確認します。
4. JavaScriptの更新後はCtrl＋F5で再読み込みします。旧版が残る場合は、サーバーやCDNのキャッシュも確認します。

本文が表示されない場合は、ブラウザーのコンソールとNetworkパネルでJavaScriptエラー、ライブラリの読み込み失敗、CORSエラー、Markdownファイルの不存在を確認します。数式の改行だけが失われる場合は、更新後のスクリプトが読み込まれていることと、元の数式の行区切りがバックスラッシュ2個であることを確認してください。

## 7. 互換性と制限

他のリポジトリやホストを利用する場合は、`main()` 内の取得元URLと取得元リンクを変更します。外部ホストにはブラウザーからの取得を許可するCORS設定が必要です。

変換済みHTMLを `innerHTML` で挿入するため、信頼できるMarkdownを使用してください。数式のエスケープは文書全体の無害化ではありません。相対リンクや画像は別途書き換えない限り、ビューアーページを基準に解決されます。GitHub固有の構文や表示との完全一致は保証されません。ライブラリのURLは完全なバージョン固定ではないため、ライブラリ更新によって動作が変わる可能性があります。

---

- 作成日：2024-09-05
- 更新日：2026-11-28
