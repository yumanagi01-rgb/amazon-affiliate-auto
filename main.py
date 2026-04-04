"""メインスクリプト - 1回実行で1ツイート投稿"""

import argparse
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from config import get_random_product, save_post_history
from content_generator import generate_tweet
from x_poster import post_tweet, test_connection


def run(dry_run: bool = False) -> None:
    """商品を選んでツイートを生成・投稿する"""
    product = get_random_product()
    print(f"[商品選択] {product['name']} ({product['genre']})")

    tweet = generate_tweet(product)
    print(f"\n[生成ツイート]\n{tweet}\n")
    print(f"[文字数] {len(tweet)}")

    if dry_run:
        print("[DRY RUN] 実際には投稿しません")
        return

    tweet_id = post_tweet(tweet, asin=product["asin"])
    save_post_history(product["asin"], tweet)
    print(f"[完了] ツイートID: {tweet_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="ガジェ美ライフ 自動投稿")
    parser.add_argument("--dry-run", action="store_true", help="投稿せずに確認のみ")
    parser.add_argument("--test", action="store_true", help="X API接続テスト")
    args = parser.parse_args()

    if args.test:
        test_connection()
        return

    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
