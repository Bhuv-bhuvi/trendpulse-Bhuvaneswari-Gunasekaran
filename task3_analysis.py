import pandas as pd


def analyze_trending_data(input_file: str = "trending_cleaned.csv") -> None:
    """Performs statistical analysis on cleaned repository data."""
    print(f"Reading dataset from {input_file}...\n")
    df = pd.read_csv(input_file)

    print("=" * 50)
    print(" 📊 TRENDPULSE SUMMARY ANALYSIS ")
    print("=" * 50)

    print(f"\n1. General Dataset Overview:")
    print(f"   - Total Repositories Analyzed: {len(df)}")
    print(f"   - Total Stars Across Repos:    {df['stars'].sum():,}")
    print(f"   - Total Forks Across Repos:    {df['forks'].sum():,}")

    print("\n2. Top 5 Most Starred Repositories:")
    top_starred = df[["name", "stars", "forks", "language"]].head(5)
    print(top_starred.to_string(index=False))

    print("\n3. Licensing Breakdown:")
    license_counts = df["license"].value_counts().head(5)
    for lic, count in license_counts.items():
        print(f"   - {lic}: {count} repos")

    print("\n4. Engagement Metrics:")
    print(f"   - Average Stars per Repo: {df['stars'].mean():.2f}")
    print(f"   - Median Stars:           {df['stars'].median():.2f}")
    print(f"   - Average Forks per Repo: {df['forks'].mean():.2f}")

    print("\n5. Stars-to-Forks Correlation:")
    correlation = df["stars"].corr(df["forks"])
    print(f"   - Pearson Correlation Coefficient: {correlation:.4f}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    analyze_trending_data()
