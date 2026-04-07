# task4_visualization.py
# TrendPulse - Task 4: Data Visualization
# This script loads the cleaned CSV from Task 2 and creates insightful charts using Matplotlib and Seaborn.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
CSV_FILE = "data/trends_cleaned_20260407.csv"   # ← Change date if your file name is different

# Output folder for images
OUTPUT_DIR = "data/visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set style for beautiful plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# ======================================================

def main():
    print("🚀 Starting TrendPulse Task 4 - Data Visualization...\n")

    # 1. Load the cleaned data
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: '{CSV_FILE}' not found!")
        print("   Please make sure Task 2 has been completed successfully.")
        return

    df = pd.read_csv(CSV_FILE)
    print(f"✅ Loaded {len(df)} stories for visualization.\n")

    # 2. Create visualizations

    # Plot 1: Stories per Category (Bar Chart)
    plt.figure(figsize=(10, 6))
    cat_counts = df['category'].value_counts()
    sns.barplot(x=cat_counts.index, y=cat_counts.values)
    plt.title('Number of Stories per Category', fontsize=16)
    plt.xlabel('Category')
    plt.ylabel('Number of Stories')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/stories_per_category.png", dpi=300)
    plt.close()
    print("📊 Saved: stories_per_category.png")

    # Plot 2: Average Score by Category (Bar Chart)
    plt.figure(figsize=(10, 6))
    avg_score = df.groupby('category')['score'].mean().sort_values(ascending=False)
    sns.barplot(x=avg_score.index, y=avg_score.values)
    plt.title('Average Score by Category', fontsize=16)
    plt.xlabel('Category')
    plt.ylabel('Average Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/avg_score_by_category.png", dpi=300)
    plt.close()
    print("📊 Saved: avg_score_by_category.png")

    # Plot 3: Score vs Number of Comments (Scatter Plot)
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x='score', y='num_comments', hue='category', alpha=0.7, s=80)
    plt.title('Score vs Number of Comments by Category', fontsize=16)
    plt.xlabel('Score (Upvotes)')
    plt.ylabel('Number of Comments')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/score_vs_comments.png", dpi=300)
    plt.close()
    print("📊 Saved: score_vs_comments.png")

    # Plot 4: Distribution of Scores (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['score'], bins=30, kde=True)
    plt.title('Distribution of Story Scores', fontsize=16)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/score_distribution.png", dpi=300)
    plt.close()
    print("📊 Saved: score_distribution.png")

    # Plot 5: Top 10 Highest Scored Stories (Horizontal Bar)
    plt.figure(figsize=(12, 8))
    top10 = df.nlargest(10, 'score')
    sns.barplot(y=top10['title'].str[:60] + '...', x=top10['score'], orient='h')
    plt.title('Top 10 Highest Scored Stories', fontsize=16)
    plt.xlabel('Score')
    plt.ylabel('Story Title')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top10_highest_scored.png", dpi=300)
    plt.close()
    print("📊 Saved: top10_highest_scored.png")

    # Final Summary
    print("\n" + "="*70)
    print("🎉 Task 4 Visualization Completed Successfully!")
    print(f"📁 All charts saved in folder: {OUTPUT_DIR}/")
    print("\nGenerated Charts:")
    print("   1. stories_per_category.png")
    print("   2. avg_score_by_category.png")
    print("   3. score_vs_comments.png")
    print("   4. score_distribution.png")
    print("   5. top10_highest_scored.png")
    print("="*70)

    print(f"\nOpen the '{OUTPUT_DIR}' folder to view all beautiful charts!")

if __name__ == "__main__":
    main()
    