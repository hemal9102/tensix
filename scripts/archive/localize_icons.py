import os
import urllib.request

root_dir = r"H:\portfolio_website\hemalshah"
icons_dir = os.path.join(root_dir, "assets", "icons")
os.makedirs(icons_dir, exist_ok=True)

index_file = os.path.join(root_dir, "index.html")

icons_to_download = {
    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg": "python-original.svg",
    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg": "docker-original.svg",
    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg": "tensorflow-original.svg",
    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg": "fastapi-original.svg",
    "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kubernetes/kubernetes-plain.svg": "kubernetes-plain.svg"
}

# Download and replace
if os.path.exists(index_file):
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    for url, filename in icons_to_download.items():
        local_path = os.path.join(icons_dir, filename)
        
        # Download the file
        try:
            urllib.request.urlretrieve(url, local_path)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            continue
            
        # Replace the URL in index.html with the local relative path
        local_url = f"assets/icons/{filename}"
        content = content.replace(url, local_url)

    # Write changes back
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated index.html to use localized icons.")
else:
    print("index.html not found.")
