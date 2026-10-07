# [[Community Hacks: Indexing Automation]]

This note details the community's programmatic hacks, scripts, and workflows used to automate or force indexing across alternative search engines like DuckDuckGo, Brave, and Kagi.

## 1. [[IndexNow Protocol]] (DuckDuckGo, Bing, Yandex)

For DuckDuckGo (and Bing/Yandex), the community standard is the **IndexNow** protocol. Since DuckDuckGo shares indexing infrastructure with Bing, pushing to IndexNow guarantees visibility.

### [[Python Automation Scripts]]
- **`index-now-for-python`**: A widely used PyPI package.
  ```python
  from index_now import submit_url_to_index_now, IndexNowAuthentication
  auth = IndexNowAuthentication(host="yoursite.com", api_key="KEY", api_key_location="...")
  submit_url_to_index_now(auth, "https://yoursite.com/new-page")
  ```

### [[GitHub Automation Scripts]]
- **GitHub Actions**: Repos like `jakob-bagterp/index-now-submit-sitemap-urls-action` automatically ping IndexNow-supported engines when you push new markdown/HTML content to your static site (Jekyll, Hugo, Astro).

## 2. [[n8n Indexing Workflows]]

While n8n is heavily used for the Google Indexing API, it can be adapted for alternative engines:
- **Sitemap Loopers**: An n8n workflow that fetches your `sitemap.xml`, parses it into JSON, and uses the HTTP Request node to POST to IndexNow endpoints (`https://api.indexnow.org/indexnow`).
- **Ping Services**: Automating `GET` requests to Pingomatic or DuckDuckGo's legacy ping URLs when a webhook is triggered by your CMS.

## 3. Hacks for Closed Engines (Brave Search & Kagi)

Unlike Google or Bing, Brave and Kagi do **not** have public push-indexing APIs. The SEO and scraping communities use indirect methods:

### Brave Search Web Discovery Project (WDP) Hack
Brave relies on anonymized user browsing (WDP) to build its index.
- **The Hack**: Communities build headless browser scripts (using Puppeteer/Playwright) integrated with proxies (like Bright Data). The script launches a Brave Browser instance (with WDP opted-in), navigates to the target URLs, and browses them. This "tricks" BraveBot into discovering the URL organically.
- **Manual Submission**: Some automate POST requests to the `https://search.brave.com/submit-url` endpoint using standard Python `requests`.

### Kagi Search
Kagi uses its own Teclis index alongside other indexes. There's no direct indexing bot.
- **The Hack**: Since Kagi heavily relies on high-quality external signals, the community approach is to use tools like **ScrapeGraphAI** or **Firecrawl** to monitor Reddit, Hacker News, and Lobsters for discussions, and automatically inject links there. Kagi parses these high-signal domains rapidly.

## Warnings from [[r/SEO]]
The r/SEO community notes that heavily abusing automated "instant indexing" APIs for general content (outside of JobPosting/BroadcastEvent) can lead to spam flags. 
