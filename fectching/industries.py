from jqdatasdk import *


def get_industries_jq(name, date=None):
    return get_industries(name, date)


def get_industry_stocks_jq(industry_code, date=None):
    return get_industry_stocks(industry_code, date)


def get_concepts_jq():
    return get_concepts()


def get_concept_stocks_jq(concepts_index, date=None):
    return get_concept_stocks(concepts_index, date)
