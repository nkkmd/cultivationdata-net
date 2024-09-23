# Markdown Viewer: ドキュメント

## 目次
1. [概要](#概要)
2. [システム構成](#システム構成)
3. [JavaScriptファイル (md.js)](#javascriptファイル-mdjs)
   - [主要な関数](#主要な関数)
   - [コード](#javascriptファイル-mdjs-のコード)
4. [HTMLファイル](#htmlファイル)
   - [構造説明](#構造説明)
   - [コード](#htmlファイルのコード)
5. [使用方法](#使用方法)
6. [Markdownファイルの互換性](#markdownファイルの互換性)
7. [注意点](#注意点)

## 概要

このMarkdown Viewerシステムは、指定されたMarkdownファイルを動的にHTMLに変換し、Webページとして表示するための軽量なソリューションです。URLパラメータを使用してMarkdownファイルを指定し、JavaScriptを使用して非同期でファイルを取得、変換、表示します。

## システム構成

システムは主に2つのファイルで構成されています：
1. JavaScriptファイル (md.js): 主要な機能を提供します。
2. HTMLファイル: 基本的なページ構造を提供し、必要なスクリプトを読み込みます。

また、外部ライブラリとして`marked.js`を使用して、MarkdownをHTMLに変換します。

## JavaScriptファイル (md.js)

### 主要な関数

1. `getMarkdownUrlFromParams()`
   - 目的: URLパラメータからMarkdownファイルのURLを取得します。
   - 動作: `window.location.search`からURLパラメータを解析し、`md`パラメータの値を返します。

2. `convertMarkdownToHtml(url)`
   - 目的: 指定されたURLからMarkdownファイルを取得し、HTMLに変換します。
   - 動作:
     - `fetch`を使用してMarkdownファイルを非同期に取得します。
     - 取得に成功した場合、`marked.parse()`を使用してMarkdownをHTMLに変換します。
     - エラーが発生した場合は、コンソールにエラーを出力し、`null`を返します。

3. `extractH1Content(html)`
   - 目的: 変換されたHTMLから最初のh1タグの内容を抽出します。
   - 動作: DOMParserを使用してHTMLを解析し、最初のh1タグのテキスト内容を返します。

4. `main()`
   - 目的: アプリケーションのメイン処理を行います。
   - 動作:
     - MarkdownファイルのベースURLを設定します。
     - URLパラメータからMarkdownファイル名を取得します。
     - パラメータが存在しない場合、エラーメッセージを表示して処理を終了します。
     - Markdownを取得してHTMLに変換し、ページに表示します。
     - h1タグの内容を抽出してページタイトルに設定します。
     - 変換に失敗した場合、エラーメッセージを表示します。

### JavaScriptファイル (md.js) のコード

```javascript
// URLパラメータからMarkdownファイルのURLを取得する関数
function getMarkdownUrlFromParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('md');
}
 
// Markdownファイルを取得し、HTMLに変換する関数
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
 
// HTMLからh1タグの内容を抽出する関数
function extractH1Content(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const h1 = doc.querySelector('h1');
    return h1 ? h1.textContent : null;
}
 
// メイン処理
async function main() {
    const URL = 'https://raw.githubusercontent.com/ユーザ名/リポジトリ名/ブランチ名/'; // Markdownファイルが置かれているURL
    const mdFile = getMarkdownUrlFromParams();
    const errorElement = document.getElementById('error');
    const contentElement = document.getElementById('content');
 
    if (!mdFile) {
        errorElement.textContent = 'URLパラメータにMarkdownファイルが指定されていません。(?md=sample/file.md)';
        return;
    }
 
    const html = await convertMarkdownToHtml(`${URL}${mdFile}`);
    if (html) {
        contentElement.innerHTML = html;
        
        // h1タグの内容を抽出してタイトルに設定
        const h1Content = extractH1Content(html);
        if (h1Content) {
            document.title = `${h1Content}`;
        }
    } else {
        errorElement.textContent = '変換に失敗したか、ファイルが見つかりません。';
    }
}
 
// ページ読み込み時に実行
window.onload = main;
```

## HTMLファイル

### 構造説明

1. `<head>`セクション
   - 文字エンコーディングをUTF-8に設定します。
   - 動的に変更可能な`<title>`タグを含みます。
   - `marked`ライブラリ（CDNから）とカスタムJavaScriptファイル（md.js）を読み込みます。

2. `<body>`セクション
   - `<div id="error">`: エラーメッセージを表示するための要素です。
   - `<div id="content">`: 変換されたMarkdownコンテンツを表示するための要素です。

### HTMLファイルのコード

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

## 使用方法

1. HTMLファイルとJavaScriptファイル（md.js）をWebサーバーにホストします。
2. URLパラメータ`md`を使用して表示したいMarkdownファイルを指定します。
   例: `https://yourserver.com/index.html?md=sample/file.md`
3. ページにアクセスすると、指定されたMarkdownファイルが読み込まれ、HTMLとして表示されます。
4. Markdownの最初のh1タグがページタイトルとして使用されます。

## Markdownファイルの互換性

このシステムは、GitHub上のMarkdownファイルを表示することを想定して例示されていますが、他のソースのMarkdownファイルでも利用可能です。以下の理由により、様々なソースからのMarkdownファイルに対応できます：

1. 汎用的なfetch API: `convertMarkdownToHtml`関数は`fetch`APIを使用しており、これは任意のURLからリソースを取得できます。

2. 柔軟なURL設定: `main`関数内の`URL`変数を適切に設定することで、任意のベースURLを指定できます。

3. marked.jsの汎用性: 使用している`marked`ライブラリは、標準的なMarkdown構文を広くサポートしており、ソースに依存しない変換が可能です。

4. パラメータベースの設計: URLパラメータを使用してMarkdownファイルを指定する設計により、任意のファイルパスやURLを柔軟に扱えます。

ただし、異なるソースのMarkdownファイルを使用する場合は、以下の点に注意が必要です：

- CORS（クロスオリジンリソース共有）ポリシー: 外部ソースからのファイル取得には、適切なCORS設定が必要です。
- ファイルの構造やURL形式: 異なるプラットフォームやサーバーでは、ファイルの構造やURLの形式が異なる場合があるため、それに応じた調整が必要になる可能性があります。
- セキュリティ: 信頼できないソースからのMarkdownファイルを表示する場合、セキュリティリスクに注意する必要があります。

## 注意点

- クロスオリジンリソース共有（CORS）の制限に注意してください。適切なサーバー設定が必要な場合があります。
- エラー処理が実装されていますが、ネットワークの問題やファイルの不存在などにより、コンテンツが表示されない場合があります。
- セキュリティ上の理由から、信頼できるソースからのMarkdownファイルのみを使用することをお勧めします。
- 異なるMarkdownの方言や拡張構文を使用している場合、完全な互換性は保証されません。標準的なMarkdown構文の使用を推奨します。
- このシステムは基本的な機能を提供しています。より高度な機能（例：目次の自動生成、スタイリングのカスタマイズなど）が必要な場合は、追加の開発が必要になります。

---
- 作成日: 2024-09-05
- 更新日: 2024-09-05