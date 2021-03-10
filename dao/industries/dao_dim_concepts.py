from sqlalchemy import select

from domain.industries import Dim_concepts


def c_dim_concepts(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'dim_concepts', if_exists, index=False)


def r_concepts_index():
    stmt = select(Dim_concepts.concepts_index)
    return stmt