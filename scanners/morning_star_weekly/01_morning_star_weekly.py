import pandas as pd
from pathlib import Path
from datetime import datetime

print("🌅 WEEKLY MORNING STAR SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\morning_star_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_morning_star_{today}.csv"

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

        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]

        # ==========================
        # CONDITIONS
        # ==========================

        # Candle 1 bearish
        cond1 = c1["close"] < c1["open"]

        # Candle 2 small body
        body2 = abs(c2["close"] - c2["open"])
        range2 = c2["high"] - c2["low"]
        cond2 = body2 <= (0.3 * range2)

        # Candle 3 bullish
        cond3 = c3["close"] > c3["open"]

        # Close above midpoint of candle 1
        midpoint = (c1["open"] + c1["close"]) / 2
        cond4 = c3["close"] > midpoint

        if cond1 and cond2 and cond3 and cond4:
            print(f"🟢 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Morning Star"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")