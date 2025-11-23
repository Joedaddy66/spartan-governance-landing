<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1xa2stNtaRDOrF-D0W-y0uxhMc4AD-9S3

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## Documentation

This project uses [MkDocs](https://www.mkdocs.org/) with the Material theme for documentation.

### View Documentation

The documentation is automatically deployed to GitHub Pages at: `https://joedaddy66.github.io/spartan-governance-landing/`

### Build Documentation Locally

**Prerequisites:** Python 3.x

1. Install MkDocs and dependencies:
   ```bash
   pip install mkdocs mkdocs-material
   ```

2. Build the documentation:
   ```bash
   mkdocs build
   ```

3. Serve locally for development:
   ```bash
   mkdocs serve
   ```
   Then visit `http://localhost:8000`

### Deploy Documentation

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via GitHub Actions.

To manually deploy:
```bash
mkdocs gh-deploy
```
