import json
import pandas as pd


def process_trending_data(
    input_file: str = "trending_raw.json",
    output_file: str = "trending_cleaned.csv",
) -> None:
    """Cleans raw JSON data and exports a structured CSV file."""
    print(f"Loading raw data from {input_file}...")

    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    items = raw_data.get("items", [])
    extracted_records = []

    for item in items:
        record = {
            "id": item.get("id"),
            "name": item.get("name"),
            "full_name": item.get("full_name"),
            "owner": (
                item.get("owner", {}).get("login")
                if item.get("owner")
                else "Unknown"
            ),
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "open_issues": item.get("open_issues_count", 0),
            "language": item.get("language") or "Unspecified",
            "license": (
                item.get("license", {}).get("spdx_id")
                if item.get("license")
                else "No License"
            ),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "description": item.get("description") or "No description provided",
        }
        extracted_records.append(record)

    df = pd.DataFrame(extracted_records)

    # Convert timestamps to datetime format
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Successfully processed {len(df)} records.")
    print(f"Cleaned data exported to {output_file}")


if __name__ == "__main__":
    process_trending_data()
