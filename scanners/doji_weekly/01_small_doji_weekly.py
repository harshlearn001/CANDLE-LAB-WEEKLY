import pandas as pd
from pathlib import Path
from datetime import datetime

print("⚖️ WEEKLY SMALL DOJI SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\doji_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_small_doji_{today}.csv"

results = []

# ==============================
# SCAN
# ==============================
files = list(DATA_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)

        if len(df) < 1:
            continue

        candle = df.iloc[-1]

        open_ = candle["open"]
        close = candle["close"]
        high = candle["high"]
        low = candle["low"]

        body = abs(close - open_)
        full_range = high - low

        # ==========================
        # SMALL DOJI CONDITION
        # ==========================
        if (
            full_range > 0 and
            body <= (0.1 * full_range)
        ):
            print(f"⚖️ {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Small Doji"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")