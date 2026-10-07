import os
import glob
from bs4 import BeautifulSoup
import json

def get_html_files(directory):
    return glob.glob(os.path.join(directory, '*.html')) + glob.glob(os.path.join(directory, 'blogs', '*.html'))

def inject_schemas_and_meta(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    if not soup.head:
        return

    # Add SEO, AEO, GEO Meta Tags
    meta_tags = [
        {'name': 'robots', 'content': 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'},
        {'name': 'author', 'content': 'Hemal Shah'},
        {'property': 'og:site_name', 'content': 'Hemal Shah'},
        {'property': 'og:type', 'content': 'website'},
    ]
    
    for tag in meta_tags:
        if 'name' in tag:
            if not soup.find('meta', attrs={'name': tag['name']}):
                new_meta = soup.new_tag('meta', attrs=tag)
                soup.head.append(new_meta)
        elif 'property' in tag:
            if not soup.find('meta', attrs={'property': tag['property']}):
                new_meta = soup.new_tag('meta', attrs=tag)
                soup.head.append(new_meta)
                
    # Basic schemas
    schemas = []
    
    # 1. WebSite Schema
    schemas.append({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Hemal Shah",
        "url": "https://hemalshah.com/"
    })
    
    # 2. Person Schema
    schemas.append({
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Hemal Shah",
        "url": "https://hemalshah.com/",
        "jobTitle": "Software Engineer"
    })
    
    # 3. LocalBusiness Schema
    schemas.append({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Hemal Shah Consulting",
        "image": "https://hemalshah.com/assets/images/logo.png",
        "url": "https://hemalshah.com/",
        "telephone": "+1234567890",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "123 Main St",
            "addressLocality": "City",
            "addressRegion": "ST",
            "postalCode": "12345",
            "addressCountry": "US"
        }
    })
    
    # Determine page specific schemas
    if 'blogs' in file_path or 'article' in file_path:
        schemas.append({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": soup.title.string if soup.title else "Blog Post",
            "author": {
                "@type": "Person",
                "name": "Hemal Shah"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Hemal Shah"
            }
        })
        
    # Inject JSON-LD
    for schema in schemas:
        script_tag = soup.new_tag('script', type='application/ld+json')
        script_tag.string = json.dumps(schema, indent=2)
        soup.head.append(script_tag)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
def main():
    directory = r'H:\hemalshah'
    files = get_html_files(directory)
    for file in files:
        print(f'Processing {file}...')
        try:
            inject_schemas_and_meta(file)
        except Exception as e:
            print(f'Error processing {file}: {e}')
            
if __name__ == '__main__':
    main()
