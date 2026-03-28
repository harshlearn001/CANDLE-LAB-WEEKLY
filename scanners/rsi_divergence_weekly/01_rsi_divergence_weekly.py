import pandas as pd
from pathlib import Path
from datetime import datetime

print("📉 WEEKLY RSI DIVERGENCE SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\rsi_divergence_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")

OUT_BULL = OUT_DIR / f"weekly_bullish_divergence_{today}.csv"
OUT_BEAR = OUT_DIR / f"weekly_bearish_divergence_{today}.csv"

bull_results = []
bear_results = []

# ==============================
# RSI FUNCTION
# ==============================
def calculate_rsi(df, period=14):
    delta = df["close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


# ==============================
# SCAN
# ==============================
files = list(DATA_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)

        if len(df) < 30:
            continue

        df = calculate_rsi(df)

        # Last 5 candles (simple swing detection)
        recent = df.tail(5)

        # --------------------------
        # PRICE SWINGS
        # --------------------------
        price_low1 = recent.iloc[1]["low"]
        price_low2 = recent.iloc[3]["low"]

        price_high1 = recent.iloc[1]["high"]
        price_high2 = recent.iloc[3]["high"]

        # --------------------------
        # RSI SWINGS
        # --------------------------
        rsi_low1 = recent.iloc[1]["RSI"]
        rsi_low2 = recent.iloc[3]["RSI"]

        rsi_high1 = recent.iloc[1]["RSI"]
        rsi_high2 = recent.iloc[3]["RSI"]

        # ==========================
        # BULLISH DIVERGENCE
        # ==========================
        if (
            price_low2 < price_low1 and     # lower low in price
            rsi_low2 > rsi_low1             # higher low in RSI
        ):
            print(f"🟢 Bullish → {file.stem}")

            bull_results.append({
                "Symbol": file.stem,
                "Type": "Bullish Divergence"
            })

        # ==========================
        # BEARISH DIVERGENCE
        # ==========================
        if (
            price_high2 > price_high1 and   # higher high in price
            rsi_high2 < rsi_high1           # lower high in RSI
        ):
            print(f"🔴 Bearish → {file.stem}")

            bear_results.append({
                "Symbol": file.stem,
                "Type": "Bearish Divergence"
            })

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(bull_results).to_csv(OUT_BULL, index=False)
pd.DataFrame(bear_results).to_csv(OUT_BEAR, index=False)

print("\n✅ SCAN COMPLETE")
print(f"🟢 Bullish: {len(bull_results)}")
print(f"🔴 Bearish: {len(bear_results)}")

print("\n📁 Saved:")
print(OUT_BULL)
print(OUT_BEAR)