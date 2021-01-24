from jqdatasdk import *


# 证券
def get_securities_jq(types=[], date=None):
    return get_all_securities(types, date)


# 成分股
def get_index_stocks_jq(index_symbol, date=None):
    return get_index_stocks(index_symbol, date)


# date默认为最近一次发布的融资标的列表
def get_margincash_stocks_jq(date=None):
    return get_margincash_stocks(date)


def get_marginsec_stocks_jq(date=None):
    return get_marginsec_stocks(date)


def get_stock_st(stocks_list, start_date, end_date, df=True, count=None):
    return get_extras('is_st', stocks_list, start_date=start_date, end_date=end_date, df=df, count=count)


# value_type:
# day
# acc_net_value 基金累计净值,
# unit_net_value 基金单位净值,
# adj_net_value 场外基金的复权净值
def get_fund_net_value_by_type(value_type, fund_list, start_date, end_date, df=True, count=None):
    return get_extras(value_type, fund_list, start_date=start_date, end_date=end_date, df=df, count=count)


# value_type:
# day
# futures_sett_price 期货结算价,
# futures_positions 期货持仓量
def get_futures_value_by_type(value_type, fund_list,
                              start_date, end_date, df=True, count=None):
    return get_extras(value_type, fund_list,
               start_date=start_date, end_date=end_date, df=df, count=count)
