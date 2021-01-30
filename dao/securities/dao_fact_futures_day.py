def c_fact_futures_day(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_futures_day', if_exists, index=False)
