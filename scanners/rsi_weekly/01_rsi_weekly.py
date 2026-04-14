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
    delta = df["CLOSE"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df


# ==============================
# SCAN
# ==============================
files = list(DATA_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)

        # 🔥 Normalize columns
        df.columns = df.columns.str.strip().str.upper()

        df = df.rename(columns={
            "CLOSE_PRICE": "CLOSE",
            "CLOSE": "CLOSE"
        })

        # ❗ Check column exists
        if "CLOSE" not in df.columns:
            print(f"{file.stem} → CLOSE missing ❌")
            continue

        # 🔥 Convert to numeric (CRITICAL)
        df["CLOSE"] = pd.to_numeric(df["CLOSE"], errors="coerce")

        # 🔥 Clean data
        df = df.dropna(subset=["CLOSE"])
        df = df[df["CLOSE"] > 0]

        if len(df) < 20:
            continue

        df = calculate_rsi(df)

        last = df.iloc[-1]
        rsi = last["RSI"]

        if pd.isna(rsi):
            print(f"{file.stem} → RSI NaN ❌")
            continue

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

        print(f"{file.stem} → RSI {round(rsi,2)} → {signal}")

    except Exception as e:
        print(f"{file.stem} → ERROR {e}")

# ==============================
# SAVE
# ==============================
pd.DataFrame(results).to_csv(OUT_FILE, index=False)

print(f"\n✅ Total: {len(results)}")
print(f"📁 Saved → {OUT_FILE}")