from jqdatasdk import *


def get_industries_jq(name, date=None):
    return get_industries(name, date)


def get_industry_stocks_jq(industry_code, date=None):
    return get_industry_stocks(industry_code, date)
