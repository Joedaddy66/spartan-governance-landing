"""#!/usr/bin/env python3

Stripe Webhook Handler & Marketplace Store Builder"""

Handles all Stripe events and triggers marketplace store creationMinimal FastAPI application for payments service integration tests.

"""This implements the endpoints needed for the end-to-end integration test.

import os"""

import jsonfrom __future__ import annotations

import stripeimport os

import asyncioimport hmac

from fastapi import FastAPI, Request, HTTPExceptionimport hashlib

from typing import Optional, Dict, Anyimport json

import loggingfrom typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException, Header

logging.basicConfig(level=logging.INFO)from pydantic import BaseModel

logger = logging.getLogger(__name__)import stripe



app = FastAPI()# Initialize Stripe with API key from environment

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_fake_for_local")

# Initialize Stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")app = FastAPI(title="Payments Service")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

class CheckoutSessionRequest(BaseModel):

# ============================================================================    amount_cents: int

# STRIPE WEBHOOK HANDLER    currency: str = "usd"

# ============================================================================    description: str

    connected_account_id: Optional[str] = None

@app.post("/webhooks/stripe")    application_fee_cents: Optional[int] = None

async def stripe_webhook(request: Request):    metadata: Optional[Dict[str, str]] = None

    """    ui_mode: str = "embedded"

    Main Stripe webhook endpoint.

    Receives events from Stripe and routes to appropriate handlers.@app.post("/create-checkout-session")

    """async def create_checkout_session(request: CheckoutSessionRequest):

    payload = await request.body()    """

    sig_header = request.headers.get("stripe-signature")    Create a Stripe Checkout Session.

        """

    try:    # Build Stripe checkout session parameters

        event = stripe.Webhook.construct_event(    params: Dict[str, Any] = {

            payload, sig_header, STRIPE_WEBHOOK_SECRET        "mode": "payment",

        )        "ui_mode": request.ui_mode,

    except ValueError:        "line_items": [{

        logger.error("Invalid payload")            "price_data": {

        raise HTTPException(status_code=400, detail="Invalid payload")                "currency": request.currency,

    except stripe.error.SignatureVerificationError:                "product_data": {

        logger.error("Invalid signature")                    "name": request.description,

        raise HTTPException(status_code=400, detail="Invalid signature")                },

                    "unit_amount": request.amount_cents,

    # Route event to appropriate handler            },

    event_type = event.get("type")            "quantity": 1,

    logger.info(f"Processing Stripe event: {event_type}")        }],

            "metadata": request.metadata or {},

    if event_type == "account.created":    }

        return await handle_account_created(event)    

    elif event_type == "account.updated":    # Add return URLs for non-embedded mode

        return await handle_account_updated(event)    if request.ui_mode != "embedded":

    elif event_type == "charge.succeeded":        params["success_url"] = os.getenv("SUCCESS_URL", "http://localhost:3000/success")

        return await handle_charge_succeeded(event)        params["cancel_url"] = os.getenv("CANCEL_URL", "http://localhost:3000/cancel")

    elif event_type == "charge.failed":    else:

        return await handle_charge_failed(event)        params["return_url"] = os.getenv("RETURN_URL", "http://localhost:3000/return")

    elif event_type == "payment_intent.succeeded":    

        return await handle_payment_intent_succeeded(event)    # Handle connected account (Stripe Connect)

    elif event_type == "customer.created":    if request.connected_account_id:

        return await handle_customer_created(event)        params["payment_intent_data"] = {

    else:            "application_fee_amount": request.application_fee_cents or int(os.getenv("APPLICATION_FEE_CENTS_DEFAULT", "0")),

        logger.info(f"Unhandled event type: {event_type}")        }

        return {"status": "received"}        # Would set stripe_account header in real implementation

    

    # Create the session using Stripe SDK

# ============================================================================    session = stripe.checkout.Session.create(**params)

# EVENT HANDLERS    

# ============================================================================    return {

        "session_id": session.get("id") or session.id,

async def handle_account_created(event: Dict[str, Any]) -> Dict[str, str]:        "client_secret": session.get("client_secret"),

    """Handle Stripe Connect account creation - Build marketplace store"""    }

    account = event["data"]["object"]

    account_id = account["id"]@app.post("/webhooks/stripe")

    async def stripe_webhook(

    logger.info(f"New Stripe Connect account created: {account_id}")    request: Request,

        stripe_signature: str = Header(None, alias="Stripe-Signature")

    try:):

        # Build the marketplace store for this account    """

        store_data = await build_marketplace_store(account)    Handle Stripe webhook events with signature verification.

        logger.info(f"Marketplace store built for {account_id}")    """

        return {"status": "success", "account_id": account_id, "store": store_data}    if not stripe_signature:

    except Exception as e:        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

        logger.error(f"Failed to build store: {str(e)}")    

        return {"status": "error", "message": str(e)}    payload_bytes = await request.body()

    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    

async def handle_account_updated(event: Dict[str, Any]) -> Dict[str, str]:    if not webhook_secret:

    """Handle account updates - Sync marketplace store"""        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET not configured")

    account = event["data"]["object"]    

    account_id = account["id"]    # Verify the webhook signature

        try:

    logger.info(f"Stripe Connect account updated: {account_id}")        # Parse signature header

            sig_parts = {}

    try:        for part in stripe_signature.split(","):

        # Update the marketplace store            if "=" not in part:

        updated_store = await update_marketplace_store(account)                raise HTTPException(status_code=400, detail="Invalid signature format: missing '=' in part")

        logger.info(f"Marketplace store updated for {account_id}")            key, value = part.split("=", 1)

        return {"status": "success", "account_id": account_id}            sig_parts[key] = value

    except Exception as e:        

        logger.error(f"Failed to update store: {str(e)}")        timestamp = sig_parts.get("t")

        return {"status": "error", "message": str(e)}        signature = sig_parts.get("v1")

        

        if not timestamp or not signature:

async def handle_charge_succeeded(event: Dict[str, Any]) -> Dict[str, str]:            raise HTTPException(status_code=400, detail="Invalid signature format: missing timestamp or signature")

    """Handle successful charge - Update order status"""        

    charge = event["data"]["object"]        # Compute expected signature

    charge_id = charge["id"]        signed_payload = f"{timestamp}.{payload_bytes.decode('utf-8')}"

            expected_sig = hmac.new(

    logger.info(f"Charge succeeded: {charge_id}")            key=webhook_secret.encode("utf-8"),

                msg=signed_payload.encode("utf-8"),

    try:            digestmod=hashlib.sha256

        # Update marketplace order status        ).hexdigest()

        await update_order_status(charge_id, "completed")        

        return {"status": "success", "charge_id": charge_id}        # Compare signatures

    except Exception as e:        if not hmac.compare_digest(signature, expected_sig):

        logger.error(f"Failed to update order: {str(e)}")            raise HTTPException(status_code=400, detail="Invalid signature: signature mismatch")

        return {"status": "error", "message": str(e)}        

    except HTTPException:

        # Re-raise HTTPExceptions as-is

async def handle_charge_failed(event: Dict[str, Any]) -> Dict[str, str]:        raise

    """Handle failed charge - Update order status"""    except ValueError as e:

    charge = event["data"]["object"]        raise HTTPException(status_code=400, detail=f"Webhook signature parsing failed: {str(e)}")

    charge_id = charge["id"]    except Exception as e:

            raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {str(e)}")

    logger.info(f"Charge failed: {charge_id}")    

        # Parse the event

    try:    event = json.loads(payload_bytes.decode("utf-8"))

        await update_order_status(charge_id, "failed")    

        return {"status": "success", "charge_id": charge_id}    # Handle different event types

    except Exception as e:    if event.get("type") == "checkout.session.completed":

        logger.error(f"Failed to update order: {str(e)}")        # Process completed checkout session

        return {"status": "error", "message": str(e)}        session_data = event["data"]["object"]

        # TODO: Add business logic here (e.g., fulfill order, update database)

        pass

async def handle_payment_intent_succeeded(event: Dict[str, Any]) -> Dict[str, str]:    

    """Handle successful payment intent"""    return {"status": "ok"}

    payment_intent = event["data"]["object"]

    payment_id = payment_intent["id"]@app.get("/health")

    async def health():

    logger.info(f"Payment intent succeeded: {payment_id}")    """Health check endpoint."""

        return {"status": "healthy"}

    try:

        await update_order_status(payment_id, "paid")if __name__ == "__main__":

        return {"status": "success", "payment_id": payment_id}    import uvicorn

    except Exception as e:    port = int(os.getenv("PORT", "8000"))

        logger.error(f"Failed to process payment: {str(e)}")    uvicorn.run(app, host="0.0.0.0", port=port)

        return {"status": "error", "message": str(e)}


async def handle_customer_created(event: Dict[str, Any]) -> Dict[str, str]:
    """Handle new customer creation"""
    customer = event["data"]["object"]
    customer_id = customer["id"]
    
    logger.info(f"New customer created: {customer_id}")
    
    try:
        await add_customer_to_store(customer_id, customer)
        return {"status": "success", "customer_id": customer_id}
    except Exception as e:
        logger.error(f"Failed to add customer: {str(e)}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# MARKETPLACE STORE BUILDER
# ============================================================================

async def build_marketplace_store(account: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a complete marketplace store from Stripe Connect account data.
    This creates the storefront structure for selling in the marketplace.
    """
    account_id = account["id"]
    
    store_structure = {
        "store_id": account_id,
        "seller_info": {
            "name": account.get("business_profile", {}).get("name", "Unnamed Store"),
            "description": account.get("business_profile", {}).get("support_address", {}).get("line1", ""),
            "country": account.get("country", "US"),
            "email": account.get("email", ""),
            "phone": account.get("business_profile", {}).get("support_phone", ""),
        },
        "store_pages": {
            "home": {
                "title": "Welcome to Our Store",
                "description": "Explore our products and services",
                "slug": "home",
                "featured_products": []
            },
            "products": {
                "title": "Products",
                "description": "Browse our catalog",
                "slug": "products",
                "categories": []
            },
            "about": {
                "title": "About Us",
                "description": "Learn about our store",
                "slug": "about"
            },
            "contact": {
                "title": "Contact Us",
                "description": "Get in touch",
                "slug": "contact",
                "email": account.get("email", "")
            }
        },
        "payment_methods": {
            "stripe_enabled": True,
            "stripe_account_id": account_id,
            "capabilities": account.get("capabilities", {})
        },
        "status": "active",
        "created_at": str(event.get("created", "")),
        "settings": {
            "currency": "usd",
            "timezone": "UTC",
            "language": "en",
            "store_type": "marketplace"
        }
    }
    
    # TODO: Save store_structure to database
    logger.info(f"Store structure created: {json.dumps(store_structure, indent=2)}")
    
    return store_structure


async def update_marketplace_store(account: Dict[str, Any]) -> Dict[str, Any]:
    """Update existing marketplace store with new account info"""
    account_id = account["id"]
    
    updates = {
        "seller_info": {
            "name": account.get("business_profile", {}).get("name", ""),
            "email": account.get("email", ""),
            "phone": account.get("business_profile", {}).get("support_phone", ""),
        },
        "payment_methods": {
            "capabilities": account.get("capabilities", {})
        },
        "updated_at": str(datetime.datetime.now())
    }
    
    # TODO: Update store in database
    logger.info(f"Store updated: {account_id}")
    
    return updates


async def add_customer_to_store(customer_id: str, customer: Dict[str, Any]) -> None:
    """Add a new customer to the marketplace store"""
    customer_data = {
        "customer_id": customer_id,
        "name": customer.get("name", ""),
        "email": customer.get("email", ""),
        "phone": customer.get("phone", ""),
        "address": customer.get("address", {}),
        "created_at": str(datetime.datetime.now())
    }
    
    # TODO: Save customer to database
    logger.info(f"Customer added to store: {customer_id}")


async def update_order_status(order_id: str, status: str) -> None:
    """Update order status in the marketplace"""
    # TODO: Update order status in database
    logger.info(f"Order {order_id} status updated to: {status}")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "stripe-webhook-handler"}


if __name__ == "__main__":
    import uvicorn
    import datetime
    uvicorn.run(app, host="0.0.0.0", port=8000)
