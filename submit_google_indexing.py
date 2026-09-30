#!/usr/bin/env python3
"""
Google Indexing API Bulk Submitter for tensix.in
Uses google-service-account.json to submit sitemap URLs directly to Google's Indexing API.
"""

import os
import re
import json
import time
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(ROOT_DIR, "google-service-account.json")
SITEMAP_FILE = os.path.join(ROOT_DIR, "sitemap.xml")
INDEXING_ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]

def get_urls_from_sitemap():
    if not os.path.exists(SITEMAP_FILE):
        print(f"[ERROR] Sitemap not found at {SITEMAP_FILE}")
        return []
    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    urls = re.findall(r"<loc>(.*?)</loc>", content)
    return urls

def get_access_token():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"[ERROR] Service account JSON not found at {SERVICE_ACCOUNT_FILE}")
        return None, None
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        credentials.refresh(Request())
        with open(SERVICE_ACCOUNT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return credentials.token, data.get("client_email")
    except Exception as e:
        print(f"[ERROR] Failed to obtain access token: {e}")
        return None, None

def submit_url(url, token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    try:
        response = requests.post(INDEXING_ENDPOINT, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("  Google Indexing API — Bulk URL Publisher (tensix.in)")
    print("=" * 60)

    urls = get_urls_from_sitemap()
    if not urls:
        print("[WARN] No URLs found in sitemap.")
        return

    print(f"\n[INFO] Found {len(urls)} URLs in sitemap.xml")
    print(f"[INFO] Using credentials: {SERVICE_ACCOUNT_FILE}")
    token, client_email = get_access_token()
    if not token:
        print("[ERROR] Authentication failed. Exiting.")
        return

    print(f"[OK] Authenticated successfully as: {client_email}")
    print("[NOTE] Ensure this service account email is added as an OWNER in Google Search Console for tensix.in / https://www.tensix.in\n")

    success_count = 0
    fail_count = 0

    for i, url in enumerate(urls, 1):
        success, result = submit_url(url, token)
        if success:
            success_count += 1
            print(f"[{i}/{len(urls)}] [OK] {url}")
        else:
            fail_count += 1
            print(f"[{i}/{len(urls)}] [FAIL] {url} -> {result}")
        time.sleep(0.15)  # gentle rate limit adherence

    print("\n" + "=" * 60)
    print(f"  Google Indexing Summary: {success_count} succeeded, {fail_count} failed")
    print("=" * 60)

if __name__ == "__main__":
    main()
