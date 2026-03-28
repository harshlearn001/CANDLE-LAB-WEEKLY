import pandas as pd
from pathlib import Path
from datetime import datetime

print("📉 WEEKLY RSI SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\rsi_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_rsi_{today}.csv"

results = []

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

        if len(df) < 20:
            continue

        df = calculate_rsi(df)

        last = df.iloc[-1]
        rsi = last["RSI"]

        if rsi < 30:
            signal = "OVERSOLD"
        elif rsi > 70:
            signal = "OVERBOUGHT"
        else:
            continue

        results.append({
            "Symbol": file.stem,
            "RSI": round(rsi, 2),
            "Signal": signal
        })

        print(f"{file.stem} → {signal}")

    except:
        continue

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")