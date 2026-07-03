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
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {schema_markup}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        mono: ['"JetBrains Mono"', 'monospace'],
                    }},
                    colors: {{
                        primary: '#33FF00', 
                        background: '#050505',
                        surface: '#050505',
                        textMain: '#33FF00',
                        textMuted: '#1A3D1A'
                    }},
                    animation: {{
                        'flicker': 'flicker 0.15s infinite',
                        'cursor': 'cursor .75s step-end infinite'
                    }},
                    keyframes: {{
                        flicker: {{
                            '0%': {{ opacity: '0.98' }},
                            '50%': {{ opacity: '1' }},
                            '100%': {{ opacity: '0.99' }}
                        }},
                        cursor: {{
                            '0%, 100%': {{ opacity: '1' }},
                            '50%': {{ opacity: '0' }}
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{
            border-radius: 0 !important;
        }}
        * {{
            border-radius: 0 !important;
        }}
        /* CRT Scanline Overlay */
        body::before {{
            content: " ";
            display: block;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 50;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }}
    </style>
</head>
<body class="bg-background text-primary font-mono antialiased min-h-screen flex flex-col selection:bg-primary selection:text-background animate-flicker">

    <nav class="border-b border-primary border-dashed p-4 sticky top-0 z-40 bg-background">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <a href="index.html" class="flex items-center text-lg font-bold hover:text-white transition-colors">
                <span class="text-primary">user@trendbyte:~$</span><span class="inline-block w-3 h-5 bg-primary ml-1 animate-cursor"></span>
            </a>
            <div class="text-sm">
                [SYS_TIME: <span id="sys-time">00:00:00</span>]
            </div>
        </div>
    </nav>
    <script>
        setInterval(() => {{
            const now = new Date();
            document.getElementById('sys-time').innerText = now.toLocaleTimeString('en-US', {{hour12: false}});
        }}, 1000);
    </script>

    <main class="max-w-4xl mx-auto px-4 py-12 flex-grow w-full z-10">
"""

FOOTER_TEMPLATE = """
    </main>
    <footer class="border-t border-primary border-dashed mt-auto py-8 text-center text-sm z-10">
        <p>> root: EOF</p>
        <p class="mt-2 text-textMuted">&copy; 2024 TrendByte [STATUS: ONLINE]</p>
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
    print("> INITIATING BUILD SEQUENCE...")
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
        post_html += f'<div class="mb-8"><a href="index.html" class="inline-block text-primary hover:bg-primary hover:text-background px-2 py-1 transition-colors">[ &lt; RETURN_TO_ROOT ]</a></div>\n'
        post_html += AD_TOP
        post_html += f'''
        <article class="border border-primary p-6 md:p-10 mb-16 relative bg-background">
            <div class="absolute -top-3 left-4 bg-background px-2 text-sm font-bold">[ POST_DATA ]</div>
            <div class="mb-8 border-b border-primary border-dashed pb-6">
                <h1 class="text-3xl md:text-5xl font-bold mb-4 uppercase">{title}</h1>
                <div class="flex gap-4 text-sm text-textMuted">
                    <span>> DATE: {date}</span>
                    <span>> SCORE: {score}</span>
                </div>
            </div>
            <div class="prose prose-invert prose-p:text-primary prose-headings:text-primary prose-a:text-white hover:prose-a:bg-primary hover:prose-a:text-background prose-a:no-underline prose-a:px-1 prose-code:text-white max-w-none">
{html_content}
            </div>
        </article>
        '''
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
        print(f"> COMPILED: {filename}")
        
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
    index_html = HEADER_TEMPLATE.format(title="TrendByte | Terminal", schema_markup=schema)
    index_html += """
        <header class="mb-16 border border-primary p-6 relative bg-background">
            <div class="absolute -top-3 left-4 bg-background px-2 text-sm font-bold">[ SYSTEM_HEADER ]</div>
            <h1 class="text-4xl md:text-6xl font-bold mb-4 uppercase">> TrendByte_Hub</h1>
            <p class="text-lg text-primary/80">> Your daily, automated feed of critical tech discussions.</p>
        </header>
    """
    index_html += AD_TOP
    index_html += '<div class="grid grid-cols-1 gap-6 mb-16">\n'
    
    for post in posts_data:
        index_html += f"""
        <div class="border border-primary border-dashed p-6 hover:border-solid hover:bg-primary/5 transition-all group relative bg-background">
            <div class="absolute -top-3 left-4 bg-background px-2 text-xs text-primary transition-colors">[ RECORD_{post['score']} ]</div>
            <h2 class="text-xl md:text-2xl font-bold leading-tight mb-4 uppercase group-hover:text-white transition-colors">{post['title']}</h2>
            <div class="flex flex-wrap items-center gap-4 text-primary text-sm mb-6">
                <span class="border border-primary px-2 py-0.5">> STATUS: TRENDING</span>
                <span>[SYS_TIME: {post['date']}]</span>
            </div>
            <div>
                <a href="{post['url']}" class="inline-block text-primary border border-primary px-4 py-2 hover:bg-primary hover:text-background transition-colors font-bold uppercase">[ EXECUTE ]</a>
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
        
    print("> BUILD_SEQUENCE_COMPLETE: /public")

if __name__ == "__main__":
    main()
