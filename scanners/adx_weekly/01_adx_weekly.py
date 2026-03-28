import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np

print("📊 WEEKLY ADX SCANNER 🔥\n")

# ==============================
# PATHS
# ==============================
DATA_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\data\weekly")

OUT_DIR = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals\adx_weekly")
OUT_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
OUT_FILE = OUT_DIR / f"weekly_adx_{today}.csv"

results = []

# ==============================
# ADX FUNCTION
# ==============================
def calculate_adx(df, period=14):

    df["H-L"] = df["high"] - df["low"]
    df["H-PC"] = abs(df["high"] - df["close"].shift(1))
    df["L-PC"] = abs(df["low"] - df["close"].shift(1))

    tr = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["TR"] = tr

    df["+DM"] = np.where(
        (df["high"] - df["high"].shift(1)) > (df["low"].shift(1) - df["low"]),
        np.maximum(df["high"] - df["high"].shift(1), 0),
        0
    )

    df["-DM"] = np.where(
        (df["low"].shift(1) - df["low"]) > (df["high"] - df["high"].shift(1)),
        np.maximum(df["low"].shift(1) - df["low"], 0),
        0
    )

    tr_smooth = df["TR"].rolling(period).mean()
    plus_dm = df["+DM"].rolling(period).mean()
    minus_dm = df["-DM"].rolling(period).mean()

    df["+DI"] = 100 * (plus_dm / tr_smooth)
    df["-DI"] = 100 * (minus_dm / tr_smooth)

    dx = (abs(df["+DI"] - df["-DI"]) / (df["+DI"] + df["-DI"])) * 100
    df["ADX"] = dx.rolling(period).mean()

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

        df = calculate_adx(df)

        last = df.iloc[-1]

        adx = last["ADX"]
        plus_di = last["+DI"]
        minus_di = last["-DI"]

        if adx > 25:
            if plus_di > minus_di:
                signal = "STRONG UPTREND"
            else:
                signal = "STRONG DOWNTREND"

            results.append({
                "Symbol": file.stem,
                "ADX": round(adx, 2),
                "+DI": round(plus_di, 2),
                "-DI": round(minus_di, 2),
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