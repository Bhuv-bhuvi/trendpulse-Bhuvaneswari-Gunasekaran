import os
import glob
import numpy as np
import pandas as pd


def find_latest_csv_file(data_dir: str = "data") -> str:
    """
    Locates the most recent cleaned CSV file in the data directory.
    """
    csv_files = glob.glob(os.path.join(data_dir, "cleaned_trends_*.csv"))
    if not csv_files:
        raise FileNotFoundError(
            "No cleaned CSV files found in 'data/'. Please run Task 2 first."
        )

    # Sort files to pick the latest one
    csv_files.sort(reverse=True)
    return csv_files[0]


def run_trend_analysis():
    """
    Task 3 Data Analysis Pipeline:
    1. Loads cleaned CSV output from Task 2.
    2. Performs statistical analysis using Pandas and NumPy.
    3. Outputs summary metrics, category breakdowns, and correlations.
    """
    print("Starting TrendPulse Task 3 Data Analysis...\n")

    input_file = find_latest_csv_file()
    print(f"Reading dataset from: {input_file}\n")
    df = pd.read_csv(input_file)

    # Convert scores and comments to NumPy arrays for NumPy-based stats
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()

    print("=" * 50)
    print(" 📊 TRENDPULSE STATISTICAL ANALYSIS ")
    print("=" * 50)

    # 1. Overall Summary Statistics (NumPy + Pandas)
    print("\n1. Overall Engagement Stats:")
    print(f"   - Total Stories Analyzed: {len(df)}")
    print(f"   - Mean Score:             {np.mean(scores):.2f}")
    print(f"   - Median Score:           {np.median(scores):.2f}")
    print(f"   - Std Dev (Score):        {np.std(scores):.2f}")
    print(f"   - Max Score:              {np.max(scores)}")
    print(f"   - Mean Comments:          {np.mean(comments):.2f}")

    # 2. Category Aggregations (Pandas groupby)
    print("\n2. Performance by Category:")
    category_summary = (
        df.groupby("category")
        .agg(
            story_count=("post_id", "count"),
            avg_score=("score", "mean"),
            total_score=("score", "sum"),
            avg_comments=("num_comments", "mean"),
        )
        .reset_index()
    )
    print(category_summary.to_string(index=False))

    # 3. Top Performing Stories
    print("\n3. Top 5 Most Upvoted Stories:")
    top_5 = df[["title", "category", "score", "num_comments"]].nlargest(5, "score")
    for idx, row in top_5.iterrows():
        print(f"   - [{row['category'].upper()}] {row['title']} ({row['score']} points, {row['num_comments']} comments)")

    # 4. Score-to-Comments Correlation (NumPy)
    print("\n4. Engagement Correlation:")
    corr_matrix = np.corrcoef(scores, comments)
    correlation = corr_matrix[0, 1]
    print(f"   - Pearson Correlation (Score vs. Comments): {correlation:.4f}")

    # 5. High Engagement Outlier Detection (NumPy percentile)
    score_75th = np.percentile(scores, 75)
    high_engagement_count = np.sum(scores > score_75th)
    print("\n5. High-Engagement Outliers:")
    print(f"   - 75th Percentile Score Threshold: {score_75th:.1f}")
    print(f"   - Stories Exceeding Threshold:     {high_engagement_count}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    run_trend_analysis()
