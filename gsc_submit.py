import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import xml.etree.ElementTree as ET

# Path to the service account credentials JSON file
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/indexing']
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

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

def notify_google(url, session):
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    response = session.post(ENDPOINT, json=payload)
    if response.status_code == 200:
        print(f"Successfully notified Google for: {url}")
    else:
        print(f"Failed to notify Google for: {url}. Status code: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        print("Please follow these steps to set up Google Search Console API indexing:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Create a project and enable the 'Web Search Indexing API'")
        print("3. Create a Service Account and generate a JSON key")
        print("4. Save the JSON key in this directory as 'service_account.json'")
        print("5. In Google Search Console, add the Service Account email as an 'Owner' of the property.")
    else:
        try:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            session = AuthorizedSession(credentials)
            
            sitemap_path = "sitemap.xml"
            urls = get_urls_from_sitemap(sitemap_path)
            
            if urls:
                print(f"Submitting {len(urls)} URLs to Google Indexing API...")
                for url in urls:
                    notify_google(url, session)
            else:
                print("No URLs found to submit.")
        except Exception as e:
            print(f"Error setting up credentials: {e}")
