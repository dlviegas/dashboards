import mysql.connector
import pandas as pd
from decouple import config

class MySQLConnector:

    def __init__(self):
        self.__mysql_host = config('RDS_HOST')
        self.__mysql_port = config('RDS_PORT')
        self.__mysql_user = config('RDS_USER')
        self.__mysql_pwd = config('RDS_PWD')
        self.__mysql_db = config('RDS_DB')

    def __open_con(self):
        self.__con = mysql.connector.connect(user=self.__mysql_user, password=self.__mysql_pwd,
                                             host=self.__mysql_host, database=self.__mysql_db
                                             )

    def __close_con(self):
        if self.__con:
            self.__con.close()

    def insert_dataframe(self, table, df):

        if not self.check_table(table):
            self.create_table(table, df)
        self.__open_con()
        cursor = self.__con.cursor()
        values = [f'%({x})s' for x in df.columns]

        add_df = (f"INSERT INTO {table} "
                  f"({', '.join(list(df.columns))}) "
                  f"VALUES ({', '.join(values)})")
        if df.shape[0] > 10000:
            limit = 10000
            j = 10000
            i = 0

            while i < df.shape[0]:
                df_insert = df.loc[i:min(i+9999, df.shape[0])].fillna('null').to_dict(orient='records')
                cursor.executemany(add_df, df_insert)
                i += limit
            pass
        else:
            cursor.executemany(add_df, df.fillna('null').to_dict(orient='records'))

        self.__con.commit()
        cursor.close()
        self.__close_con()

    def select_table(self, query, dataframe=False):
        self.__open_con()
        cursor = self.__con.cursor()
        cursor.execute(query)
        result = list(cursor)

        cursor.close()
        self.__close_con()

        if dataframe:
            col_names = [x[0] for x in cursor.description]
            result = pd.DataFrame(result, columns=col_names)

        return result

    def check_table(self, table_name):
        schema, table = table_name.split('.')
        query = f"""SELECT * 
FROM information_schema.tables
WHERE table_schema = '{schema}' 
    AND table_name = '{table}'
LIMIT 1;"""

        result = self.select_table(query, dataframe=False)

        return bool(result)

    def create_table(self, table_name, df):
        self.__open_con()
        cursor = self.__con.cursor()

        cols = [f'{x} {MySQLConnector.dtype_mapping()[str(y)]}' for x, y in zip(df.columns, df.dtypes)]

        query = f"""
        CREATE TABLE {table_name} (
            {', '.join(cols)}
        );
        """

        cursor.execute(query)

        self.__con.commit()
        cursor.close()
        self.__close_con()

    @classmethod
    def dtype_mapping(cls):
        return {'object': 'TEXT',
                'int64': 'INT',
                'int32': 'SMALLINT',
                'float64': 'FLOAT',
                'datetime64': 'DATETIME',
                'bool': 'TINYINT',
                'category': 'TEXT',
                'timedelta[ns]': 'TEXT',
                'datetime64[ns]': 'TEXT',
                'list': 'TEXT'}

