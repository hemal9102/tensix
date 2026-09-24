import requests
import json
import xml.etree.ElementTree as ET

def get_urls_from_sitemap(sitemap_path):
    urls = []
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url in root.findall('ns:url/ns:loc', namespace):
            if url.text:
                urls.append(url.text)
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
    return urls

def submit_indexnow(host, key, key_location, url_list):
    endpoint = "https://api.indexnow.org/IndexNow"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": url_list
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        if response.status_code == 200 or response.status_code == 202:
            print(f"Successfully submitted to IndexNow. Status code: {response.status_code}")
        else:
            print(f"Failed to submit. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error submitting to IndexNow: {e}")

if __name__ == '__main__':
    host = "hemalshah.vercel.app"
    key = "c4b69324e9334bbba3ff6f3f02db4fb6"
    key_location = f"https://{host}/{key}.txt"
    sitemap_path = "sitemap.xml"
    
    urls = get_urls_from_sitemap(sitemap_path)
    if urls:
        print(f"Submitting {len(urls)} URLs to IndexNow...")
        submit_indexnow(host, key, key_location, urls)
    else:
        print("No URLs found to submit.")
