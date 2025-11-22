"""
Stripe Webhook Handler & Marketplace Store Builder

Handles all Stripe events and triggers marketplace store creation.
"""

from __future__ import annotations

import os
import json
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel
import stripe

# Initialize Stripe with API key from environment
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_fake_for_local")

app = FastAPI(title="Payments Service")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


class CheckoutSessionRequest(BaseModel):
    amount_cents: int
    currency: str = "usd"
    description: str
    connected_account_id: Optional[str] = None
    application_fee_cents: Optional[int] = None
    metadata: Optional[Dict[str, str]] = None
    ui_mode: str = "embedded"


@app.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutSessionRequest):
    """
    Create a Stripe Checkout Session.
    """
    # Build Stripe checkout session parameters
    params: Dict[str, Any] = {
        "mode": "payment",
        "ui_mode": request.ui_mode,
        "line_items": [{
            "price_data": {
                "currency": request.currency,
                "product_data": {
                    "name": request.description,
                },
                "unit_amount": request.amount_cents,
            },
            "quantity": 1,
        }],
        "metadata": request.metadata or {},
    }

    # Add return URLs for non-embedded mode
    if request.ui_mode != "embedded":
        params["success_url"] = os.getenv("SUCCESS_URL", "http://localhost:3000/success")
        params["cancel_url"] = os.getenv("CANCEL_URL", "http://localhost:3000/cancel")
    else:
        params["return_url"] = os.getenv("RETURN_URL", "http://localhost:3000/return")

    # Handle connected account (Stripe Connect)
    if request.connected_account_id:
        params["payment_intent_data"] = {
            "application_fee_amount": request.application_fee_cents or int(os.getenv("APPLICATION_FEE_CENTS_DEFAULT", "0")),
        }

    # Create the session using Stripe SDK
    session = stripe.checkout.Session.create(**params)

    return {
        "session_id": session.get("id") or session.id,
        "client_secret": session.get("client_secret"),
    }


@app.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature")
):
    """
    Handle Stripe webhook events with signature verification.
    """
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    payload_bytes = await request.body()
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    if not webhook_secret:
        # This is insecure and should only be enabled in a controlled test environment.
        if os.getenv("ALLOW_INSECURE_WEBHOOKS") != "true":
            raise HTTPException(
                status_code=500,
                detail="STRIPE_WEBHOOK_SECRET not configured. Set it, or set ALLOW_INSECURE_WEBHOOKS=true for testing."
            )
        event = json.loads(payload_bytes)
    else:
        try:
            event = stripe.Webhook.construct_event(
                payload=payload_bytes, sig_header=stripe_signature, secret=webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")

    # Handle different event types
    if event.get("type") == "checkout.session.completed":
        # Process completed checkout session
        session_data = event["data"]["object"]
        # TODO: Add business logic here (e.g., fulfill order, update database)
        pass

    # Return the expected response for GitHub Actions workflow
    return {"received": True}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
