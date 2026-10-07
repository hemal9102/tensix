# Indexing Automation for Kagi, Brave Search, and Mojeek

This note covers the availability of [[Indexing Automation]] (like [[IndexNow]] or [[Google Search Console]]-style APIs) and manual submission methods for independent search engines: [[Kagi]], [[Brave Search]], and [[Mojeek]].

## [[Kagi]]
* **API / Automated Submission:** None. Kagi does not provide an official Webmaster Tools portal, Indexing API, or support for the [[IndexNow]] protocol.
* **Manual Submission:** There is no "Submit URL" feature.
* **How it works:** Kagi maintains its own index using **KagiBot**. To get indexed, webmasters must rely on organic discovery. Ensuring the site is accessible, has high-quality content, and uses standard `robots.txt` and sitemap practices is the only way to be crawled.

## [[Brave Search]]
* **API / Automated Submission:** No direct indexing API or official [[IndexNow]] integration for direct pushes.
* **Manual Submission:** Brave provides a simple URL submission tool at `https://search.brave.com/submit-url`.
* **How it works:** 
  * Ensure your `sitemap.xml` is linked in your `robots.txt` file, which Brave's crawler will discover.
  * Brave heavily relies on the **Web Discovery Project (WDP)**, an opt-in feature where Brave browser users anonymously contribute browsing data to help discover and index new pages.
  * Building quality backlinks and traditional SEO remains effective.

## [[Mojeek]]
* **API / Automated Submission:** No public webmaster tools or [[IndexNow]] support for general web search indexing. Mojeek does offer paid API services ([[Mojeek Web Search API]] and [[Mojeek Site Search API]]) for organizations, where the Site Search API includes on-demand crawling for internal site search purposes.
* **Manual Submission:** No manual URL submission form exists.
* **How it works:** Mojeek operates an entirely independent crawler. It discovers sites automatically through organic, genuine links on the web. If you suspect crawling issues, you can reach out via the [Mojeek Community](https://community.mojeek.com/).

## Summary
Unlike major engines that support programmatic submission, these privacy-focused and independent engines primarily rely on classic web crawling, user-assisted discovery (Brave's WDP), and standard `robots.txt`/`sitemap.xml` conventions rather than dedicated [[Indexing Automation]].
