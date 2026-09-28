import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def create_visualizations(input_file: str = "trending_cleaned.csv") -> None:
    """Generates visual charts based on processed dataset."""
    print(f"Loading data for visualization from {input_file}...")
    df = pd.read_csv(input_file)

    sns.set_theme(style="whitegrid")

    # Chart 1: Top 10 Most Starred Repositories
    plt.figure(figsize=(10, 6))
    top_10 = df.nlargest(10, "stars")
    ax = sns.barplot(
        data=top_10,
        x="stars",
        y="name",
        palette="viridis",
        hue="name",
        legend=False,
    )
    plt.title("Top 10 Most Starred Repositories", fontsize=14, fontweight="bold")
    plt.xlabel("Stars Count", fontsize=12)
    plt.ylabel("Repository Name", fontsize=12)
    plt.tight_layout()
    plt.savefig("top_repos.png", dpi=300)
    plt.close()
    print("Saved 'top_repos.png'")

    # Chart 2: Stars vs Forks Scatter Plot
    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=df,
        x="stars",
        y="forks",
        alpha=0.7,
        color="#2b5c8f",
        s=70,
        edgecolor="w",
    )
    plt.title("Stars vs. Forks Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Stars", fontsize=12)
    plt.ylabel("Forks", fontsize=12)
    plt.tight_layout()
    plt.savefig("stars_vs_forks.png", dpi=300)
    plt.close()
    print("Saved 'stars_vs_forks.png'")


if __name__ == "__main__":
    create_visualizations()
