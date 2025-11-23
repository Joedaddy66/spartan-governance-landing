# Getting Started

This guide will help you get the Spartan Governance Landing application running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher recommended)
- **npm** (comes with Node.js)
- A **Gemini API key** from [Google AI Studio](https://ai.google.dev/)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Joedaddy66/spartan-governance-landing.git
cd spartan-governance-landing
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required packages including:
- React 19
- Google Generative AI SDK
- Vite
- TypeScript

### 3. Configure Environment Variables

Create a `.env.local` file in the root directory:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

!!! warning "API Key Security"
    Never commit your `.env.local` file to version control. It's already included in `.gitignore`.

### 4. Run the Development Server

```bash
npm run dev
```

The application should now be running at `http://localhost:5173` (or another port if 5173 is in use).

## Build for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Preview Production Build

To preview the production build locally:

```bash
npm run preview
```

## View Your App in AI Studio

You can also view and edit your app in AI Studio:

[https://ai.studio/apps/drive/1xa2stNtaRDOrF-D0W-y0uxhMc4AD-9S3](https://ai.studio/apps/drive/1xa2stNtaRDOrF-D0W-y0uxhMc4AD-9S3)

## Troubleshooting

### Port Already in Use

If port 5173 is already in use, Vite will automatically try the next available port. Check the console output for the actual URL.

### Missing Dependencies

If you encounter missing dependency errors, try:

```bash
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- Explore the [Stripe Integration](stripe/architecture.md) documentation
- Check out the component library in the `components/` directory
- Review the API configuration in `config.yaml`
