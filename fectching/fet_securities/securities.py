from jqdatasdk import *


# 证券
def get_securities_jq(types=[], date=None):
    return get_all_securities(types, date)


# 成分股
def get_index_stocks_jq(index_symbol, date=None):
    return get_index_stocks(index_symbol, date)
