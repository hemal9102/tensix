import re

with open('H:/hemalshah/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    css = style_match.group(1)
    
    # Print media queries
    medias = re.findall(r'@media[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', css)
    print("Media Queries:")
    for m in medias:
        if 'footer' in m or 'color' in m or 'background' in m:
            print(m)
            
    # Print color styles in footer
    footer_styles = re.findall(r'\.site-footer[^{]*\{[^{}]*\}', css)
    print("\nFooter Styles:")
    for fs in footer_styles:
        print(fs)
        
    print("\nAny color that looks like #11192c:")
    print(re.findall(r'color\s*:\s*#[a-fA-F0-9]{3,6}', css))
