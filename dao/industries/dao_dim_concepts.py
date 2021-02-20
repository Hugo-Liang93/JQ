def c_dim_concepts(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'dim_concepts', if_exists, index=False)