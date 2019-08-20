#!/usr/bin/env python
# coding: utf8
import pymysql

class MysqlPython(object):

    _instance   = None
    _host       = None
    _user       = None
    _password   = None
    _database   = None
    _session    = None
    _connection = None
    _charset = None

    def __init__(self, host='ip', user='lion', password='pass', database='dbname', charset='utf8'):
        self._host     = host
        self._user     = user
        self._password = password
        self._database = database
        self._charset = charset


    def open(self):
        try:
            cnx = pymysql.connect(self._host, self._user, self._password, self._database, charset=self._charset)
            self._connection = cnx
            self._session    = cnx.cursor()
        except pymysql.Error as e:
            print("Error %d: %s" % (e.args[0],e.args[1]))

    def close_connect(self):
        self._session.close()
        self._connection.close()


    def update(self, table, where=None, **kwargs):
        query  = "UPDATE %s SET " % table
        keys   = kwargs.keys()
        values = tuple(kwargs.values())
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
        query += " WHERE %s" % where

        self._session.execute(query, values)
        self._connection.commit()

        update_rows = self._session.rowcount

        return update_rows


    def select(self, table, where=None, *args):
        query = 'SELECT '
        keys = args
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        # self.__open()
        self._session.execute(query)

        number_rows = self._session.rowcount
        number_columns = len(self._session.description)

        try:
            result = [item for item in self._session.fetchone()]
            result = dict(zip(args, result))
        except:
            result = []

        # self.__close()

        return result


    def select_all(self, table, where=None, *args):
        result = []
        query = 'SELECT '
        keys = args
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        print(query)
        print(type(query))
        self._session.execute(query)


        all_rows = self._session.rowcount
        try:
            row = [item for item in self._session.fetchall()]
            for res in row:
                result.append(dict(zip(args, res)))
        except:
            result = []


        print('number_rows: %s' % all_rows)
        return result


    def select_all_for_count_row(self, table, where=None, *args):
        result = []
        query = 'SELECT '
        keys = args
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`" + key + "`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        print(query)
        print(type(query))
        self._session.execute(query)


        all_rows = self._session.rowcount
        try:
            row = [item for item in self._session.fetchall()]
            for res in row:
                result.append(dict(zip(args, res)))
        except:
            result = []


        print('number_rows: %s' % all_rows)
        return all_rows

    def insert(self, table, **kwargs):
        print(kwargs)
        query = "INSERT INTO %s " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values())
        query += "(" + ",".join(["`%s`"] * len(keys)) %  tuple (keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"

        self._session.execute(query, values)
        self._connection.commit()
        return self._session.lastrowid


    def delete(self, table, where):
        query = "DELETE FROM %s WHERE %s" % (table, where)
        self._session.execute(query)
        self._connection.commit()
        return self._session.lastrowid


connect_mysql = MysqlPython('ip', 'username', 'pass', 'dbname', charset='utf8')
connect_mysql.open()