"""セールイベントのハッシュタグを管理する"""

import json
from datetime import datetime
from pathlib import Path

SALE_CONFIG_FILE = Path(__file__).parent / "sale_config.json"

# 日付ベースの定期セール定義 (month, day_start, day_end, name, hashtags)
SCHEDULED_SALES = [
    {
        "name": "新生活セール",
        "months": [3, 4],
        "hashtags": ["#新生活セール", "#新生活", "#Amazon新生活"],
    },
    {
        "name": "プライムデー",
        "months": [7],
        "hashtags": ["#プライムデー", "#PrimeDay", "#Amazonプライムデー"],
    },
    {
        "name": "ブラックフライデー",
        "months": [11],
        "hashtags": ["#ブラックフライデー", "#BlackFriday", "#Amazonブラックフライデー"],
    },
    {
        "name": "年末セール",
        "months": [12],
        "hashtags": ["#年末セール", "#Amazon年末", "#お買い物"],
    },
    {
        "name": "初売りセール",
        "months": [1],
        "hashtags": ["#初売り", "#Amazon初売り", "#新年"],
    },
]


def get_sale_hashtags() -> list[str]:
    """現在有効なセールのハッシュタグを返す"""
    hashtags = []

    # 方法1: sale_config.jsonの手動設定を確認
    if SALE_CONFIG_FILE.exists():
        with open(SALE_CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
        if config.get("active") and config.get("hashtags"):
            hashtags.extend(config["hashtags"])
            return hashtags  # 手動設定が優先

    # 方法2: 日付ベースで自動判定
    month = datetime.now().month
    for sale in SCHEDULED_SALES:
        if month in sale["months"]:
            hashtags.extend(sale["hashtags"])
            break

    return hashtags


def get_current_sale_name() -> str | None:
    """現在のセール名を返す（ログ用）"""
    if SALE_CONFIG_FILE.exists():
        with open(SALE_CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
        if config.get("active") and config.get("name"):
            return config["name"]

    month = datetime.now().month
    for sale in SCHEDULED_SALES:
        if month in sale["months"]:
            return sale["name"]

    return None
