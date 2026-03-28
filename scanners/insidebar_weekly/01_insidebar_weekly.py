import pandas as pd
from pathlib import Path
from datetime import datetime

print("📦 WEEKLY INSIDE BAR SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\insidebar_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_insidebar_{today}.csv"

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

        # ==========================
        # INSIDE BAR CONDITION
        # ==========================
        if (
            curr["high"] < prev["high"] and
            curr["low"] > prev["low"]
        ):
            print(f"📦 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Inside Bar",
                "Prev High": prev["high"],
                "Prev Low": prev["low"]
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")