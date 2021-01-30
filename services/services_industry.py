from dao.industries.dao_dim_type_industry import r_type_industry
from fectching.industries import get_industries_jq
from datetime import datetime


def s_get_industry_by_type(db_operation):
    types = db_operation.conn_operate_orm(r_type_industry()).scalars().all()
    for type_name in types:
        df = get_industries_jq(type_name, date=datetime.now().strftime('%Y-%m-%d'))
