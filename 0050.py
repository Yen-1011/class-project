import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 設定參數
ticker_symbol = "0050.TW"
start_date = "2025-01-01"
end_date = "2026-01-01"
initial_capital = 1000000
fee_rate = 0.001425
fee_discount = 0.6
tax_rate = 0.001

# 2. 下載資料
stock = yf.Ticker(ticker_symbol)
df = stock.history(start=start_date, end=end_date)

if df.empty:
    print("找不到資料")
else:
    prices = df['Close']
    start_price = prices.iloc[0]

    # 3. 計算買進後的剩餘股數
    buy_fee_factor = 1 + (fee_rate * fee_discount)
    shares_owned = initial_capital / (start_price * buy_fee_factor)

    actual_buy_cost = shares_owned * start_price
    buy_fee = actual_buy_cost * fee_rate * fee_discount

    # 4. 計算每日資產淨值 (若當天賣出的話)
    raw_value = prices * shares_owned
    sell_fees = raw_value * fee_rate * fee_discount
    sell_taxes = raw_value * tax_rate
    net_portfolio_value = raw_value - sell_fees - sell_taxes

    # 5. 資料視覺化
    plt.figure(figsize=(12, 6))
    plt.plot(net_portfolio_value.index, net_portfolio_value.values,
             color='#2ca02c', linewidth=2, label='Net Portfolio Value (After Fees & Tax)')

    plt.axhline(y=initial_capital, color='#d62728', linestyle='--', alpha=0.6, label='Initial Capital (1M)')

    plt.title(f'2025 Net Profit Analysis: {ticker_symbol} (Post-Tax & Fees)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Value (TWD)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.gcf().autofmt_xdate()

    # 6. 最終結算
    final_net_value = net_portfolio_value.iloc[-1]
    total_net_profit = final_net_value - initial_capital
    net_roi = (total_net_profit / initial_capital) * 100

    print("-" * 40)
    print(f"【2025 年度結算報告 - 扣除交易成本】")
    print(f"買進股價: {start_price:.2f} TWD")
    print(f"持有股數: {shares_owned:.2f} 股")
    print(f"買進手續費: {buy_fee:,.0f} TWD")
    print(f"年底賣出淨所得: {final_net_value:,.0f} TWD")
    print(f"全年度淨損益: {total_net_profit:,.0f} TWD")
    print(f"實質淨報酬率: {net_roi:.2f}%")
    print("-" * 40)

    plt.show()
