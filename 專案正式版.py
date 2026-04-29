#正式版
# 使用者輸入初始金額、回測日期
# import datetime
# import yfinance as yf

# while True:
#     try:
#         capital=float(input("Initial capital："))
#         break
#     except ValueError:
#          print("請輸入數字！")
# while True:
#     try:
#         years=int(input("請選擇1~5年："))
#         if years in [1,2,3,4,5]:
#             break
#         else:
#             print("請輸入1,2,3,4,5")
#     except ValueError:
#         print("請輸入數字！")
# 股票清單
# 定義0050變動清單
with open("2021.01_0050list.txt","r") as f:
    initial_list=f.read().strip()
change_list={
    "2021-03-19":{"add":["1590.tw","8046.tw"],"remove":["2883.tw","2890.tw"]},
    "2021-06-21":{"add":[""],"remove":[""]},
    "2021-09-20":{"add":[""],"remove":[""]},
    "2021-12-20":{"add":[""],"remove":[""]},
    "2022-03-21":{"add":[""],"remove":[""]},
    }
print(initial_list)
# 【數據層】： 從 yfinance 下載資料 $\rightarrow$ 清洗缺失值 $\rightarrow$ 計算每日報酬。
# 凱利公式
# 資金分配交易成本
# 視覺化和結果導出