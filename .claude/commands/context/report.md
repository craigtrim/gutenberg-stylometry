# Report Context

Create and deploy JSX reports for stylometric analysis.

**User Instructions:** $ARGUMENTS

## Report Location

Reports are located in `/Users/craigtrim/git/gutenburg-stylometry/reports/`.

Each subdirectory is a report (e.g., `reports/ttr/`).

## Report Structure

Each report folder contains:
- `app.jsx` - Main React component (entry point)
- `package.json` - Dependencies
- `vite.config.js` - Build config
- `index.html` - HTML shell
- `main.jsx` - React mount point
- `dist/` - Built output (after `npm run build`)

## Reference Report

**TTR Report:** `reports/ttr/app.jsx`

Read this to match existing patterns for:
- Light theme styling
- Data visualization components (BoxPlot, Histogram)
- Summary statistics tables
- Sortable work detail tables

## Creating a New Report

1. Create the report directory:
   ```bash
   mkdir -p /Users/craigtrim/git/gutenburg-stylometry/reports/REPORT_NAME
   ```

2. Create `package.json`:
   ```json
   {
     "name": "REPORT_NAME-report",
     "private": true,
     "version": "1.0.0",
     "type": "module",
     "scripts": {
       "dev": "vite",
       "build": "vite build",
       "preview": "vite preview"
     },
     "dependencies": {
       "react": "^18.2.0",
       "react-dom": "^18.2.0"
     },
     "devDependencies": {
       "@vitejs/plugin-react": "^4.2.1",
       "vite": "^5.0.0"
     }
   }
   ```

3. Create `vite.config.js`:
   ```javascript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   export default defineConfig({
     plugins: [react()],
     base: './',
   })
   ```

4. Create `index.html`:
   ```html
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>REPORT_TITLE</title>
       <style>
         * { margin: 0; padding: 0; box-sizing: border-box; }
       </style>
     </head>
     <body>
       <div id="root"></div>
       <script type="module" src="/main.jsx"></script>
     </body>
   </html>
   ```

5. Create `main.jsx`:
   ```jsx
   import React from 'react'
   import ReactDOM from 'react-dom/client'
   import App from './app.jsx'

   ReactDOM.createRoot(document.getElementById('root')).render(
     <React.StrictMode>
       <App />
     </React.StrictMode>
   )
   ```

6. Create `app.jsx` with report content (see reference report for patterns)

## Light Theme Styles

```jsx
const styles = {
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    backgroundColor: "#f8fafc",
    color: "#1e293b",
    minHeight: "100vh",
    padding: 32,
    maxWidth: 1000,
    margin: "0 auto",
  },
  card: {
    backgroundColor: "#ffffff",
    borderRadius: 12,
    padding: 24,
    border: "1px solid #e2e8f0",
    boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
    marginBottom: 24,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 600,
    marginBottom: 16,
    color: "#1e293b",
  },
};
```

## Building a Report

```bash
cd /Users/craigtrim/git/gutenburg-stylometry/reports/REPORT_NAME
npm install
npm run build
```

## Deploying to S3

Deploy to the `craigtrim.com` bucket:

```bash
cd /Users/craigtrim/git/gutenburg-stylometry/reports/REPORT_NAME
aws s3 sync dist/ s3://craigtrim.com/reports/REPORT_NAME/ --profile dwc_s3
```

## Live URLs

Reports are available at: `http://craigtrim.com/reports/REPORT_NAME/`

Current reports:
- TTR Analysis: http://craigtrim.com/reports/ttr/

## Updating a Report

1. Edit `app.jsx` with new content/data
2. Rebuild and redeploy:
   ```bash
   cd /Users/craigtrim/git/gutenburg-stylometry/reports/REPORT_NAME
   npm run build
   aws s3 sync dist/ s3://craigtrim.com/reports/REPORT_NAME/ --profile dwc_s3
   ```

## Git Policy

Do not commit to git unless explicitly requested.

## Instructions

Follow the user's instructions provided in `$ARGUMENTS`. This may include:
- Creating a new report
- Updating an existing report with new author data
- Adding new visualizations
- Deploying reports to S3
