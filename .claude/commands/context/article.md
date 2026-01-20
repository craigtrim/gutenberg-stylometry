# Article Context

Work with HTML articles for craigtrim.com based on the user's instructions.

**User Instructions:** $ARGUMENTS

## Finding Articles

Articles are located in `/Users/craigtrim/git/mville/cosc-agentic-systems/site/articles/`.

To find available articles, list the directory. Each subdirectory is an article.

**Status indicators:**
- Folders ending in `.draft` are not deployed
- All other folders are deployed or ready for deployment

## Article Structure

Each article folder contains:
- `index.html` - The article HTML
- `images/` - Article images (optional)

## Reference Articles for Styling

Read these to match existing voice and styling:
- `site/articles/glitch-tokens/index.html`
- `site/articles/bpe-history/index.html`
- `site/articles/words-learning-company-they-keep/index.html`

## Writing Rules

### Prohibited
- **No em dashes** - Use commas, semicolons, or restructure sentences
- **No "The Uncomfortable Truth"** - Never use this phrase

### Voice and Tone
- Academic but accessible - assume intelligent reader, not specialist
- Concrete examples - always ground abstractions in specifics
- Historical context - show what came before, why it mattered
- No hyperbole - let the facts carry the weight
- Short paragraphs - rarely more than 3-4 sentences
- Punch endings - sections often end with a short, direct sentence

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💬</text></svg>">
    <title>ARTICLE TITLE</title>
    <style>
        :root {
            --text-color: #292929;
            --bg-color: #fff;
            --accent-color: #1a8917;
            --border-color: #e6e6e6;
            --code-bg: #f4f4f4;
        }
        * { box-sizing: border-box; }
        body {
            font-family: charter, Georgia, Cambria, "Times New Roman", Times, serif;
            font-size: 21px;
            line-height: 1.58;
            color: var(--text-color);
            background-color: var(--bg-color);
            margin: 0;
            padding: 0;
        }
        article {
            max-width: 680px;
            margin: 0 auto;
            padding: 40px 24px 80px;
        }
        h1 {
            font-family: sohne, "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 42px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 16px;
        }
        h2 {
            font-family: sohne, "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 28px;
            font-weight: 700;
            margin-top: 56px;
            margin-bottom: 16px;
        }
        p { margin-bottom: 24px; }
        .lead {
            font-size: 22px;
            line-height: 1.5;
            margin-bottom: 32px;
        }
        code {
            font-family: Menlo, Monaco, "Courier New", monospace;
            font-size: 16px;
            background-color: var(--code-bg);
            padding: 2px 6px;
            border-radius: 3px;
        }
        pre {
            font-family: Menlo, Monaco, "Courier New", monospace;
            font-size: 15px;
            background-color: var(--code-bg);
            padding: 20px;
            border-radius: 4px;
            overflow-x: auto;
            margin-bottom: 24px;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 24px;
            font-size: 16px;
            color: #757575;
        }
        .separator {
            text-align: center;
            margin: 48px 0;
            color: #757575;
            letter-spacing: 0.5em;
        }
        figure { margin: 40px 0; text-align: center; }
        figure img { max-width: 100%; border-radius: 4px; }
        figcaption { font-size: 16px; color: #757575; margin-top: 12px; font-style: italic; }
        figure.breakout {
            margin-left: -140px;
            margin-right: -140px;
            max-width: calc(100% + 280px);
        }
        @media (max-width: 900px) {
            figure.breakout { margin-left: 0; margin-right: 0; max-width: 100%; }
        }
    </style>
</head>
<body>
    <article>
        <a href="../" class="back-link">&larr; All Articles</a>
        <h1>Article Title</h1>
        <p class="lead"><em>Opening hook paragraph.</em></p>

        <!-- CONTENT -->

        <div class="separator">. . .</div>
        <div class="references">
            <h2>References</h2>
            <ol>
                <li>Author. (Year). <a href="URL">"Title."</a> Source.</li>
            </ol>
        </div>
    </article>
</body>
</html>
```

## Image Markup

**All visual images use `class="breakout"`** - This extends 140px beyond each side of the text column (960px total width). Use breakout for:
- Photos
- Illustrations
- Diagrams
- Demo screenshots
- Any visual content

**Only code blocks and tables stay within 680px** - Use plain `<figure>` (no breakout class) only for `<pre>` code blocks or data tables.

**Lightbox images** (illustrations, diagrams, photos):
```html
<figure class="breakout">
    <img src="images/name.png" class="lightbox-trigger" data-caption="Modal caption" alt="Description">
    <figcaption>Caption below image</figcaption>
</figure>
```

**Demo link images** (screenshots linking to demos):
```html
<figure class="breakout">
    <a href="https://craigtrim.com/demos/demo-name/" target="_blank">
        <img src="images/demo-screenshot.png" alt="Demo description" style="cursor: pointer;">
    </a>
    <figcaption><a href="https://craigtrim.com/demos/demo-name/" target="_blank">Interactive</a>: Demo description</figcaption>
</figure>
```

**Embedded demo iframe:**
```html
<figure class="interactive-demo">
    <iframe src="https://craigtrim.com/demos/demo-name/"
        style="width: 100%; height: 500px; border: 0; border-radius: 8px;"
        title="Demo Title"
        sandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts">
    </iframe>
</figure>
```

**Code blocks / tables (no breakout):**
```html
<figure>
    <pre style="font-size: 14px; text-align: left;">
    ... code or table content ...
    </pre>
    <figcaption>Caption for code/table</figcaption>
</figure>
```

## Deploy to S3

Single article:
```bash
aws s3 sync /Users/craigtrim/git/mville/cosc-agentic-systems/site/articles/ARTICLE_NAME s3://craigtrim.com/articles/ARTICLE_NAME/ --profile dwc_s3
```

All articles:
```bash
aws s3 sync /Users/craigtrim/git/mville/cosc-agentic-systems/site/articles s3://craigtrim.com/articles/ --profile dwc_s3
```

## Live URLs

All deployed articles are at: `https://craigtrim.com/articles/ARTICLE_NAME/`

## Landing Pages

When adding new articles, update:
- `site/articles/writing/index.html` - Add article card
- `site/index.html` - Add to `allArticles` array

## Creating New Articles

For new articles, create as draft first:
- Folder: `site/articles/{slug}.draft/`
- Remove `.draft` suffix when ready to publish

Use kebab-case for folder names:
- "Context Windows" → `context-windows.draft/`
- "BPE History" → `bpe-history.draft/`

## Converting PDF to Article

When converting from Medium PDF export:
1. Read the PDF to extract content
2. Ask user for image paths, types (lightbox vs demo-link), and captions
3. Ask for metadata (category, read time, description, tags)
4. Create folder structure and copy images
5. Generate HTML matching the template
6. Update landing pages

## Git Policy

**Do not commit to git.** Git commits will happen later and separately.

## Instructions

Follow the user's instructions provided in `$ARGUMENTS`. This may include:
- Creating a new article
- Editing an existing article
- Converting a PDF to article
- Deploying an article
- Fixing content or styling issues
- Adding images or demos to an article

Read the relevant `index.html` file before making changes to understand existing content.
