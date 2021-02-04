from basic.db_operation import *
from basic.jq_auth import jqAuth
from services.initial_db import initial
from services.services_industry import s_get_industry_by_type, s_get_industry_stocks
from services.services_securities import *

if __name__ == '__main__':
    # jqAuth()
    db_operation = DBOperation(db='jq', user='root', pasw='root')
    initial(db_operation.conn)
    # s_get_industry_by_type(db_operation)
    # s_get_securities_to_db(db_operation)
    # s_get_index_stocks_to_db(db_operation)
    # s_tag_margin_cash(db_operation)
    # s_tag_margin_sec(db_operation)
    # 半小时
    # s_initial_fund_net_value_day(db_operation,'2017-01-01','2021-01-28')
    # s_initial_stock_st(db_operation,'2017-01-01','2021-01-28')
    # s_initial_stock_locked_shares(db_operation, '2017-01-01', '2025-01-28')
    # s_index_stocks_weight(db_operation)
    s_get_industry_stocks(db_operation)