import urllib.request
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse

# HackerNews API Endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def sanitize_filename(title):
    # Remove invalid characters for filenames
    filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename

def generate_markdown(story):
    title = story.get('title', 'No Title')
    url = story.get('url', f"https://news.ycombinator.com/item?id={story.get('id')}")
    author = story.get('by', 'Unknown')
    score = story.get('score', 0)
    timestamp = story.get('time', 0)
    desc = story.get('text', '') # Sometimes HN posts have text
    
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    domain = urlparse(url).netloc if url else 'news.ycombinator.com'
    
    # Create SEO-friendly markdown content
    content = f"""---
title: "{title.replace('"', '')}"
date: {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')}
author: {author}
score: {score}
domain: {domain}
---

# {title}

> SYSTEM_LOG: METADATA_EXTRACTED
> PUBLISHED: {date_str} 
> AUTHOR_ID: {author} 
> THREAT_SCORE (UPVOTES): {score}
> TARGET_DOMAIN: {domain}

### [ EXECUTE_CONNECTION_TO_TARGET ]({url})
### [ VIEW_HACKER_NETWORK_COMMENTS ](https://news.ycombinator.com/item?id={story.get('id')})

---
## > INITIATING PACKET DECRYPTION...
## > ANALYZING DATA STREAM...

This data packet represents a highly trending node in the HackerNews mainframe. 
High threat scores indicate a significant disruption or innovation in the tech sector. 

**Auto-Generated Analysis:**
- The author `{author}` has successfully broadcasted this signal to the network.
- The target payload is hosted at `{domain}`.
- `{score}` network nodes have acknowledged and verified this packet's importance.

*User Directive: Monitor this sector for further developments. Stay frosty.*
"""
    return content

def main():
    print("> INITIATING HACKER_NEWS MAINFRAME CONNECTION...")
    try:
        story_ids = fetch_json(TOP_STORIES_URL)
        
        # Increased to 40 stories
        top_ids = story_ids[:40]
        
        # Ensure data directory exists
        os.makedirs("content/posts", exist_ok=True)
        
        for item_id in top_ids:
            story = fetch_json(ITEM_URL_TEMPLATE.format(item_id))
            if story and story.get('type') == 'story' and story.get('title'):
                filename = sanitize_filename(story['title']) + f"-{item_id}.md"
                filepath = os.path.join("content/posts", filename)
                
                md_content = generate_markdown(story)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"> DOWNLOADED_NODE: {filepath}")
                
        print("> DATA FETCH COMPLETE. TERMINATING CONNECTION.")
    except Exception as e:
        print(f"> ERROR: {e}")

if __name__ == "__main__":
    main()
