from datetime import datetime

from dao.dao_fact_fund_net_value_day import c_fund_net_day, d_fund_list
from dao.dao_fact_index_stock import d_security, c_index_stock, d_security_list
from dao.dao_fact_securities import c_securities, r_security_type, r_securities_by_type, u_securities_margincash, \
    u_securities_marginsec, r_securities_by_fund_flag
from fectching.fet_securities.securities import get_securities_jq, get_index_stocks_jq, get_margincash_stocks_jq, \
    get_marginsec_stocks_jq, get_fund_net_value_by_type
import pandas as pd


def s_get_securities_to_db(db_operation, types=[], date=datetime.now().strftime('%Y-%m-%d')):
    if not types:
        types = db_operation.conn_operate_orm(r_security_type()).scalars().all()
    df_securities = get_securities_jq(types, date)
    df_securities = df_securities.reset_index()
    df_securities.rename(columns={'index': 'security'}, inplace=True)
    df_securities['fetching_date'] = datetime.now().strftime('%Y-%m-%d')
    c_securities(db_operation, df_securities)


def s_get_index_stocks_to_db(db_operation, index=None, date=datetime.now().strftime('%Y-%m-%d')):
    dfs = pd.DataFrame()
    if not index:
        indexs = db_operation.conn_operate_orm(r_securities_by_type('index')).scalars().all()
        for ind in indexs:
            df = __format_index_stock(ind, date)
            dfs = pd.concat([df, dfs])
        db_operation.conn_operate_orm(d_security_list(indexs))
        c_index_stock(db_operation, dfs)
    else:
        df = __format_index_stock(index, date)
        db_operation.conn_operate_orm(d_security(index))
        c_index_stock(db_operation, df)


def __format_index_stock(index, date):
    stock_list = get_index_stocks_jq(index, date)
    df = pd.DataFrame(stock_list, columns=['child_stock'])
    df['security'] = index
    df['effective_date'] = date
    return df


def s_tag_margincash(db_operation, margincash_stocks_date=datetime.now().strftime('%Y-%m-%d')):
    margincash_list = get_margincash_stocks_jq(margincash_stocks_date)
    db_operation.conn_operate_orm(u_securities_margincash(margincash_list, margincash_stocks_date))


def s_tag_marginsec(db_operation, marginsec_stocks_date=datetime.now().strftime('%Y-%m-%d')):
    marginsec_list = get_marginsec_stocks_jq(marginsec_stocks_date)
    db_operation.conn_operate_orm(u_securities_marginsec(marginsec_list, marginsec_stocks_date))


def s_inital_fund_net_value_day(db_operation, start_date, end_date, fund_list=[]):
    output_df = pd.DataFrame()
    if not fund_list:
        fund_list = db_operation.conn_operate_orm(r_securities_by_fund_flag()).scalars().all()
    print(fund_list)
    # initial
    # db_operation.conn_operate_orm(d_fund_list(fund_list))
    for type_value in ['acc_net_value', 'unit_net_value', 'adj_net_value']:
        input_df = get_fund_net_value_by_type(type_value, fund_list, start_date, end_date)
        result_df = __format_fund_value_day(input_df, type_value)
        if not output_df.size:
            output_df = result_df
        else:
            output_df = pd.merge(output_df,result_df,on=['security','security_date'])
    c_fund_net_day(db_operation, output_df)


def __format_fund_value_day(input_df, type_value):
    mid_df = pd.DataFrame()
    input_df = input_df.reset_index()
    input_df.rename(columns={'index': 'security_date'}, inplace=True)
    # need to update
    for col in input_df.columns.values:
        if col == 'security_date':
            continue
        mid_df = pd.concat([mid_df,pd.DataFrame({
            'security': col,
            'security_date': input_df['security_date'],
            type_value: input_df[col]
        })] ,ignore_index=True)

    return mid_df