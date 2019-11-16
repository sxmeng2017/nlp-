"""
这里是一个简单的werkzeug的使用例子
当我们从run_simple开始回溯它的调用。会找到inner
之后就是make_server，再之后就是BaseWSGIServer
这个类使用了httpServer类。这就到底了。
所以这个例子的调用是
先利用httpServer类搭建一个服务器程序.将服务器初始化，保证用handle
建立的连接socket明确好有fd句柄。复写serve_forever方法。使用try,except
保证服务器在出问题的情况下可以正常关闭。有handle_error方法，控制错误信息输出
正常使用get_request方法获取消息。该方法不含其它特殊处理。

之后使用make_server进行调用，完成服务器创建功能。该方法存在的理由是，制作了不同类型
的WSGIServer类。都放在这个方法下进行选择。返回WSGIServer类

run_simple方法中的inner则帮助为不提供fd的make_server方法返回的结果提供一个开始服务的封装
让任务启动前会在日志文件中添加启动信息。然后启动服务器
其中还有use_reloader选项，可以不创建server，而是使用socker套接字去建立简单连接
保证port是可用的。

run_simple会启动serve_forever方法让http服务器启动。这也是该实例的最后结果



"""

import os

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

class Shortly(object):
    def dispatch_request(self, request):
        return Response('Hello Werkzeug')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ)

def create_app(with_static=True):
    app = Shortly()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app,{
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })

if __name__ == '__main__':
    app = create_app()
    run_simple('127.0.0.1', 6666, app, use_debugger=True, use_reloader=True)
