import os
import re

root_dir = r"H:\portfolio_website\hemalshah"

def inject_local_seo(content):
    # 1. Add Geo Meta Tags to Head
    geo_tags = """
  <!-- Local SEO Meta Tags -->
  <meta name="geo.region" content="IN-GJ" />
  <meta name="geo.placename" content="Ahmedabad" />
  <meta name="geo.position" content="23.0225;72.5714" />
  <meta name="ICBM" content="23.0225, 72.5714" />
"""
    if 'name="geo.region"' not in content:
        head_end_idx = content.find("</head>")
        if head_end_idx != -1:
            content = content[:head_end_idx] + geo_tags + content[head_end_idx:]

    # 2. Add address to Person in JSON-LD
    person_addr = ',\n        "address": {"@type": "PostalAddress", "addressLocality": "Ahmedabad", "addressRegion": "Gujarat", "addressCountry": "India"}'
    if '"addressLocality": "Ahmedabad"' not in content:
        # We find where Person block ends (e.g. before "url": "https... or "worksFor") and inject
        # Safer: just append it after "name": "Hemal Shah"
        content = re.sub(
            r'("name": "Hemal Shah",)',
            r'\1' + person_addr,
            content
        )

    # 3. Add areaServed to Organization
    org_area = ',\n        "areaServed": [{"@type": "City", "name": "Ahmedabad"}, {"@type": "State", "name": "Gujarat"}, {"@type": "Country", "name": "India"}]'
    if '"areaServed"' not in content:
        content = re.sub(
            r'("name": "HK Engineering",)',
            r'\1' + org_area,
            content
        )
        
    return content

def process_all(directory):
    for root, dirs, files in os.walk(directory):
        if 'hk' in root.split(os.sep) or 'assets' in root.split(os.sep) or 'node_modules' in root.split(os.sep) or '.git' in root.split(os.sep):
            continue
            
        for file in files:
            if file.endswith(".html") and not file.startswith('google'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = inject_local_seo(content)
                
                # If index.html, inject a discreet local SEO footer
                if file == 'index.html':
                    local_footer = """
  <!-- Local SEO Anchor -->
  <div class="local-seo-anchor" style="text-align:center; padding: 2rem 1rem; color: #94a3b8; font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.02); background: #080d19;">
    Hemal Shah - Rated as a top AI Automation Engineer and the best SaaS Developer in Ahmedabad, Gujarat, India.
  </div>
  </main>"""
                    if "best SaaS Developer in Ahmedabad" not in new_content:
                        new_content = new_content.replace('</main>', local_footer)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected Local SEO into {file_path}")

process_all(root_dir)

# Also update the Python generators so future runs include it
scripts_to_update = ["inject_eeat_metadata.py", "inject_nextgen_schemas.py"]
for script in scripts_to_update:
    script_path = os.path.join(root_dir, script)
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add to Person
        if '"addressLocality"' not in content:
            content = re.sub(
                r'("name": "Hemal Shah",)',
                r'\1\n        "address": {"@type": "PostalAddress", "addressLocality": "Ahmedabad", "addressRegion": "Gujarat", "addressCountry": "India"},',
                content
            )
        
        # Add to Organization
        if '"areaServed"' not in content:
            content = re.sub(
                r'("name": "HK Engineering",)',
                r'\1\n        "areaServed": [{"@type": "City", "name": "Ahmedabad"}, {"@type": "State", "name": "Gujarat"}, {"@type": "Country", "name": "India"}],',
                content
            )
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {script} with local SEO JSON-LD")

print("Local SEO Injection Complete.")
