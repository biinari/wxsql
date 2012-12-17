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

    def getTables(self, db_name=None):
        cur = self.conn.cursor()
        if db_name != None:
            cur.execute("SHOW TABLES FROM `%s`" % db_name)
        else:
            cur.execute("SHOW TABLES")
        r = cur.fetchall()
        cur.close()
        return [i[0] for i in r]

    def escape(self, obj):
        return self.conn.escape(obj)

    def __del__(self):
        self.conn.close()

def main():
    db = DB()
    print db.getDatabases()

if __name__ == '__main__':
    main()
