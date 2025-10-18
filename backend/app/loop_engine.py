"""
Loop Engine for the Autonomy Loop.

This component orchestrates continuous scans, offer generation and feedback
analysis. In its simplest form it runs the market agent and offer builder
periodically, producing new offers when fresh market data arrives. In a
production deployment this engine would also monitor sales metrics from
Stripe (or other payment providers) and adjust pricing or messaging accordingly.
"""

from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from .market_agent import run as run_market_agent
from .offer_builder import run as run_offer_builder
from .utils import get_offer_data, get_latest_market_topic


def loop_once() -> None:
    """Execute a single iteration of the autonomy loop.

    This involves scanning the market, building an offer and reporting the
    outcome. Additional feedback mechanisms could be added here to adjust
    future iterations based on performance.
    """
    print(f"\n🔄 Loop iteration started: {datetime.utcnow().isoformat()}")
    run_market_agent()
    run_offer_builder()
    offer = get_offer_data()
    if offer:
        print(f"🎁 Current offer: {offer['name']} (${offer['price_cents']/100:.2f})")
    else:
        print("⚠️ No offer found after build step.")


def run() -> None:
    """Run the loop engine.

    The engine continuously executes loop iterations with a configurable
    sleep interval (default 5 minutes). If the environment variable
    RUN_ONCE is set to any non-empty value, the engine will execute only
    a single iteration and exit. This is useful for testing or integration
    into orchestrators like loop.ps1.
    """
    interval = int(os.getenv("LOOP_INTERVAL", "300"))
    once = bool(os.getenv("RUN_ONCE"))
    if once:
        loop_once()
        return
    print("🚀 Loop engine started. Running indefinitely...")
    while True:
        loop_once()
        print(f"⏳ Sleeping for {interval} seconds...")
        time.sleep(interval)


if __name__ == "__main__":
    run()