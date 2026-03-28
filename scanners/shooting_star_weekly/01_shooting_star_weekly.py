import pandas as pd
from pathlib import Path
from datetime import datetime

print("🌠 WEEKLY SHOOTING STAR SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\shooting_star_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_shooting_star_{today}.csv"

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

        candle = df.iloc[-1]

        open_ = candle["open"]
        close = candle["close"]
        high = candle["high"]
        low = candle["low"]

        body = abs(close - open_)
        full_range = high - low

        upper_wick = high - max(open_, close)
        lower_wick = min(open_, close) - low

        # ==========================
        # SHOOTING STAR CONDITIONS
        # ==========================
        if (
            full_range > 0 and
            body <= (0.3 * full_range) and
            upper_wick >= (0.6 * full_range) and
            lower_wick <= (0.1 * full_range)
        ):
            print(f"🔴 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Shooting Star"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")