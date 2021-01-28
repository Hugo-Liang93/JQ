def c_stock_locked(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_stock_lockd_shares', if_exists, index=False)
