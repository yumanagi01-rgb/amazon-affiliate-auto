"""X (Twitter) に投稿する"""

import io
import time
import requests
import tweepy
from config import (
    X_API_KEY,
    X_API_KEY_SECRET,
    X_ACCESS_TOKEN,
    X_ACCESS_TOKEN_SECRET,
)


def get_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_KEY_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET,
    )


def get_v1_api() -> tweepy.API:
    """メディアアップロード用のv1 API"""
    auth = tweepy.OAuth1UserHandler(
        X_API_KEY, X_API_KEY_SECRET,
        X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET,
    )
    return tweepy.API(auth)


def fetch_product_image(asin: str) -> bytes | None:
    """ASINからAmazon商品画像を取得する"""
    url = f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SL500_.jpg"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and len(response.content) > 5000:
            return response.content
    except Exception:
        pass
    return None


def upload_image(image_data: bytes) -> str | None:
    """画像をXにアップロードしてmedia_idを返す"""
    try:
        api = get_v1_api()
        media = api.media_upload(
            filename="product.jpg",
            file=io.BytesIO(image_data),
        )
        return media.media_id_string
    except Exception as e:
        print(f"[画像アップロード失敗] {e}")
        return None


def post_tweet(text: str, asin: str | None = None) -> str:
    """ツイートを投稿してツイートIDを返す"""
    client = get_client()
    media_ids = None

    if asin:
        print("[商品画像取得中...]")
        image_data = fetch_product_image(asin)
        if image_data:
            media_id = upload_image(image_data)
            if media_id:
                media_ids = [media_id]
                print("[画像添付OK]")
            else:
                print("[画像なしで投稿]")
        else:
            print("[画像取得失敗 - テキストのみ投稿]")

    for attempt in range(1, 4):
        try:
            if media_ids:
                response = client.create_tweet(text=text, media_ids=media_ids, user_auth=True)
            else:
                response = client.create_tweet(text=text, user_auth=True)
            tweet_id = response.data["id"]
            print(f"[投稿完了] https://x.com/ynhmaf/status/{tweet_id}")
            return tweet_id
        except tweepy.errors.Forbidden as e:
            print(f"[403エラー詳細 attempt={attempt}] api_codes={e.api_codes} api_messages={e.api_messages}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[レスポンスボディ] {e.response.text}")
                headers = e.response.headers
                print(f"[レート制限] remaining={headers.get('x-rate-limit-remaining')} reset={headers.get('x-rate-limit-reset')} limit={headers.get('x-rate-limit-limit')}")
            if attempt < 3:
                wait = attempt * 10
                print(f"[リトライ] {wait}秒後に再試行します...")
                time.sleep(wait)
            else:
                raise


def test_connection() -> bool:
    """接続テスト"""
    try:
        client = get_client()
        me = client.get_me()
        print(f"[接続OK] @{me.data.username}")
        return True
    except Exception as e:
        print(f"[接続エラー] {e}")
        return False
