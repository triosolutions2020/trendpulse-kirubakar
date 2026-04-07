import requests
import json
import time
import os
from datetime import datetime

# ====================== TrendPulse - Task 1: Data Collection ======================
# This script fetches trending stories from Hacker News API and categorizes them.

# Define categories and their keywords (case-insensitive matching)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    """Assign a category to the story based on keywords in the title."""
    if not title:
        return "other"
    
    title_lower = title.lower()
    
    for category, keywords in CATEGORIES.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    return "other"  # Default if no keywords match

# Step 1: Fetch top story IDs (up to 500)
print("Fetching top story IDs from Hacker News...")
headers = {"User-Agent": "TrendPulse/1.0"}

try:
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", headers=headers)
    response.raise_for_status()
    story_ids = response.json()[:500]  # Take first 500 IDs
    print(f"Successfully fetched {len(story_ids)} story IDs.")
except Exception as e:
    print(f"Error fetching story IDs: {e}")
    story_ids = []

# Step 2: Fetch story details and categorize (max 25 per category)
stories = []
collected_count = {cat: 0 for cat in CATEGORIES}
collected_count["other"] = 0

print("\nFetching individual story details and categorizing...")

for story_id in story_ids:
    if sum(collected_count.values()) >= 125:  # Stop once we have ~125 stories
        break
    
    try:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        resp = requests.get(item_url, headers=headers)
        resp.raise_for_status()
        story = resp.json()
        
        if not story or story.get("type") != "story" or not story.get("title"):
            continue
            
        title = story.get("title", "")
        category = get_category(title)
        
        # Limit to 25 stories per category
        if category in collected_count and collected_count[category] >= 25:
            continue
            
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),   # descendants = number of comments
            "author": story.get("by", ""),
            "collected_at": datetime.now().isoformat()
        }
        
        stories.append(story_data)
        collected_count[category] += 1
        
        print(f"Collected: {category} | {title[:60]}...")
        
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        continue

# Step 3: Save to JSON file in data/ folder
os.makedirs("data", exist_ok=True)

today = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2, ensure_ascii=False)

total_collected = len(stories)
print(f"\n✅ Collection completed!")
print(f"Collected {total_collected} stories.")
print(f"Saved to: {filename}")
print("Category breakdown:", collected_count)
