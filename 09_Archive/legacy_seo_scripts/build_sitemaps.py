import os
import math
from datetime import datetime

def build_sitemaps():
    source_dir = r"H:\portfolio_website\hemalshah\aeo_geo_pages"
    output_dir = r"H:\portfolio_website\hemalshah"
    base_url = "https://hemalshah.vercel.app/aeo_geo_pages/"
    max_urls_per_sitemap = 40000

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(source_dir):
        print(f"Directory not found: {source_dir}")
        return

    # Gather all .html files
    html_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".html"):
                # Get relative path from source_dir to properly construct URL
                rel_path = os.path.relpath(os.path.join(root, file), source_dir)
                # Convert windows separators to url separators
                rel_url = rel_path.replace(os.sep, "/")
                html_files.append(rel_url)
    
    html_files.sort()
    total_files = len(html_files)
    print(f"Found {total_files} .html files.")

    if total_files == 0:
        print("No files to process.")
        return

    num_sitemaps = math.ceil(total_files / max_urls_per_sitemap)
    
    lastmod = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")

    sitemap_files = []

    for i in range(num_sitemaps):
        sitemap_filename = f"sitemap_geo_{i+1}.xml"
        sitemap_path = os.path.join(output_dir, sitemap_filename)
        sitemap_files.append(sitemap_filename)
        
        start_idx = i * max_urls_per_sitemap
        end_idx = min((i + 1) * max_urls_per_sitemap, total_files)
        
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            
            for j in range(start_idx, end_idx):
                url = base_url + html_files[j]
                # Optional XML escaping for URLs could be added here if needed,
                # e.g., replacing & with &amp;
                url = url.replace('&', '&amp;').replace("'", '&apos;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
                
                f.write('  <url>\n')
                f.write(f'    <loc>{url}</loc>\n')
                f.write(f'    <lastmod>{lastmod}</lastmod>\n')
                f.write('    <changefreq>weekly</changefreq>\n')
                f.write('  </url>\n')
                
            f.write('</urlset>\n')
        
        print(f"Generated {sitemap_filename} with {end_idx - start_idx} URLs.")

    # Generate sitemap index
    index_path = os.path.join(output_dir, "sitemap_index.xml")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        
        for sitemap_filename in sitemap_files:
            # Assuming the sitemaps themselves are hosted at the root of the site
            sitemap_url = f"https://hemalshah.vercel.app/{sitemap_filename}"
            f.write('  <sitemap>\n')
            f.write(f'    <loc>{sitemap_url}</loc>\n')
            f.write(f'    <lastmod>{lastmod}</lastmod>\n')
            f.write('  </sitemap>\n')
            
        f.write('</sitemapindex>\n')
    
    print(f"Generated sitemap_index.xml with {num_sitemaps} sitemap references.")

if __name__ == "__main__":
    build_sitemaps()
