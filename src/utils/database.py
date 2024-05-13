import pymysql  # type: ignore

def create_database(host, port, user, password, database: str):
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        connection.commit()
        print(f"Database '{database}' initialized")
    finally:
        connection.close()


class HexbotDB:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        create_database(host, port, user, password, self.database)

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def create_table(self, table: str, **kwargs):
        columns = ', '.join([f"{column_name} {column_type}" for column_name, column_type in kwargs.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table} (id INT AUTO_INCREMENT PRIMARY KEY, {columns});"
        self.execute_query(query)
    
    def write_row(self, table: str, **kwargs):
        columns = ', '.join(kwargs.keys())
        values = ', '.join([f"'{value}'" for value in kwargs.values()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values});"
        self.execute_query(query)
    
    def update_row(self, table: str, col: str, data, **kwargs):
        set_values = ', '.join([f"{key} = '{value}'" for key, value in kwargs.items()])
        query = f"UPDATE {table} SET {set_values} WHERE {col}='{data}';"
        self.execute_query(query)

    def read_row(self, table: str, **kwargs):
        where_conditions = " AND ".join([f"{key}='{value}'" for key, value in kwargs.items()])
        query = f"SELECT * FROM {table} WHERE {where_conditions};"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchone()
            return data
        
    def row_exists(self, table: str, **kwargs):
        where_conditions = " AND ".join([f"{key}='{value}'" for key, value in kwargs.items()])
        query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {where_conditions});"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return bool(list(result.values())[0])
    
    def remove_row(self, table: str, **kwargs):
        where_conditions = " AND ".join([f"{key}='{value}'" for key, value in kwargs.items()])
        query = f"DELETE FROM {table} WHERE {where_conditions};"
        self.execute_query(query)
    
    def clear_table(self, table: str):
        query = f"TRUNCATE TABLE {table}"
        self.execute_query(query)
    
    def get_rows(self, table: str, **kwargs):
        where_conditions = " AND ".join([f"{key} = '{value}'" for key, value in kwargs.items()]) if kwargs else ""
        query = f"SELECT * FROM {table} WHERE {where_conditions};"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return data
