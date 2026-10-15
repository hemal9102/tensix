# TenSix Competitor Outflank — Action Plan

Date: 2026-10-15 16:10 | Judge: OpenRouter typesafe/jev-1.13 decisions (calibrated)
Competitors analyzed: kanhasoft.com, dngwebdeveloper.com, duplextech.com, suntecindia.com, areinfotech.com, esparkinfo.com, orangemantra.com, greencubes.co.in

> Free recon: curl sitemap crawl + Google Suggest + Jev intent/value clustering. No paid SEO API. Techniques per `docs/05 - Competitor Reverse-Engineering ...`.

## 1. Competitor snapshot

| Rival | Pages (sitemap) | Service pages scanned | TTFB | Server/cache |
|---|---|---|---|---|
| kanhasoft.com | 127 | 34 | 0.86s | cloudflare / DYNAMIC |
| dngwebdeveloper.com | 71 | 35 | 0.06s | hcdn |
| duplextech.com | 422 | 35 | 0.09s | nginx/1.26.3 |
| suntecindia.com | 762 | 35 | 0.84s | Apache |
| areinfotech.com | 288 | 35 | 1.20s | LiteSpeed |
| esparkinfo.com | 960 | 35 | 0.40s | cloudflare / BYPASS |
| orangemantra.com | 1774 | 35 | 0.08s | cloudflare / HIT |
| greencubes.co.in | 180 | 35 | 0.30s | Apache |

**Speed edge:** kanhasoft.com, suntecindia.com, areinfotech.com have TTFB > 0.6s — TenSix's static edge (<50ms) is a direct Core Web Vitals ranking lever against them (doc §1C/§6).

## 2. Keyword clusters (what buyers search; what rivals target)

### CTO / Tech Leadership  (4 keywords, 3 high-value)

**High-value targets:**
- fractional cto cost
- fractional cto
- fractional cto india

<details><summary>Other cto / tech leadership keywords (1)</summary>

- fractional cto hourly rate

</details>

### Money Service (build)  (120 keywords, 36 high-value)

**High-value targets:**
- custom erp software development company
- custom crm development agency
- custom crm software development company
- custom saas development agency
- custom crm development company dubai
- custom crm development agency in dubai
- custom crm development company
- custom crm software development dubai
- custom crm software development services
- custom saas development company
- custom crm software development
- custom crm development services
- custom saas product development
- custom crm web portal development company
- custom crm development
- custom saas development services
- custom saas solution
- custom crm software development agency in india
- custom saas development
- b2b marketplace development company
- custom crm development company in mumbai
- ai agent development services
- custom saas app development
- b2b website development agency
- business process automation services

<details><summary>Other money service (build) keywords (30)</summary>

- aeo geo seo checker
- affordable website development in ahmedabad
- ai agent development
- ai agent development company in india
- ai agent development cost
- ai agent development proposal
- ai agent development proposal pdf
- ai agent development sw engineer
- ai enabled knowledge base
- ai ml development
- ai ml development company
- ai ml development company in australia
- ai ml development company in canada
- ai ml development company in india
- ai ml development company in uk
- ai ml development company in usa
- ai ml software development company
- android app development
- android app development ai
- android app development cost
- android app development cost in india
- android app development kotlin
- android app development online
- android app development using ai
- android development
- android development studio
- angular app development company
- angular application development
- angular mobile app development
- angular native app development

</details>

### Local (Ahmedabad)  (7 keywords, 0 high-value)

<details><summary>Other local (ahmedabad) keywords (7)</summary>

- about ahmedabad
- ai ml development company in ahmedabad
- b2b locations
- b2b sites in usa
- digital marketing agency ahmedabad
- ecommerce website design company ahmedabad
- ecommerce website development ahmedabad

</details>

### Comparison / Alternatives  (16 keywords, 1 high-value)

**High-value targets:**
- best custom crm development companies in india

<details><summary>Other comparison / alternatives keywords (15)</summary>

- ai agent development tools
- artificial intelligence best company in india
- artificial intelligence companies in india
- artificial intelligence top companies in india
- artificial intelligence top companies india
- best ai ml development company in pune
- best b2b manufacturing websites
- best website development ahmedabad
- best website development company ahmedabad
- blockchain development top companies india
- cloud application development company top companies
- data science top companies
- data science top companies india
- devops top companies
- email deliverability tools

</details>

### Informational  (59 keywords, 0 high-value)

<details><summary>Other informational keywords (30)</summary>

- about india
- acquisition aeo geo seo
- aeo geo llm seo
- aeo geo seo difference
- aeo geo seo full form
- aeo geo seo strategy
- ai agent development framework
- ai development and machine learning
- ai development empowered by data annotation
- ai enabled knowledge management
- ai enabled systems
- ai enabled technologies
- ai knowledge base example
- amazon marketing cloud
- amazon ses configuration
- amazon ses configuration for sending email
- amazon ses configuration set
- amazon ses dkim setup
- amazon ses email setup
- amazon ses settings
- amazon ses setup
- amazon ses setup guide
- amazon ses setup smtp
- amazon simple email service setup
- android app development ai tool free
- android app development language
- android app development software
- android app development tools
- android development documentation
- android development environment

</details>

### Irrelevant  (14 keywords, 0 high-value)

<details><summary>Other irrelevant keywords (14)</summary>

- 3d design portfolio website
- 3d modeling portfolio website
- about us images for website
- amazon marketing agency india
- amazon marketing head india
- android development board
- b2b factory website
- b2b manufacturing companies
- b2b manufacturing marketplace
- business process automation analyst
- business process automation icon
- ecommerce digital marketing agency
- email deliverability engineer
- email deliverability specialist job

</details>

## 3. TenSix priority actions

1. **Own the CTO/leadership cluster** — TenSix already has a fractional-CTO service; build dedicated, honest pages for: fractional cto cost, fractional cto, fractional cto india. This is the highest-ticket, lowest-competition cluster for a solo studio.
3. **Out-specify money-service keywords** — custom erp software development company, custom crm development agency, custom crm software development company, custom saas development agency, custom crm development company dubai, custom crm development agency in dubai. Each needs a 45–55 word Position-0 answer card + FAQPage schema + fixed-price plan (doc §4, CLAUDE.md §4.2/§5).
4. **Capture comparison intent** — 16 comparison/alternative queries exist (e.g. ai agent development tools, artificial intelligence best company in india, artificial intelligence companies in india, artificial intelligence top companies in india). TenSix's existing 'vs agencies' page can be extended honestly.
5. **After publishing**, push via Google Indexing API + IndexNow for instant crawl (doc §5).

## 4. Per-rival target slugs (what they rank on; mirror honestly where TenSix is absent)

**kanhasoft.com:** ai enabled knowledge base, ai ml development company, android app development, angular application development, cloud saas based application development, codeigniter application development, crm software development, custom amazon seller tools, custom software development, django application development, erp software development, flutter app development company, hire angular developers, hire django developers, hire laravel developers

**dngwebdeveloper.com:** about, b2b portal development, cargo management system, cms website development, courier software, custom website designing, directory portal development, dynamic website designing, dynamic website development, e learning portal development, get quote, inventory management software, job portal development, logistic software, matrimonial portal development

**duplextech.com:** about us, artificial intelligence development ai ml, big data analytics company, block chain development company, blogs, cancellation and refund policy, careers, cloud computing solutions company, contact us, crm or lead management system, crm software development company, custom erp software development company, custom software development company, digital marketing seo smo, ecommerce website application development

**suntecindia.com:** about us, ai development empowered by data annotation, amazon vendor central case management reduced issue resolution time for beauty brand, business process outsourcing company, case study data quality management, client success stories, contactus, creating premium amazon a plus content for a global art retailer, custom list building for cloud based software testing platform, data, data mining and research for a healthcare consultancy, digital engineering, digital marketing, ecommerce, ecommerce order analysis with executive dashboards

**areinfotech.com:** 3d design portfolio, about us, all, amazon marketing, android development, blogs, case studies, client speak, contact us, content writing, digital marketing agency ahmedabad, digital marketing hospitals, domain name registration, ecommerce digital marketing agency, ecommerce website development

**esparkinfo.com:** artificial intelligence top companies india, blockchain development top companies india, cloud application development company top companies, data science top companies, data science top companies india, devops top companies, generative ai adaptive ai development top companies, generative ai ai agent top companies india, generative ai ai copilot top companies, generative ai top companies, generative ai top companies india, machine learning top companies, mobile development react native top companies, software development custom top companies india, software development digital transformation top companies india

**orangemantra.com:** germany mobile application development berlin hamburg frankfurt, hire java developer, hire magento developer, magento developer brisbane sydney australia, magento developer toronto canada, magento developer united kingdom, magento developer united states, magento ecommerce store development paris lyon marseille, magento store, norway app development oslo bergen trondheim stavanger, norway digital marketing oslo bergen trondheim stavanger, norway magento ecommerce oslo bergen trondheim stavanger, norway wordpress development oslo bergen trondheim stavanger, prestashop development, prestashop development paris lyon marseille

**greencubes.co.in:** about us, benefits of hiring full website design company, careers, case studies, case studies alkaline herb shop custom shopify website development, case studies carefree charters custom wordpress development, case studies gokul traders custom wordpress development, case studies involve your senses custom shopify website development, case studies munchy theme custom shopify website development, case studies ocubio custom wordpress development, case studies vulcan infrastructure custom wordpress development, contact, current opening, ecommerce website design company ahmedabad, global presence

