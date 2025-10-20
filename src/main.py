# src/main.py
"""
Entry point for the One Piece data scraper.

For now: scrape devil fruits and save the raw dump to data/raw/devil_fruits_raw.csv
"""

from pathlib import Path
import csv
from src.scraper.devil_fruits import scrape_devil_fruits

RAW_DIR = Path("data/raw")
RAW_FILE = RAW_DIR / "devil_fruits_raw.csv"
FIELDNAMES = ["name", "url", "section", "row_label"]

def ensure_raw_dir():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

def save_raw_csv(items, path=RAW_FILE, fieldnames=FIELDNAMES):
    """Write the raw scraper output to CSV (UTF-8)."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for it in items:
            row = {k: (it.get(k) or "") for k in fieldnames}
            writer.writerow(row)

def main():
    print("Starting One Piece data scraper...")
    ensure_raw_dir()

    # Scrape everything (use limit for quick tests)
    fruits = scrape_devil_fruits(limit=None)

    if not fruits:
        print("No fruits scraped — nothing saved.")
        return

    save_raw_csv(fruits, RAW_FILE)
    print(f"Saved raw output to: {RAW_FILE.resolve()} ({len(fruits)} rows)")

    # Quick preview
    preview = min(8, len(fruits))
    print("\nPreview (first {} rows):".format(preview))
    for i, f in enumerate(fruits[:preview], start=1):
        print(f"{i}. {f.get('name','')}  |  {f.get('url','')}  |  {f.get('section','')}  |  {f.get('row_label','')}")

if __name__ == "__main__":
    main()
