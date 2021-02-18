from sqlalchemy import select, delete

from domain.industries import Fact_industry


def c_fact_industry(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_industry', if_exists, index=False)


def r_industry_by_industry_parent(industry_parents=None):
    stmt = select(Fact_industry.industry_parent,Fact_industry.industry)
    if industry_parents:
        stmt = stmt.where(Fact_industry.industry_parent.in_(industry_parents))
    return stmt


def r_industry_industry_parent():
    stmt = select(Fact_industry.industry_parent, Fact_industry.industry)
    return stmt


def r_industry_parent(industry):
    stmt = select(Fact_industry.industry_parent)
    if not industry:
        stmt = stmt.where(Fact_industry.industry == industry)
    return stmt


def d_industry_by_industry_parent(industry_parents):
    stmt = delete(Fact_industry).where(Fact_industry.industry_parent.in_(industry_parents))
    return stmt


def d_industry(industry):
    stmt = delete(Fact_industry).where(Fact_industry.industry.in_(industry))
    return stmt
