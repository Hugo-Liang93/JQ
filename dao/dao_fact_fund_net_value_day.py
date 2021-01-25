from sqlalchemy import delete

from domain.securities import Fact_fund_net_value_day


def c_fund_net_day(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_fund_net_value_day', if_exists, index=False)


def d_fund_list(fund_list):
    stmt = delete(Fact_fund_net_value_day).where(Fact_fund_net_value_day.security._in(fund_list))
    return stmt
