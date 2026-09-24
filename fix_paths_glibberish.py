import os, glob, re

root_dir = r"H:\portfolio_website\hemalshah"
py_files = glob.glob(os.path.join(root_dir, "*.py"))
count = 0

patterns = [
    r'(?i)H:\\portfolio_website\\hemalshah',
    r'(?i)C:\\dump\\hemalshah'
]

for file_path in py_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for p in patterns:
        new_content = re.sub(p, r'C:\\hk\\DUMP\\glibberish', new_content)
        
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated {os.path.basename(file_path)}")

print(f"\nSuccessfully updated {count} Python files to point to {root_dir}")
