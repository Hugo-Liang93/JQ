# 1.4导入方式
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey

Base = declarative_base()


class Fact_securities(Base):
    __tablename__ = 'fact_securities'
    security = Column(String(50),primary_key=True)
    display_name = Column(String(50))
    name = Column(String(50))
    security_date = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    type = Column(String(50))
    # 标明标的是否可融券
    marginsec_stocks = Column(String(50))
    # 可融券标的日期
    marginsec_stocks_date = Column(DateTime)
    children = relationship("Fact_index_stock",cascade="all, delete")


class Fact_index_stock(Base):
    __tablename__ = 'fact_index_stock'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security = Column(String(50),ForeignKey('fact_securities.security'))
    child_stock = Column(String(50))
    effective_date = Column(DateTime)

class Dim_type_securities(Base):
    __tablename__ = 'dim_type_securities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    security_type = Column(String(50))
    security_cn = Column(String(50))
    in_securities_list = Column(String(50))




def initial(engine):
    Base.metadata.drop_all(engine, tables=[Fact_securities.__table__,Fact_index_stock.__table__])
    Base.metadata.create_all(engine)
