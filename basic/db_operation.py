import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DBOperation(object):
    def __init__(self, db, user, pasw, host='localhost'):
        self.db = db
        self.user = user
        self.pasw = pasw
        self.host = host
        self.open_conn()

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, val):
        self._conn = val

    def open_conn(self):
        connect_url = 'mysql+pymysql://' + self.user + ':' + self.pasw + '@' + self.host + ':3306/' + self.db
        self._conn = create_engine(connect_url, echo=True)

    def conn_operate_core(self, operate_func):
        with self._conn.connect() as conn:
            result = operate_func(conn)
            return result

    def conn_operate_orm(self, operate_func):
        with Session(self._conn) as session:
            return operate_func(session)

    def close_conn(self):
        self._conn.dispose()

    def to_sql(self, df, table, index=True):
        with self._conn.connect() as conn:
            df.to_sql(name=table, con=conn, if_exists="append", index=index)

    def read_sql(self, sql):
        with self._conn.connect() as conn:
            return pd.read_sql(sql, self._conn)