"""Module for aggregating the extracted data"""
from pathlib import Path

# Read in data
csv_paths = [path for path in Path("../data/per letter").iterdir()]
csvs = []

if __name__ == "__main__":
    print(csv_paths)
