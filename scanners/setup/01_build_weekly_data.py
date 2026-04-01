import pandas as pd
from pathlib import Path

print("📅 BUILDING WEEKLY DATA (HOLIDAY SMART) 🔥\n")

# ==============================
# PATHS
# ==============================
DAILY_DIR = Path(r"H:\MarketForge\data\master\Equity_stock_master")
OUT_DIR   = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

# 🔥 HOLIDAY FILE
HOLIDAY_FILE = "H:\\CANDLE-LAB-WEEKLY\\config\\nse_holidays_2026.csv"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# LOAD HOLIDAYS
# ==============================
holiday_df = pd.read_csv(HOLIDAY_FILE)
holiday_df["DATE"] = pd.to_datetime(holiday_df["DATE"])
HOLIDAYS = set(holiday_df["DATE"])

# ==============================
# FUNCTION: GET LAST TRADING DAY
# ==============================
def get_last_trading_day(group):
    valid = group[~group["DATE"].isin(HOLIDAYS)]
    if valid.empty:
        return None
    return valid.iloc[-1]

# ==============================
# PROCESS FILES
# ==============================
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
        # HANDLE VOLUME
        # ==============================
        if "TOTTRDQTY" not in df.columns:
            df["TOTTRDQTY"] = 0

        # ==============================
        # CREATE WEEK GROUP (MONDAY BASE)
        # ==============================
        df["WEEK"] = df["DATE"].dt.to_period("W-MON")

        weekly_rows = []

        # ==============================
        # BUILD WEEKLY (SMART)
        # ==============================
        for _, g in df.groupby("WEEK"):
            g = g.sort_values("DATE")

            last_row = get_last_trading_day(g)
            if last_row is None:
                continue

            weekly_rows.append({
                "date": last_row["DATE"],                 # 🔥 correct trading day
                "open": g["OPEN"].iloc[0],
                "high": g["HIGH"].max(),
                "low": g["LOW"].min(),
                "close": last_row["CLOSE"],               # 🔥 correct close
                "volume": g["TOTTRDQTY"].sum()
            })

        weekly = pd.DataFrame(weekly_rows)

        if weekly.empty:
            print(f"⚠️ Empty weekly → {file.stem}")
            continue

        # ==============================
        # SAVE
        # ==============================
        symbol = file.stem
        out_file = OUT_DIR / f"{symbol}.csv"

        weekly.sort_values("date", inplace=True)
        weekly.to_csv(out_file, index=False)

        print(f"✅ {symbol} → {len(weekly)} weeks")

    except Exception as e:
        print(f"❌ ERROR → {file.stem} | {e}")

print("\n🔥 WEEKLY BUILD COMPLETE (HOLIDAY SMART)")