from basic.db_operation import *
from basic.jq_auth import jqAuth
from services.initial_db import initial
from services.services_securities_basic import *

if __name__ == '__main__':
    jqAuth()
    db_operation = DBOperation(db='jq', user='root', pasw='root')
    # initial(db_operation.conn)
    # s_get_securities_to_db(db_operation)
    # s_get_index_stocks_to_db(db_operation)
    # s_tag_margincash(db_operation)
    # s_tag_marginsec(db_operation)
    s_inital_fund_net_value_day(db_operation,'2020-06-01','2021-01-25')