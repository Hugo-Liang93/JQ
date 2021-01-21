from sqlalchemy import select

from domain.securities import Dim_type_securities, Fact_securities


def r_get_security_type():
    stmt = select(Dim_type_securities.security_type).where(Dim_type_securities.in_securities_list == 'Y')
    return stmt


def r_get_index():
    stmt = select(Fact_securities.security).where(Fact_securities.type == 'index')
    return stmt
