import pandas as pd
from pathlib import Path

print("📅 BUILDING WEEKLY DATA (FNO ONLY) 🔥\n")

# ==============================
# PATHS
# ==============================
DAILY_DIR = Path(r"H:\MarketForge\data\master\Equity_stock_master")
OUT_DIR   = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly_1")

EXPIRY_FILE = Path(r"H:\CANDLE-LAB-WEEKLY\config\nifty_weekly_expiry.csv")
HOLIDAY_FILE = Path(r"H:\CANDLE-LAB-WEEKLY\config\nse_holidays_2026.csv")

# 🔥 FNO SYMBOL FILE
FNO_FILE = Path(r"H:\CANDLE-LAB-WEEKLY\config\fno_symbols\fno_symbols.csv")

OUT_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# LOAD FNO SYMBOLS (FINAL)
# ==============================
from pathlib import Path
import pandas as pd

FNO_FILE = Path(r"H:\CANDLE-LAB-WEEKLY\config\fno_symbols.csv")

print(f"📄 Using FNO file: {FNO_FILE}")

fno_df = pd.read_csv(FNO_FILE)

if "SYMBOL" not in fno_df.columns:
    raise ValueError("❌ Column 'SYMBOL' not found in FNO file")

FNO_SYMBOLS = (
    fno_df["SYMBOL"]
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .tolist()
)

print(f"✔ FNO Symbols Loaded: {len(FNO_SYMBOLS)}")
# ==============================
# LOAD EXPIRY
# ==============================
exp_df = pd.read_csv(EXPIRY_FILE)
exp_df["EXPIRY_DATE"] = pd.to_datetime(exp_df["EXPIRY_DATE"])
expiry_dates = exp_df.sort_values("EXPIRY_DATE")["EXPIRY_DATE"].tolist()

# ==============================
# LOAD HOLIDAYS
# ==============================
holiday_df = pd.read_csv(HOLIDAY_FILE)
holiday_df["DATE"] = pd.to_datetime(holiday_df["DATE"], format="%Y-%m-%d", errors="coerce")
HOLIDAYS = set(holiday_df["DATE"])

# ==============================
# FUNCTION
# ==============================
def get_last_trading_day(df):
    valid = df[~df["DATE"].isin(HOLIDAYS)]
    return valid.iloc[-1] if not valid.empty else None

# ==============================
# PROCESS FILES
# ==============================
files = list(DAILY_DIR.glob("*.csv"))

print(f"\n📂 Total files found: {len(files)}\n")

for file in files:

    symbol = file.stem.upper()

    # 🔥 FILTER HERE
    if symbol not in FNO_SYMBOLS:
        continue

    try:
        df = pd.read_csv(file)

        if df.empty:
            continue

        df.columns = df.columns.str.strip().str.upper()

        required = {"DATE", "OPEN", "HIGH", "LOW", "CLOSE"}
        if not required.issubset(df.columns):
            print(f"❌ Skipped → {symbol}")
            continue

        df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
        df = df.dropna(subset=["DATE"]).sort_values("DATE")

        if len(df) < 10:
            continue

        if "TOTTRDQTY" not in df.columns:
            df["TOTTRDQTY"] = 0

        weekly_rows = []

        for i in range(1, len(expiry_dates)):
            start = expiry_dates[i - 1]
            end   = expiry_dates[i]

            window = df[(df["DATE"] > start) & (df["DATE"] <= end)]

            if window.empty:
                continue

            window = window.sort_values("DATE")

            last_row = get_last_trading_day(window)
            if last_row is None:
                continue

            weekly_rows.append({
                "date": last_row["DATE"],
                "open": window["OPEN"].iloc[0],
                "high": window["HIGH"].max(),
                "low": window["LOW"].min(),
                "close": last_row["CLOSE"],
                "volume": window["TOTTRDQTY"].sum()
            })

        weekly = pd.DataFrame(weekly_rows)

        if weekly.empty:
            print(f"⚠️ Empty → {symbol}")
            continue

        out_file = OUT_DIR / f"{symbol}.csv"

        weekly.sort_values("date", inplace=True)
        weekly.to_csv(out_file, index=False)

        print(f"✅ {symbol:<15} → {len(weekly)} weeks")

    except Exception as e:
        print(f"❌ ERROR → {symbol} | {e}")

print("\n🔥 FNO WEEKLY BUILD COMPLETE\n")