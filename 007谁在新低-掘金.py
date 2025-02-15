# -*- coding: utf-8 -*-
"""
文件名: 007谁在新低-掘金.py
功能: 使用掘金量化API识别沪深300指数成分股中处于N日新低的股票
作者: [您的名字]
日期: [当前日期]
"""

from __future__ import print_function, absolute_import
from datetime import datetime, timedelta
from gm.api import *
import pandas as pd

# 常量设置
API_TOKEN = "59e9c8cd18899c191fa133d4cdb08d66efba3dd9"
N_DAYS = 30  # 查找新低的天数范围
INDEX_CODE = 'SHSE.000300'  # 沪深300指数的代码

def setup_api():
    """设置API token"""
    set_token(API_TOKEN)

def get_date_range():
    """获取日期范围"""
    today = datetime.today()
    n_days_ago = today - timedelta(days=N_DAYS)
    return n_days_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def get_index_constituents(index_code):
    """获取指数成分股"""
    constituents = stk_get_index_constituents(index_code)
    return list(constituents['symbol'])

def get_historical_data(symbols, start_date, end_date):
    """获取历史数据"""
    return history(symbol=symbols, frequency='1d', start_time=start_date, end_time=end_date, df=True)

def find_n_day_low_stocks(history_data):
    """找出N日新低的股票"""
    low_stocks = []
    for symbol in history_data['symbol'].unique():
        stock_data = history_data[history_data['symbol'] == symbol]
        latest_data = stock_data.iloc[-1]
        if latest_data['low'] == stock_data['low'].min():
            low_stocks.append((symbol, latest_data['eob'], latest_data['low']))
    return low_stocks

def main():
    """主函数"""
    # 设置API
    setup_api()

    # 获取日期范围
    start_date, end_date = get_date_range()

    # 获取沪深300指数的成分股
    constituent_symbols = get_index_constituents(INDEX_CODE)

    # 获取历史数据
    history_data = get_historical_data(constituent_symbols, start_date, end_date)

    # 找出最近N日新低的股票
    low_stocks = find_n_day_low_stocks(history_data)

    # 将结果转换为DataFrame并打印
    low_stocks_df = pd.DataFrame(low_stocks, columns=['股票代码', '日期', '最低价'])
    print(f"最近{N_DAYS}日新低的股票：")
    print(low_stocks_df)

if __name__ == "__main__":
    main()
