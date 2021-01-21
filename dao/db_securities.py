from dao.crud.securities import *


def securities_to_db(db_operation, df):
    db_operation.to_sql(df, 'fact_securities', index=False)


# ORM Operation
def get_security_type(session):
    result = session.execute(r_get_security_type())
    return result.scalars().all()


def get_indexs_db(session):
    result = session.execute(r_get_index())
    return result.scalars().all()

def del_index_stock
