import os
import glob
import json
import pandas as pd


def find_latest_json_file(data_dir: str = "data") -> str:
    """
    Locates the most recent JSON file saved in the data directory.
    """
    json_files = glob.glob(os.path.join(data_dir, "trends_*.json"))
    if not json_files:
        raise FileNotFoundError("No JSON files found in the 'data/' directory. Please run Task 1 first.")
    
    # Sort files to pick the latest one
    json_files.sort(reverse=True)
    return json_files[0]


def clean_and_process_data():
    """
    Task 2 Data Processing Pipeline:
    1. Loads raw JSON data from Task 1.
    2. Cleans text, handles missing values, and enforces types using pandas.
    3. Exports cleaned structured data to CSV.
    """
    print("Starting TrendPulse Task 2 Data Processing...")

    # Step 1: Find and load the latest Task 1 JSON output
    input_file = find_latest_json_file()
    print(f"Loading raw data from: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if not raw_data:
        print("Raw JSON file is empty. Exiting processing.")
        return

    # Step 2: Convert to pandas DataFrame for cleaning
    df = pd.DataFrame(raw_data)

    # --- Cleaning & Data Transformation ---
    
    # 1. Fill missing numeric values with 0
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # 2. Clean text fields (fill missing values & strip extra whitespace)
    df["title"] = df["title"].fillna("Untitled").astype(str).str.strip()
    df["author"] = df["author"].fillna("anonymous").astype(str).str.strip()
    df["category"] = df["category"].fillna("uncategorized").astype(str).str.strip().str.lower()

    # 3. Ensure post_id is an integer
    df["post_id"] = pd.to_numeric(df["post_id"], errors="coerce").astype("Int64")

    # 4. Remove duplicate posts if any exist
    initial_count = len(df)
    df = df.drop_duplicates(subset=["post_id"])
    duplicates_removed = initial_count - len(df)
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicate records.")

    # 5. Format timestamp column to standardized ISO datetime format
    df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")

    # Step 3: Export cleaned data to CSV
    # Derive output filename based on input filename (e.g., cleaned_trends_20260928.csv)
    base_name = os.path.basename(input_file).replace("trends_", "cleaned_trends_").replace(".json", ".csv")
    output_path = os.path.join("data", base_name)

    df.to_csv(output_path, index=False, encoding="utf-8")

    print("\n" + "=" * 50)
    print(" 🧹 TASK 2 DATA CLEANING COMPLETE ")
    print("=" * 50)
    print(f"Total Rows Cleaned & Saved: {len(df)}")
    print(f"Cleaned CSV File Path:       {output_path}")
    print("=" * 50)


if __name__ == "__main__":
    clean_and_process_data()
