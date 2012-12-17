import pymysql

class DB(object):
    """ Database Connection """
    conn = None

    def __init__(self):
        self.connect(host='localhost', port=3306, user='root', passwd='')

    def connect(self, *args, **kwargs):
        self.conn = pymysql.connect(*args, **kwargs)

    def getDatabases(self):
        cur = self.conn.cursor()
        cur.execute("SHOW DATABASES")
        r = cur.fetchall()
        cur.close()
        return [i[0] for i in r]

    def getTables(self, database=None):
        cur = self.conn.cursor()
        if database != None:
            cur.execute("SHOW TABLES FROM `%s`" % database)
        else:
            cur.execute("SHOW TABLES")
        r = cur.fetchall()
        cur.close()
        return [i[0] for i in r]

    def escape(self, obj):
        return self.conn.escape(obj)
    
    def selectDatabase(self, database):
        cur = self.conn.cursor()
        cur.execute("USE `%s`" % database)
        cur.close()

    def __del__(self):
        self.conn.close()

def main():
    db = DB()
    print db.getDatabases()

if __name__ == '__main__':
    main()
