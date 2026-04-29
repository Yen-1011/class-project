import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 參數設定
# ==========================================
INITIAL_CAPITAL = 1000000.0
START_DATE = '2025-01-01'
END_DATE = '2025-12-31'
WINDOW = 30
REBALANCE_DAYS = 10
FEE_RATE = 0.002

# 量化組標的
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT', 'JNJ', 'PG', 'UNH', 'HD', 'BAC']
# 大盤組標的
BENCHMARK = 'SPY'

# ==========================================
# 2. 下載數據 (包含大盤)
# ==========================================
print("正在下載歷史資料...")
all_tickers = TICKERS + [BENCHMARK]
raw_data = yf.download(all_tickers, start=START_DATE, end=END_DATE)['Close']
raw_data = raw_data.ffill().dropna()

data = raw_data[TICKERS]           # 量化組用的股票
benchmark_data = raw_data[BENCHMARK] # 大盤組用的數據

daily_returns = data.pct_change().fillna(0)

# ==========================================
# 3. 回測執行 (量化組 vs 大盤組)
# ==========================================
equity_curve = pd.Series(index=data.index, dtype=float)
equity = INITIAL_CAPITAL
cash = INITIAL_CAPITAL
current_positions = pd.Series(0.0, index=data.columns)
rebalance_dates = data.index[WINDOW::REBALANCE_DAYS]

for i in range(WINDOW, len(data)):
    date = data.index[i]
    # 更新量化組價值
    current_positions = current_positions * (1 + daily_returns.iloc[i])
    equity = current_positions.sum() + cash
    equity_curve[date] = equity
    
    # 再平衡
    if date in rebalance_dates:
        hist_ret = daily_returns.iloc[i-WINDOW:i]
        p = (hist_ret > 0).sum() / WINDOW
        avg_win = hist_ret[hist_ret > 0].mean().fillna(0.0001)
        avg_loss = hist_ret[hist_ret < 0].abs().mean().fillna(0.0001)
        b = avg_win / avg_loss
        kelly = p - (1 - p) / b
        
        valid_kelly = kelly[kelly > 0].nlargest(10)
        half_kelly = valid_kelly * 0.5
        
        total_k = half_kelly.sum()
        target_weights = half_kelly / total_k if total_k > 1.0 else half_kelly
        target_positions = target_weights * equity
        target_positions = target_positions.reindex(data.columns).fillna(0.0)
        
        turnover = (target_positions - current_positions).abs().sum()
        cash = equity - target_positions.sum() - (turnover * FEE_RATE)
        current_positions = target_positions
        equity_curve[date] = current_positions.sum() + cash

# 計算大盤組 (Buy & Hold)
# 邏輯：第一天就全壓 SPY
benchmark_curve = (benchmark_data / benchmark_data.iloc[WINDOW]) * INITIAL_CAPITAL
benchmark_curve = benchmark_curve.iloc[WINDOW:]

# ==========================================
# 4. 績效對比
# ==========================================
def get_stats(curve):
    ret = (curve.iloc[-1] / curve.iloc[0]) - 1
    daily_ret = curve.pct_change().dropna()
    sharpe = (daily_ret.mean() / daily_ret.std()) * np.sqrt(252)
    return ret, sharpe

q_ret, q_sharpe = get_stats(equity_curve.dropna())
b_ret, b_sharpe = get_stats(benchmark_curve)

print(f"\n【量化組 (半凱利策略)】 總報酬: {q_ret*100:.2f}%, 夏普值: {q_sharpe:.2f}")
print(f"【大盤組 (SPY 躺平)】   總報酬: {b_ret*100:.2f}%, 夏普值: {b_sharpe:.2f}")

# ==========================================
# 5. 繪圖
# ==========================================
plt.figure(figsize=(12, 6))
plt.plot(equity_curve, label='Quantitative (Half-Kelly)', color='#1f77b4', lw=2)
plt.plot(benchmark_curve, label='Benchmark (S&P 500)', color='#d62728', linestyle='--', lw=2)
plt.title('Strategy vs Benchmark (2025-2025)', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.show()