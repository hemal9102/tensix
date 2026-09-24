import os
import glob

directory = 'H:/hemalshah'
files = glob.glob(directory + '/**/*.html', recursive=True)

css_patch = """
/* Mobile Contrast Fix */
@media (max-width: 768px) {
  .site-footer { background-color: #080d19 !important; }
  .site-footer, .site-footer p, .site-footer a, .site-footer address { color: #cbd5e1 !important; }
  .site-footer h3, .site-footer h4 { color: #ffffff !important; }
}
"""

count = 0
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        original_content = content
        
        if "/* Mobile Contrast Fix */" not in content:
            # Insert right before the last </style>
            idx = content.rfind("</style>")
            if idx != -1:
                content = content[:idx] + css_patch + content[idx:]
                
        if content != original_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"Updated {f}")
            count += 1
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Total HTML files updated: {count}")
