from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, Float

Base = declarative_base()


class Dim_type_industry(Base):
    __tablename__ = 'dim_type_industry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_parent = Column(String(50))
    industry_type = Column(String(50))
    industry_parent_name = Column(String(50))


class Fact_industry(Base):
    __tablename__ = 'fact_industry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_parent = Column(String(50), ForeignKey('dim_type_industry.industry_parent'))
    industry = Column(String(50))
    industry_name = Column(String(50))
    industry_active_date = Column(DateTime)
    fetching_date = Column(DateTime)


class Fact_industry_stocks(Base):
    __tablename__ = 'fact_industry_stocks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_parent = Column(String(50), ForeignKey('dim_type_industry.industry_parent'))
    industry = Column(String(50), ForeignKey('fact_industry.industry'))
    stock = Column(String(50), ForeignKey('fact_securities.security'))
    fetching_date = Column(DateTime)


def initial_industries(engine):
    Base.metadata.create_all(engine)
