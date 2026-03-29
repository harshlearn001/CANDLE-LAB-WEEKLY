import pandas as pd
from pathlib import Path

print("📅 WEEKLY UPDATE (MANUAL WEEK) 🔥\n")

# ============================================
# MANUAL INPUT
# ============================================
WEEK_START = "2026-03-23"
WEEK_END   = "2026-03-30"   # 👈 last trading day

WEEK_START = pd.to_datetime(WEEK_START)
WEEK_END   = pd.to_datetime(WEEK_END)

# ============================================
# PATHS
# ============================================
DAILY_DIR = Path(r"H:\MarketForge\data\master\Equity_stock_master")
OUT_DIR   = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR.mkdir(parents=True, exist_ok=True)

files = list(DAILY_DIR.glob("*.csv"))

for file in files:
    try:
        symbol = file.stem
        out_file = OUT_DIR / f"{symbol}.csv"

        df = pd.read_csv(file)

        if df.empty:
            continue

        # CLEAN
        df.columns = df.columns.str.strip().str.upper()

        required = {"DATE", "OPEN", "HIGH", "LOW", "CLOSE"}
        if not required.issubset(df.columns):
            print(f"❌ Skipped → {symbol}")
            continue

        # DATE FIX
        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df.dropna(subset=["DATE"]).sort_values("DATE")

        # VOLUME SAFE
        if "TOTTRDQTY" not in df.columns:
            df["TOTTRDQTY"] = 0

        # ============================================
        # FILTER CUSTOM WEEK
        # ============================================
        df = df[(df["DATE"] >= WEEK_START) & (df["DATE"] <= WEEK_END)]

        if df.empty:
            continue

        # ============================================
        # BUILD SINGLE WEEK
        # ============================================
        weekly = pd.DataFrame()

        weekly.loc[0, "date"] = WEEK_END
        weekly.loc[0, "open"] = df["OPEN"].iloc[0]
        weekly.loc[0, "high"] = df["HIGH"].max()
        weekly.loc[0, "low"] = df["LOW"].min()
        weekly.loc[0, "close"] = df["CLOSE"].iloc[-1]
        weekly.loc[0, "volume"] = df["TOTTRDQTY"].sum()

        # ============================================
        # APPEND LOGIC
        # ============================================
        if out_file.exists():
            old = pd.read_csv(out_file)
            old["date"] = pd.to_datetime(old["date"])

            last_date = old["date"].max()
            old = old[old["date"] < last_date]

            final = pd.concat([old, weekly])
        else:
            final = weekly

        final.sort_values("date", inplace=True)
        final.to_csv(out_file, index=False)

        print(f"🔄 Updated {symbol}")

    except Exception as e:
        print(f"❌ ERROR → {file.stem} | {e}")

print("\n🔥 WEEKLY MANUAL COMPLETE")