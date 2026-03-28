import pandas as pd
from pathlib import Path

print("📅 BUILDING WEEKLY DATA 🔥\n")

# ==============================
# PATHS
# ==============================
DAILY_DIR = Path(r"H:\MarketForge\data\master\Equity_stock_master")
OUT_DIR   = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR.mkdir(parents=True, exist_ok=True)

files = list(DAILY_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)

        if df.empty:
            continue

        # ==============================
        # FIX COLUMN NAMES
        # ==============================
        df.columns = df.columns.str.strip().str.upper()

        required = {"DATE", "OPEN", "HIGH", "LOW", "CLOSE"}
        if not required.issubset(df.columns):
            print(f"❌ Skipped (columns) → {file.stem}")
            continue

        # ==============================
        # DATE PARSE
        # ==============================
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df.dropna(subset=["DATE"]).sort_values("DATE")

        if len(df) < 10:
            continue

        # ==============================
        # HANDLE VOLUME SAFELY
        # ==============================
        if "TOTTRDQTY" not in df.columns:
            df["TOTTRDQTY"] = 0

        # ==============================
        # WEEKLY RESAMPLE
        # ==============================
        weekly = df.resample("W", on="DATE").agg({
            "OPEN": "first",
            "HIGH": "max",
            "LOW": "min",
            "CLOSE": "last",
            "TOTTRDQTY": "sum"
        }).dropna()

        if weekly.empty:
            print(f"⚠️ Empty weekly → {file.stem}")
            continue

        # Rename to standard format
        weekly.columns = ["open", "high", "low", "close", "volume"]

        symbol = file.stem
        out_file = OUT_DIR / f"{symbol}.csv"

        weekly.to_csv(out_file, index=False)

        print(f"✅ {symbol} → {len(weekly)} weeks")

    except Exception as e:
        print(f"❌ ERROR → {file.stem} | {e}")

print("\n🔥 WEEKLY DATA READY")