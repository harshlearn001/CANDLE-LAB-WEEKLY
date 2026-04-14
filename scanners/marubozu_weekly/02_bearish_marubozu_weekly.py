import pandas as pd
from pathlib import Path
from datetime import datetime

print("🔴 WEEKLY BEARISH MARUBOZU 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\marubozu_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_bearish_marubozu_{today}.csv"

# ==============================
# PARAMETERS (UPDATED)
# ==============================
MIN_BODY_RATIO = 0.70
WICK_TOLERANCE = 0.005

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

        curr = df.iloc[-1]

        rng = curr["high"] - curr["low"]
        if rng <= 0:
            continue

        body = abs(curr["close"] - curr["open"])
        body_ratio = body / rng

        if body_ratio < MIN_BODY_RATIO:
            continue

        upper_wick = curr["high"] - max(curr["open"], curr["close"])
        lower_wick = min(curr["open"], curr["close"]) - curr["low"]

        tol = curr["close"] * WICK_TOLERANCE

        if (
            curr["close"] < curr["open"] and
            upper_wick <= tol and
            lower_wick <= tol
        ):
            print(f"🔴 {file.stem}")

            results.append({
                "Symbol": file.stem,
                "Pattern": "Bearish Marubozu",
                "BodyRatio": round(body_ratio, 2)
            })

    except Exception as e:
        print(f"Error {file.stem}: {e}")

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")