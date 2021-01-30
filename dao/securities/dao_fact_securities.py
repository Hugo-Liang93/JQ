from sqlalchemy import select, update, and_

from domain.securities import *


def c_securities(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_securities', if_exists, index=False)


# ORM Operation

# 获取能security产品列表
def r_fetching_security_type():
    stmt = select(Dim_type_securities.security_type).where(Dim_type_securities.in_securities == True)
    return stmt


# 获取指定类型产品数据
def r_securities_by_type(securities_type):
    stmt = select(Fact_securities.security).where(Fact_securities.type == securities_type)
    return stmt


# 获取Fund的产品列表
def r_securities_is_fund():
    stmt = select(Dim_type_securities.security_type).where(Dim_type_securities.is_fund == True)
    return stmt


# 获取指定类型产品列表并包含生效时间
def r_securities_by_type_date(type_stmt, start_date, end_date):
    stmt = select(Fact_securities.security, Fact_securities.type). \
        where(
        and_(
            Fact_securities.type.in_(type_stmt),
            Fact_securities.start_date <= end_date,
            Fact_securities.end_date >= start_date
        )
    )
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
