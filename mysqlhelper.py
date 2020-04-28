import pymysql
class MysqlHelper(object):
    # 需要有mysql的链接
    # 还需要有游标（cursor）
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', port = 3306,
                                    user = 'root', passwd = '123456',
                                    db = 'py18', charset = 'utf8mb4')
        self.cursor = self.conn.cursor()

    def execute_modify_sql(self, sql, data):
        self.cursor.execute(sql, data)
        self.conn.commit()
    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    helper = MysqlHelper()
    insert_sql = 'INSERT INTO weibo_test(weibo_text) VALUES(%s)'
    # INSERT INTO dianfei_test(name, feiyong) VALUES('hello',50);
    data = ('你好',)    # 加了
    print(type(data))
    helper.execute_modify_sql(insert_sql, data)
    helper.cursor.execute('select * from weibo_test')
    C = helper.cursor.fetchone()
    print(C)