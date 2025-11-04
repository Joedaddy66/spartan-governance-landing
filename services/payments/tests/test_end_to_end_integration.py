#!/usr/bin/env python3
"""
Integration test (local, in-process) exercising:
  create-checkout-session -> (embedded client) -> webhook (checkout.session.completed)

Notes:
- Runs in-process using FastAPI TestClient against services.payments.main.app
- Stubs stripe.checkout.Session.create to avoid real Stripe API calls.
- Signs the webhook payload using the STRIPE_WEBHOOK_SECRET to exercise signature verification.
- Requires pytest to run.
"""
from __future__ import annotations
import os
import time
import json
import hmac
import hashlib
import pytest
from typing import Dict, Any
from fastapi.testclient import TestClient

# Import the FastAPI app (ensure PYTHONPATH includes repo root or run pytest from repo root)
from services.payments.main import app  # type: ignore

# Helpers: mimic stripe webhook signing scheme used in the harness
def sign_payload(payload_bytes: bytes, webhook_secret: str) -> str:
    timestamp = str(int(time.time()))
    signed_payload = timestamp + "." + payload_bytes.decode("utf-8")
    mac = hmac.new(key=webhook_secret.encode("utf-8"), msg=signed_payload.encode("utf-8"), digestmod=hashlib.sha256)
    signature = mac.hexdigest()
    header = f"t={{timestamp}},v1={{signature}}"
    return header

def make_checkout_session_payload(session_id: str = "cs_test_abc", amount_total: int = 1200, currency: str = "usd") -> Dict[str, Any]:
    return {
        "id": "evt_test_checkout_completed_001",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session_id,
                "object": "checkout.session",
                "amount_total": amount_total,
                "currency": currency,
                "payment_intent": "pi_test_123",
                "metadata": {"integration_test": "true"},
            }
        }
    }

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    """
    Ensure environment variables expected by the app are set for the test.
    STRIPE_WEBHOOK_SECRET must be set to exercise signature verification.
    """
    monkeypatch.setenv("STRIPE_SECRET_KEY", os.getenv("STRIPE_SECRET_KEY", "sk_test_fake_for_local"))
    # Use a deterministic webhook secret for the test
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_test_secret"))
    monkeypatch.setenv("PLATFORM_DOMAIN", "http://localhost:3000")
    monkeypatch.setenv("RETURN_URL", "http://localhost:3000/return")
    monkeypatch.setenv("SUCCESS_URL", "http://localhost:3000/success")
    monkeypatch.setenv("CANCEL_URL", "http://localhost:3000/cancel")
    monkeypatch.setenv("APPLICATION_FEE_CENTS_DEFAULT", "75")
    yield

def test_create_session_and_webhook_end_to_end(monkeypatch):
    """
    End-to-end logical test:
      1) POST /create-checkout-session (compat route)
      2) Verify client_secret returned
      3) POST signed checkout.session.completed to /webhooks/stripe
      4) Verify webhook endpoint returns 200 and {"status":"ok"}
    """
    # 1) Stub stripe.checkout.Session.create to return a fake embedded session
    class FakeSession(dict):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.update(kwargs)
        def get(self, k, d=None):
            return super().get(k, d)

    def fake_checkout_session_create(**kwargs):
        # Simulate Stripe returning session id and client_secret for embedded mode
        return FakeSession(id="cs_test_abc", client_secret="cs_test_client_secret_abc")

    # Apply monkeypatch to the stripe SDK method used by the app
    import stripe
    monkeypatch.setattr(stripe.checkout.Session, "create", staticmethod(fake_checkout_session_create))

    client = TestClient(app)

    # 2) Call /create-checkout-session (compat route)
    payload = {
        "amount_cents": 1200,
        "currency": "usd",
        "description": "ISP-METRIC-L-DROP-V1",
        "connected_account_id": "acct_test_123",  # exercise destination branch
        "application_fee_cents": 75,
        "metadata": {"tenant": "alpha", "packet": "L-DROP-V1"},
        "ui_mode": "embedded"
    }
    resp = client.post("/create-checkout-session", json=payload)
    assert resp.status_code == 200, f"create-checkout-session failed: {{resp.status_code}} {{resp.text}}"
    body = resp.json()
    assert "client_secret" in body and body["client_secret"] is not None, f"expected client_secret in response, got: {{body}}"

    # Simulated embedded client would use client_secret; we skip Stripe.js - now simulate webhook

    # 3) Build and sign checkout.session.completed payload
    evt = make_checkout_session_payload(session_id="cs_test_abc", amount_total=1200, currency="usd")
    evt_bytes = json.dumps(evt).encode("utf-8")
    webhook_secret = os.environ["STRIPE_WEBHOOK_SECRET"]
    sig_header = sign_payload(evt_bytes, webhook_secret)

    # 4) POST signed webhook to /webhooks/stripe
    headers = {"Content-Type": "application/json", "Stripe-Signature": sig_header}
    webhook_resp = client.post("/webhooks/stripe", data=evt_bytes, headers=headers)
    assert webhook_resp.status_code == 200, f"webhook handler returned {{webhook_resp.status_code}}: {{webhook_resp.text}}"
    assert webhook_resp.json() == {"status": "ok"}

    # Sanity: ensure logs or additional processing would be triggered (TODO in app)
    # For now, success of signature verification and 200 response is sufficient evidence.