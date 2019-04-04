import mysql.connector as mariadb


class DBA:

    def __init__(self, dbconfig):
        self.dbconfig = dbconfig

    def connect(self):
        mariadb_connection = mariadb.connect(
            host=self.dbconfig.host,
            user=self.dbconfig.usr,
            password=self.dbconfig.pwd,
            database=self.dbconfig.databse)

        return mariadb_connection

    def dict(self, query, params):
        con = self.connect()
        cur = con.cursor()

        result = cur.execute(query, params)
        columns = [col[0] for col in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        con.close()

        return rows


class DBConfiguration:

    def __init__(self, usr="", pwd="", host="", database=""):
        self.usr = usr
        self.pwd = pwd
        self.host = host
        self.databse = database
