# The Omnipresent 15-Point AEO/GEO Schema Architecture
Date: August 2026

## Concept
Traditional SEO uses "siloed" schemas (e.g., `JobPosting` on job pages, `Organization` on the About page, `FAQPage` on the FAQ page). This forces search engines to crawl multiple pages to build a complete Knowledge Graph of the company.

To optimize for Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) specifically for LLMs (ChatGPT, Gemini, Perplexity, Google SGE), we moved to an **Omnipresent `@graph` Architecture**.

## Implementation
Every single page (over 50+ static HTML pages and dynamic PHP pages) now serves a single, massive JSON-LD `@graph` object that contains up to 17 interconnected schema types. This ensures that no matter which URL an AI crawler visits, it instantly learns everything about the Job Recruitment brand, its services, location, trust signals, and dataset.

## The 15+ Schemas Injected Per Page
1. **EmploymentAgency**: A specialized `LocalBusiness` type.
2. **ImageObject**: The canonical company logo.
3. **PostalAddress**: SG Highway, Ahmedabad, Gujarat (Local SEO).
4. **GeoCoordinates**: Exact Latitude and Longitude for Maps integration.
5. **ContactPoint**: HR Support telephone with `availableLanguage` (Hindi, English, Gujarati).
6. **AggregateRating**: A global 4.9-star trust rating to establish E-E-A-T.
7. **Organization**: The parent corporate entity.
8. **Brand**: Includes the slogan "Your Career, Our Priority".
9. **Person**: The Founder/Senior Recruitment Strategist to satisfy the "Experience/Expertise" in E-E-A-T.
10. **WebSite**: The domain authority and root object.
11. **SearchAction**: `potentialAction` to enable Sitelink Search Box.
12. **WebPage**: The specific URL being crawled.
13. **BreadcrumbList**: The navigation path.
14. **Service**: Job Placement and Corporate Recruitment services.
15. **OfferCatalog / Offer**: The taxonomy of recruitment services offered.
16. **Dataset**: A declaration of the Ahmedabad Job Market Data available on the site.
17. **FAQPage**: Crucial anti-scam QA ("100% Free Agency").

## Code Structure
All these nodes are linked together using `@id`. For example, `WebPage` has `about: {"@id": "https://jobrecruitment.in/#employment-agency"}`, and `EmploymentAgency` has `image: {"@id": "https://jobrecruitment.in/#logo"}`.

### Dynamic Generation
For PHP pages (`job.php`, `job-details.php`), this graph is generated dynamically via `backend/core/SchemaGenerator.php` to inject specific `$role`, `$location`, and `$salary` data into the graph.

For HTML static pages, it was injected en-masse via a custom Python script (`inject_omni_schema_15.py`).

## Impact
This guarantees maximum entity recognition. Search engines no longer need to guess if we are a recruitment agency in Ahmedabad; it is explicitly fed to them in a machine-readable format on every interaction.
