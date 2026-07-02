import urllib.request
import json
import os
import re
from datetime import datetime

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
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    # Create SEO-friendly markdown content
    content = f"""---
title: "{title.replace('"', '')}"
date: {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')}
author: {author}
score: {score}
---

# {title}

**Published on:** {date_str} | **Author:** {author} | **Score:** {score}

We've curated this trending tech discussion just for you.

[Read the full story here]({url})

## Why this matters
Trending topics on HackerNews often indicate shifts in the tech industry, new tools you should be aware of, or important security updates. Stay ahead of the curve by following these top discussions.

---
"""
    return content

def main():
    print("Fetching top stories from HackerNews...")
    try:
        story_ids = fetch_json(TOP_STORIES_URL)
        
        # Limit to top 10 stories to keep it lightweight
        top_10_ids = story_ids[:10]
        
        # Ensure data directory exists
        os.makedirs("content/posts", exist_ok=True)
        
        for item_id in top_10_ids:
            story = fetch_json(ITEM_URL_TEMPLATE.format(item_id))
            if story and story.get('type') == 'story' and story.get('title'):
                filename = sanitize_filename(story['title']) + f"-{item_id}.md"
                filepath = os.path.join("content/posts", filename)
                
                md_content = generate_markdown(story)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"Generated: {filepath}")
                
        print("Data fetching complete.")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()
