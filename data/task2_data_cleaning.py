# task2_data_cleaning.py
# TrendPulse - Task 2: Clean JSON to CSV
# This script loads the JSON file from Task 1, cleans the data, and saves it as CSV.

import pandas as pd
import json
import os
from datetime import datetime

# ==================== CONFIGURATION ====================
# Change this if your JSON filename is different
JSON_FILE = "data/trends_20260407.json"   # ← Update date if needed

# Output CSV file
CSV_FILE = "data/trends_cleaned_20260407.csv"

# ======================================================

def main():
    print("🚀 Starting TrendPulse Task 2 - Data Cleaning...\n")

    # Step 1: Check if JSON file exists
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: File '{JSON_FILE}' not found!")
        print("   Please make sure you have run Task 1 first.")
        return

    # Step 2: Load the JSON file
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} stories from {JSON_FILE}")
    except Exception as e:
        print(f"❌ Error loading JSON: {e}")
        return

    # Step 3: Convert to Pandas DataFrame
    df = pd.DataFrame(data)

    print(f"📊 Initial DataFrame shape: {df.shape} (rows x columns)")

    # Step 4: Data Cleaning

    # 4.1 Fill missing values
    df['score'] = df['score'].fillna(0).astype(int)
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    df['author'] = df['author'].fillna('unknown')
    df['title'] = df['title'].fillna('No Title')

    # 4.2 Convert collected_at to proper datetime
    df['collected_at'] = pd.to_datetime(df['collected_at'], errors='coerce')

    # 4.3 Remove any duplicate stories (based on post_id)
    initial_rows = len(df)
    df = df.drop_duplicates(subset=['post_id'])
    print(f"🧹 Removed {initial_rows - len(df)} duplicate stories")

    # 4.4 Strip whitespace from text columns
    df['title'] = df['title'].str.strip()
    df['author'] = df['author'].str.strip()

    # 4.5 Add a new useful column: title length
    df['title_length'] = df['title'].str.len()

    # Step 5: Reorder columns nicely
    column_order = [
        'post_id', 'title', 'category', 'score', 
        'num_comments', 'author', 'collected_at', 'title_length'
    ]
    df = df[column_order]

    # Step 6: Create data folder (just in case)
    os.makedirs("data", exist_ok=True)

    # Step 7: Save to CSV
    df.to_csv(CSV_FILE, index=False, encoding='utf-8')

    print("\n" + "="*60)
    print("🎉 Task 2 Completed Successfully!")
    print(f"📊 Final cleaned data: {len(df)} stories")
    print(f"💾 Saved to: {CSV_FILE}")
    print("="*60)

    # Show summary by category
    print("\nCategory Distribution:")
    print(df['category'].value_counts().sort_index())

    print("\nSample Data (first 5 rows):")
    print(df.head())


if __name__ == "__main__":
    main()
    