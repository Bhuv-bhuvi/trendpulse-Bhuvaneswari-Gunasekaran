import os
import json
import time
from datetime import datetime
import requests

# Define keywords for category matching
CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def categorize_title(title: str) -> str:
    """Checks story title against keywords to assign a category."""
    if not title:
        return None
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None

def fetch_top_stories() -> list:
    """Fetches top 500 story IDs from HackerNews API."""
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    headers = {"User-Agent": "TrendPulse/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()[:500]
        else:
            print(f"Error fetching top story IDs: {response.status_code}")
            return []
    except Exception as e:
        print(f"Failed to fetch story list: {e}")
        return []

def main():
    print("Starting TrendPulse Task 1 Data Collection...")
    story_ids = fetch_top_stories()
    if not story_ids:
        print("No story IDs retrieved. Exiting.")
        return

    categorized_stories = {cat: [] for cat in CATEGORY_KEYWORDS.keys()}
    headers = {"User-Agent": "TrendPulse/1.0"}

    for story_id in story_ids:
        # Stop once all categories have 25 stories
        if all(len(stories) >= 25 for stories in categorized_stories.values()):
            break

        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code != 200:
                continue
            
            story = res.json()
            if not story or story.get("type") != "story":
                continue

            title = story.get("title", "")
            category = categorize_title(title)

            if category and len(categorized_stories[category]) < 25:
                story_record = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                categorized_stories[category].append(story_record)
                time.sleep(2)  # Rate limiting per category match

        except Exception as e:
            print(f"Error processing story {story_id}: {e}")
            continue

    # Flatten stories
    all_collected_stories = []
    for stories in categorized_stories.values():
        all_collected_stories.extend(stories)

    # Save to data directory
    os.makedirs("data", exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{date_str}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_collected_stories, f, indent=4)

    print(f"Collected {len(all_collected_stories)} stories. Saved to {file_path}")

if __name__ == "__main__":
    main()
