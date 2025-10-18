"""
FastAPI application for the Autonomy Loop backend.

This API exposes endpoints for retrieving the latest offer and recent
market trends. The endpoints are intended for use by the frontend and
other services. CORS is enabled to allow browser-based clients running
on different origins (e.g. Vite dev server).
"""

from __future__ import annotations

from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .utils import read_jsonl, get_offer_data, LOOP_DATA_DIR

import os
import stripe


app = FastAPI(title="Autonomy Loop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/offers/latest", response_model=Dict[str, Any])
async def latest_offer() -> Dict[str, Any]:
    """Return the most recently generated offer.

    If no offer exists, a 404 error is returned.
    """
    offer = get_offer_data()
    if not offer:
        raise HTTPException(status_code=404, detail="No offer available")
    return offer


@app.get("/market", response_model=List[Dict[str, Any]])
async def market_feed(limit: int = 20) -> List[Dict[str, Any]]:
    """Return recent market scan entries.

    The optional `limit` parameter controls how many entries are returned,
    defaulting to 20. Entries are returned in the order they were
    recorded (latest last).
    """
    scan_file = LOOP_DATA_DIR / "market_scan.jsonl"
    data = list(read_jsonl(scan_file))
    return data[-limit:]


@app.get("/")
async def root() -> Dict[str, str]:
    """Simple root endpoint providing a human-friendly message."""
    return {"message": "Welcome to the Autonomy Loop API"}


@app.post("/checkout-session", response_model=Dict[str, Any])
async def create_checkout_session() -> Dict[str, Any]:
    """Create a Stripe Checkout session for the current offer.

    This endpoint expects a Stripe price identifier to be present in the
    current offer. If Stripe is not configured or no price ID is
    available, a 400 error is returned. On success the created session
    URL is returned.
    """
    offer = get_offer_data()
    price_id = offer.get("stripe_price_id") if offer else None
    if not price_id:
        raise HTTPException(status_code=400, detail="Offer not configured for checkout")
    stripe_api_key = os.getenv("STRIPE_API_KEY")
    if not stripe_api_key:
        raise HTTPException(status_code=500, detail="Stripe API key not configured")
    stripe.api_key = stripe_api_key
    # Determine the base URL for redirection (defaults to localhost dev server)
    domain = os.getenv("FRONTEND_BASE_URL", f"http://localhost:{os.getenv('FRONTEND_PORT', '5174')}")
    try:
        session = stripe.checkout.Session.create(
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=f"{domain}/?success=true",
            cancel_url=f"{domain}/?canceled=true",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {"url": session.url}