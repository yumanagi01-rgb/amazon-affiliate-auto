"""設定・環境変数の読み込み"""

import os
import json
import random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
AMAZON_ASSOCIATE_ID = os.environ.get("AMAZON_ASSOCIATE_ID", "ynhmaf-22")

X_API_KEY = os.environ["X_API_KEY"]
X_API_KEY_SECRET = os.environ["X_API_KEY_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_TOKEN_SECRET = os.environ["X_ACCESS_TOKEN_SECRET"]

PRODUCTS_DIR = Path(__file__).parent / "products"
HISTORY_FILE = Path(__file__).parent / "post_history.json"


def get_amazon_url(asin: str) -> str:
    return f"https://www.amazon.co.jp/dp/{asin}?tag={AMAZON_ASSOCIATE_ID}"


def load_all_products() -> list[dict]:
    products = []
    for json_file in PRODUCTS_DIR.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            items = json.load(f)
            for item in items:
                item["genre"] = json_file.stem
            products.extend(items)
    return products


def get_random_product() -> dict:
    products = load_all_products()
    history = _load_history()
    posted_asins = {h["asin"] for h in history}

    # 未投稿の商品を優先
    unposted = [p for p in products if p["asin"] not in posted_asins]
    pool = unposted if unposted else products

    return random.choice(pool)


def save_post_history(asin: str, tweet_text: str) -> None:
    history = _load_history()
    history.append({"asin": asin, "tweet": tweet_text[:50], "posted_at": _now()})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def _load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, encoding="utf-8") as f:
        return json.load(f)


def _now() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
