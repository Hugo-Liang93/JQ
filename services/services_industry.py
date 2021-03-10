from dao.industries.dao_dim_concepts import c_dim_concepts, r_concepts_index
from dao.industries.dao_dim_type_industry import r_parent_industry, r_parent_industry_by_type
from dao.industries.dao_fact_industry import c_fact_industry, r_industry_parent, r_industry_by_industry_parent, \
    r_industry_industry_parent
from dao.industries.dao_fact_industry_stocks import c_fact_industry_stocks, d_industry_stocks_by_industry, \
    d_industry_stocks_list
from fectching.industries import get_industries_jq, get_industry_stocks_jq, get_concepts_jq, get_concept_stocks_jq
from datetime import datetime
import pandas as pd


# 获取当天存在的行业
def s_get_industry_by_type(db_operation, industry_parent_type=None, active_date=datetime.now().strftime('%Y-%m-%d')):
    output_df = pd.DataFrame()
    if not industry_parent_type:
        types = db_operation.conn_operate_orm(r_parent_industry()).scalars().all()
    else:
        types = db_operation.conn_operate_orm(r_parent_industry_by_type(industry_parent_type)).scalars().all()
    for type_name in types:
        industry_parent = get_industries_jq(type_name, date=active_date)
        industry_parent = industry_parent.reset_index()
        industry_parent['fetching_date'] = active_date
        industry_parent['industry_parent'] = type_name
        industry_parent.rename(
            columns={'index': 'industry', 'name': 'industry_name', 'start_date': 'industry_active_date'}, inplace=True)
        output_df = pd.concat([industry_parent, output_df], sort=True)
    c_fact_industry(db_operation, output_df)


def s_get_industry_stocks(db_operation, industry_parent=None, industry=None):
    if industry:
        industry_parent = db_operation.conn_operate_orm(r_industry_parent(industry)).scalars().all()
        stock_df = s_get_industry_stocks_by_industry(industry, industry_parent)
        db_operation.conn_operate_orm(d_industry_stocks_by_industry(industry))
        c_fact_industry_stocks(db_operation, stock_df)
    else:
        stock_df = pd.DataFrame()
        del_list = []
        if industry_parent:
            industry_tuple_list = db_operation.conn_operate_orm(r_industry_by_industry_parent(industry_parent)).all()
        else:
            industry_tuple_list = db_operation.conn_operate_orm(r_industry_industry_parent()).all()
        for industry_parent,industry in industry_tuple_list:
            del_list.append(industry)
            stock_mid = s_get_industry_stocks_by_industry(industry, industry_parent)
            stock_df = pd.concat([stock_df, stock_mid], sort=True)
        d_industry_stocks_list(del_list)
        c_fact_industry_stocks(db_operation, stock_df)


def s_get_industry_stocks_by_industry(industry, industry_parent):
    stock_list = get_industry_stocks_jq(industry)
    stock_df = pd.DataFrame(stock_list, columns=['stock'])
    stock_df['industry_parent'] = industry_parent
    stock_df['industry'] = industry
    stock_df['fetching_date'] = datetime.now().strftime('%Y-%m-%d')
    return stock_df


def s_get_concepts():
    concepts_df = get_concepts_jq()
    concepts_df.rename(
            columns={'index': 'concepts_index', 'name': 'concepts_name', 'start_date': 'concepts_start_date'}, inplace=True)
    c_dim_concepts(concepts_df)


def s_get_concept_stocks(db_operation,concepts_index):
    if concepts_index:
        stock_list = get_concept_stocks_jq(concepts_index)
    else:
        concepts_index = db_operation.conn_operate_orm(r_concepts_index()).scalars().all()
    stock_df = pd.DataFrame(stock_list, columns=['stock'])


def s_get_stocks_by_concept(concepts_index):
    stock_list = get_concept_stocks_jq(concepts_index)
    stock_df = pd.DataFrame(stock_list, columns=['stock'])