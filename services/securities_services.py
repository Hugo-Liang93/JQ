from datetime import datetime

from dao.dao_fact_index_stock import d_security, c_index_stock
from dao.dao_fact_securities import c_securities, r_security_type, r_securities_by_type
from fectching.fet_securities.securities import get_securities_jq, get_index_stocks_jq
import pandas as pd


def s_get_securities_to_db(db_operation, types=[], date=datetime.now().strftime('%Y-%m-%d')):
    if not types:
        types = db_operation.conn_operate_orm(r_security_type()).scalars().all()
    df_securities = get_securities_jq(types, date)
    df_securities = df_securities.reset_index()
    df_securities.rename(columns={'index': 'security'}, inplace=True)
    df_securities['security_date'] = datetime.now().strftime('%Y-%m-%d')
    c_securities(db_operation, df_securities)


def s_get_index_stocks_to_db(db_operation, index=None, date=datetime.now().strftime('%Y-%m-%d')):
    if not index:
        indexs = db_operation.conn_operate_orm(r_securities_by_type('index')).scalars().all()
        for ind in indexs:
            df = __formate_index_stock(ind, date)
            db_operation.conn_operate_orm(d_security(ind))
            c_index_stock(db_operation, df)
    else:
        df = __formate_index_stock(index, date)
        db_operation.conn_operate_orm(d_security(index))
        c_index_stock(db_operation, df)


def __formate_index_stock(index, date):
    stock_list = get_index_stocks_jq(index, date)
    df = pd.DataFrame(stock_list, columns=['child_stock'])
    df['security'] = index
    df['effective_date'] = date
    return df
