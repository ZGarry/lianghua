# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *
import talib
# 单双均线没有任何意义可言


# 策略中必须有init方法
def init(context):
    # 定义一些初始变量，5日线和10日线非常好
    context.FAST = 5
    context.SLOW = 10
    context.symbol = 'SZSE.000651'
    context.period = context.SLOW + 1
    subscribe(context.symbol, '1d', count=context.period)


def on_bar(context, bars):
    print(bars[0].bob)
    # 获取数据'
    # 获取当前以及前period天的数据
    prices = context.data(symbol=context.symbol, frequency='1d', count=context.period, fields='open')
    # 计算出均线
    fast_avg = talib.SMA(prices.values.reshape(context.period), context.FAST)
    slow_avg = talib.SMA(prices.values.reshape(context.period), context.SLOW)

    # amount = context.account.positions(symbol = context.symbol)
    if fast_avg[-1] > slow_avg[-1]:
        # 升破买入，降破卖出
        # 理论上来说，当前已经满仓就无需买入。系统也会自动拒绝买入
        order_target_percent(symbol=context.symbol, percent=1, position_side=1, order_type=2)
        print('买入')
    if fast_avg[-1] < slow_avg[-1]:
        order_target_percent(symbol=context.symbol, percent=0, position_side=1, order_type=2)
        print('卖出')


if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        backtest_match_mode市价撮合模式，以下一tick/bar开盘价撮合:0，以当前tick/bar收盘价撮合：1
        '''
    run(strategy_id='9af8a37f-29fa-11ef-b158-74563ca4fe2b',
        filename='4 双均线策略.py',
        mode=MODE_BACKTEST,
        token='59e9c8cd18899c191fa133d4cdb08d66efba3dd9',
        backtest_start_time='2013-01-01 08:00:00',
        backtest_end_time='2023-12-31 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001,
        backtest_match_mode=1)

