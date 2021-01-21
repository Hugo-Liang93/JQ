from datetime import datetime
from dao.db_securities import securities_to_db, get_security_type, get_indexs_db
from fectching.fet_securities.securities import get_securities_jq, get_index_stocks_jq
import pandas as pd


def s_get_securities_to_db(db_operation, types=[], date=datetime.now().strftime('%Y-%m-%d')):
    if not types:
        types = db_operation.conn_operate_orm(get_security_type)
    df_securities = get_securities_jq(types, date)
    df_securities = df_securities.reset_index()
    df_securities.rename(columns={'index': 'security'}, inplace=True)
    df_securities['security_date'] = datetime.now().strftime('%Y-%m-%d')
    securities_to_db(db_operation, df_securities)


def s_get_index_stocks_to_db(db_operation, index=None, date=datetime.now().strftime('%Y-%m-%d')):
    if index:
        indexs = db_operation.conn_operate_orm(get_indexs_db)
        for ind in indexs:
            stock_list = get_index_stocks_jq(ind,date)
            df = pd.DataFrame(stock_list,columns=['security'])
            df['index'] = ind
            securities_to_db(db_operation, df)
