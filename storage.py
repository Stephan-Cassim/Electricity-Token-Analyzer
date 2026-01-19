import csv
import os
from datetime import datetime

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "tokens.csv")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def append_record(year: int, month: int, value: float):
    """Append a record to CSV with columns: date,year,month,value"""
    ensure_data_dir()
    date_str = f"{year:04d}-{month:02d}-01"
    header = ["date", "year", "month", "value"]
    write_header = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([date_str, year, month, f"{value:.3f}"])

def read_all():
    """Return list of records as dicts sorted by date ascending"""
    if not os.path.exists(CSV_PATH):
        return []
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                r["year"] = int(r["year"])
                r["month"] = int(r["month"])
                r["value"] = float(r["value"])
                r["date"] = datetime.strptime(r["date"], "%Y-%m-%d").date()
                rows.append(r)
            except Exception:
                continue
    rows.sort(key=lambda x: x["date"])
    return rows
