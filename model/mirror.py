import hashlib

from db.dba import *


class Mirror:

    ENCODING = "cp1252"
    buckets = {}

    def __init__(self, dbconf1, dbconf2, table_name1, table_name2, links):
        """
        Initializes the configuration for checking the data

        Arguments:
            dbconf1 {DBConfiguration} -- Configuration for connection
            to the database of table 1
            dbconf2 {DBConfiguration} -- Configuration for connection
            to the database of table 1
            links {FieldLink[]} -- Array containing the mapping of
            columns from t1 and t2
        """
        self.dbconf1 = dbconf1
        self.dbconf2 = dbconf2
        self.table_name1 = table_name1
        self.table_name2 = table_name2
        self.links = links

    def __load_data(self, dbconf, table_name):
        sql = """
            SELECT *
            FROM %s;
        """ % table_name

        dba = DBA(dbconf)

        return dba.dict(sql, [])

    def load_db_data(self):
        self.data1 = self.__load_data(self.dbconf1, self.table_name1)
        self.data2 = self.__load_data(self.dbconf2, self.table_name2)

    def sort_data(self):

        for rec in self.data1:
            sha = hashlib.sha256()
            for link in self.links:
                sha.update(self.encodestr(rec[link.f1]))

            rec['hash'] = sha.hexdigest()
            self.bucketadd(rec, 'data1')

        for rec in self.data2:
            sha = hashlib.sha256()
            for link in self.links:
                sha.update(self.encodestr(rec[link.f2]))

            rec['hash'] = sha.hexdigest()
            self.bucketadd(rec, 'data2')

        print(str(self.buckets))

    def encodestr(self, val):
        return str(val).encode(self.ENCODING)

    def bucketadd(self, item, pos):
        if item['hash'] not in self.buckets:
            self.buckets[item['hash']] = self.bucket()

        self.buckets[item['hash']][pos].append(item)

    def bucket(self):
        return {'data1': [], 'data2': []}


class FieldLink:

    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    # TODO receive a function that stablishes rules for the mapping
    # of one field to another


