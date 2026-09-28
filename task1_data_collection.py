import json
import requests


def fetch_trending_data(
    topic: str = "python", limit: int = 50, output_file: str = "trending_raw.json"
) -> None:
    """Fetches trending repositories from GitHub API and saves raw JSON."""
    print(f"Fetching top {limit} trending repositories for '{topic}'...")

    url = f"https://api.github.com/search/repositories?q={topic}+stars:>1000&sort=stars&order=desc&per_page={limit}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Successfully collected {len(data.get('items', []))} records.")
        print(f"Raw data saved to {output_file}")
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        response.raise_for_status()


if __name__ == "__main__":
    fetch_trending_data()
