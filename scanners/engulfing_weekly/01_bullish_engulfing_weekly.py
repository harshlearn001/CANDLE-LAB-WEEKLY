import pandas as pd
from pathlib import Path
from datetime import datetime

print("🟢 WEEKLY BULLISH ENGULFING 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\engulfing_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_bullish_engulfing_{today}.csv"

results = []

# ==============================
# SCAN
# ==============================
files = list(DATA_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)

        if len(df) < 2:
            continue

        df = df.tail(2)

        prev = df.iloc[0]
        curr = df.iloc[1]

        # Bullish Engulfing
        if (
            prev["close"] < prev["open"] and   # previous bearish
            curr["close"] > curr["open"] and   # current bullish
            curr["open"] < prev["close"] and
            curr["close"] > prev["open"]
        ):
            print(f"🟢 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Bullish Engulfing"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")