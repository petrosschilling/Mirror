import mysql.connector as mariadb


class DBA:

    def __init__(self, dbconfig):
        self.con = self.create_connection(dbconfig)
        self.cursor = self.con.cursor()

    def create_connection(self, dbconfig):
        mariadb_connection = mariadb.connect(
            host=dbconfig.host,
            user=dbconfig.usr,
            password=dbconfig.pwd,
            database=dbconfig.databse)

        return mariadb_connection

    def dict(self, query, params):
        result = self.cursor.execute(query, params)
        columns = [col[0] for col in self.cursor.description]
        rows = [dict(zip(columns, row)) for row in self.cursor.fetchall()]

        return rows


class DBConfiguration:

    def __init__(self, usr="", pwd="", host="", database=""):
        self.usr = usr
        self.pwd = pwd
        self.host = host
        self.databse = database
