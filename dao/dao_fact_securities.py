from sqlalchemy import select, delete

from domain.securities import *


def c_securities(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_securities', if_exists, index=False)


# ORM Operation

def r_security_type():
    stmt = select(Dim_type_securities.security_type).where(Dim_type_securities.in_securities_list == 'Y')
    return stmt


def r_securities_by_type(securities_type):
    stmt = select(Fact_securities.security).where(Fact_securities.type == securities_type)
    return stmt



