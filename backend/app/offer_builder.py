"""
Offer Builder for the Autonomy Loop.

This script reads the most recent trending topic from the market scan and
generates a corresponding offer. If a Stripe API key is available via
environment variables, the product and price are created on Stripe; otherwise
the offer details are stored locally. The offer information is then written
to loop_data/offer.json for consumption by the frontend and loop engine.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import stripe

from .utils import get_latest_market_topic, LOOP_DATA_DIR, write_json


def build_offer() -> Dict[str, Any] | None:
    """Generate an offer based on the latest market topic.

    Returns a dictionary with offer details, or None if no topics are
    available. The result includes the product name, description, price in
    cents, currency, creation timestamp and optionally Stripe identifiers.
    """
    topic = get_latest_market_topic()
    if not topic:
        print("⚠️ No market topics available. Run market_agent.py first.")
        return None

    # Compose a simple offer based on the topic
    name = f"AI {topic.title()} Accelerator"
    description = (
        f"Unlock the full potential of {topic} with our AI-driven accelerator."
        " This comprehensive service combines cutting-edge technology with"
        " expert insights to help you dominate your niche."
    )
    # Price in cents (e.g. 4999 => $49.99)
    price_cents = 4999
    currency = os.getenv("CURRENCY", "usd")
    created_at = datetime.utcnow().isoformat()

    offer: Dict[str, Any] = {
        "topic": topic,
        "name": name,
        "description": description,
        "price_cents": price_cents,
        "currency": currency,
        "created_at": created_at,
    }

    stripe_key = os.getenv("STRIPE_API_KEY")
    if stripe_key:
        try:
            stripe.api_key = stripe_key
            product = stripe.Product.create(
                name=name,
                description=description,
            )
            price = stripe.Price.create(
                unit_amount=price_cents,
                currency=currency,
                product=product.id,
            )
            offer["stripe_product_id"] = product.id
            offer["stripe_price_id"] = price.id
            print(f"✅ Created product on Stripe: {product.id}")
        except Exception as exc:
            print(f"⚠️ Failed to create Stripe product: {exc}")
            # Fall back to generating a local product identifier
            offer["stripe_product_id"] = None
            offer["stripe_price_id"] = None
    else:
        # Generate a random product ID for local use
        offer["stripe_product_id"] = None
        offer["stripe_price_id"] = None
        print("ℹ️ STRIPE_API_KEY not set. Offer will be stored locally.")

    return offer


def run() -> None:
    """Entry point for building and persisting an offer."""
    offer = build_offer()
    if not offer:
        return
    output_path = LOOP_DATA_DIR / "offer.json"
    write_json(output_path, offer)
    print(f"✅ Offer written to {output_path}")


if __name__ == "__main__":
    run()