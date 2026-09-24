import os
import re
import json
import urllib.request
import urllib.parse

root_dir = r"H:\portfolio_website\hemalshah"
key = "c4b69324e9334bbba3ff6f3f02db4fb6"
host = "hemalshah.vercel.app"

def get_urls_from_sitemap():
    sitemap_path = os.path.join(root_dir, 'sitemap.xml')
    if not os.path.exists(sitemap_path):
        print(f"Error: {sitemap_path} not found.")
        return []
        
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    urls = re.findall(r'<loc>(.*?)</loc>', content)
    return urls

def submit_to_indexnow(urls):
    if not urls:
        print("No URLs found to submit.")
        return

    # Using Bing's IndexNow endpoint (they auto-share with Yandex, Seznam, etc.)
    endpoint = "https://api.indexnow.org/indexnow"
    
    data = {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls
    }
    
    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(endpoint, data=json_data, headers={'Content-Type': 'application/json; charset=utf-8'})
    
    try:
        response = urllib.request.urlopen(req)
        print(f"IndexNow Submission Successful! HTTP Status: {response.getcode()}")
        print(f"Submitted {len(urls)} URLs for instant indexing.")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        error_msg = e.read().decode('utf-8')
        print(f"Details: {error_msg}")
    except Exception as e:
        print(f"Error submitting to IndexNow: {str(e)}")

if __name__ == "__main__":
    urls = get_urls_from_sitemap()
    if urls:
        for u in urls[:5]:
            print(f"Found URL: {u}")
        print("...")
        submit_to_indexnow(urls)
