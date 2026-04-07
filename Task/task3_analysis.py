# task3_analysis.py
# TrendPulse - Task 3: NumPy & Pandas Analysis
# This script loads the cleaned CSV from Task 2, performs data analysis using Pandas and NumPy,
# and generates insights about trending stories on Hacker News.

import pandas as pd
import numpy as np
from datetime import datetime
import os

# ==================== CONFIGURATION ====================
# Update the date if your cleaned CSV has a different name
CSV_FILE = "data/trends_cleaned_20260407.csv"

# Output file for analysis results
ANALYSIS_FILE = "data/analysis_report_20260407.txt"

# ======================================================

def main():
    print("🚀 Starting TrendPulse Task 3 - NumPy & Pandas Analysis...\n")

    # Step 1: Check if cleaned CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: File '{CSV_FILE}' not found!")
        print("   Please run Task 2 first to generate the cleaned CSV.")
        return

    # Step 2: Load the cleaned CSV into Pandas DataFrame
    df = pd.read_csv(CSV_FILE)

    print(f"✅ Loaded {len(df)} stories from {CSV_FILE}")
    print(f"📊 DataFrame shape: {df.shape} (rows x columns)\n")

    # Step 3: Basic Data Overview using Pandas & NumPy
    print("=== BASIC STATISTICS ===")
    print(df.describe())  # Shows count, mean, std, min, max for numeric columns

    # Step 4: Analysis using NumPy and Pandas

    # 4.1 Average score and comments per category
    print("\n=== AVERAGE SCORE & COMMENTS BY CATEGORY ===")
    category_stats = df.groupby('category').agg({
        'score': ['mean', 'max', 'count'],
        'num_comments': ['mean', 'max']
    }).round(2)
    print(category_stats)

    # 4.2 Top 10 highest scored stories (using Pandas + NumPy for sorting)
    print("\n=== TOP 10 HIGHEST SCORED STORIES ===")
    top_stories = df.nlargest(10, 'score')[['title', 'category', 'score', 'num_comments', 'author']]
    print(top_stories.to_string(index=False))

    # 4.3 Using NumPy for correlation between score and comments
    print("\n=== CORRELATION BETWEEN SCORE AND COMMENTS ===")
    correlation = np.corrcoef(df['score'], df['num_comments'])[0, 1]
    print(f"Correlation coefficient: {correlation:.4f}")
    if correlation > 0.5:
        print("→ Strong positive correlation: Higher scored stories tend to have more comments.")
    elif correlation > 0.3:
        print("→ Moderate positive correlation.")
    else:
        print("→ Weak correlation.")

    # 4.4 Stories with highest engagement (score + comments)
    df['engagement'] = df['score'] + df['num_comments'] * 2   # Weighted engagement
    print("\n=== TOP 5 MOST ENGAGED STORIES ===")
    top_engagement = df.nlargest(5, 'engagement')[['title', 'category', 'score', 'num_comments', 'engagement']]
    print(top_engagement.to_string(index=False))

    # 4.5 Category distribution (percentage)
    print("\n=== CATEGORY DISTRIBUTION (Percentage) ===")
    cat_counts = df['category'].value_counts()
    cat_percent = (cat_counts / len(df) * 100).round(2)
    print(pd.concat([cat_counts, cat_percent], axis=1, keys=['Count', 'Percentage (%)']))

    # Step 5: Save Analysis Report to a text file
    os.makedirs("data", exist_ok=True)

    with open(ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        f.write(f"TrendPulse Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total stories analyzed: {len(df)}\n\n")
        
        f.write("Category Distribution:\n")
        f.write(cat_percent.to_string() + "\n\n")
        
        f.write("Average Score by Category:\n")
        f.write(df.groupby('category')['score'].mean().round(2).to_string() + "\n\n")
        
        f.write("Top 10 Highest Scored Stories:\n")
        f.write(top_stories.to_string(index=False) + "\n\n")
        
        f.write(f"Score-Comments Correlation: {correlation:.4f}\n")

    print("\n" + "="*60)
    print("🎉 Task 3 Analysis Completed Successfully!")
    print(f"📊 Key insights generated using Pandas & NumPy")
    print(f"💾 Analysis report saved to: {ANALYSIS_FILE}")
    print("="*60)

    # Optional: Show a quick summary
    print("\nQuick Summary:")
    print(f"• Highest score     : {df['score'].max()}")
    print(f"• Most comments     : {df['num_comments'].max()}")
    print(f"• Most popular category : {df['category'].mode()[0]}")


if __name__ == "__main__":
    main()