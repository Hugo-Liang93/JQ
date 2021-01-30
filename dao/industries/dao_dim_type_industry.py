from sqlalchemy.sql import Select

from domain.industries import Dim_type_industry


def r_type_industry():
    stmt = Select(Dim_type_industry.industry)
    return stmt