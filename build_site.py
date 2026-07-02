import os
import glob
import markdown
import re
from datetime import datetime

# Directory structure
CONTENT_DIR = "content/posts"
OUTPUT_DIR = "public"

# Templates
HEADER_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {schema_markup}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Outfit', 'sans-serif'],
                        display: ['Space Grotesk', 'sans-serif']
                    }},
                    colors: {{
                        primary: '#38bdf8', 
                        secondary: '#818cf8', 
                        surface: '#1e293b', 
                        background: '#0f172a', 
                        textMain: '#f8fafc',
                        textMuted: '#94a3b8'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(129, 140, 248, 0.08), transparent 25%);
            background-attachment: fixed;
        }}
        .glass-panel {{
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
    </style>
</head>
<body class="bg-background text-textMain font-sans antialiased selection:bg-primary/30">

    <nav class="bg-surface/50 backdrop-blur-md border-b border-slate-700/50 shadow-lg sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <a href="index.html" class="flex items-center gap-2 text-2xl font-extrabold text-white hover:opacity-80 transition-opacity font-display">
                <span class="bg-gradient-to-r from-primary to-secondary text-transparent bg-clip-text">TrendByte</span>
            </a>
        </div>
    </nav>

    <main class="max-w-5xl mx-auto px-4 py-12">
"""

FOOTER_TEMPLATE = """
    </main>
    <footer class="bg-surface border-t border-slate-800 mt-12 py-12 text-center text-textMuted text-sm font-semibold">
        <p>&copy; 2024 TrendByte. All rights reserved.</p>
    </footer>
</body>
</html>
"""

AD_TOP = ""

AD_BOTTOM = ""

def extract_frontmatter(md_text):
    frontmatter = {}
    content = md_text
    
    match = re.match(r'^---\n(.*?)\n---\n(.*)', md_text, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        content = match.group(2)
        
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                frontmatter[key.strip()] = val.strip().strip('"').strip("'")
                
    return frontmatter, content

def main():
    print("Building premium static site...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    md_files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    
    posts_data = []
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_text = f.read()
            
        frontmatter, content = extract_frontmatter(md_text)
        
        html_content = markdown.markdown(content)
        
        title = frontmatter.get('title', 'Untitled')
        date = frontmatter.get('date', 'Unknown Date')
        score = frontmatter.get('score', '0')
        
        filename = os.path.basename(md_file).replace('.md', '.html')
        
        # Build Schema
        schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "datePublished": "{date}",
      "author": {{
        "@type": "Organization",
        "name": "TrendByte"
      }}
    }}
    </script>
        """

        post_html = HEADER_TEMPLATE.format(title=title, schema_markup=schema)
        post_html += f'<a href="index.html" class="inline-flex items-center gap-2 mb-8 text-textMuted hover:text-white transition-colors bg-slate-800/50 px-4 py-2 rounded-full text-sm font-semibold border border-slate-700 hover:border-slate-500">&larr; Back to Hub</a>\n'
        post_html += AD_TOP
        post_html += f'<article class="prose prose-invert max-w-none glass-panel p-8 md:p-12 rounded-3xl mb-16 shadow-2xl">\n{html_content}\n</article>\n'
        post_html += AD_BOTTOM
        post_html += FOOTER_TEMPLATE
        
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(post_html)
            
        posts_data.append({
            'title': title,
            'date': date,
            'score': score,
            'url': filename
        })
        print(f"Built: {filename}")
        
    # Generate index.html
    schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "TrendByte",
      "url": "https://trendbyte.local/"
    }
    </script>
    """
    index_html = HEADER_TEMPLATE.format(title="TrendByte | Trending Content", schema_markup=schema)
    index_html += """
        <header class="text-center mb-16 relative">
            <h1 class="text-5xl md:text-6xl font-black mb-6 font-display bg-gradient-to-r from-primary to-secondary text-transparent bg-clip-text">TrendByte Hub</h1>
            <p class="text-xl text-textMuted max-w-2xl mx-auto">Your daily, automated feed of the most critical technology discussions and emerging trends across the web.</p>
        </header>
    """
    index_html += AD_TOP
    index_html += '<div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">\n'
    
    for post in posts_data:
        index_html += f"""
        <div class="group glass-panel rounded-2xl p-8 border border-slate-700 hover:border-primary transition-all duration-300 shadow-lg hover:shadow-2xl flex flex-col justify-between">
            <h2 class="text-2xl font-bold font-display leading-tight mb-4 group-hover:text-primary transition-colors"><a href="{post['url']}" class="before:absolute before:inset-0 block">{post['title']}</a></h2>
            <div class="flex items-center gap-4 text-textMuted text-sm font-semibold">
                <span class="bg-primary/10 text-primary px-3 py-1 rounded-full uppercase tracking-wider text-xs">Trending</span>
                <span>{post['date']}</span>
                <span class="ml-auto text-yellow-500">⭐ {post['score']}</span>
            </div>
        </div>
        """
        
    index_html += '</div>\n'
    index_html += AD_BOTTOM
    index_html += FOOTER_TEMPLATE
    
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    # Generate robots.txt
    robots_txt = "User-agent: *\nAllow: /\n\nSitemap: https://synthetic-sage.github.io/trend-byte/sitemap.xml\n"
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), 'w', encoding='utf-8') as f:
        f.write(robots_txt)
        
    # Generate sitemap.xml
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url>\n    <loc>https://synthetic-sage.github.io/trend-byte/</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    for post in posts_data:
        sitemap += f'  <url>\n    <loc>https://synthetic-sage.github.io/trend-byte/{post["url"]}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap += '</urlset>'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(sitemap)
        
    print(f"Premium site built successfully in /{OUTPUT_DIR} directory.")

if __name__ == "__main__":
    main()
