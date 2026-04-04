"""スケジューラー - 1日5回自動投稿"""

import sys
import io
import time
import schedule
import traceback
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from config import get_random_product, save_post_history
from content_generator import generate_tweet
from x_poster import post_tweet


def job() -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*40}")
    print(f"[{now}] 投稿開始")
    try:
        product = get_random_product()
        print(f"[商品選択] {product['name']}")
        tweet = generate_tweet(product)
        print(f"[ツイート]\n{tweet}")
        tweet_id = post_tweet(tweet, asin=product["asin"])
        save_post_history(product["asin"], tweet)
        print(f"[完了] ID: {tweet_id}")
    except Exception as e:
        print(f"[エラー] {e}")
        traceback.print_exc()


def main() -> None:
    print("ガジェ美ライフ 自動投稿スケジューラー起動")
    print("投稿時刻: 7:00 / 12:00 / 18:00 / 20:00 / 22:00")
    print("停止: Ctrl+C\n")

    schedule.every().day.at("07:00").do(job)
    schedule.every().day.at("12:00").do(job)
    schedule.every().day.at("18:00").do(job)
    schedule.every().day.at("20:00").do(job)
    schedule.every().day.at("22:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
