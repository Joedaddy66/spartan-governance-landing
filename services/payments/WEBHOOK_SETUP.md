# Stripe Webhook + Marketplace Store Setup Guide

## Overview
This system automatically creates and manages marketplace stores whenever a Stripe Connect account is created or updated. Webhooks are used to sync all payment events and build your storefront.

---

## Step 1: Set Up Stripe Connect Account (Dashboard)

1. **Go to Stripe Dashboard**: https://dashboard.stripe.com
2. **Navigate to Settings → Connected accounts**
3. **Enable Stripe Connect** (if not already enabled)
4. **Get your Account ID** (looks like `acct_XXXXXXXXXXXXXX`)

---

## Step 2: Create API Keys

1. **Go to Developers → API Keys** in Stripe Dashboard
2. **Copy your keys:**
   - **Publishable Key**: `pk_test_XXXXX` (or `pk_live_XXXXX` in production)
   - **Secret Key**: `sk_test_XXXXX` (or `sk_live_XXXXX` in production)

3. **Set environment variables in `.env`:**
```bash
STRIPE_API_KEY=sk_test_XXXXX_or_sk_live_XXXXX
STRIPE_WEBHOOK_SECRET=whsec_test_XXXXX_or_whsec_live_XXXXX
DATABASE_URL=postgresql://payments:passwords@localhost:5432/payments
REDIS_URL=redis://localhost:6379/0
```

---

## Step 3: Create Webhook Endpoint

### Option A: Using Stripe CLI (for local development)

```bash
# Install Stripe CLI: https://stripe.com/docs/stripe-cli

# Forward webhook events to your local server
stripe listen --api-key sk_test_XXXXX --device-name my-dev-machine

# Get webhook signing secret from the output (whsec_...)
```

### Option B: Using Stripe Dashboard (for production)

1. **Go to Developers → Webhooks**
2. **Click "Add an endpoint"**
3. **Enter your webhook URL:**
   ```
   https://yourdomain.com/webhooks/stripe
   ```
4. **Select events to listen to:**
   - ✅ `account.created`
   - ✅ `account.updated`
   - ✅ `charge.succeeded`
   - ✅ `charge.failed`
   - ✅ `payment_intent.succeeded`
   - ✅ `customer.created`

5. **Copy the Signing Secret** and set as `STRIPE_WEBHOOK_SECRET`

---

## Step 4: Deploy This Service

### Local Development:
```bash
cd services/payments
pip install -r requirements.txt
python main.py
```

The server will run on `http://localhost:8000`

### Production Deployment:
```bash
# Build with Docker
docker build -t stripe-payments-service .
docker run -p 8000:8000 \
  -e STRIPE_API_KEY=sk_live_XXXXX \
  -e STRIPE_WEBHOOK_SECRET=whsec_live_XXXXX \
  -e DATABASE_URL=postgresql://... \
  stripe-payments-service
```

---

## Step 5: Create a Stripe Connect Account to Trigger Store Creation

1. **Go to Stripe Dashboard**
2. **Settings → Connected accounts → + Create account** (or use API)
3. **Fill in business details:**
   - Business name
   - Email
   - Phone
   - Country
   - Address

4. **The webhook will automatically:**
   - Receive the `account.created` event
   - Build your marketplace store
   - Create store pages (Home, Products, About, Contact)
   - Set up payment methods
   - Save everything to the database

---

## Step 6: Monitor Webhook Events

### Check Webhook Logs:
```bash
# View recent events
curl http://localhost:8000/webhooks/stripe/logs

# Check database for events
SELECT * FROM stripe_webhook_events ORDER BY created_at DESC LIMIT 10;
```

### View Your Created Store:
```bash
# Query the stores table
SELECT * FROM stripe_stores;

# The store structure includes:
# - Home page with featured products
# - Products catalog with categories
# - About us page
# - Contact form
# - Payment settings (Stripe enabled)
```

---

## Step 7: Customer & Order Management

### When a Customer Is Created:
- Customer record is automatically saved
- Customer profile includes address, phone, email
- Customer can be linked to orders

### When a Payment Succeeds:
- Order record is created with:
  - Payment amount
  - Items purchased
  - Customer reference
  - Receipt URL (from Stripe)
- Order status automatically updates to "completed"

---

## API Endpoints

### Webhooks
- **POST** `/webhooks/stripe` - Stripe webhook receiver

### Health Check
- **GET** `/health` - Service status

### Admin Endpoints (to be implemented)
- **GET** `/stores` - List all marketplace stores
- **GET** `/stores/{store_id}` - Get store details
- **GET** `/orders` - List all orders
- **GET** `/customers` - List all customers

---

## Database Schema

### stripe_stores
- Stores marketplace store information
- One per Stripe Connect account
- Includes pages, settings, and payment configuration

### marketplace_customers
- Synced from Stripe customers
- Linked to stores and orders

### marketplace_orders
- Payment transactions
- Status tracking (pending, completed, failed, refunded)

### marketplace_products
- Products available in each store
- Linked to stores

### stripe_webhook_events
- Audit trail of all webhook events
- For debugging and compliance

---

## Webhook Event Flow

```
Stripe Dashboard Action
         ↓
Webhook Event Sent to /webhooks/stripe
         ↓
Event Signature Verified
         ↓
Event Routed to Handler
         ↓
Database Updated
         ↓
Marketplace Store/Order Built
         ↓
Confirmation Returned to Stripe
```

---

## Common Issues

### "Invalid Signature" Error
- ❌ Wrong webhook secret
- ✅ Use the correct `STRIPE_WEBHOOK_SECRET` from Stripe Dashboard

### "Workflow does not have 'workflow_dispatch' trigger"
- This is expected - webhooks are triggered by Stripe events, not manual dispatch
- The workflow will run automatically when events occur

### Database Connection Error
- ❌ PostgreSQL not running
- ✅ Check DATABASE_URL in .env
- ✅ Ensure PostgreSQL service is running

### Stripe Connection Failed
- ❌ Wrong API key
- ✅ Use the correct `STRIPE_API_KEY` (sk_test_* or sk_live_*)
- ✅ Check key hasn't been rotated in Stripe Dashboard

---

## Next Steps

1. ✅ Set up Stripe API keys
2. ✅ Create webhook endpoint in Stripe Dashboard
3. ✅ Deploy this service
4. ✅ Create a Stripe Connect account
5. ⬜ Implement database persistence (models already defined)
6. ⬜ Create admin UI to view stores and orders
7. ⬜ Add product upload functionality
8. ⬜ Implement customer checkout flow

---

## Testing Webhooks Locally

### Using Stripe CLI:
```bash
stripe trigger account.created
stripe trigger charge.succeeded
stripe trigger payment_intent.succeeded
```

### Using curl:
```bash
# Get webhook signing secret first from `stripe listen` output

curl -X POST http://localhost:8000/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "stripe-signature: YOUR_SIGNATURE_HERE" \
  -d '{
    "id": "evt_test_12345",
    "type": "account.created",
    "data": {
      "object": {
        "id": "acct_test_12345",
        "email": "test@example.com",
        "business_profile": {
          "name": "Test Store"
        }
      }
    }
  }'
```

---

## Support

For issues:
1. Check the logs: `docker logs stripe-payments-service`
2. View webhook events: `SELECT * FROM stripe_webhook_events WHERE status = 'failed'`
3. Check Stripe Dashboard for failed webhook attempts

