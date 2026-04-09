# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *

import datetime
import numpy as np
import pandas as pd

'''
股票范围：
沪深三百全部股票池
买入条件：
选择20天之内涨幅最大的前20只股票
卖出条件：
持有20天就卖出
买入金额：
每次买入10w。总金额1kw。

每二十天排名之前20天的全部的股票涨跌幅，买其中涨幅前二十大的，持有20day。
'''

n = 0


def init(context):
    # 动能轮动指数-沪深三百
    context.symbol = 'SHSE.000300'
    # 用于统计数据的天数
    context.days = 20

    # GM语法，一天执行一次，内生将1天执行一次
    schedule(schedule_func=algo, date_rule='1d', time_rule='09:35:00')


def algo(context):
    global n
    # 每个交易日一次，每N日真正执行一次
    need_trigger = False
    if n % context.days == 0:
        need_trigger = True
        n += 1
    else:
        n += 1
        # 跳出执行
        return

    # 当天日期
    now_str = context.now.strftime('%Y-%m-%d')
    print(now_str, "执行一次")

    # 获取最近20个交易日(不包括自己)
    # 日期的list str
    last_days = get_previous_n_trading_dates(exchange='SHSE', date=now_str, n=context.days-1)
    last_days.append(now_str)

    # 获取所有成分股
    all_link = stk_get_index_constituents(index=context.symbol, trade_date=last_days[0])
    symbols = list(all_link['symbol'])
    pass

    # 判断是否为每个月第一个交易日

    # 获取并计算指数收益率
    return_index_his1 = history(symbol=symbols, frequency='1d', start_time=last_days[0], fields='symbol,close,bob',
                                adjust=ADJUST_PREV, end_time=last_days[0], df=True)

    return_index_his2 = history(symbol=symbols, frequency='1d', start_time=last_days[-1], fields='symbol,close,bob',
                                adjust=ADJUST_PREV, end_time=last_days[-1], df=True)

    merged_df = pd.merge(return_index_his1, return_index_his2, on='symbol', how='inner')
    merged_df['return'] = (merged_df['close_y'] - merged_df['close_x'])/merged_df['close_x']

    # 收盘价张最多的20个股票
    top_20_returns = merged_df.sort_values(by='return', ascending=False).head(20)

    to_buy = list(top_20_returns['symbol'])
    # 计算权重(预留出2%资金，防止剩余资金不够手续费抵扣)
    percent = 0.98 / len(top_20_returns)
    # 获取当前所有仓位
    positions = get_position()
    # 平不在标的池的股票（注：本策略交易以开盘价为交易价格，当调整定时任务时间时，需调整对应价格）
    for position in positions:
        symbol = position['symbol']
        if symbol not in to_buy:
            # 开盘价（日频数据）
            # new_price = history_n(symbol=symbol, frequency='1d', count=1, end_time=now_str, fields='open', adjust=ADJUST_PREV, adjust_end_time=context.backtest_end_time, df=False)[0]['open']
            # # 当前价（tick数据，免费版本有时间权限限制；实时模式，返回当前最新 tick 数据，回测模式，返回回测当前时间点的最近一分钟的收盘价）
            # new_price = current(symbols=symbol)[0]['price']
            order_target_percent(symbol=symbol, percent=0, order_type=OrderType_Limit, position_side=PositionSide_Long)

    # 买入标的池中的股票（注：本策略交易以开盘价为交易价格，当调整定时任务时间时，需调整对应价格）
    for symbol in to_buy:
        # 开盘价（日频数据）
        # new_price = history_n(symbol=symbol, frequency='1d', count=1, end_time=now_str, fields='open', adjust=ADJUST_PREV, adjust_end_time=context.backtest_end_time, df=False)[0]['open']
        # # 当前价（tick数据，免费版本有时间权限限制；实时模式，返回当前最新 tick 数据，回测模式，返回回测当前时间点的最近一分钟的收盘价）
        # new_price = current(symbols=symbol)[0]['price']
        order_target_percent(symbol=symbol, percent=percent, order_type=OrderType_Limit, position_side=PositionSide_Long)


def on_backtest_finished(context, indicator):
    print('*' * 50)
    print('回测已完成，请通过右上角“回测历史”功能查询详情。')


if __name__ == '__main__':
    '''
    strategy_id策略ID,由系统生成
    filename文件名,请与本文件名保持一致
    mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
    token绑定计算机的ID,可在系统设置-密钥管理中生成
    backtest_start_time回测开始时间
    backtest_end_time回测结束时间
    backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
    backtest_initial_cash回测初始资金
    backtest_commission_ratio回测佣金比例
    backtest_slippage_ratio回测滑点比例
    backtest_match_mode市价撮合模式，以下一tick/bar开盘价撮合:0，以当前tick/bar收盘价撮合：1
    '''
    run(strategy_id='e507f863-29fb-11ef-8122-74563ca4fe2b',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='59e9c8cd18899c191fa133d4cdb08d66efba3dd9',
        backtest_start_time='2010-01-01 08:00:00',
        backtest_end_time='2020-12-31 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001,
        backtest_match_mode=1)
