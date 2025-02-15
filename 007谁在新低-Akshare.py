import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 获取今天的日期
today = datetime.today()
# 计算60天前的日期
sixty_days_ago = today - timedelta(days=60)

# 将日期格式化为字符串，用于API请求
today_str = today.strftime("%Y%m%d")
sixty_days_ago_str = sixty_days_ago.strftime("%Y%m%d")

# 获取沪深300成分股列表
hs300_stocks = ak.index_stock_cons_csindex(symbol="000300")
hs300_codes = hs300_stocks['成分券代码'].tolist()

# 定义一个函数来获取股票的历史数据并计算60日最低价
def get_60_day_low(stock_code):
    try:
        # 获取股票历史数据
        stock_data = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=sixty_days_ago_str, end_date=today_str)
        # 计算60日最低价
        stock_data['60_day_low'] = stock_data['收盘'].rolling(window=60).min()
        # 获取最新一天的数据
        latest_data = stock_data.iloc[-1]
        # 判断是否处于60日新低
        if latest_data['收盘'] == latest_data['60_day_low']:
            return stock_code, latest_data['日期'], latest_data['收盘']
        else:
            return None
    except Exception as e:
        print(f"Error processing {stock_code}: {e}")
        return None

# 遍历所有沪深300成分股，找出处于60日新低的股票
low_stocks = []
for stock_code in hs300_codes:
    print(stock_code)
    result = get_60_day_low(stock_code)
    if result:
        low_stocks.append(result)

# 将结果转换为DataFrame
low_stocks_df = pd.DataFrame(low_stocks, columns=['股票代码', '日期', '收盘'])

# 打印结果
print(low_stocks_df)