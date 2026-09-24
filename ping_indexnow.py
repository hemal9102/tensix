import json
import urllib.request
import re

def submit_indexnow():
    host = "hemalshah.vercel.app"
    key = "hemalshah-indexnow-2026"
    key_location = f"https://{host}/{key}.txt"
    
    # Parse URLs from sitemap
    with open("sitemap_geo_1.xml", "r", encoding="utf-8") as f:
        content = f.read()
    
    urls = re.findall(r"<loc>(.*?)</loc>", content)
    
    endpoint = "https://api.indexnow.org/indexnow"
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls
    }
    
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"IndexNow Submission Status: {response.status}")
            print(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"IndexNow Error: {e.code} - {e.reason}")
        print(e.read().decode('utf-8'))
    except Exception as e:
        print(f"IndexNow Error: {e}")

if __name__ == "__main__":
    submit_indexnow()
