# GitHub Pages Configuration

This page provides information about the GitHub Pages setup for this project.

## Current Configuration

The documentation site is deployed to GitHub Pages using GitHub Actions. The deployment workflow automatically runs when changes are pushed to the `main` branch.

## Site URL

Once enabled, the documentation will be available at:

**[https://joedaddy66.github.io/spartan-governance-landing/](https://joedaddy66.github.io/spartan-governance-landing/)**

## Enabling GitHub Pages

!!! info "Repository Owner Action Required"
    GitHub Pages must be enabled in the repository settings by the repository owner.

To enable GitHub Pages:

1. Go to **Settings** → **Pages** in the repository
2. Under **Source**, select **GitHub Actions**
3. The next push to `main` will trigger the deployment

For detailed instructions, see the [GitHub Pages Setup Guide](https://github.com/Joedaddy66/spartan-governance-landing/blob/main/GITHUB_PAGES_SETUP.md) in the repository.

## Automatic Deployment

The deployment workflow (`.github/workflows/mkdocs-gh-pages.yml`) automatically:

- Builds the documentation using MkDocs
- Deploys to GitHub Pages
- Runs on every push to `main` branch
- Can be manually triggered from the Actions tab

## Local Development

To work on the documentation locally:

```bash
# Install dependencies
pip install mkdocs mkdocs-material

# Serve locally with live reload
mkdocs serve
```

Visit `http://localhost:8000` to preview your changes.

## Adding Content

To add new documentation:

1. Create new `.md` files in the `docs/` directory
2. Update `mkdocs.yml` to include the new pages in the navigation
3. Commit and push to your branch
4. Once merged to `main`, the site will automatically update

## Checking Deployment Status

To check the deployment status:

1. Go to the **Actions** tab in the GitHub repository
2. Look for the "Deploy MkDocs to GitHub Pages" workflow
3. Click on a run to see details and logs

## Build Configuration

The site is built using:

- **MkDocs**: Static site generator
- **Material Theme**: Modern, responsive theme
- **Extensions**: Code highlighting, admonitions, tabs, and more

All configuration is in `mkdocs.yml` at the repository root.
