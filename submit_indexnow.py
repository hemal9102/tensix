import requests
import json
import xml.etree.ElementTree as ET
import os

def get_urls_from_sitemap(sitemap_path):
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url in root.findall('ns:url/ns:loc', namespace):
            if url.text:
                urls.append(url.text.strip())
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
    return urls

def submit_indexnow(host, key, key_location, url_list):
    endpoints = [
        "https://api.indexnow.org/IndexNow",
        "https://www.bing.com/IndexNow"
    ]
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list
    }
    
    for endpoint in endpoints:
        try:
            print(f"Submitting to {endpoint} ...")
            response = requests.post(endpoint, json=payload, headers=headers, timeout=15)
            if response.status_code in [200, 202]:
                print(f"[OK] Successfully submitted to {endpoint}. Status code: {response.status_code}")
            else:
                print(f"[WARN] Response from {endpoint}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[ERROR] Submitting to {endpoint}: {e}")

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    sitemap_path = os.path.join(root_dir, "sitemap.xml")
    host = "www.tensix.in"
    key = "85d35ffc8a454f8ba91ab6e0dde7adf4"
    key_location = f"https://{host}/{key}.txt"
    
    urls = get_urls_from_sitemap(sitemap_path)
    if urls:
        print(f"Found {len(urls)} URLs in {sitemap_path}")
        submit_indexnow(host, key, key_location, urls)
    else:
        print("No URLs found in sitemap.")
