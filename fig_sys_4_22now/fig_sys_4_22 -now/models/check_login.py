# encoding:utf-8


from Base import Base

class CheckLogin(Base):
    def __init__(self):
        Base.__init__ (self)  # 执行父类

    def check_login(self, username, password):
        
        if len(username) == 0:
            return 0
        elif len(password) == 0:
            return 0

        sql = "SELECT password FROM login_users WHERE username = %s"
        result = self.mysql_db.query(sql, username)

        for value in result:
            if value.password == password:
                return 1
        else:
            return 0