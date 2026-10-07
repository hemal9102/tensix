"""Build /services/<slug>.html pages and refresh the generated parts of services.html.

Stdlib only. Idempotent: re-running produces identical files.

    python build_service_pages.py

SERVICES is the single source of truth for every service page, the pricing
cards on the services hub (between the BEGIN/END pricing markers) and the
hub's JSON-LD. Head boilerplate, header and footer are copied from services.html.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
HUB = os.path.join(ROOT, "services.html")
OUT_DIR = os.path.join(ROOT, "services")
SITE = "https://www.tensix.in"
ID = "https://tensix.in"
OG_IMAGE = SITE + "/assets/tensix-swiss-logo.jpg"
AREA = [
    {"@type": "City", "name": "Ahmedabad"},
    {"@type": "State", "name": "Gujarat"},
    {"@type": "Country", "name": "India"},
    "Worldwide",
]


def plan(name, price, period, hook, features, cta, slug, usd="", featured=False):
    return dict(name=name, price=price, usd=usd, period=period, hook=hook,
                features=features, cta=cta, slug=slug, featured=featured)


# Body strings are HTML (escape & as &amp;). title/description are plain text.
SERVICES = [
    dict(
        slug="ai-agent-development", hub_group="pricing-ai",
        name="AI Agent Development", service_type="AI agent and AI assistant development",
        summary="AI assistants that answer from your own documents, and AI agents that handle repetitive work.",
        h1="AI Assistants and Agents That Do Real Work for Your Business",
        title="AI Agent and Assistant Development, Ahmedabad | TENSIX",
        description="Custom AI assistants and agents that answer from your own documents, handle repetitive work and connect to your tools. Fixed prices from ₹29,999.",
        answer="TENSIX builds custom AI assistants and AI agents (software that reads information, decides and acts for you) that work with your own documents, data and tools. You get a working system on your own accounts, at fixed prices from ₹29,999, and you own all the code.",
        who=[
            "Teams that answer the same customer or staff questions again and again",
            "Businesses with manuals, SOPs or product catalogues that people struggle to search",
            "Owners who want leads, documents or reports handled without adding staff",
            "Companies that want to use AI but need their data to stay in their own systems",
        ],
        steps=[
            "Call: you explain the task you want the AI to take over, and you agree with Hemal what a good result looks like.",
            "Written plan and fixed price: which documents, tools and channels (website, WhatsApp, Slack) it will use.",
            "Build and test: Hemal builds the system, using AI coding tools to move faster, and tests it on your real examples.",
            "Launch on your accounts: it goes live on your website or chat tools, and your team gets a short walkthrough.",
            "Hand-over: you receive the code, logins and notes. Ongoing support is available if you want it.",
        ],
        plans=[
            plan("Custom RAG Document Assistant", "₹29,999", "/ one-time setup",
                 "An AI assistant that answers questions using only your own manuals, SOPs and documents (this is called RAG).",
                 ["Reads your PDFs and documents and finds answers by meaning, not just keywords",
                  "Chat box for your website, or a bot inside WhatsApp or Slack",
                  "Shows which document and page each answer came from, so staff can check it",
                  "Simple upload page to add new documents any time",
                  "<strong>Turnaround:</strong> 5–7 business days"],
                 "Start with a document assistant →", "ai-rag"),
            plan("Multi-Agent AI Workflow", "₹59,999", "/ one-time setup",
                 "A small team of AI agents, each with one job, that work together on a repeating task such as research and writing.",
                 ["Agents pass work along a chain, for example research → write → review → publish",
                  "Connected to your database and apps so the agents can look things up and update records",
                  "Runs on a schedule you choose",
                  "Checks at each step; work that fails a check is retried or sent to a person",
                  "<strong>Turnaround:</strong> 10–14 business days"],
                 "Plan a multi-agent workflow →", "ai-swarm", featured=True),
            plan("End-to-End AI Process", "₹99,999+", "/ custom scope",
                 "A complete business process run by AI from start to finish, with a person able to review and step in.",
                 ["Example process: find a lead → check fit → add details → send email → book a call → log it in your CRM",
                  "Works with voice notes, scanned documents and text",
                  "Dashboard to see what the system did and approve important steps",
                  "<strong>Turnaround:</strong> 2–4 weeks"],
                 "Scope an AI system →", "ai-enterprise"),
        ],
        faqs=[
            ("What is an AI agent, in simple words?",
             "An AI agent is software that can read information, make a simple decision and take an action, such as replying to a query, updating a sheet or sending an email. It follows rules you agree on, and important steps can be sent to a person for approval."),
            ("Will the AI make up wrong answers?",
             "The document assistant is set up to answer only from your own documents and to show the source of each answer. No AI is perfect, so Hemal tests it on your real questions before launch, and anyone can check where an answer came from."),
            ("Which AI models do you use?",
             "Hemal picks the model that fits the job and the budget, for example models from OpenAI, Anthropic (Claude), Google (Gemini) or open-source options. The system can be moved to another model later if prices or quality change."),
            ("Is my business data safe?",
             "Your documents and data stay in accounts you own, such as your own database and cloud. Only the text needed for each answer is sent to the AI model, and provider settings that do not train on your data where they are available."),
            ("How long does it take and what does it cost?",
             "A document assistant costs ₹29,999 and takes 5–7 business days. A multi-agent workflow costs ₹59,999 and takes 10–14 business days. Larger end-to-end systems start at ₹99,999 and take 2–4 weeks."),
            ("Are there running costs after launch?",
             "Yes, usually small ones. You pay the AI provider and hosting directly, based on how much the system is used. Hemal estimates these costs before work starts."),
        ],
        related=["data-scraping-automation", "custom-software-saas-development", "fractional-cto-retainers"],
    ),
    dict(
        slug="custom-software-saas-development", hub_group="pricing-software",
        name="Custom Software and SaaS Development", service_type="Custom software, CRM, ERP and SaaS development",
        summary="Back-end systems, CRMs, ERPs and SaaS products built around how your business works.",
        h1="Custom Software, CRM and SaaS Built Around How You Work",
        title="Custom Software, CRM and SaaS Development | TENSIX",
        description="Custom software, CRMs, ERPs and SaaS products built for your exact workflow. Fixed prices from ₹34,999, and you own all the code. Based in Ahmedabad.",
        answer="TENSIX builds custom business software: back-end systems, internal tools like CRMs and ERPs, and complete SaaS products (software you sell online by subscription). Prices are fixed from ₹34,999, and you own all the source code from day one.",
        who=[
            "Businesses that have outgrown Excel sheets and WhatsApp groups",
            "Founders who want to launch a software product and test it with real customers",
            "Companies paying for several subscriptions that do not fit their process",
            "Teams that need an app or website connected to their own data",
        ],
        steps=[
            "Call to understand your process, your users and the problem you want solved.",
            "Written scope with screens, features and a fixed price, agreed before any work starts.",
            "Build in stages, with a working demo you can click through at each stage.",
            "Testing with your real data and users, then launch on your own cloud account.",
            "Hand-over of code, logins and a short guide, plus staff training for larger systems.",
        ],
        plans=[
            plan("Custom Backend API &amp; Microservice", "₹34,999", "/ fixed project fee",
                 "The behind-the-scenes engine for your app or website: it stores data, applies your business rules and talks to other software.",
                 ["Fast back-end built with Python (FastAPI)",
                  "Well-organised PostgreSQL or Supabase database",
                  "Secure logins, with different access levels for different staff",
                  "Automatic documentation so other developers can use it",
                  "Packaged with Docker so it is easy to move to any server",
                  "<strong>Turnaround:</strong> 7–10 business days"],
                 "Discuss a custom API →", "software-api", usd="$450"),
            plan("Custom SaaS MVP &amp; Platform Build", "₹69,999", "/ fixed project fee",
                 "A first working version of your software product (an MVP), ready for real customers to sign up and pay.",
                 ["Modern web app built with Next.js",
                  "Back-end with caching and usage limits to keep it fast and protected",
                  "Online payments and subscriptions with Razorpay, Stripe or PayPal",
                  "User dashboard, team accounts and an admin panel",
                  "Automatic emails such as sign-up and password reset",
                  "<strong>Turnaround:</strong> 14–21 business days"],
                 "Plan your SaaS product →", "software-saas", usd="$899", featured=True),
            plan("Custom CRM, ERP &amp; Enterprise Business OS", "₹1,25,000+", "/ custom milestone scope",
                 "Your own operations software, built around your process, to replace scattered tools and spreadsheets.",
                 ["Your business rules built in: approvals, stock, orders, billing or whatever your process needs",
                  "Background jobs for heavy work like reports and bulk imports",
                  "Department-wise access, activity logs and approval steps",
                  "Automatic database backups stored off-site",
                  "Full source code, documentation and staff training",
                  "<strong>Turnaround:</strong> 3–5 weeks"],
                 "Scope your CRM or ERP →", "software-enterprise", usd="$1,650+"),
        ],
        faqs=[
            ("Why custom software instead of ready-made software?",
             "Ready-made software is quick to start but makes you change your process to fit it, and monthly fees grow as you add users. Custom software fits how you already work, and because you own it there is no per-user fee to TENSIX."),
            ("Who owns the code?",
             "You do. The code goes into your own GitHub account and the software runs on your own cloud or server account, so you can hire anyone to work on it later."),
            ("What is an MVP?",
             "An MVP (minimum viable product) is the first simple version of a product, with just enough features for real customers to use and pay for. It lets you test the idea before spending more."),
            ("Can it connect to Tally, WhatsApp or my existing software?",
             "Usually yes, if the other software allows connections through an API or data export. Hemal checks this on the first call and confirms it in the written scope before you pay."),
            ("How is the price decided?",
             "Every project has a fixed price agreed in writing before work starts. Larger projects are split into milestones, each with clear deliverables."),
            ("What happens after launch?",
             "You can book changes when you need them, or choose a monthly retainer for regular updates and upkeep."),
        ],
        related=["website-development", "ai-agent-development", "cloud-devops"],
    ),
    dict(
        slug="website-development", hub_group="pricing-web",
        name="Website Development", service_type="Website design and development",
        summary="Fast, mobile-friendly business websites that turn visitors into enquiries.",
        h1="Fast, Mobile-Friendly Business Websites That Bring In Enquiries",
        title="Website Design and Development in Ahmedabad | TENSIX",
        description="Fast, mobile-friendly business websites with WhatsApp, enquiry forms and SEO basics built in. Fixed prices from ₹14,999, ready in 5 to 14 business days.",
        answer="TENSIX designs and builds business websites that load fast on phones, look professional and turn visitors into enquiries through forms, WhatsApp and call buttons. Prices are fixed from ₹14,999, and most sites are ready in 5 to 14 business days.",
        who=[
            "Local businesses that need a professional website for the first time",
            "Companies with a slow or outdated WordPress site",
            "Businesses that want enquiries to arrive straight on WhatsApp or email",
            "Firms that want to update their own blog and pages without a developer",
        ],
        steps=[
            "Call about your business, your customers and the pages you need.",
            "Page list and fixed price agreed in writing.",
            "Design and build, with a preview link you can check on your phone.",
            "Your feedback is applied, then the site goes live on your domain with SSL (the padlock in the browser).",
            "If you are replacing an old site, old page addresses are redirected so you keep your Google rankings.",
        ],
        plans=[
            plan("Basic Website", "₹14,999", "/ one-time investment",
                 "A clean, professional website that builds trust with new customers.",
                 ["6–10 pages (for example Home, About, Services, Contact)",
                  "Works well on phones and tablets",
                  "WhatsApp button and email enquiry form",
                  "Google Maps location and links to your social profiles",
                  "Fast loading and basic on-page SEO set-up",
                  "Launch on Hostinger hosting",
                  "<strong>Turnaround:</strong> 5–7 business days"],
                 "Start a basic website →", "web-basic"),
            plan("Lead-Capture Website", "₹24,999", "/ one-time investment",
                 "A bigger website designed to collect enquiries and send them to you instantly.",
                 ["15+ custom pages",
                  "Enquiries saved in a database, with instant WhatsApp or email alerts",
                  "Built with React.js, a Node.js or PHP back-end and a MySQL database",
                  "Floating click-to-call and WhatsApp buttons",
                  "Redirects from old pages so a redesign keeps your Google rankings",
                  "Google Analytics and Search Console set up to track visits and enquiries",
                  "<strong>Turnaround:</strong> 7–10 business days"],
                 "Build a lead website →", "web-standard", featured=True),
            plan("Complete Digital Platform", "₹45,000", "/ one-time investment",
                 "A full website with your own admin panel, so your team can manage content without code.",
                 ["Built with Next.js and React, with smooth animations",
                  "Admin dashboard to manage blogs, enquiries and page content",
                  "Back-end on Node.js or FastAPI with a PostgreSQL or MySQL database",
                  "Structured data (schema), sitemaps and llms.txt so Google and AI tools can read your site",
                  "Security set-up, SSL and a CDN (servers worldwide for faster loading)",
                  "30 days of support after launch, including speed checks",
                  "<strong>Turnaround:</strong> 10–14 business days"],
                 "Plan a full platform →", "web-premium"),
        ],
        faqs=[
            ("Do I own the website?",
             "Yes. The domain, hosting account and code are in your name, and all logins are handed over at launch."),
            ("Can I update the website myself?",
             "On the Complete Digital Platform plan you get an admin panel to edit blogs and page content. On the smaller plans Hemal makes content changes for you when needed, or an editor can be added later."),
            ("Will my new website rank on Google?",
             "Every site is built with the basics Google looks for: fast loading, mobile-friendly pages, clear titles and structured data. Nobody can promise a ranking, but these basics give you a strong start. For ongoing visibility, see the <a href=\"/services/geo-aeo-seo\">AI search visibility service</a>."),
            ("I already have a WordPress site. Can you redesign it?",
             "Yes. Hemal rebuilds it as a faster site and redirect every old page address to the new one, so visitors and Google do not hit broken links."),
            ("What do I need to provide?",
             "Your logo, photos, business details and a short description of your services. If your text is not ready, Hemal helps you write simple, clear content."),
            ("Are there yearly costs?",
             "You pay for your domain and hosting directly to the provider. There is no yearly fee to TENSIX unless you choose a support plan."),
        ],
        related=["geo-aeo-seo", "email-deliverability", "custom-software-saas-development"],
    ),
    dict(
        slug="cloud-devops", hub_group="pricing-cloud",
        name="Cloud Server and DevOps Setup", service_type="Cloud VPS, CI/CD and DevOps setup",
        summary="Secure cloud servers, automatic deployments, backups and monitoring.",
        h1="Secure Cloud Servers and Automatic Deployments, Set Up for You",
        title="Cloud Server, VPS and DevOps Setup | TENSIX",
        description="Secure cloud server (VPS) set-up, automatic deployments from GitHub, daily off-site backups and monitoring. Fixed prices from ₹11,999. Based in Ahmedabad.",
        answer="TENSIX sets up and secures cloud servers (VPS) so your website or app runs fast and safely, and new versions go live automatically when your code changes. Firewalls, SSL, backups and monitoring are set up properly, at fixed prices from ₹11,999.",
        who=[
            "Businesses whose website is slow or goes down on shared hosting",
            "Development teams that still upload files to the server by hand",
            "Companies that have never checked whether their backups actually work",
            "Anyone running several sites who wants one secure, easy-to-manage server",
        ],
        steps=[
            "Review of your current hosting, apps and traffic.",
            "Recommendation of a server and provider, with a fixed price.",
            "Server set-up and security: firewall, key-only login, SSL and updates.",
            "Your sites or apps are moved over with a plan to switch back if anything goes wrong.",
            "Hand-over of all logins, with a short note on how everything is set up.",
        ],
        plans=[
            plan("Cloud VPS Hardening &amp; Nginx Proxy", "₹11,999", "/ one-time setup",
                 "A properly secured Linux server, so you are no longer limited by shared hosting.",
                 ["Server set-up on Oracle Cloud, Plesk, DigitalOcean or Hostinger",
                  "Firewall, key-only login and automatic blocking of password-guessing attacks",
                  "Nginx web server with compression and security headers for faster, safer pages",
                  "Free SSL certificates that renew automatically",
                  "<strong>Turnaround:</strong> 2–3 business days"],
                 "Secure my server →", "cloud-hardening"),
            plan("Automated GitHub Actions CI/CD", "₹21,999", "/ one-time setup",
                 "New versions of your app go live automatically when your developers push code (this is called CI/CD).",
                 ["Everything in the server hardening plan",
                  "Automatic deployment from GitHub to your server over a secure connection",
                  "Your app packaged with Docker so it runs the same everywhere",
                  "Health checks before switching to a new version, to avoid downtime during updates",
                  "Telegram, Discord or WhatsApp alerts when a deployment succeeds or fails",
                  "<strong>Turnaround:</strong> 4–6 business days"],
                 "Automate my deployments →", "cloud-cicd", featured=True),
            plan("Plesk Cluster &amp; Disaster Recovery", "₹38,000", "/ one-time setup",
                 "Several sites on one well-managed server, with daily off-site backups and monitoring.",
                 ["Plesk control panel or Docker Compose set-up for multiple sites",
                  "Automatic daily backups to separate storage (AWS S3 or Oracle)",
                  "Monitoring of CPU, memory, disk and traffic, with alerts",
                  "Cloudflare DNS with DDoS protection (blocks floods of fake traffic)",
                  "<strong>Turnaround:</strong> 6–8 business days"],
                 "Plan my server set-up →", "cloud-plesk"),
        ],
        faqs=[
            ("What is a VPS?",
             "A VPS (virtual private server) is your own private space on a cloud server. Unlike shared hosting, other websites cannot slow yours down, and you control the security settings."),
            ("What is CI/CD?",
             "CI/CD means that when your developers save new code to GitHub, it is checked and put live automatically. It removes manual uploads and the mistakes that come with them."),
            ("Will my website go down during the move?",
             "Hemal plans moves to keep downtime as short as possible: the new server is fully prepared first and the switch happens at a quiet time. The old server stays ready in case you need to switch back."),
            ("Which cloud provider should I use?",
             "It depends on your budget and traffic. Oracle Cloud, DigitalOcean, AWS and Hostinger are all options, and Hemal recommends one in writing before you buy anything."),
            ("Who pays for the server?",
             "You pay the cloud provider directly, in your own account. The TENSIX fee covers only the set-up work."),
            ("What if something breaks after set-up?",
             "Hemal sets up monitoring and automatic restarts so problems are caught early. For ongoing care, the <a href=\"/services/fractional-cto-retainers\">Growth Engine Retainer</a> includes server updates, backups and security checks."),
        ],
        related=["custom-software-saas-development", "email-deliverability", "fractional-cto-retainers"],
    ),
    dict(
        slug="email-deliverability", hub_group="pricing-email",
        name="Email Deliverability and Setup", service_type="Email deliverability and email infrastructure setup",
        summary="Business emails that reach the inbox, plus low-cost bulk and cold email set-ups.",
        h1="Get Your Business Emails Into the Inbox, Not the Spam Folder",
        title="Email Deliverability and Amazon SES Setup | TENSIX",
        description="Stop business emails landing in spam. TENSIX sets up SPF, DKIM and DMARC, Amazon SES bulk sending and separate cold email domains. Fixed prices from ₹12,999.",
        answer="TENSIX fixes the settings that decide whether your emails reach the inbox, and sets up low-cost systems for newsletters and bulk email. Prices are fixed from ₹12,999, and the basic fix usually takes 2–3 business days.",
        who=[
            "Businesses whose emails or invoices end up in customers' spam folders",
            "Companies paying high monthly fees for newsletter tools",
            "Apps that need to send sign-up, OTP or order emails reliably",
            "Sales teams that want to run cold email without risking the main company domain",
        ],
        steps=[
            "Check of your domain, current email settings and any blacklists.",
            "Fixed price and a written list of the changes.",
            "Every service that sends email for you is listed, then the domain records and sending service are set up.",
            "Test emails are sent to Gmail, Outlook and Yahoo to confirm they arrive correctly.",
            "Hand-over of logins and a short guide to keep your sender reputation healthy.",
        ],
        plans=[
            plan("Email Inbox Fix", "₹12,999", "/ one-time setup",
                 "The settings Gmail and Yahoo now require, so your emails are trusted instead of sent to spam.",
                 ["SPF, DKIM and DMARC records (the identity checks email providers use) set up correctly",
                  "Custom return-path domain, which removes \"via amazon.com\" style labels",
                  "Google Postmaster Tools and Microsoft SNDS set up so you can watch your sender reputation",
                  "Blacklist check and review of spam-trigger words",
                  "<strong>Turnaround:</strong> 2–3 business days"],
                 "Fix my email delivery →", "email-deliverability"),
            plan("Amazon SES / Oracle Email Engine", "₹22,999", "/ one-time setup",
                 "Your own bulk email system on Amazon SES or Oracle Cloud, where you pay the provider per email instead of a large monthly subscription.",
                 ["Amazon SES or Oracle Cloud email set-up, including the request to move out of trial (sandbox) mode",
                  "SMTP and API logins for your website, app or CRM",
                  "Automatic handling of bounces and complaints to protect your reputation",
                  "Self-hosted newsletter tool (Mailcoach, Sendy or Ghost)",
                  "Dedicated IP address and a 30-day warm-up plan",
                  "<strong>Turnaround:</strong> 4–6 business days"],
                 "Set up my email system →", "email-ses-engine", featured=True),
            plan("Cold Email Setup", "₹44,999", "/ one-time setup",
                 "A separate set-up for cold email, so your main company domain stays protected.",
                 ["Separate sending domains for outreach, kept apart from your main domain",
                  "Automatic mailbox warm-up with Instantly or Smartlead",
                  "Custom tracking domains for open and click tracking",
                  "BIMI set-up so your logo can show in Gmail and Apple Mail (needs a verified mark certificate)",
                  "Automatic follow-up emails using n8n or Python",
                  "<strong>Turnaround:</strong> 7–10 business days"],
                 "Set up cold email →", "email-cold-infra"),
        ],
        faqs=[
            ("Why are my emails going to spam?",
             "Most often your domain is missing SPF, DKIM or DMARC records, which email providers use to check that a message really comes from you. Since 2024, Gmail and Yahoo require these from anyone sending in volume."),
            ("What are SPF, DKIM and DMARC?",
             "They are three small text records in your domain settings. Together they tell Gmail, Outlook and others which servers may send email for you, and what to do with fake emails that use your name."),
            ("Can you guarantee my emails will reach the inbox?",
             "No one can honestly guarantee that, because Gmail and Outlook make the final decision. Hemal sets up everything they check, test it, and give you tools to watch your reputation."),
            ("How much does Amazon SES cost to run?",
             "Amazon charges per email sent, which for most businesses costs much less than a monthly newsletter subscription. You pay Amazon directly, and Hemal estimates the cost before set-up."),
            ("Will this affect my normal email, like Google Workspace?",
             "No. Your mailboxes keep working. Hemal lists every service that sends email for you before changing anything, and only add or correct the records that prove your emails are genuine."),
            ("Is cold email allowed?",
             "Rules differ by country. Hemal sets up the technical side, including unsubscribe links, but you are responsible for whom you email and for following the laws that apply to you."),
        ],
        related=["website-development", "cloud-devops", "data-scraping-automation"],
    ),
    dict(
        slug="data-scraping-automation", hub_group="pricing-scraping",
        name="Data Scraping and Workflow Automation", service_type="Web scraping, data extraction and workflow automation",
        summary="Automatic data entry from emails and invoices, lead lists and website tracking.",
        h1="Stop Copy-Pasting: Automatic Data Collection and Entry",
        title="Web Scraping and Workflow Automation | TENSIX",
        description="Automatic data entry from emails and invoices, Google Maps lead lists and custom website trackers with alerts. Fixed prices from ₹16,999. Based in Ahmedabad.",
        answer="TENSIX builds small automatic systems that collect data for you: reading invoices from your inbox, building lead lists from Google Maps, or tracking competitor prices on websites. The data goes straight into Google Sheets, your database or your CRM, at fixed prices from ₹16,999.",
        who=[
            "Offices where staff type invoice or order details from email into Excel or Tally",
            "Sales teams that need lists of local businesses to contact",
            "Shops and brands that want to track competitor prices",
            "Anyone paying per-task fees for Zapier who wants a cheaper option",
        ],
        steps=[
            "Show Hemal the manual task: which emails, websites or files, and where the data should go.",
            "Hemal checks what is possible and allowed, then you agree a fixed price.",
            "Build and test on your real data, and review the output with you.",
            "Set to run automatically on a schedule, with alerts if something fails.",
            "Hand-over of the code or Docker package so you can run it yourself.",
        ],
        plans=[
            plan("Automated Gmail &amp; Doc Parser", "₹16,999", "/ one-time setup",
                 "Bills, purchase orders and bank alerts from your inbox, entered into your sheet or database automatically.",
                 ["Secure connection to your Gmail or other inbox, checking for new mail around the clock",
                  "Attachments such as PDF, Excel and CSV files downloaded automatically",
                  "Reads invoice number, vendor, amount and line items using OCR (text reading) and AI",
                  "Sends the data to Google Sheets, Notion or a PostgreSQL database",
                  "WhatsApp alert for high-value or urgent invoices",
                  "<strong>Turnaround:</strong> 3–5 business days"],
                 "Automate my inbox →", "scraper-gmail"),
            plan("Google Maps Lead Finder", "₹24,999", "/ one-time setup",
                 "Lists of local businesses in any city and category, ready for your sales team, without a monthly tool subscription.",
                 ["Collects business listings for any category and city, using Playwright (browser automation)",
                  "Business name, phone, email (where available), website, rating and address",
                  "Cleans phone numbers, checks emails and removes duplicates",
                  "Export to CSV or Excel, or send straight to your CRM",
                  "Delivered as a Docker package you can run whenever you need",
                  "<strong>Turnaround:</strong> 4–6 business days"],
                 "Get a lead list tool →", "scraper-google-maps", featured=True),
            plan("Competitor &amp; Listing Tracker", "₹49,999", "/ one-time setup",
                 "A custom tool that watches websites for you, such as competitor prices, property listings or tenders.",
                 ["Automated browser that handles modern, script-heavy websites",
                  "Competitor price tracking with alerts when prices change",
                  "Collects listings such as real estate, jobs or tenders into one place",
                  "Runs on a schedule on your server and retries automatically if a run fails",
                  "Database and simple API to use the collected data",
                  "<strong>Turnaround:</strong> 7–12 business days"],
                 "Plan a custom scraper →", "scraper-custom"),
        ],
        faqs=[
            ("Is web scraping legal?",
             "Collecting publicly available information is generally allowed, but each website has its own terms, and personal data has extra rules. Hemal reviews the sources with you before building."),
            ("What is n8n, and why not just use Zapier?",
             "n8n is a workflow tool like Zapier that can run on your own server. Self-hosted n8n has no per-task fees, so it usually costs much less once you run many automations."),
            ("What if a website changes and the scraper stops working?",
             "Websites do change. The scraper sends an alert when a run fails, and fixes can be done on request or as part of a monthly retainer."),
            ("Can it read scanned invoices?",
             "In most cases, yes. It uses OCR (software that reads text from images) together with AI to pick out the fields you need. Hemal tests it on a sample of your real invoices first."),
            ("Where does the data go?",
             "Wherever you already work: Google Sheets, Excel, Notion, a PostgreSQL database or your CRM. You choose during scoping."),
            ("Do I need a server?",
             "For tools that run on a schedule, a small cloud server is usually enough. Hemal can set it up for you, and you pay the hosting provider directly."),
        ],
        related=["ai-agent-development", "email-deliverability", "cloud-devops"],
    ),
    dict(
        slug="geo-aeo-seo", hub_group=None,
        name="AI Search Visibility (GEO, AEO and SEO)", service_type="Generative engine optimisation, answer engine optimisation and technical SEO",
        summary="Help Google and AI assistants like ChatGPT understand, find and quote your business.",
        h1="Get Found on Google and Cited by ChatGPT, Gemini and Perplexity",
        title="GEO, AEO and SEO for AI Search Visibility | TENSIX",
        description="Help Google, ChatGPT, Gemini and Perplexity understand and cite your business with technical SEO, structured data and clear answer pages. Custom quote.",
        answer="TENSIX makes your website easy for Google and AI assistants like ChatGPT, Gemini and Perplexity to read, understand and quote. Hemal fixes technical SEO, add structured data and write clear answer-style pages, priced as a custom quote after a short review of your site.",
        who=[
            "Businesses that get little traffic from Google despite having a website",
            "Companies that want to be mentioned when customers ask ChatGPT or Gemini for a recommendation",
            "Local businesses in Ahmedabad that want to show up in nearby searches",
            "Service and software firms whose offer is hard to explain in a search result",
        ],
        steps=[
            "Review of how your site appears on Google and in AI answers today.",
            "Written plan and custom quote listing the fixes and new pages.",
            "Technical fixes: speed, page titles, sitemaps, structured data (schema) and llms.txt.",
            "Clear question-and-answer content for your main services.",
            "Submission to Google Search Console and Bing, then regular check-ins if you choose a retainer.",
        ],
        plans=[
            plan("GEO, AEO &amp; SEO Programme", "Custom quote", "/ based on your website",
                 "A plan built around your website, your market and the questions your customers ask.",
                 ["Technical SEO check: speed, mobile, indexing and broken links",
                  "Structured data (schema) so search engines understand your business, services and FAQs",
                  "llms.txt and clean page summaries for AI tools",
                  "Answer-style pages for the questions your customers actually ask",
                  "Local search checks so nearby customers can find you",
                  "Ongoing help available through the Growth Engine Retainer"],
                 "Request a quote →", "geo-aeo-seo", featured=True),
        ],
        faqs=[
            ("What is the difference between SEO, AEO and GEO?",
             "SEO (search engine optimisation) helps your pages rank in normal Google results. AEO (answer engine optimisation) shapes your content so it can be used as a direct answer, such as a featured snippet or voice answer. GEO (generative engine optimisation) helps AI tools like ChatGPT, Gemini and Perplexity understand your business and mention it in their answers."),
            ("Can you guarantee that ChatGPT will recommend my business?",
             "No. Nobody controls what AI tools say. Hemal makes your information clear, consistent and easy for them to read, which improves your chances of being found and quoted."),
            ("What is structured data or schema?",
             "Structured data is a hidden label in your web pages that states facts in a fixed format, such as your business name, address, services and prices. It helps search engines understand you correctly and show richer results."),
            ("What is llms.txt?",
             "llms.txt is a simple text file on your website that gives AI tools a short, clean summary of your site with links to key pages. It is a new, optional standard and quick to add."),
            ("Why is there no fixed price?",
             "The work depends on the size and condition of your website. After a short review, Hemal sends a written quote that lists exactly what will be done."),
            ("How long before I see results?",
             "Technical fixes can be done quickly, but search engines and AI tools can take weeks or months to pick up changes. Hemal shares before-and-after checks so you can see what changed."),
        ],
        related=["website-development", "fractional-cto-retainers", "ai-agent-development"],
    ),
    dict(
        slug="fractional-cto-retainers", hub_group="pricing-retainer",
        name="Monthly Retainers and Fractional CTO", service_type="Monthly engineering retainer and fractional CTO",
        summary="Monthly engineering, server care, code audits and technical leadership from Hemal Shah.",
        h1="Ongoing Tech Help Every Month, Without Hiring a Full Team",
        title="Monthly Tech Retainers and Fractional CTO | TENSIX",
        description="Monthly engineering, server care, AI automation, code audits and technical leadership from Hemal Shah, with no long contract. Plans from ₹39,999 a month.",
        answer="TENSIX retainers give you a set amount of engineering work, server care and technical advice every month, delivered directly by founder Hemal Shah with the help of AI tools. Plans start at ₹39,999 a month, and the Growth Engine plan can be paused or cancelled at the end of any 30-day cycle.",
        who=[
            "Growing businesses that need regular tech work but not a full-time developer",
            "Founders who want a senior person to make technical decisions with them",
            "Companies with a website, app or server that needs regular updates and care",
            "Teams that want a code audit or architecture advice before a big build",
        ],
        steps=[
            "Call to list your current systems, goals and problems.",
            "Choose a plan and agree the first month's priorities in writing.",
            "Work happens in planned sprints (short blocks of focused work).",
            "Regular updates on WhatsApp or Telegram, and a review at the end of each month.",
            "All code goes into your own GitHub account, and you can change plans as your needs change.",
        ],
        plans=[
            plan("Growth Engine Retainer", "₹39,999", "/ month (cancel anytime)",
                 "Regular engineering, search visibility work and server care for a growing business.",
                 ["Regular structured data and content updates to help Google and AI tools understand your site",
                  "One engineering sprint a month: a new feature, automation or landing page",
                  "Server care: security updates, caching, SSL renewals and off-site backups",
                  "Email health checks: DMARC reports and bounce rates monitored",
                  "Direct Telegram or WhatsApp line to Hemal Shah, with a 4-hour response target (10am–7pm IST, Monday to Saturday)",
                  "No lock-in: pause, change or cancel at the end of any 30-day cycle"],
                 "Start a Growth retainer →", "retainer-growth", usd="$499"),
            plan("AI Build Plan", "₹79,999", "/ month (rolling agreement)",
                 "More engineering time, plus AI automations that run for your business every day, managed by Hemal Shah.",
                 ["2 AI automations running continuously, for example lead collection and document processing",
                  "2 engineering sprints a month for priority features, APIs or automations",
                  "A private connector (MCP server) that lets AI tools use your database safely",
                  "All code committed to your private GitHub every week",
                  "Self-hosted n8n and background workers, with no per-task fees",
                  "Priority support, with a 1-hour response target for urgent issues (10am–7pm IST, Monday to Saturday)"],
                 "Discuss the AI Build Plan →", "retainer-ai-pod", usd="$999", featured=True),
            plan("Part-Time CTO Plan", "₹1,49,999", "/ month (exclusive allocation)",
                 "Part-time technology leadership (a fractional CTO) plus hands-on building, for companies that are scaling up.",
                 ["Technology roadmap, vendor choices and compliance reviews",
                  "AI automations as needed: scraping, document assistants, CRM connections and multi-agent workflows",
                  "Weekly planning and review call with Hemal Shah",
                  "Reliable infrastructure: standby servers in a second region, Docker and automatic deployments",
                  "Security groundwork for SOC 2 or GDPR audits: activity logs, access levels and protected secrets",
                  "Only 2 of these slots are offered at a time"],
                 "Apply for a CTO slot →", "retainer-fractional-cto", usd="$1,850"),
        ],
        faqs=[
            ("What is a fractional CTO?",
             "A fractional CTO is a senior technology leader who works with you part-time. You get help with technical decisions, planning and hiring without paying a full-time salary."),
            ("Is TENSIX a team or one person?",
             "TENSIX is run by one person, founder Hemal Shah. He uses AI coding and automation tools to work faster and reviews all the work himself, so you always deal with him directly."),
            ("Can I cancel?",
             "The Growth Engine Retainer can be paused, changed or cancelled at the end of any 30-day cycle. The other plans run on a rolling monthly agreement, with notice terms agreed in writing before you start."),
            ("What counts as one engineering sprint?",
             "A sprint is a focused block of work with a clear goal agreed at the start of the month, such as one new feature, one automation or one landing page."),
            ("Do you also do one-off code audits?",
             "Yes. Hemal can review your code, database or cloud set-up and give you a written list of problems and fixes covering speed, security and cost. <a href=\"/contact\">Contact Hemal</a> for a quote."),
            ("Who owns the work done under a retainer?",
             "You do. All code goes into your own GitHub account and runs on your own cloud accounts."),
        ],
        related=["ai-agent-development", "cloud-devops", "geo-aeo-seo"],
    ),
]
BY_SLUG = {s["slug"]: s for s in SERVICES}
CHECK = '<svg fill="none" height="18" stroke="currentColor" stroke-width="2.5" viewbox="0 0 24 24" width="18" aria-hidden="true"><polyline points="20 6 9 17 4 12"></polyline></svg>'


def text(h):
    """HTML fragment -> plain text for JSON-LD."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def page_url(slug):
    return f"{SITE}/services/{slug}"


def service_id(slug):
    return f"{ID}/services/{slug}#service"


def render_card(p):
    usd = f'<span class="pricing-usd">({p["usd"]})</span>' if p["usd"] else ""
    badge = '<span class="pricing-badge">Recommended</span>\n' if p["featured"] else ""
    feats = "\n".join(f"<li>{CHECK} <span>{f}</span></li>" for f in p["features"])
    style = "primary" if p["featured"] else "secondary"
    return f"""<div class="pricing-card{' featured' if p['featured'] else ''} hover-lift">
{badge}<div class="pricing-header">
<h3>{p['name']}</h3>
<p class="pricing-hook">{p['hook']}</p>
<div class="pricing-price-wrap"><span class="pricing-price">{p['price']}{usd}</span> <span class="pricing-period">{p['period']}</span></div>
</div>
<ul class="pricing-features">
{feats}
</ul>
<a class="pricing-cta cta-button {style}" href="/contact?plan={p['slug']}">{p['cta']}</a>
</div>"""


def render_faq(q, a):
    return f'<details class="faq-accordion">\n<summary>{q}</summary>\n<div class="faq-answer"><p>{a}</p></div>\n</details>'


def faq_schema(page_id, pairs):
    return {"@type": "FAQPage", "@id": page_id + "#faq", "mainEntity": [
        {"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}}
        for q, a in pairs]}


def offer(p):
    o = {"@type": "Offer", "name": text(p["name"]), "url": f"{SITE}/contact?plan={p['slug']}",
         "availability": "https://schema.org/InStock"}
    digits = re.sub(r"\D", "", p["price"])
    if digits:
        o["price"] = digits
        o["priceCurrency"] = "INR"
        if p["price"].endswith("+"):
            o["description"] = "Starting price. The final price depends on the agreed scope."
    else:
        o["description"] = "Custom quote based on the size and needs of your website."
    return o


def ld_json(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{data}\n</script>'


def between(src, start, end, new):
    """Replace the text between two markers (markers kept)."""
    i = src.index(start) + len(start)
    j = src.index(end, i)
    return src[:i] + new + src[j:]


# ---------- services.html hub ----------

def build_hub(hub):
    groups = []
    order = ["pricing-web", "pricing-email", "pricing-scraping", "pricing-cloud",
             "pricing-software", "pricing-ai", "pricing-retainer"]
    for i, gid in enumerate(order):
        s = next(x for x in SERVICES if x["hub_group"] == gid)
        cards = "\n".join(render_card(p) for p in s["plans"])
        groups.append(f"""<div class="pricing-group{' active' if i == 0 else ''}" id="{gid}">
<div class="pricing-grid">
{cards}
</div>
<p class="details-link"><a class="card-link" href="/services/{s['slug']}">See full details: {s['name']} →</a></p>
</div>""")
    hub = between(hub, "<!-- BEGIN generated pricing groups -->", "<!-- END generated pricing groups -->",
                  "\n" + "\n".join(groups) + "\n")

    title = text(re.search(r"<title>(.*?)</title>", hub, re.S).group(1))
    desc = html.unescape(re.search(r'<meta content="([^"]*)" name="description"', hub).group(1))
    faqs = re.findall(r'<details class="faq-accordion">\s*<summary>(.*?)</summary>\s*<div class="faq-answer">(.*?)</div>', hub, re.S)
    hub_id = f"{ID}/services"
    graph = [
        {"@type": "WebPage", "@id": hub_id + "#webpage", "url": f"{SITE}/services", "name": title,
         "description": desc, "inLanguage": "en-IN", "isPartOf": {"@id": f"{ID}/#website"},
         "about": {"@id": f"{ID}/#organization"}, "publisher": {"@id": f"{ID}/#organization"},
         "breadcrumb": {"@id": hub_id + "#breadcrumb"}, "mainEntity": {"@id": hub_id + "#catalog"}},
        {"@type": "BreadcrumbList", "@id": hub_id + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{SITE}/services"}]},
        {"@type": "OfferCatalog", "@id": hub_id + "#catalog", "name": "TENSIX services",
         "url": f"{SITE}/services", "provider": {"@id": f"{ID}/#organization"},
         "itemListElement": [
             {"@type": "Offer", "name": s["name"], "url": page_url(s["slug"]),
              "itemOffered": {"@id": service_id(s["slug"]), "name": s["name"]}} for s in SERVICES]},
        faq_schema(hub_id, faqs),
    ]
    return re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _: ld_json(graph), hub, count=1, flags=re.S)


# ---------- service pages ----------

def nested(fragment):
    """services/<slug>.html sits one folder down: fix document-relative asset paths."""
    fragment = re.sub(r'((?:src|href)=")(assets/|script\.js)', r"\1../\2", fragment)
    return fragment.replace("url('assets/", "url('../assets/")


def build_page(s, parts):
    url, pid = page_url(s["slug"]), f"{ID}/services/{s['slug']}"
    title, desc = html.escape(s["title"]), html.escape(s["description"])
    assert len(title) <= 60, (s["slug"], len(title))
    assert 120 <= len(desc) <= 160, (s["slug"], len(desc))
    graph = [
        {"@type": "WebPage", "@id": pid + "#webpage", "url": url, "name": s["title"], "description": s["description"],
         "inLanguage": "en-IN", "isPartOf": {"@id": f"{ID}/#website"}, "about": {"@id": service_id(s["slug"])},
         "publisher": {"@id": f"{ID}/#organization"}, "breadcrumb": {"@id": pid + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": pid + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{SITE}/services"},
            {"@type": "ListItem", "position": 3, "name": s["name"], "item": url}]},
        {"@type": "Service", "@id": service_id(s["slug"]), "name": s["name"], "description": text(s["answer"]),
         "url": url, "serviceType": s["service_type"], "provider": {"@id": f"{ID}/#organization"},
         "areaServed": AREA, "offers": [offer(p) for p in s["plans"]]},
        faq_schema(pid, s["faqs"]),
    ]
    main_plan = next((p for p in s["plans"] if p["featured"]), s["plans"][0])
    who = "\n".join(f"<li>{w}</li>" for w in s["who"])
    steps = "\n".join(
        f'<div class="pipeline-step-card"><div class="pipeline-step-num">{i}</div><p class="pipeline-step-desc">{t}</p></div>'
        for i, t in enumerate(s["steps"], 1))
    cards = "\n".join(render_card(p) for p in s["plans"])
    faqs = "\n".join(render_faq(q, a) for q, a in s["faqs"])
    related = "\n".join(
        f'<a class="service-item hover-lift" href="/services/{r}"><h3>{BY_SLUG[r]["name"]}</h3>'
        f'<p>{BY_SLUG[r]["summary"]}</p><span class="card-link">See details →</span></a>'
        for r in s["related"])
    return f"""{parts['head_top']}<title>{title}</title>
<meta content="{desc}" name="description"/>
{parts['styles']}
<link href="{url}" rel="canonical"/>
<meta content="TENSIX" name="author"/>
<meta content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" name="robots"/>
<meta content="website" property="og:type"/>
<meta content="TENSIX" property="og:site_name"/>
<meta content="{title}" property="og:title"/>
<meta content="{desc}" property="og:description"/>
<meta content="{url}" property="og:url"/>
<meta content="{OG_IMAGE}" property="og:image"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{title}" name="twitter:title"/>
<meta content="{desc}" name="twitter:description"/>
<meta content="{OG_IMAGE}" name="twitter:image"/>
{ld_json(graph)}
</head>
<body>{parts['header']}<main>
<section class="page-hero">
<nav aria-label="Breadcrumb" class="breadcrumb"><a href="/">Home</a> › <a href="/services">Services</a> › <span>{s['name']}</span></nav>
<h1>{s['h1']}</h1>
<p class="aeo-direct-answer" style="max-width:720px;margin:0 auto 1.5rem;">{s['answer']}</p>
<div style="display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap;position:relative;">
<a class="cta-button primary" href="/contact?plan={main_plan['slug']}">Book a consultation</a>
<a class="cta-button secondary" href="#plans">See plans and prices ↓</a>
</div>
</section>
<section class="section" id="who">
<div class="section-inner">
<div class="section-header"><h2 class="section-title">Who this is for</h2></div>
<ul class="svc-list">
{who}
</ul>
</div>
</section>
<section class="section bg-alt" id="how">
<div class="section-inner">
<div class="section-header"><h2 class="section-title">How it works</h2><p>Every project is planned, built and checked by Hemal Shah, who uses AI tools to work faster.</p></div>
<div class="delivery-pipeline-grid">
{steps}
</div>
</div>
</section>
<section class="section" id="plans">
<div class="section-inner">
<div class="section-header"><h2 class="section-title">Plans and prices</h2><p>Fixed scope agreed in writing before work starts. You own the code and accounts.</p></div>
<div class="pricing-grid">
{cards}
</div>
</div>
</section>
<section class="section bg-alt" id="faq">
<div class="section-inner">
<div class="section-header"><h2 class="section-title">Common questions</h2></div>
<div class="faq-list">
{faqs}
</div>
</div>
</section>
<section class="section" id="related">
<div class="section-inner">
<div class="section-header"><h2 class="section-title">Related services</h2></div>
<div class="service-categories">
{related}
</div>
<p class="details-link"><a class="card-link" href="/services">See all services and prices →</a></p>
</div>
</section>
<section class="section" style="background:linear-gradient(135deg,rgba(59,130,246,0.08),rgba(139,92,246,0.08));border-top:1px solid rgba(15,23,42,0.05);">
<div class="section-inner text-center">
<h2 class="section-title" style="font-size:2rem;font-weight:700;color:#0F172A;margin-bottom:1rem;">Ready to talk about {s['name']}?</h2>
<p style="color:var(--color-text-muted);margin:0 auto 2rem;max-width:600px;">Tell Hemal what you need. You get a written plan and a price before any work starts.</p>
<div class="hero-buttons">
<a class="cta-button primary" href="/contact?plan={main_plan['slug']}">Contact TENSIX</a>
<a class="cta-button secondary" href="/work">See past work</a>
</div>
</div>
</section>
</main>
{parts['footer']}
</body>
</html>
"""


def write(path, content):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != content:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("wrote", os.path.relpath(path, ROOT))


def main():
    hub = open(HUB, encoding="utf-8").read()
    hub = build_hub(hub)
    write(HUB, hub)

    head = hub[:hub.index("</head>")]
    styles_start = head.index('<link href="assets/favicon.png"')
    if "</style>" in head[styles_start:]:
        styles_end = head.rindex("</style>") + len("</style>")
    else:
        styles_end = head.index('<link href="https://www.tensix.in/services" rel="canonical"/>')
    parts = {
        "head_top": head[:head.index("<title>")],
        "styles": nested(head[styles_start:styles_end].strip()),
        "header": nested(hub[hub.index("<body>") + len("<body>"):hub.index("<main>")]),
        "footer": nested(hub[hub.index('<footer class="site-footer">'):hub.index("</footer>") + len("</footer>")]
                         + "\n" + hub[hub.index('<script defer="" src="script.js'):hub.index("</body>")].rstrip()),
    }
    os.makedirs(OUT_DIR, exist_ok=True)
    for s in SERVICES:
        write(os.path.join(OUT_DIR, s["slug"] + ".html"), build_page(s, parts))


if __name__ == "__main__":
    main()
