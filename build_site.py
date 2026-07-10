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
    <title>{title} | TrendByte Tech News</title>
    <meta name="description" content="Access the top trending tech news, programming discussions, and Hacker News insights daily on TrendByte's terminal interface.">
    <meta name="keywords" content="Tech News, Hacker News, Programming, Software Engineering, Developer News">
    <meta name="google-site-verification" content="cYEGz4VEddhjiC7JheW4BjuhlZDbfq6EEmkmXTUiJyA" />
    {schema_markup}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link href="styles.css" rel="stylesheet">
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
    <footer class="border-primary border-dashed bg-background mt-auto relative z-50">
        <div class="max-w-7xl mx-auto px-6 py-12">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8 text-sm text-primary">
                <div>
                    <h3 class="font-bold mb-4 text-white hover:text-primary transition-colors">TrendByte</h3>
                    <p class="opacity-70">Empowering professionals with top-tier tools.</p>
                </div>
                <div>
                    <h3 class="font-bold mb-4 text-white hover:text-primary transition-colors">Tools</h3>
                    <ul class="space-y-2 opacity-70">
                        <li><a href="/" class="hover:text-white hover:text-primary transition-colors">Home</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="font-bold mb-4 text-white hover:text-primary transition-colors">Company</h3>
                    <ul class="space-y-2 opacity-70">
                        <li><a href="/about.html" class="hover:text-white hover:text-primary transition-colors">About Us</a></li>
                        <li><a href="/contact.html" class="hover:text-white hover:text-primary transition-colors">Contact</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="font-bold mb-4 text-white hover:text-primary transition-colors">Legal &amp; Compliance</h3>
                    <ul class="space-y-2 opacity-70">
                        <li><a href="/privacy-policy.html" class="hover:text-white hover:text-primary transition-colors">Privacy Policy</a></li>
                        <li><a href="/terms-of-service.html" class="hover:text-white hover:text-primary transition-colors">Terms of Service</a></li>
                        <li><a href="/disclaimer.html" class="hover:text-white hover:text-primary transition-colors font-bold">Disclaimer</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-primary border-dashed pt-8 flex flex-col md:flex-row justify-between items-center text-primary opacity-70 text-xs font-semibold">
                <p>&copy; 2026 TrendByte. All rights reserved.</p>
                <p class="mt-4 md:mt-0">Content is aggregated/curated from third-party sources. TrendByte does not claim ownership of linked articles.</p>
            </div>
        </div>
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
            'local_url': filename,
            'url': frontmatter.get('url', filename)
        })
        print(f"> COMPILED: {filename}")
        
    # Generate index.html
    schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "url": "https://trendbyte.local/"
    }
    </script>
    """
    index_html = HEADER_TEMPLATE.format(title="TrendByte | Terminal", schema_markup=schema)
    index_html += """
        <header class="mb-12 border border-primary p-6 relative bg-background">
            <div class="absolute -top-3 left-4 bg-background px-2 text-sm font-bold">[ SYSTEM_HEADER ]</div>
            <h1 class="sr-only">Top Tech News, Hacker News Trends, and Programming Discussions 2026</h1>
            <div class="text-4xl md:text-6xl font-bold mb-4 uppercase" aria-hidden="true">> TrendByte_Hub</div>
            <p class="text-lg text-primary/80">> Your daily, automated feed of critical tech discussions and software engineering news.</p>
        </header>
        
        <div class="mb-8 border border-primary p-4 bg-background flex items-center">
            <label class="text-primary font-bold mr-3">> grep -i</label>
            <input type="text" id="terminal-filter" class="bg-background text-primary border-none outline-none flex-grow placeholder-primary/50 focus:ring-0" placeholder="_SEARCH_PACKETS..." autocomplete="off">
        </div>
        <script>
            document.getElementById('terminal-filter').addEventListener('input', function(e) {
                const query = e.target.value.toLowerCase();
                const posts = document.querySelectorAll('.post-card');
                let count = 0;
                posts.forEach(card => {
                    const text = card.textContent.toLowerCase();
                    if(text.includes(query)) {
                        card.style.display = 'block';
                        count++;
                    } else {
                        card.style.display = 'none';
                    }
                });
                document.getElementById('result-count').textContent = count;
            });
        </script>
        
        <div class="mb-4 text-sm">> DISPLAYING <span id="result-count">{len(posts_data)}</span> PACKETS</div>
    """
    index_html += '<div class="grid grid-cols-1 gap-6 mb-16">\n'
    
    for post in posts_data:
        import urllib.parse
        raw_url = post.get('url', '')
        domain_str = post.get('domain', '')
        if not domain_str and raw_url and raw_url.startswith('http'):
            domain_str = urllib.parse.urlparse(raw_url).netloc
        if not domain_str:
            domain_str = 'unknown.node'
            
        score_val = int(post.get('score', 0))
        status = 'TRENDING' if score_val > 100 else 'ACTIVE'
        
        # We will use post['local_url'] for the generated HTML file, and post['url'] for the external link.
        local_url = post.get('local_url', '#')
        ext_url = post.get('url', local_url)
        
        index_html += f'''
        <div class="post-card border border-primary border-dashed p-6 hover:border-solid hover:bg-primary/5 transition-all group relative bg-background">
            <div class="absolute -top-3 left-4 bg-background px-2 text-xs text-primary transition-colors">[ RECORD_{post['score']} ]</div>
            <h2 class="text-xl md:text-2xl font-bold leading-tight mb-4 uppercase group-hover:text-white transition-colors">{post['title']}</h2>
            <div class="flex flex-wrap items-center gap-4 text-primary text-sm mb-4">
                <span class="border border-primary px-2 py-0.5">> STATUS: {status}</span>
                <span>[SYS_TIME: {post['date']}]</span>
                <span>[TARGET: {domain_str}]</span>
            </div>
            <p class="text-textMuted text-sm mb-6">> DECRYPTING SUMMARY: Threat score ({post['score']}) detected at destination node {domain_str}. Network consensus indicates tech sector activity.</p>
            <div class="flex gap-4 flex-wrap">
                <a href="{local_url}" class="inline-block text-primary border border-primary px-4 py-2 hover:bg-primary hover:text-background transition-colors font-bold uppercase">[ READ_LOCAL ]</a>
                <a href="{ext_url}" target="_blank" rel="noopener noreferrer" class="inline-block text-primary border border-primary border-dashed px-4 py-2 hover:border-solid hover:bg-primary hover:text-background transition-colors font-bold uppercase">[ ACCESS_REMOTE ]</a>
            </div>
        </div>
        '''
        
    index_html += '</div>\n'
    
    # Inject SEO Content Block
    index_html += """
        <section class="border border-primary border-dashed p-6 mb-16 bg-background">
            <h2 class="text-xl font-bold mb-4">> WHY_USE_TRENDBYTE?</h2>
            <div class="text-textMuted text-sm space-y-4">
                <p>TrendByte is the ultimate terminal-style aggregator for <strong>top tech news</strong>, <strong>programming discussions</strong>, and <strong>Hacker News trends</strong>. Designed for developers and software engineers, our system autonomously scrapes, analyzes, and delivers the highest-signal discussions from across the web directly to your terminal UI.</p>
                <p>Stay ahead of the curve with daily updates on artificial intelligence, web development, cybersecurity, and open-source releases. Bypass the noise and access purely technical insights with our blazing-fast, zero-bloat platform.</p>
            </div>
        </section>
    """
    
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
        
    import subprocess
    print("> COMPILING TAILWIND CSS...")
    subprocess.run(["tailwindcss.exe", "-i", "input.css", "-o", "public/styles.css", "--minify"])
    print("> BUILD_SEQUENCE_COMPLETE: /public")

if __name__ == "__main__":
    main()
