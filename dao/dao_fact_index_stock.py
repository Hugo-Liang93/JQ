from sqlalchemy import delete

from domain.securities import Fact_index_stock

def c_index_stock(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_index_stock', if_exists, index=False)


def d_security(security):
    stmt = delete(Fact_index_stock).where(Fact_index_stock.security == security)
    return stmt