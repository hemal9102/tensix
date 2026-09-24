import glob
from bs4 import BeautifulSoup

directory = 'H:/hemalshah/blogs'
files = glob.glob(directory + '/**/*.html', recursive=True)

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    header = soup.find('header', class_='site-header')
    main = soup.find('main', class_='page-content')
    blog_post = soup.find('div', class_='blog-post')
    article = soup.find('article')
    footer = soup.find('footer', class_='site-footer')
    
    print(f"File: {f}")
    print(f"  Header: {'Yes' if header else 'No'}")
    print(f"  Main: {'Yes' if main else 'No'}")
    print(f"  Blog Post Container: {'Yes' if blog_post else 'No'}")
    print(f"  Article: {'Yes' if article else 'No'}")
    print(f"  Footer: {'Yes' if footer else 'No'}")
    
    # Check if CSS matches
    style = soup.find('style')
    if style:
        print(f"  Style Length: {len(style.text)}")
    else:
        print("  Style: No")
    print("-" * 40)
