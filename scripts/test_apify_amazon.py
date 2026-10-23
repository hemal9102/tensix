import time
import httpx
import json

import os
APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")

def test_amazon_live_asin():
    # Use real live Amazon product: Apple AirPods Pro 2 (ASIN: B0D1XD1ZV3)
    actor_id = "junglee~free-amazon-product-scraper"
    run_url = f"https://api.apify.com/v2/acts/{actor_id}/runs?token={APIFY_TOKEN}"
    run_input = {
        "categoryUrls": [
            {"url": "https://www.amazon.com/dp/B0D1XD1ZV3"}
        ],
        "maxItems": 1
    }
    
    print(f"[*] Dispatching live ASIN (B0D1XD1ZV3) to Apify...")
    r = httpx.post(run_url, json=run_input, timeout=15)
    
    if r.status_code in [200, 201]:
        run_data = r.json().get("data", {})
        run_id = run_data.get("id")
        dataset_id = run_data.get("defaultDatasetId")
        print(f"[+] Run Triggered: {run_id}")
        
        poll_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
        for attempt in range(12):
            time.sleep(5)
            pr = httpx.get(poll_url, timeout=10)
            status = pr.json().get("data", {}).get("status")
            print(f"  [>] Status = {status} (Check {attempt+1})")
            if status == "SUCCEEDED":
                items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}"
                items = httpx.get(items_url, timeout=10).json()
                if items:
                    sample = items[0]
                    print("\n[✓] APACHE/AKAMAI BYPASS SUCCESS:")
                    print("  * Title:", sample.get("title"))
                    print("  * Price:", sample.get("price"))
                    print("  * Rating Stars:", sample.get("stars"))
                    print("  * Total Reviews:", sample.get("reviewsCount"))
                    print("  * Brand:", sample.get("brand"))
                    print("  * ASIN:", sample.get("asin"))
                    specs = sample.get("specifications", {})
                    if specs and isinstance(specs, dict):
                        print("  * Extracted Spec Matrix:")
                        for k, v in list(specs.items())[:5]:
                            print(f"     - {k}: {v}")
                return items
            elif status in ["FAILED", "ABORTED"]:
                print(f"[!] Run ended: {status}")
                break

if __name__ == "__main__":
    test_amazon_live_asin()
