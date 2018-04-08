# encoding:utf-8

"""
Base handler
"""

import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie('username')
        return user

    def get_authenticated(self):
        """
        认证
        :return:
        """
        if not self.get_current_user():
            self.redirect('/login')
            return