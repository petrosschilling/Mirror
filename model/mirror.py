import hashlib
from inspect import signature

from db.dba import *


class Mirror:

    ENCODING = "cp1252"

    buckets = {}
    buckets_diff = {}

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

    def run_diff(self):
        self._load_db_data()
        self._sort_data()
        self._isolate_diffs()
        print(str(self.buckets_diff))
        return self.buckets_diff

    def _load_db_data(self):
        self.data1 = self.__load_data(self.dbconf1, self.table_name1)
        self.data2 = self.__load_data(self.dbconf2, self.table_name2)

    def _sort_data(self):
        for rec in self.data1:
            sha = hashlib.sha256()
            for link in self.links:
                if link.ignore:
                    continue
                modifiedval = link.func1(rec[link.col1])
                sha.update(self._encodestr(modifiedval))

            rec['hash'] = sha.hexdigest()
            self._bucketadd(rec, 'data1')

        for rec in self.data2:
            sha = hashlib.sha256()
            for link in self.links:
                if link.ignore:
                    continue
                modifiedval = link.func2(rec[link.col2])
                sha.update(self._encodestr(modifiedval))

            rec['hash'] = sha.hexdigest()
            self._bucketadd(rec, 'data2')

    def _isolate_diffs(self):
        id_link = self._get_id_link()

        for key in self.buckets.keys():
            data1_len = len(self.buckets[key]['data1'])
            data2_len = len(self.buckets[key]['data2'])

            if not data1_len == data2_len:
                self.buckets_diff[key] = self.buckets[key]

                if data1_len > data2_len:
                    message = self._create_message(
                        self.table_name1,
                        self.buckets_diff[key]['data1'][0][id_link.col1])
                    self.buckets_diff[key]['message'] = message
                else:
                    message = self._create_message(
                        self.table_name2,
                        self.buckets_diff[key]['data2'][0][id_link.col2])
                    self.buckets_diff[key]['message'] = message

    def _create_message(self, table_name, id_value):
        msg_nomatch = "Table: %s -> Record ID: %s -> Match Not found"
        return msg_nomatch % (self.table_name2, id_value)

    def _get_id_link(self):
        for link in self.links:
            if link.isid:
                return link
        return None

    def _encodestr(self, val):
        return str(val).encode(self.ENCODING)

    def _bucketadd(self, item, pos):
        if item['hash'] not in self.buckets:
            self.buckets[item['hash']] = self._bucket()

        self.buckets[item['hash']][pos].append(item)

    def _bucket(self):
        return {"message": "", 'data1': [], 'data2': []}


class FieldLink:

    def __init__(
        self, col1, col2, func1=None, func2=None, isfilter=False,
        filter_val="", ignore=False, isid=False
    ):
        self.col1 = col1
        self.col2 = col2
        self.isfilter = isfilter
        self.filter_val = filter_val
        self.ignore = ignore
        self.isid = isid
        self.func1 = self.__validate_func(func1)
        self.func2 = self.__validate_func(func2)

    def __validate_func(self, f):
        if f is None:
            f = self.__default_function
        if not callable(f):
            raise TypeError("func must be a function e.g. foo(bar): pass")
        return f

    def __default_function(self, a):
        """Just a default function to be called in case there is no
        implementation None is passed as argument

        Arguments:
            a {String} -- a string

        Returns:
            String -- a string
        """

        return a
