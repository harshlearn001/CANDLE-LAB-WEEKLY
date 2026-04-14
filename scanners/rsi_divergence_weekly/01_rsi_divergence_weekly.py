import pandas as pd
from pathlib import Path
from datetime import datetime

print("📉 WEEKLY RSI DIVERGENCE SCANNER (FINAL PRO) 🔥\n")

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
# NORMALIZE
# ==============================
def normalize(df):
    df.columns = df.columns.str.strip().str.upper()

    df = df.rename(columns={
        "CLOSE_PRICE": "CLOSE",
        "OPEN_PRICE": "OPEN",
        "HI_PRICE": "HIGH",
        "LO_PRICE": "LOW",
        "TRADE_DATE": "DATE"
    })

    return df

# ==============================
# RSI
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
# SWINGS
# ==============================
def find_swings(df, window=3):

    df['SWING_LOW'] = df['LOW'][
        df['LOW'] == df['LOW'].rolling(window, center=True).min()
    ]

    df['SWING_HIGH'] = df['HIGH'][
        df['HIGH'] == df['HIGH'].rolling(window, center=True).max()
    ]

    return df

# ==============================
# SCAN
# ==============================
files = list(DATA_DIR.glob("*.csv"))

for file in files:
    try:
        df = pd.read_csv(file)
        df = normalize(df)

        if not {'CLOSE','HIGH','LOW'}.issubset(df.columns):
            continue

        # 🔥 Clean data
        df['CLOSE'] = pd.to_numeric(df['CLOSE'], errors='coerce')
        df['HIGH']  = pd.to_numeric(df['HIGH'], errors='coerce')
        df['LOW']   = pd.to_numeric(df['LOW'], errors='coerce')

        df = df.dropna(subset=['CLOSE','HIGH','LOW'])
        df = df[df['CLOSE'] > 0]

        if len(df) < 50:
            continue

        df = df.sort_values("DATE").tail(200)

        df = calculate_rsi(df)
        df = find_swings(df)

        swing_lows = df.dropna(subset=['SWING_LOW'])
        swing_highs = df.dropna(subset=['SWING_HIGH'])

        signal = None

        # ==========================
        # BULLISH
        # ==========================
        if len(swing_lows) >= 2:
            prev_low = swing_lows.iloc[-2]
            curr_low = swing_lows.iloc[-1]

            if (len(df) - df.index.get_loc(curr_low.name)) <= 5:
                if curr_low['LOW'] < prev_low['LOW'] and curr_low['RSI'] > prev_low['RSI']:
                    signal = "BULLISH"

        # ==========================
        # BEARISH
        # ==========================
        if len(swing_highs) >= 2:
            prev_high = swing_highs.iloc[-2]
            curr_high = swing_highs.iloc[-1]

            if (len(df) - df.index.get_loc(curr_high.name)) <= 5:
                if curr_high['HIGH'] > prev_high['HIGH'] and curr_high['RSI'] < prev_high['RSI']:
                    signal = "BEARISH"

        # ==========================
        # FINAL OUTPUT
        # ==========================
        if signal == "BULLISH":
            print(f"🟢 Bullish → {file.stem}")
            bull_results.append({
                "Symbol": file.stem,
                "Type": "Bullish Divergence"
            })

        elif signal == "BEARISH":
            print(f"🔴 Bearish → {file.stem}")
            bear_results.append({
                "Symbol": file.stem,
                "Type": "Bearish Divergence"
            })

    except Exception as e:
        print(f"{file.stem} → ERROR {e}")

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