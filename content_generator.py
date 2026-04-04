"""Claude APIを使ってツイート文を生成する"""

import anthropic
from config import ANTHROPIC_API_KEY, get_amazon_url
from sale_manager import get_sale_hashtags, get_current_sale_name


def generate_tweet(product: dict) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    url = get_amazon_url(product["asin"])
    features = "・".join(product["features"])

    # 商品ハッシュタグ（最大2つ）+ セールタグ（最大1つ）
    product_tags = " ".join(product["hashtags"][:2])
    sale_tags = get_sale_hashtags()
    hashtags = product_tags
    if sale_tags:
        hashtags += f" {sale_tags[0]}"

    sale_name = get_current_sale_name()
    if sale_name:
        print(f"[セール] {sale_name}")

    prompt = f"""以下のAmazon商品を紹介するXの投稿文を日本語で作成してください。

商品名: {product["name"]}
カテゴリ: {product["category"]}
特徴: {features}
価格帯: {product["price_range"]}

## 条件
- 全体で200文字以内（URLとハッシュタグを除く）
- 絵文字を2〜3個使う
- 読者が思わず見たくなる魅力的な文章
- 「私も使ってる」「本当におすすめ」など親近感のある表現
- URLやハッシュタグは含めない（後で追加します）

本文のみ出力してください。"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    body = response.content[0].text.strip()
    tweet = f"{body}\n\n{url}\n\n{hashtags}"

    # X の文字数上限は280文字
    if len(tweet) > 280:
        # 本文を短縮
        max_body = 280 - len(url) - len(hashtags) - 4
        body = body[:max_body] + "…"
        tweet = f"{body}\n\n{url}\n\n{hashtags}"

    return tweet
