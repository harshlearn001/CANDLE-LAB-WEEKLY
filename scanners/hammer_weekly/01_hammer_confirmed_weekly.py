import pandas as pd
from pathlib import Path
from datetime import datetime

print("🟢 WEEKLY HAMMER WITH CONFIRMATION 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\hammer_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_hammer_confirmed_{today}.csv"

results = []

# ==============================
# SCAN
# ==============================
files = list(DATA_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)

        if len(df) < 3:
            continue

        # Last 2 candles
        hammer = df.iloc[-2]
        confirm = df.iloc[-1]

        open_ = hammer["open"]
        close = hammer["close"]
        high = hammer["high"]
        low = hammer["low"]

        body = abs(close - open_)
        full_range = high - low

        lower_wick = min(open_, close) - low
        upper_wick = high - max(open_, close)

        # ==========================
        # HAMMER CONDITIONS
        # ==========================
        is_hammer = (
            full_range > 0 and
            body <= (0.3 * full_range) and
            lower_wick >= (0.6 * full_range) and
            upper_wick <= (0.1 * full_range)
        )

        # ==========================
        # CONFIRMATION
        # ==========================
        is_confirmed = confirm["close"] > high

        if is_hammer and is_confirmed:
            print(f"🟢 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Hammer Confirmed"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")