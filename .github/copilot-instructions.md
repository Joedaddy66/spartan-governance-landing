# Copilot Instructions for Spartan Governance Landing

## Project Overview

This is an AI-powered marketing content assistant built with React, TypeScript, Vite, and Google Gemini AI. The application provides two main features:
1. **Promo Pack Generator**: Creates comprehensive marketing kits with AI assistance
2. **Live Conversation**: Real-time chat interface with Gemini AI

The project also includes a FastAPI-based payment service with Stripe integration for handling webhooks and marketplace functionality.

## Technology Stack

### Frontend
- **Framework**: React 19.2.0 with TypeScript
- **Build Tool**: Vite 6.2.0
- **Styling**: Tailwind CSS (utility classes)
- **AI Integration**: Google Gemini AI (@google/genai)
- **Module System**: ESNext with bundler resolution

### Backend (Payment Service)
- **Framework**: FastAPI (Python)
- **Payment Processing**: Stripe API
- **Containerization**: Docker
- **Deployment**: Railway, Google Cloud Run

### Infrastructure
- **Hosting**: Vercel (frontend), Railway/GCP Cloud Run (backend)
- **Documentation**: MkDocs with Material theme → GitHub Pages
- **CI/CD**: GitHub Actions
- **API Gateway**: Google Cloud API Gateway with Firebase Auth

## Project Structure

```
.
├── App.tsx                      # Main application component with tab navigation
├── index.tsx                    # React app entry point
├── components/                  # React components
│   ├── PromoPackGenerator.tsx   # AI marketing kit generator
│   ├── LiveConversation.tsx     # Real-time chat interface
│   ├── StripeEventViewer.tsx    # Stripe events visualization
│   ├── LoadingSpinner.tsx       # Loading indicator
│   └── IconComponents.tsx       # SVG icon components
├── services/
│   ├── geminiService.ts         # Google Gemini API integration
│   └── payments/                # FastAPI payment service
│       ├── main.py              # Stripe webhook handler
│       ├── models.py            # Pydantic models
│       ├── requirements.txt     # Python dependencies
│       └── tests/               # Python tests
├── lib/
│   └── firebaseAdmin.ts         # Firebase Admin SDK setup
├── utils/                       # Utility functions
├── docs/                        # MkDocs documentation source
├── config.yaml                  # GCP API Gateway OpenAPI spec
├── vite.config.ts               # Vite configuration
└── .github/workflows/           # CI/CD pipelines
```

## Development Workflow

### Running Locally

1. **Frontend Development**:
   ```bash
   npm install
   npm run dev  # Starts dev server on 0.0.0.0:3000 (accessible via http://localhost:3000)
   ```
   - Set `GEMINI_API_KEY` in `.env.local` for AI features
   - Vite dev server runs on port 3000 (binds to 0.0.0.0 for network access) with hot module replacement

2. **Building for Production**:
   ```bash
   npm run build   # Outputs to dist/
   npm run preview # Preview production build
   ```

3. **Documentation**:
   ```bash
   pip install mkdocs mkdocs-material
   mkdocs serve    # Serves docs at http://localhost:8000
   mkdocs build    # Builds to site/
   ```

4. **Payment Service**:
   ```bash
   cd services/payments
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

### Code Style and Conventions

- **TypeScript**: Use strict typing, prefer `React.FC` for components
- **Components**: Functional components with hooks
- **Styling**: Tailwind utility classes with dark theme (gray-900 background)
- **State Management**: React hooks (`useState`, `useEffect`)
- **API Calls**: Async/await pattern
- **File Naming**: PascalCase for components, camelCase for utilities
- **Python**: Follow PEP 8, use type hints, Pydantic models for validation

### Environment Variables

Frontend (`.env.local`):
- `GEMINI_API_KEY`: Google Gemini API key (required for AI features)

Backend (`services/payments/.env`):
- `STRIPE_SECRET_KEY`: Stripe API secret key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook signing secret

### Testing

- No automated frontend tests currently configured
- Python payment service has tests in `services/payments/tests/`
- Manual testing recommended for React components
- Use `npm run build` to validate TypeScript compilation

## CI/CD Pipelines

### GitHub Actions Workflows

1. **deploy.yaml**: Deploys API Gateway to GCP
   - Triggers on push to `main`
   - Uses Workload Identity Federation for GCP auth
   - Deploys OpenAPI config and gateway

2. **mkdocs-gh-pages.yml**: Deploys documentation
   - Builds MkDocs site
   - Publishes to GitHub Pages
   - URL: https://joedaddy66.github.io/spartan-governance-landing/

3. **railway-deploy.yml**: Deploys payment service to Railway

4. **stripe-monitor.yml**: Monitors Stripe events

5. **payments-integration-test.yml**: Tests payment integrations

## Key Features and Implementation Details

### AI Integration (Gemini)
- Service layer in `services/geminiService.ts`
- API key passed via environment variable
- Streaming responses supported for live conversation
- Multimodal capabilities (text, images)

### Payment Processing
- Stripe Connect for marketplace functionality
- Webhook verification with signature validation
- Support for both direct charges and Connect platform fees
- Events handled: `account.created`, `charge.succeeded`, `payment_intent.succeeded`, etc.

### Security
- Firebase JWT authentication for API Gateway
- API key-based rate limiting
- Stripe webhook signature verification
- Zero Trust architecture with GCP API Gateway

### Deployment
- Frontend: Vercel (configured in `vercel.json`)
- Backend: Railway or GCP Cloud Run (Dockerfile provided)
- Documentation: GitHub Pages (automated via workflow)

## Common Development Tasks

### Adding a New Component
1. Create in `components/` directory using PascalCase
2. Export as default or named export
3. Import and use in `App.tsx` or parent component
4. Follow existing component structure (functional with TypeScript)

### Modifying AI Behavior
- Update `services/geminiService.ts`
- Configure model parameters (temperature, topK, etc.)
- Handle streaming vs. non-streaming responses appropriately

### Adding Stripe Events
1. Update event handlers in `services/payments/main.py`
2. Add corresponding Pydantic models in `models.py`
3. Test with Stripe CLI: `stripe listen --forward-to localhost:8000/webhooks/stripe`

### Updating Documentation
1. Edit files in `docs/` directory (Markdown)
2. Update `mkdocs.yml` for navigation/structure
3. Test locally with `mkdocs serve`
4. Auto-deploys on push to main

## Important Notes

- **No TypeScript Emit**: `tsconfig.json` has `"noEmit": true` - TypeScript only for type checking
- **Path Aliases**: Use `@/*` to reference root directory files
- **Port Configuration**: Dev server runs on 3000 (configured in `vite.config.ts`)
- **React Version**: Using React 19.2.0 - be aware of new features and deprecations
- **Module Resolution**: Using `bundler` mode for modern module resolution
- **API Key Exposure**: Never commit API keys; use `.env.local` and `.gitignore`

## Dependencies to Note

### Frontend
- `react` and `react-dom` v19.2.0 (latest)
- `@google/genai` for Gemini AI integration
- `@vitejs/plugin-react` for JSX transformation
- No CSS framework installed (using Tailwind via CDN or utility classes)

### Backend (Python)
- `fastapi` for API framework
- `stripe` for payment processing
- `pydantic` for data validation
- See `services/payments/requirements.txt` for full list

## Architecture Patterns

- **Component-Based**: React components with clear separation of concerns
- **Service Layer**: API integrations abstracted into service modules
- **Environment-Based Config**: Different configs for dev/prod via env vars
- **Webhook-Driven**: Payment events handled via Stripe webhooks
- **Zero Trust Security**: API Gateway with JWT + API key authentication

## Troubleshooting

### Build Failures
- Verify Node.js version compatibility (requires modern Node for React 19)
- Check TypeScript errors: `npx tsc --noEmit`
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

### API Integration Issues
- Verify API keys are set in `.env.local`
- Check browser console for CORS or network errors
- Ensure Vite is properly passing env vars (check `vite.config.ts` define section)

### Deployment Issues
- GCP: Verify Workload Identity Federation secrets
- Railway: Check environment variables in Railway dashboard
- Vercel: Ensure build command and output directory are correct

## Best Practices

1. **Type Safety**: Always define TypeScript interfaces/types for props and state
2. **Error Handling**: Use try-catch for async operations, display user-friendly errors
3. **Environment Variables**: Never hardcode sensitive data, use env vars
4. **Component Reusability**: Extract common patterns into reusable components
5. **Performance**: Lazy load components if needed, optimize re-renders with React.memo
6. **Security**: Validate all webhook signatures, sanitize user inputs
7. **Documentation**: Keep MkDocs up to date with architectural changes
8. **Git Workflow**: Use conventional commits, create PRs for review

## Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Vite Documentation](https://vitejs.dev/)
- [React 19 Documentation](https://react.dev/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
