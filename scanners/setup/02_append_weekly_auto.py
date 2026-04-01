import pandas as pd
from pathlib import Path

print("📅 WEEKLY UPDATE (AUTO + NSE HOLIDAY) 🔥\n")

# ============================================
# SETTINGS
# ============================================
USE_LAST_TRADING_DAY = True

# ============================================
# PATHS
# ============================================
DAILY_DIR = Path(r"H:\MarketForge\data\master\Equity_stock_master")
OUT_DIR   = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

# 🔥 HOLIDAY FILE
HOLIDAY_FILE = "H:\\CANDLE-LAB-WEEKLY\\config\\nse_holidays_2026.csv"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================
# LOAD HOLIDAYS
# ============================================
holiday_df = pd.read_csv(HOLIDAY_FILE)
holiday_df["DATE"] = pd.to_datetime(holiday_df["DATE"])
HOLIDAYS = set(holiday_df["DATE"])

# ============================================
# FUNCTION: FIX WEEK LAST DATE
# ============================================
def get_actual_last_trading_day(df_week):
    # remove holiday dates
    valid_days = df_week[~df_week.index.isin(HOLIDAYS)]

    if valid_days.empty:
        return None

    return valid_days.index.max()

# ============================================
# PROCESS FILES
# ============================================
files = list(DAILY_DIR.glob("*.csv"))

for file in files:
    try:
        symbol = file.stem
        out_file = OUT_DIR / f"{symbol}.csv"

        df = pd.read_csv(file)

        if df.empty:
            continue

        # CLEAN COLUMNS
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

        df.set_index("DATE", inplace=True)

        # ============================================
        # WEEKLY RESAMPLE (FRIDAY BASE)
        # ============================================
        weekly = df.resample("W-FRI").agg({
            "OPEN": "first",
            "HIGH": "max",
            "LOW": "min",
            "CLOSE": "last",
            "TOTTRDQTY": "sum"
        }).dropna()

        if weekly.empty:
            continue

        weekly.reset_index(inplace=True)

        # ============================================
        # 🔥 FIX LAST TRADING DAY USING HOLIDAYS
        # ============================================
        if USE_LAST_TRADING_DAY:

            # get last week range
            last_week_end = weekly["DATE"].iloc[-1]

            # get all dates in that week from original df
            week_data = df[df.index.to_period("W-FRI") == last_week_end.to_period("W-FRI")]

            actual_last_day = get_actual_last_trading_day(week_data)

            if actual_last_day is not None:
                weekly.loc[weekly.index[-1], "DATE"] = actual_last_day

        # FINAL FORMAT
        weekly.columns = ["date", "open", "high", "low", "close", "volume"]

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

print("\n🔥 WEEKLY AUTO COMPLETE (HOLIDAY SMART)")