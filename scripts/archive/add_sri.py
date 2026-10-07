"""
add_sri.py — Inject SRI (Subresource Integrity) integrity + crossorigin attributes
into every CDN <script> and <link> tag across all HTML files.

Hashes were computed with: sha384(fetch(url)) → base64
Run once; safe to re-run (skips tags that already have integrity).
"""
import os
from bs4 import BeautifulSoup

# Pre-computed SHA-384 hashes for every pinned CDN asset
SRI_MAP = {
    "https://cdnjs.cloudflare.com/ajax/libs/typed.js/2.0.12/typed.min.js":
        "sha384-NMn9+T8zIKnDUstqb5le7vdLNSyAgSU9DtEPT/b7ks9NJQpPk4Dc9b1tI8oyzimc",
    "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js":
        "sha384-06z5D//U/xpvxZHuUz92xBvq3DqBBFi7Up53HRrbV7Jlv7Yvh/MZ7oenfUe9iCEt",
    "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js":
        "sha384-WJdEkJKrbsqw0evQ4GB6mlsKe5cGTxBOw4KAEIa52ZLB7DDpliGkwdme/HMa5n1m",
    "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js":
        "sha384-9WmlN8ABpoFSSHvBGGjhvB3E/D8UkNB9HpLJjBQFC2VSQsM1odiQDv4NbEo+7l15",
    "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css":
        "sha384-wFjoQjtV1y5jVHbt0p35Ui8aV8GVpEZkyF99OXWqP/eNJDU93D3Ugxkoyh6Y2I4A",
}


def inject_sri(file_path: str) -> int:
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    changed = 0

    # <script src="...">
    for tag in soup.find_all("script", src=True):
        url = tag["src"]
        if url in SRI_MAP and not tag.get("integrity"):
            tag["integrity"] = SRI_MAP[url]
            tag["crossorigin"] = "anonymous"
            changed += 1

    # <link rel="stylesheet" href="..."> or preload
    for tag in soup.find_all("link", href=True):
        url = tag["href"]
        if url in SRI_MAP and not tag.get("integrity"):
            tag["integrity"] = SRI_MAP[url]
            tag["crossorigin"] = "anonymous"
            changed += 1

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"[SRI] +{changed} tag(s) -> {file_path}")

    return changed


def run(directory: str) -> None:
    total = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fname in files:
            if fname.endswith(".html"):
                total += inject_sri(os.path.join(root, fname))
    print(f"\nDone. {total} CDN tag(s) hardened with SRI across all HTML files.")


if __name__ == "__main__":
    run(os.getcwd())
