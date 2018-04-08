# encoding:utf-8

"""
login handler
"""

from models.check_login import CheckLogin
from base_handler import BaseHandler

class LoginHandler(BaseHandler):
    """首页控制"""

    def get(self):

        self.render(
                'login.html',
                flag=0
        )

    def post(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        if CheckLogin().check_login(username, password) == 1:
            self.set_secure_cookie('username',username)
            self.redirect('/')
            return 
        else:
            self.render(
                'login.html',
                flag=1
                )
            
        