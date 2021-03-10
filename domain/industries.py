from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean, Float
from domain.domain_base import Base


class Dim_type_industry(Base):
    __tablename__ = 'dim_type_industry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_parent = Column(String(50),index = True)
    industry_type = Column(String(50))
    industry_parent_name = Column(String(50))


class Dim_concepts(Base):
    __tablename__ = 'dim_concepts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    concepts_index = Column(String(50),index = True)
    concepts_name = Column(String(50))
    concepts_start_date = Column(DateTime)


class Fact_industry(Base):
    __tablename__ = 'fact_industry'
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_parent = Column(String(50), ForeignKey('dim_type_industry.industry_parent'))
    industry = Column(String(50),index = True)
    industry_name = Column(String(50))
    industry_active_date = Column(DateTime)
    fetching_date = Column(DateTime)


class Fact_industry_stocks(Base):
    __tablename__ = 'fact_industry_stocks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    industry_parent = Column(String(50), ForeignKey('dim_type_industry.industry_parent'))
    industry = Column(String(50), ForeignKey('fact_industry.industry'))
    # 不作foreign key 是因为板块下有些code在securities全表中找不到
    stock = Column(String(50))
    fetching_date = Column(DateTime)


class Fact_concept_stocks(Base):
    __tablename__ = 'fact_concept_stocks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    concepts_index = Column(String(50), ForeignKey('dim_concepts.concepts_index'))


def initial_industries(engine):
    Base.metadata.drop_all(engine, tables=[Dim_concepts.__table__])
    Base.metadata.create_all(engine)
