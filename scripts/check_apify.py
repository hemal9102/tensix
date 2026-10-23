import httpx

import os
APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")

def check_apify_actors():
    url = f"https://api.apify.com/v2/store?search=amazon&limit=6&token={APIFY_TOKEN}"
    r = httpx.get(url, timeout=10)
    if r.status_code == 200:
        items = r.json().get("data", {}).get("items", [])
        for it in items:
            actor_id = f"{it.get('username')}/{it.get('name')}"
            title = it.get("title")
            pricing = it.get("pricingModel")
            print(f"Actor: {actor_id} | Title: {title} | Pricing: {pricing}")
    else:
        print("Error:", r.text)

if __name__ == "__main__":
    check_apify_actors()
