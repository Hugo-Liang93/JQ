from sqlalchemy import select, update

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


def u_securities_margincash(margincash_list, margincash_date):
    stmt = update(Fact_securities) \
        .where(Fact_securities.security.in_(margincash_list)) \
        .values({'margincash_stocks': True, 'margincash_stocks_date': margincash_date})
    return stmt


def u_securities_marginsec(marginsec_list, marginsec_date):
    stmt = update(Fact_securities) \
        .where(Fact_securities.security.in_(marginsec_list)) \
        .values({'marginsec_stocks': True, 'marginsec_stocks_date': marginsec_date})
    return stmt
