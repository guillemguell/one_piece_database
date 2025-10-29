# src/main.py
"""
Entry point for the One Piece data scraper.

For now: scrape devil fruits and save the raw dump to data/raw/devil_fruits_raw.csv
"""

from pathlib import Path
import csv

# Devil fruits scraper
from src.scraper.devil_fruits import scrape_devil_fruits

RAW_DIR = Path("data/raw")
RAW_FILE_DF = RAW_DIR / "devil_fruits_raw.csv"
FIELDNAMES_DF = [
    "name", "url", "category", "subcategory", "is_canon", "habilities",
    "japanese_name", "romanized_name", "official_english_name", "meaning",
    "usage_debut", "type", "previous_user", "current_user"
]



def ensure_raw_dir():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

def save_raw_df_csv(items, path=RAW_FILE_DF, fieldnames=FIELDNAMES_DF):
    """Write the raw scraper output to CSV (UTF-8)."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for it in items:
            print(it)
            row = {k: (it.get(k) or "") for k in fieldnames}
            writer.writerow(row)

def main():
    print("Starting One Piece data scraper...")
    ensure_raw_dir()

    fruits = scrape_devil_fruits(limit=None)

    if not fruits:
        print("No fruits scraped — nothing saved.")
        return

    save_raw_df_csv(fruits, RAW_FILE_DF)
    print(f"Saved raw output to: {RAW_FILE_DF.resolve()} ({len(fruits)} rows)")


if __name__ == "__main__":
    main()
