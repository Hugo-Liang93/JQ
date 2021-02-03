from sqlalchemy import delete

from domain.industries import Fact_industry_stocks


def c_fact_industry_stocks(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_industry_stocks', if_exists, index=False)


def d_industry_stocks_by_industry(industry):
    stmt = delete(Fact_industry_stocks).where(Fact_industry_stocks.industry_parent == industry)
    return stmt


def d_industry_stocks_list(industry_list):
    stmt = delete(Fact_industry_stocks).where(Fact_industry_stocks.industry_parent.in_(industry_list))
    return stmt