#!/usr/bin/python
# coding=utf-8
"""
系统服务器启动
"""

import tornado.web
import tornado.ioloop
import tornado.httpserver
from application import Application
from tornado.options import define, options

define("port", default=8808, help="run on the given port", type=int)

def main():

    options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer( Application() )
    http_server.listen(options.port)
    
    print "Development server is running at http://127.0.0.1:%s"%options.port
    print "Quit the server with control+c"

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    #python fig_server.py --port=8800
    main()