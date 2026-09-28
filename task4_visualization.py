import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


def generate_trend_visualizations():
    """
    Task 4 Visualization Pipeline:
    1. Reads cleaned CSV from Task 2.
    2. Generates charts using Seaborn and Matplotlib.
    3. Saves generated images to an images/ directory.
    """
    print("Starting TrendPulse Task 4 Data Visualization...\n")

    input_file = find_latest_csv_file()
    print(f"Reading dataset for visualization from: {input_file}")
    df = pd.read_csv(input_file)

    # Create directory for saving charts if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Apply global styling
    sns.set_theme(style="whitegrid")

    # --- Chart 1: Average Score by Category ---
    plt.figure(figsize=(10, 6))
    category_scores = (
        df.groupby("category")["score"].mean().reset_index().sort_values(by="score", ascending=False)
    )

    ax1 = sns.barplot(
        data=category_scores,
        x="score",
        y="category",
        palette="Blues_r",
        hue="category",
        legend=False,
    )
    plt.title("Average HackerNews Score by Category", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Average Upvote Score", fontsize=12)
    plt.ylabel("Category", fontsize=12)
    plt.tight_layout()

    chart1_path = "images/category_avg_scores.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"Saved Chart 1 -> {chart1_path}")

    # --- Chart 2: Score vs. Comments Scatter Plot ---
    plt.figure(figsize=(10, 6))
    ax2 = sns.scatterplot(
        data=df,
        x="score",
        y="num_comments",
        hue="category",
        style="category",
        s=80,
        alpha=0.8,
    )
    plt.title("HackerNews Story Score vs. Number of Comments", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Upvote Score", fontsize=12)
    plt.ylabel("Number of Comments", fontsize=12)
    plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    chart2_path = "images/score_vs_comments.png"
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"Saved Chart 2 -> {chart2_path}")

    print("\n" + "=" * 50)
    print(" 🎨 TASK 4 VISUALIZATION COMPLETE ")
    print("=" * 50)


if __name__ == "__main__":
    generate_trend_visualizations()
