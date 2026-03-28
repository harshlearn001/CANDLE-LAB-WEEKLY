@echo off

echo ======================================
echo   CANDLE-LAB WEEKLY PIPELINE 🔥
echo ======================================

call conda activate TradeSense

REM ======================================
REM BUILD WEEKLY DATA
REM ======================================
echo.
echo [BUILD WEEKLY DATA]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\setup
python 01_build_weekly_data.py

REM ======================================
REM TREND + MOMENTUM
REM ======================================
echo.
echo [WEEKLY ADX]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\adx_weekly
python 01_adx_weekly.py

echo.
echo [WEEKLY RSI]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\rsi_weekly
python 01_rsi_weekly.py

echo.
echo [WEEKLY RSI DIVERGENCE]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\rsi_divergence_weekly
python 01_rsi_divergence_weekly.py

REM ======================================
REM REVERSAL PATTERNS
REM ======================================
echo.
echo [WEEKLY ENGULFING]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\engulfing_weekly
python 01_bullish_engulfing_weekly.py
python 02_bearish_engulfing_weekly.py

echo.
echo [WEEKLY HAMMER]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\hammer_weekly
python 01_hammer_confirmed_weekly.py

echo.
echo [WEEKLY HANGING MAN]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\hangingman_weekly
python 01_hangingman_confirmed_weekly.py

echo.
echo [WEEKLY SHOOTING STAR]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\shooting_star_weekly
python 02_shooting_star_confirmed_weekly.py

echo.
echo [WEEKLY GRAVESTONE]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\gravestone_weekly
python 01_gravestone_weekly.py

echo.
echo [WEEKLY MORNING STAR]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\morning_star_weekly
python 01_morning_star_weekly.py

echo.
echo [WEEKLY PIERCING PATTERN]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\piercing_pattern_weekly
python 01_piercing_pattern_weekly.py

echo.
echo [WEEKLY HARAMI]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\harami_weekly
python 01_harami_weekly.py

REM ======================================
REM BREAKOUT / VOLATILITY
REM ======================================
echo.
echo [WEEKLY INSIDE BAR]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\insidebar_weekly
python 01_insidebar_weekly.py

echo.
echo [WEEKLY LONG LEGGED DOJI]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\longleg_doji_weekly
python 01_longleg_doji_weekly.py

echo.
echo [WEEKLY SMALL DOJI]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\doji_weekly
python 01_small_doji_weekly.py

echo.
echo [WEEKLY NR7]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\nr7_weekly
python 01_nr7_weekly.py

echo.
echo [MASTER ENGINE]
cd /d H:\CANDLE-LAB-WEEKLY\scanners\master
python 01_master_signal_engine.py

REM ======================================
REM DONE
REM ======================================
echo.
echo ======================================
echo   WEEKLY PIPELINE COMPLETED ✅
echo ======================================

pause