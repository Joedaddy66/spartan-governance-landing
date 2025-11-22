# 🚀 Quick Start: Stripe Webhook Marketplace Setup

## What We Just Built For You

✅ **Stripe Webhook Handler** - Receives all Stripe events
✅ **Automatic Store Builder** - Creates marketplace storefront from Stripe account
✅ **Customer Sync** - Automatically tracks customers
✅ **Order Management** - Tracks all transactions
✅ **Payment Events** - Handles success/failure/refunds
✅ **Database Models** - Full schema for storing everything
✅ **Docker Ready** - Deploy anywhere

---

## 🔑 Step 1: Get Your Stripe Keys (3 minutes)

1. Go to: https://dashboard.stripe.com/apikeys
2. Copy your **Secret Key** (starts with `sk_test_` or `sk_live_`)
3. Go to: https://dashboard.stripe.com/webhooks
4. Click **Add endpoint**
5. Enter: `https://yourdomain.com/webhooks/stripe` (or your URL)
6. Select events:
   - ✅ account.created
   - ✅ account.updated  
   - ✅ charge.succeeded
   - ✅ charge.failed
   - ✅ payment_intent.succeeded
   - ✅ customer.created
7. Copy the **Signing Secret** (starts with `whsec_`)

---

## 🛠 Step 2: Set Up Environment

Create `.env` file in `services/payments/`:

```bash
STRIPE_API_KEY=your_stripe_api_key_here
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_here
DATABASE_URL=postgresql://payments:passwords@localhost:5432/payments
REDIS_URL=redis://localhost:6379/0
```

---

## 🏃 Step 3: Run the Service

### Option A: Local (Development)
```bash
cd services/payments
pip install -r requirements.txt
python main.py
```

Service runs on: `http://localhost:8000`

### Option B: Docker (Production)
```bash
cd services/payments
docker build -t stripe-payments .
docker run -p 8000:8000 \
  -e STRIPE_API_KEY=sk_test_XXXXX \
  -e STRIPE_WEBHOOK_SECRET=whsec_test_XXXXX \
  stripe-payments
```

---

## 🏪 Step 4: Create Your First Store

Go to Stripe Dashboard and create a **Stripe Connect account**:
1. Settings → Connected accounts
2. Click **+ Create account**
3. Fill in business details:
   - Business name
   - Email
   - Phone
   - Country
   - Address

**The webhook will automatically:**
- ✅ Receive `account.created` event
- ✅ Build your marketplace store
- ✅ Create all store pages
- ✅ Set up payment processing
- ✅ Save to database

Your store is now LIVE! 🎉

---

## 📊 View Your Store

Query the database:
```sql
-- See all stores
SELECT id, store_name, status, created_at 
FROM stripe_stores 
ORDER BY created_at DESC;

-- See all customers
SELECT id, name, email 
FROM marketplace_customers;

-- See all orders
SELECT id, amount, status, created_at 
FROM marketplace_orders;

-- See webhook event log
SELECT event_type, status, created_at 
FROM stripe_webhook_events 
ORDER BY created_at DESC;
```

---

## 💳 How It Works

### When Customer Makes a Payment:

```
Stripe Payment Page
       ↓
Customer Enters Card
       ↓
Payment Processes
       ↓
Stripe Webhook Sends Event
       ↓
/webhooks/stripe Receives It
       ↓
System Verifies Signature
       ↓
Order Created/Updated
       ↓
Database Saved
       ↓
Customer Sees Success ✅
```

### When Account Changes:

```
Stripe Dashboard Update
       ↓
Webhook: account.updated
       ↓
Store Settings Synced
       ↓
Database Updated
       ↓
Marketplace Store Refreshed
```

---

## 🧪 Test Webhooks Locally

Using Stripe CLI:
```bash
# Install: https://stripe.com/docs/stripe-cli

# Start listening
stripe listen --api-key sk_test_XXXXX

# In another terminal, trigger events
stripe trigger account.created
stripe trigger charge.succeeded
stripe trigger payment_intent.succeeded
```

---

## 📁 File Structure

```
services/payments/
├── main.py                 # 🔴 Webhook handler (MAIN FILE)
├── models.py              # 📊 Database models
├── requirements.txt       # 📦 Dependencies
├── Dockerfile            # 🐳 Docker config
├── .env.example          # 🔑 Environment template
└── WEBHOOK_SETUP.md      # 📖 Detailed setup guide
```

---

## 🎯 What Each Event Does

| Event | Action |
|-------|--------|
| `account.created` | 🏪 Build marketplace store |
| `account.updated` | 🔄 Update store settings |
| `charge.succeeded` | ✅ Mark order as paid |
| `charge.failed` | ❌ Mark order as failed |
| `payment_intent.succeeded` | 💰 Record payment |
| `customer.created` | 👤 Add customer to store |

---

## 🔐 Security Checklist

- ✅ Webhook signature verified before processing
- ✅ API keys stored in environment variables (not in code)
- ✅ Database credentials secured
- ✅ HTTPS required for production
- ✅ Webhook events logged for audit trail

---

## 🚀 Production Deployment

### On AWS/DigitalOcean/Azure:

1. Set up PostgreSQL database
2. Set up Redis cache
3. Deploy Docker image:
   ```bash
   docker push youregistry/stripe-payments
   # Deploy to your cloud provider
   ```
4. Set environment variables in your provider
5. Point Stripe webhook to: `https://yourdomain.com/webhooks/stripe`
6. Enable SSL/TLS

---

## 💡 Next: Custom Features

Once running, you can add:
- 🛒 Product catalog management
- 👥 Customer dashboard
- 📈 Sales analytics
- 🎁 Discount codes
- 📧 Email notifications
- 📱 Mobile app integration

---

## ❓ Troubleshooting

**"Invalid Signature" error?**
- Check `STRIPE_WEBHOOK_SECRET` matches Stripe Dashboard

**"Connection refused"?**
- Check PostgreSQL is running
- Check DATABASE_URL is correct

**Webhook not triggering?**
- Check webhook URL in Stripe Dashboard
- Check service is running and accessible
- Check firewall/network settings

**Events not saving?**
- Check database connection
- Check models are correct
- Review logs

---

## 📞 Need Help?

1. Check `WEBHOOK_SETUP.md` for detailed guide
2. View logs: `docker logs stripe-payments`
3. Check Stripe Dashboard → Webhooks for failed events
4. Query database for saved events

---

**You're all set! Your Stripe webhook marketplace is ready to go! 🎉**

