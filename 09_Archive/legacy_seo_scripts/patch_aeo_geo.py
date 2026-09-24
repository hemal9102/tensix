import glob
import json
import os
from bs4 import BeautifulSoup

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.write() if False else f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    if not soup.head:
        return
        
    changed = False
    
    # 1. Expand Meta Description
    desc = soup.find('meta', attrs={'name': 'description'})
    if desc and desc.get('content'):
        original = desc['content']
        suffix = " Specializing in custom software development, Next.js, FastAPI, and Generative Engine Optimization (GEO) for scalable AI agent workflows and enterprise data architectures."
        if suffix not in original:
            desc['content'] = original + suffix
            changed = True
            
    # 2. Inject SiteNavigationElement
    nav_script = soup.find(string=lambda text: text and '"SiteNavigationElement"' in text)
    if not nav_script:
        nav_schema = [
            { "@context": "https://schema.org", "@type": "SiteNavigationElement", "name": "Home", "url": "https://hemalshah.vercel.app/" },
            { "@context": "https://schema.org", "@type": "SiteNavigationElement", "name": "About", "url": "https://hemalshah.vercel.app/whoami" },
            { "@context": "https://schema.org", "@type": "SiteNavigationElement", "name": "Projects", "url": "https://hemalshah.vercel.app/work" },
            { "@context": "https://schema.org", "@type": "SiteNavigationElement", "name": "Services", "url": "https://hemalshah.vercel.app/services" },
            { "@context": "https://schema.org", "@type": "SiteNavigationElement", "name": "Blog", "url": "https://hemalshah.vercel.app/blogs" },
            { "@context": "https://schema.org", "@type": "SiteNavigationElement", "name": "Contact", "url": "https://hemalshah.vercel.app/contact" }
        ]
        script_tag = soup.new_tag('script', type='application/ld+json')
        script_tag.string = json.dumps(nav_schema, indent=2)
        soup.head.append(script_tag)
        changed = True

    # 3. Inject Isolated Service Schemas
    service_script = soup.find(string=lambda text: text and '"AI Agent Development"' in text)
    if not service_script:
        services = [
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": "AI Agent Development",
                "description": "Custom AI agent workflows, LLM integration, and FastAPI backends for enterprise automation."
            },
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": "Web Scraping & Data Extraction",
                "description": "High-frequency automated web crawlers and scraping agents to securely extract critical business market intelligence."
            },
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": "Generative Engine Optimization (GEO)",
                "description": "Target AI search engines like ChatGPT, Gemini, and Perplexity with semantic entity structures and high information gain content."
            }
        ]
        for service in services:
            script_tag = soup.new_tag('script', type='application/ld+json')
            script_tag.string = json.dumps(service, indent=2)
            soup.head.append(script_tag)
        changed = True

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Patched {file_path}")

def main():
    files = glob.glob('H:/hemalshah/**/*.html', recursive=True)
    for f in files:
        if 'node_modules' in f:
            continue
        process_file(f)

if __name__ == '__main__':
    main()
