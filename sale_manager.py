"""セールイベントのハッシュタグを管理する"""

import json
from datetime import date, datetime
from pathlib import Path

SALE_CONFIG_FILE = Path(__file__).parent / "sale_config.json"

# 日付範囲ベースの定期セール定義
# start/end は (月, 日) のタプル
SCHEDULED_SALES = [
    {
        "name": "新生活セール",
        "start": (3, 1),
        "end": (4, 6),
        "hashtags": ["#新生活セール", "#新生活", "#Amazon新生活"],
    },
    {
        "name": "プライムデー",
        "start": (7, 11),
        "end": (7, 17),
        "hashtags": ["#プライムデー", "#PrimeDay", "#Amazonプライムデー"],
    },
    {
        "name": "ブラックフライデー",
        "start": (11, 22),
        "end": (11, 29),
        "hashtags": ["#ブラックフライデー", "#BlackFriday", "#Amazonブラックフライデー"],
    },
    {
        "name": "年末セール",
        "start": (12, 1),
        "end": (12, 31),
        "hashtags": ["#年末セール", "#Amazon年末", "#お買い物"],
    },
    {
        "name": "初売りセール",
        "start": (1, 1),
        "end": (1, 15),
        "hashtags": ["#初売り", "#Amazon初売り", "#新年"],
    },
]


def _is_active_sale(sale: dict) -> bool:
    """今日がセール期間内かどうか判定する"""
    today = datetime.now().date()
    year = today.year
    start = date(year, *sale["start"])
    end = date(year, *sale["end"])
    return start <= today <= end


def get_sale_hashtags() -> list[str]:
    """現在有効なセールのハッシュタグを返す"""
    # 方法1: sale_config.jsonの手動設定を確認（優先）
    if SALE_CONFIG_FILE.exists():
        with open(SALE_CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
        if config.get("active") and config.get("hashtags"):
            return list(config["hashtags"])

    # 方法2: 日付範囲ベースで自動判定
    for sale in SCHEDULED_SALES:
        if _is_active_sale(sale):
            return list(sale["hashtags"])

    return []


def get_current_sale_name() -> str | None:
    """現在のセール名を返す（ログ用）"""
    if SALE_CONFIG_FILE.exists():
        with open(SALE_CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
        if config.get("active") and config.get("name"):
            return config["name"]

    for sale in SCHEDULED_SALES:
        if _is_active_sale(sale):
            return sale["name"]

    return None
