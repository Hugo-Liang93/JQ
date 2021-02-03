from sqlalchemy import select

from domain.industries import Dim_type_industry


def r_parent_industry():
    stmt = select(Dim_type_industry.industry_parent)
    return stmt


def r_parent_industry_by_type(industry_type):
    stmt = select(Dim_type_industry.industry_parent).where(Dim_type_industry.industry_type == industry_type)
    return stmt
