import pymysql

class DB(object):
    """ MySQL Database abstraction """

    conn = None
    """ Database Connection """

    def __init__(self):
        """ Connect to database with default settings. """
        # TODO: Get settings from a named stanza in config
        self.connect(host='localhost', port=3306, user='root', passwd='')

    def connect(self, *args, **kwargs):
        """ Obtain a connection to the database. """
        self.conn = pymysql.connect(*args, **kwargs)

    def get_databases(self):
        """ Return a list of database schema names. """
        result = self.query("SHOW DATABASES")
        return [i[0] for i in result]

    def _get_tables(self, table_type, database=None):
        if database != None:
            from_db = ' FROM `%s`' % database
        else:
            from_db = ''
        result = self.query("SHOW FULL TABLES{} WHERE Table_type='{}'".format(
            from_db, table_type))
        return [i[0] for i in result]

    def get_tables(self, database=None):
        """ Return a list of table names in current or given database. """
        return self._get_tables('BASE TABLE', database)

    def get_views(self, database=None):
        """ Return a list of view names in current or given database. """
        return self._get_tables('VIEW', database)

    def get_columns(self, database=None, table=None):
        """ Return a list of column names in given table. """
        if database != None:
            from_table = "`%s`.`%s`" % (database, table)
        else:
            from_table = "`%s`" % table
        result = self.query("SHOW COLUMNS FROM {}".format(from_table))
        return [i[0] for i in result]
    
    def get_indexes(self, database=None, table=None):
        """ Return a list of index names in given table. """
        if database != None:
            from_table = "`%s`.`%s`" % (database, table)
        else:
            from_table = "`%s`" % table
        result = self.query("SHOW INDEXES FROM {}".format(from_table))
        return [i[0] for i in result]

    def escape(self, obj):
        """ Escape an object for use in an SQL query. """
        return self.conn.escape(obj)

    def select_database(self, database):
        """ Select a database schema. """
        self.execute("USE `%s`" % database)

    def execute(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        cursor.close()

    def query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def __del__(self):
        """ Destructor, close connection. """
        self.conn.close()

def main():
    """ Print a list of database names for a quick sanity test. """
    db = DB()
    print db.get_databases()

if __name__ == '__main__':
    main()
