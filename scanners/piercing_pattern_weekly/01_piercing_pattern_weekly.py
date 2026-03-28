import pandas as pd
from pathlib import Path
from datetime import datetime

print("🟢 WEEKLY PIERCING PATTERN SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\piercing_pattern_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_piercing_pattern_{today}.csv"

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

        prev = df.iloc[-2]
        curr = df.iloc[-1]

        prev_open = prev["open"]
        prev_close = prev["close"]

        curr_open = curr["open"]
        curr_close = curr["close"]

        # ==========================
        # CONDITIONS
        # ==========================

        # Candle 1 bearish
        cond1 = prev_close < prev_open

        # Gap down open
        cond2 = curr_open < prev_close

        # Close above midpoint
        midpoint = (prev_open + prev_close) / 2
        cond3 = curr_close > midpoint

        # Current bullish
        cond4 = curr_close > curr_open

        if cond1 and cond2 and cond3 and cond4:
            print(f"🟢 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Piercing Pattern"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")