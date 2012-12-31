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
        cur = self.conn.cursor()
        cur.execute("SHOW DATABASES")
        r = cur.fetchall()
        cur.close()
        return [i[0] for i in r]

    def get_tables(self, database=None):
        """ Return a list of table names in current or given database. """
        cur = self.conn.cursor()
        if database != None:
            cur.execute("SHOW TABLES FROM `%s`" % database)
        else:
            cur.execute("SHOW TABLES")
        r = cur.fetchall()
        cur.close()
        return [i[0] for i in r]

    def escape(self, obj):
        """ Escape an object for use in an SQL query. """
        return self.conn.escape(obj)
    
    def select_database(self, database):
        """ Select a database schema. """
        cur = self.conn.cursor()
        cur.execute("USE `%s`" % database)
        cur.close()

    def __del__(self):
        """ Destructor, close connection. """
        self.conn.close()

def main():
    """ Print a list of database names for a quick sanity test. """
    db = DB()
    print db.get_databases()

if __name__ == '__main__':
    main()
