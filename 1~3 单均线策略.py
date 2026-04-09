# coding=utf-8
# 本地回测保持和客户端的策略id一致，就可以输出回测报告
# 客户端中数据管理可以查找关注股票的编号
# 单双均线没有任何意义可言
from __future__ import print_function, absolute_import
from gm.api import *
import talib


# 策略中必须有init方法
def init(context):
    # 调整这个时间
    context.FAST = 30
    # 可选股票 SHZSE.000300, 茅台and其他
    context.symbol = 'SHSE.601288'
    context.period = context.FAST + 1
    subscribe(context.symbol, '1d', count=context.period)


def on_bar(context, bars):
    print(bars[0].bob)
    # 获取数据'
    # 获取当前以及前period天的数据
    prices = context.data(symbol=context.symbol, frequency='1d', count=context.period, fields='close')
    # 计算出均线
    fast_avg = talib.SMA(prices.values.reshape(context.period), context.FAST)

    # 升破买入，降破卖出
    if prices['close'].iloc[-1] > fast_avg[-1]:
        order_target_percent(symbol=context.symbol, percent=1, position_side=1, order_type=2)
        print('买入标的')
    else:
        order_target_percent(symbol=context.symbol, percent=0, position_side=1, order_type=2)
        print('卖出标的')


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
    # 如果你复制到你自己的客户端，需要覆盖这个策略id
    run(strategy_id='1ace6ad1-2df4-11ef-9aac-00155d7d95e0',
        filename='1~3 单均线策略.py',
        mode=MODE_BACKTEST,
        token='59e9c8cd18899c191fa133d4cdb08d66efba3dd9',
        backtest_start_time='2011-01-01 08:00:00',
        backtest_end_time='2023-12-31 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=10000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001,
        backtest_match_mode=1)

