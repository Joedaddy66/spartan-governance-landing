# GitHub Pages Setup Instructions

This document provides step-by-step instructions for enabling GitHub Pages for this repository.

## Overview

GitHub Pages has been configured to deploy from the MkDocs build using GitHub Actions. The documentation will be automatically built and deployed when changes are pushed to the `main` branch.

## Enabling GitHub Pages

To enable GitHub Pages for this repository, follow these steps:

### Step 1: Navigate to Repository Settings

1. Go to the repository on GitHub: [https://github.com/Joedaddy66/spartan-governance-landing](https://github.com/Joedaddy66/spartan-governance-landing)
2. Click on **Settings** (in the repository navigation menu)

### Step 2: Access Pages Settings

1. In the left sidebar, scroll down to **Code and automation** section
2. Click on **Pages**

### Step 3: Configure GitHub Pages Source

1. Under **Source**, select **GitHub Actions** from the dropdown menu
   - This tells GitHub to use the GitHub Actions workflow for deployment
   - The workflow file `.github/workflows/mkdocs-gh-pages.yml` will handle the build and deployment

### Step 4: Save and Deploy

1. Once you select "GitHub Actions", the configuration is saved automatically
2. The next push to the `main` branch will trigger the workflow
3. GitHub Pages will be deployed at: `https://joedaddy66.github.io/spartan-governance-landing/`

## Verification

After the workflow runs successfully:

1. Go to the **Actions** tab in the repository
2. You should see a workflow run for "Deploy MkDocs to GitHub Pages"
3. Once it completes, visit `https://joedaddy66.github.io/spartan-governance-landing/` to see the documentation

## Workflow Details

The GitHub Actions workflow (`.github/workflows/mkdocs-gh-pages.yml`) will:

1. **Trigger on**:
   - Pushes to the `main` branch
   - Manual workflow dispatch

2. **Build process**:
   - Checkout the repository
   - Install Python and MkDocs with Material theme
   - Build the documentation site
   - Upload the site as a Pages artifact

3. **Deploy process**:
   - Deploy the artifact to GitHub Pages
   - Make it available at the GitHub Pages URL

## Troubleshooting

### Workflow Not Running

- Check that the `.github/workflows/mkdocs-gh-pages.yml` file exists in the `main` branch
- Ensure GitHub Actions are enabled for the repository (Settings → Actions → General)

### Build Failures

- Check the Actions tab for error messages
- Verify that `mkdocs.yml` is valid
- Ensure all documentation files referenced in `mkdocs.yml` exist

### Pages Not Updating

- Check that GitHub Pages source is set to "GitHub Actions"
- Verify the workflow completed successfully
- Check if there are any GitHub Pages deployment restrictions in the repository settings

## Manual Deployment

If you prefer to deploy manually instead of using GitHub Actions:

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Deploy to GitHub Pages
mkdocs gh-deploy
```

This will build the site and push it to the `gh-pages` branch. You would then need to configure GitHub Pages to deploy from the `gh-pages` branch instead of GitHub Actions.

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
