import os

root_dir = r"H:\portfolio_website\hemalshah"

def process_all(directory):
    for root, dirs, files in os.walk(directory):
        if 'hk' in root.split(os.sep) or 'assets' in root.split(os.sep) or 'node_modules' in root.split(os.sep) or '.git' in root.split(os.sep):
            continue
            
        for file in files:
            if file.endswith(".html") and not file.startswith('google'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Update JSON-LD FAQ
                content = content.replace(
                    '"name": "What services does HK Engineering offer?"',
                    '"name": "What services does Hemal Shah offer?"'
                )
                
                # 2. Update HTML FAQ Questions
                
                # Index / Services
                content = content.replace(
                    "Can you automate workflows with n8n and custom Python scrapers?",
                    "Can Hemal Shah automate workflows with n8n and custom Python scrapers?"
                )
                content = content.replace(
                    "What is your deployment stack for SaaS products?",
                    "What is Hemal Shah's deployment stack for SaaS products?"
                )
                
                # WhoAmI
                content = content.replace(
                    "How do you build AI Agents and RAG systems?",
                    "How does Hemal Shah build AI Agents and RAG systems?"
                )
                content = content.replace(
                    "What technologies do you use for Full-Stack Python Backend Development?",
                    "What technologies does Hemal Shah use for Full-Stack Python Backend Development?"
                )
                content = content.replace(
                    "How do you handle automated web scraping and workflow automation?",
                    "How does Hemal Shah handle automated web scraping and workflow automation?"
                )
                content = content.replace(
                    "What is your deployment strategy for custom SaaS applications?",
                    "What is Hemal Shah's deployment strategy for custom SaaS applications?"
                )
                content = content.replace(
                    "Do you provide freelance consulting for AI automation?",
                    "Does Hemal Shah provide freelance consulting for AI automation?"
                )
                content = content.replace(
                    "What drives you outside of coding and engineering?",
                    "What drives Hemal Shah outside of coding and engineering?"
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated FAQs in {file_path}")

process_all(root_dir)

# Also update the python scripts so future runs don't revert the JSON-LD
scripts_to_update = ["inject_eeat_metadata.py", "inject_nextgen_schemas.py"]
for script in scripts_to_update:
    script_path = os.path.join(root_dir, script)
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(
            '"name": "What services does HK Engineering offer?"',
            '"name": "What services does Hemal Shah offer?"'
        )
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {script}")

print("All FAQs updated with Hemal Shah.")
