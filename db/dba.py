import mysql.connector as mariadb
from mysql.connector.errors import InterfaceError


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

        def testconnection():
            success = True
            try:
                con = self.connect()
            except InterfaceError as ex:
                print("Failed to connect to database" + str(ex))
                sucess = False
            else:
                con.close()
            finally:
                return success


class DBConfiguration:

    def __init__(self, usr="", pwd="", host="", database=""):
        self.usr = usr
        self.pwd = pwd
        self.host = host
        self.databse = database
