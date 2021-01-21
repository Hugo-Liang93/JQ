from basic.db_operation import *
from basic.jq_auth import jqAuth
from services.initial_db import initial
from services.securities_services import s_get_securities_to_db

if __name__ == '__main__':
    jqAuth()
    db_operation = DBOperation(db='jq', user='root', pasw='root')
    initial(db_operation.conn)
    s_get_securities_to_db(db_operation)