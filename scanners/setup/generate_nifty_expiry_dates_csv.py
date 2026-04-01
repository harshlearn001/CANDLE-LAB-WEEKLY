#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CANDLE-LAB | WEEKLY EXPIRY FROM SINGLE FILE

✔ Works with single NIFTY.csv
✔ Extracts all expiry dates (weekly + monthly)
✔ Clean + fast
✔ Production ready
"""

import pandas as pd
from pathlib import Path

print("📊 BUILDING WEEKLY EXPIRY FROM NIFTY.csv\n")

# ============================================
# PATH
# ============================================
DATA_FILE = Path(r"H:\MarketForge\data\master\option_master\INDICES\NIFTY.csv")
OUT_FILE  = Path(r"H:\CANDLE-LAB-WEEKLY\config\nifty_weekly_expiry.csv")

# ============================================
# LOAD DATA
# ============================================
df = pd.read_csv(DATA_FILE)

df.columns = df.columns.str.strip().str.upper()

# ============================================
# CHECK COLUMN
# ============================================
if "EXP_DATE" not in df.columns:
    print("❌ EXP_DATE column not found")
    exit()

# ============================================
# CONVERT DATE
# ============================================
df["EXP_DATE"] = pd.to_datetime(df["EXP_DATE"], format="%Y%m%d", errors="coerce")

df = df.dropna(subset=["EXP_DATE"])

# ============================================
# EXTRACT UNIQUE EXPIRIES
# ============================================
expiry_df = (
    df[["EXP_DATE"]]
    .drop_duplicates()
    .sort_values("EXP_DATE")
    .rename(columns={"EXP_DATE": "EXPIRY_DATE"})
)

# ============================================
# SAVE
# ============================================
expiry_df.to_csv(OUT_FILE, index=False)

# ============================================
# LOG
# ============================================
print(f"✅ Expiry file created → {OUT_FILE}")
print(f"📊 Total expiries: {len(expiry_df)}")

print("\n📌 SAMPLE:")
print(expiry_df.head())

print("\n📌 LAST:")
print(expiry_df.tail())