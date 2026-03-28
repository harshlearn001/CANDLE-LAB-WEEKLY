import pandas as pd
from pathlib import Path
from datetime import datetime

print("🧠 MASTER SIGNAL ENGINE (WEEKLY) 🔥\n")

BASE = Path(r"H:\CANDLE-LAB-WEEKLY\analysis\equity\signals")

today = datetime.now().strftime("%Y-%m-%d")

# ==============================
# LOAD FILES SAFELY
# ==============================
def load(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

adx = load(BASE / "adx_weekly" / f"weekly_adx_{today}.csv")
rsi = load(BASE / "rsi_weekly" / f"weekly_rsi_{today}.csv")

bull_eng = load(BASE / "engulfing_weekly" / f"weekly_bullish_engulfing_{today}.csv")
bear_eng = load(BASE / "engulfing_weekly" / f"weekly_bearish_engulfing_{today}.csv")

hammer = load(BASE / "hammer_weekly" / f"weekly_hammer_confirmed_{today}.csv")
hanging = load(BASE / "hangingman_weekly" / f"weekly_hangingman_confirmed_{today}.csv")

shooting = load(BASE / "shooting_star_weekly" / f"weekly_shooting_star_confirmed_{today}.csv")
gravestone = load(BASE / "gravestone_weekly" / f"weekly_gravestone_{today}.csv")

nr7 = load(BASE / "nr7_weekly" / f"weekly_nr7_{today}.csv")
inside = load(BASE / "insidebar_weekly" / f"weekly_insidebar_{today}.csv")

div_bull = load(BASE / "rsi_divergence_weekly" / f"weekly_bullish_divergence_{today}.csv")
div_bear = load(BASE / "rsi_divergence_weekly" / f"weekly_bearish_divergence_{today}.csv")

# ==============================
# ALL SYMBOLS
# ==============================
symbols = set()

for df in [adx, rsi, bull_eng, bear_eng, hammer, hanging,
           shooting, gravestone, nr7, inside, div_bull, div_bear]:
    if not df.empty and "Symbol" in df.columns:
        symbols.update(df["Symbol"].tolist())

print("📊 Total symbols:", len(symbols))

# ==============================
# SCORING ENGINE
# ==============================
results = []

for sym in symbols:

    score = 0
    reasons = []

    # --------------------------
    # ADX
    # --------------------------
    if not adx.empty:
        row = adx[adx["Symbol"] == sym]
        if not row.empty:
            sig = row.iloc[0]["Signal"]
            if "UPTREND" in sig:
                score += 2
                reasons.append("ADX_UP")
            elif "DOWNTREND" in sig:
                score -= 2
                reasons.append("ADX_DOWN")

    # --------------------------
    # RSI
    # --------------------------
    if not rsi.empty:
        row = rsi[rsi["Symbol"] == sym]
        if not row.empty:
            if row.iloc[0]["Signal"] == "OVERSOLD":
                score += 1
                reasons.append("RSI_OS")
            elif row.iloc[0]["Signal"] == "OVERBOUGHT":
                score -= 1
                reasons.append("RSI_OB")

    # --------------------------
    # DIVERGENCE
    # --------------------------
    if not div_bull.empty and sym in div_bull["Symbol"].values:
        score += 2
        reasons.append("BULL_DIV")

    if not div_bear.empty and sym in div_bear["Symbol"].values:
        score -= 2
        reasons.append("BEAR_DIV")

    # --------------------------
    # STRONG PATTERNS
    # --------------------------
    if sym in bull_eng["Symbol"].values if not bull_eng.empty else []:
        score += 2
        reasons.append("BULL_ENG")

    if sym in bear_eng["Symbol"].values if not bear_eng.empty else []:
        score -= 2
        reasons.append("BEAR_ENG")

    if sym in hammer["Symbol"].values if not hammer.empty else []:
        score += 2
        reasons.append("HAMMER")

    if sym in hanging["Symbol"].values if not hanging.empty else []:
        score -= 2
        reasons.append("HANGING")

    # --------------------------
    # WEAK PATTERNS
    # --------------------------
    if sym in shooting["Symbol"].values if not shooting.empty else []:
        score -= 1
        reasons.append("SHOOTING")

    if sym in gravestone["Symbol"].values if not gravestone.empty else []:
        score -= 1
        reasons.append("GRAVESTONE")

    # --------------------------
    # BREAKOUT
    # --------------------------
    if sym in nr7["Symbol"].values if not nr7.empty else []:
        score += 1
        reasons.append("NR7")

    if sym in inside["Symbol"].values if not inside.empty else []:
        score += 1
        reasons.append("INSIDE")

    # ==========================
    # FINAL DECISION
    # ==========================
    if score >= 3:
        signal = "BUY"
    elif score <= -3:
        signal = "SELL"
    else:
        continue

    results.append({
        "Symbol": sym,
        "Score": score,
        "Signal": signal,
        "Reasons": ",".join(reasons)
    })

# ==============================
# SAVE OUTPUT
# ==============================
out = pd.DataFrame(results)

OUT_DIR = BASE / "master"
OUT_DIR.mkdir(exist_ok=True)

OUT_FILE = OUT_DIR / f"final_weekly_trades_{today}.csv"

if not out.empty:
    out = out.sort_values("Score", ascending=False)
    out.to_csv(OUT_FILE, index=False)

    print("\n🔥 FINAL TRADES GENERATED")
    print(out.head(10))
    print("📁 Saved →", OUT_FILE)

else:
    print("\n⚠️ No strong signals today")