def c_fund_net_day(db_operation, df, if_exists='append'):
    db_operation.to_sql(df, 'fact_fund_net_value_day', if_exists, index=False)
