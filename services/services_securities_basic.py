from datetime import datetime

from dao.securities.dao_fact_fund_net_value_day import c_fund_net_day, d_fund_list
from dao.securities.dao_fact_index_stock import c_index_stock, d_security_list
from dao.securities.dao_fact_locked_shares import c_stock_locked
from dao.securities.dao_fact_securities import *
from dao.securities.dao_fact_stock_st import c_stock_st
from fectching.securities import *
import pandas as pd


def s_get_securities_to_db(db_operation, types=[], date=datetime.now().strftime('%Y-%m-%d')):
    if not types:
        types = db_operation.conn_operate_orm(r_fetching_security_type()).scalars().all()
    df_securities = get_securities_jq(types, date)
    df_securities = df_securities.reset_index()
    df_securities.rename(columns={'index': 'security'}, inplace=True)
    df_securities['fetching_date'] = datetime.now().strftime('%Y-%m-%d')
    c_securities(db_operation, df_securities)


def s_get_index_stocks_to_db(db_operation, indexs=[], date=datetime.now().strftime('%Y-%m-%d')):
    dfs = pd.DataFrame()
    if not indexs:
        indexs = db_operation.conn_operate_orm(r_securities_by_type('index')).scalars().all()
    for index in indexs:
        stock_list = get_index_stocks_jq(index, date)
        df = pd.DataFrame(stock_list, columns=['child_stock'])
        df['security'] = index
        df['effective_date'] = date
        dfs = pd.concat([df, dfs])
    db_operation.conn_operate_orm(d_security_list(indexs))
    c_index_stock(db_operation, dfs)


def s_index_stocks_weight(db_operation, indexs=[], date=datetime.now().strftime('%Y-%m-%d')):
    output_df = pd.DataFrame()
    if not indexs:
        indexs = db_operation.conn_operate_orm(r_securities_by_type('index')).scalars().all()
    for index in indexs:
        stock_weight = get_index_weights_jq(index, date)
        stock_weight = stock_weight.reset_index()
        stock_weight['security'] = index
        stock_weight.rename(columns={'code': 'child_stock', 'date': 'effective_date','index':'child_stock' }, inplace=True)
        output_df = pd.concat([stock_weight, output_df],sort=True)
    db_operation.conn_operate_orm(d_security_list(indexs))
    c_index_stock(db_operation, output_df)


def s_tag_margin_cash(db_operation, margincash_stocks_date=datetime.now().strftime('%Y-%m-%d')):
    margincash_list = get_margincash_stocks_jq(margincash_stocks_date)
    db_operation.conn_operate_orm(u_securities_margincash(margincash_list, margincash_stocks_date))


def s_tag_margin_sec(db_operation, marginsec_stocks_date=datetime.now().strftime('%Y-%m-%d')):
    marginsec_list = get_marginsec_stocks_jq(marginsec_stocks_date)
    db_operation.conn_operate_orm(u_securities_marginsec(marginsec_list, marginsec_stocks_date))


def s_initial_fund_net_value_day(db_operation, start_date, end_date, fund_list=[]):
    output_df = pd.DataFrame(columns=['security', 'security_date', 'acc_net_value', 'unit_net_value', 'adj_net_value'])
    if not fund_list:
        # 所有code list
        fund_result = db_operation.conn_operate_orm(
            r_securities_by_type_date(r_securities_is_fund(), start_date, end_date)).all()
        # 转pd
        fund_df = pd.DataFrame(fund_result)
        # 遍历type
        for fund_type in fund_df[1].unique():
            fund_list = fund_df[fund_df[1] == fund_type][0].to_list()
            db_operation.conn_operate_orm(d_fund_list(fund_list))
            output_df = output_df.append(__fund_net_value(fund_list, start_date, end_date, fund_type), sort=True)
    else:
        db_operation.conn_operate_orm(d_fund_list(fund_list))
        output_df = __fund_net_value(fund_list, start_date, end_date, output_df)
    na_df = output_df.isnull().sum(axis=1)
    # 删除所有
    na_list = na_df[na_df == 3].index.to_list()
    output_df = output_df.drop(labels=na_list)
    c_fund_net_day(db_operation, output_df)


def s_initial_stock_st(db_operation, start_date, end_date, stock_list=[]):
    if not stock_list:
        stock_list = db_operation.conn_operate_orm(
            r_securities_by_type_date(['stock'], start_date, end_date)).scalars().all()
    output_df = get_stock_st(stock_list, start_date, end_date)
    output_df = __format_extracts_value_day(output_df, "is_st")
    c_stock_st(db_operation, output_df)


def s_initial_stock_locked_shares(db_operation, start_date, end_date, stock_list=[]):
    if not stock_list:
        stock_list = db_operation.conn_operate_orm(
            r_securities_by_type_date(['stock'], start_date, end_date)).scalars().all()
    output_df = get_stock_locked_shares(stock_list, start_date, end_date)
    output_df.rename(columns={'code': 'security'}, inplace=True)
    c_stock_locked(db_operation, output_df)


# format dataframe

def __fund_net_value(fund_list, start_date, end_date, fund_type='stock_fund'):
    output_df = pd.DataFrame()
    for type_value in ['acc_net_value', 'unit_net_value', 'adj_net_value']:
        # 场外基金的复权净值只支持场外
        if type_value == 'adj_net_value' and fund_type != 'stock_fund':
            continue
        # 返回DF
        input_df = get_fund_net_value_by_type(type_value, fund_list, start_date, end_date)
        result_df = __format_extracts_value_day(input_df, type_value)
        if not output_df.size:
            output_df = result_df
        else:
            output_df = pd.merge(output_df, result_df, on=['security', 'security_date'])
    return output_df


def __format_extracts_value_day(input_df, type_value):
    mid_df = pd.DataFrame()
    input_df = input_df.reset_index()
    input_df.rename(columns={'index': 'security_date'}, inplace=True)
    for col in input_df.columns.values:
        if col == 'security_date':
            continue
        mid_df = pd.concat([mid_df, pd.DataFrame({
            'security': col,
            'security_date': input_df['security_date'],
            type_value: input_df[col]
        })], ignore_index=True)
    return mid_df