

def c_stock_st(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_stock_st', if_exists, index=False)



