"""
Market Pulse Agent for the Autonomy Loop.

This module scrapes multiple public sources to identify trending topics and
writes them to a JSON Lines file in the loop_data directory. Each entry in
the file includes the source, a timestamp and the topic string.

Sources currently include:
  * Reddit trending subreddits
  * Google Trends daily trending searches for the US
  * Amazon Movers & Shakers product names

This script can be run directly to perform a one-off scan. It is also invoked
by the loop orchestrator to feed downstream offer generation.
"""

from __future__ import annotations

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from typing import List, Dict


HEADERS = {
    "User-Agent": "AutonomyLoop-MarketAgent/1.0 (https://drox.ai)"
}

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOOP_DATA_DIR = BASE_DIR / "loop_data"
LOOP_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = LOOP_DATA_DIR / "market_scan.jsonl"


def fetch_reddit_trends() -> List[str]:
    """Fetch trending subreddits from Reddit's trending API.

    Returns up to five subreddit titles. The API may fail if Reddit
    rate‑limits or changes its interface; in that case, an empty list is
    returned.
    """
    url = "https://www.reddit.com/r/trendingsubreddits.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return [child["data"]["title"] for child in data["data"]["children"][:5]]
    except Exception:
        return []


def fetch_google_trends() -> List[str]:
    """Fetch daily trending search topics for the US from Google Trends.

    Returns up to five trending topics. If the request fails, an empty list
    is returned.
    """
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "xml")
        return [item.title.text.strip() for item in soup.find_all("item")[:5]]
    except Exception:
        return []


def fetch_amazon_movers() -> List[str]:
    """Fetch product names from Amazon's Movers & Shakers page.

    Returns up to five product titles. Amazon may block automated requests,
    so this method may frequently return an empty list unless requests are
    proxied through a user agent with cookies. This script intentionally
    does not include proxy logic; it simply falls back gracefully.
    """
    url = "https://www.amazon.com/gp/movers-and-shakers"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.select(".zg-item-immersion .p13n-sc-truncated")
        return [item.get_text(strip=True) for item in items[:5]]
    except Exception:
        return []


def emit_jsonl(source: str, topics: List[str]) -> None:
    """Append trend entries to the output file as JSON lines.

    Args:
        source: The name of the trend source (e.g. 'reddit').
        topics: A list of strings representing trending topics.
    """
    now = datetime.utcnow().isoformat()
    with OUTPUT_FILE.open("a", encoding="utf-8") as f:
        for topic in topics:
            entry = {
                "source": source,
                "timestamp": now,
                "topic": topic,
            }
            json.dump(entry, f)
            f.write("\n")


def run() -> None:
    """Execute the market scan across all sources and write results."""
    print("📡 Market Pulse Agent started")
    all_sources: Dict[str, List[str]] = {
        "reddit": fetch_reddit_trends(),
        "google_trends": fetch_google_trends(),
        "amazon_movers": fetch_amazon_movers(),
    }
    for source, topics in all_sources.items():
        if topics:
            emit_jsonl(source, topics)
            print(f"  ↳ {source} OK: {len(topics)} topics")
        else:
            print(f"  ↳ {source} FAILED or returned no data")
    print(f"✅ Trends written to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()