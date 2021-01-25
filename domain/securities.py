# 1.4导入方式
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, Float

Base = declarative_base()


class Fact_securities(Base):
    __tablename__ = 'fact_securities'
    security = Column(String(50), primary_key=True)
    display_name = Column(String(50))
    name = Column(String(50))
    fetching_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    type = Column(String(50))
    # 标明标的是否可融资
    margincash_stocks = Column(Boolean, default=False)
    margincash_stocks_date = Column(DateTime)
    # 标明标的是否可融券
    marginsec_stocks = Column(Boolean, default=False)
    # 可融券标的日期
    marginsec_stocks_date = Column(DateTime)
    children = relationship("Fact_index_stock", cascade="all, delete")


class Fact_index_stock(Base):
    __tablename__ = 'fact_index_stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security = Column(String(50), ForeignKey('fact_securities.security'))
    child_stock = Column(String(50))
    effective_date = Column(DateTime)


# 股票ST
class Fact_stock_st(Base):
    __tablename__ = 'fact_stock_st'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security = Column(String(50), ForeignKey('fact_securities.security'))
    security_date = Column(DateTime)
    is_st = Column(Boolean, default=False)


# 基金净值
class Fact_fund_net_value_day(Base):
    __tablename__ = 'fact_fund_net_value_day'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security = Column(String(50), ForeignKey('fact_securities.security'))
    security_date = Column(DateTime)
    acc_net_value = Column(Float)
    unit_net_value = Column(Float)
    adj_net_value = Column(Float)


# 期货净值
class Fact_futures_day(Base):
    __tablename__ = 'fact_futures_day'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security = Column(String(50), ForeignKey('fact_securities.security'))
    security_date = Column(DateTime)
    futures_sett_price = Column(Float)
    futures_positions = Column(Float)


class Dim_type_securities(Base):
    __tablename__ = 'dim_type_securities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security_type = Column(String(50))
    security_cn = Column(String(50))
    in_securities = Column(Boolean, default=False)
    is_fund = Column(Boolean, default=False)
    is_futures = Column(Boolean, default=False)


def initial(engine):
    Base.metadata.drop_all(engine, tables=[Fact_securities.__table__,
                                           Fact_index_stock.__table__, Fact_stock_st.__table__,
                                           Fact_fund_net_value_day.__table__, Fact_futures_day.__table__])
    Base.metadata.create_all(engine)
