import re
# https://c-bata.link/webframework-in-python/


def application(env,start_response):
    path=env["PATH_INFO"]
    if path=="/":
        start_response("200 OK",[("Content-Type", "text/plain; charset=utf-8")])
        return [b"Hello, world!"]

    elif path=="/foo":
        start_response("200 OK",[("Content-Type", "text/plain; charset=utf-8")])
        return [b"foo"]

class Router:
    def __init__(self):
        self.routes = []

    def add(self,method,path,callback):
        self.routes.append({
            "method":method,
            "path":path,
            "path_compiled":re.compile(path),
            "callback":callback
        })
    def match(self,method,path):
        error_callback=http404
        for r in self.routes:
            matched=re.compile(r["path"]).match(path)
            if not matched:
                continue
            error_callback=http405
            url_vars=matched.groupdict()
            if r["method"]==method:
                return r["callback"], url_vars
        return error_callback,{}


def http404(env,start_response):
    start_response("404 Not Found",[("Content-Type", "text/plain; charset=utf-8")])
    return [b"404 Not Found"]
    
    
def http405(env,start_response):
    start_response("405 Method Not Allowed",[("Content-Type", "text/plain; charset=utf-8")])
    return [b"405 Method Not Allowed"]

class App:
    def __init__(self):
        self.router = Router()
        
    def route(self,path=None,method="GET",callback=None):
        def decorator(func):
            self.router.add(method,path,func)
            return func
        return decorator(callback) if callback else decorator
    def __call__(self,env,start_response):
        method=env["REQUEST_METHOD"].upper()
        path=env["PATH_INFO"] or "/"
        callback,kwargs = self.router.match(method,path)
        return callback(env,start_response,**kwargs)
    
app = App()


@app.route('^/$', 'GET')
def hello(request, start_response):
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'Hello World']


@app.route('^/user/$', 'POST')
def create_user(request, start_response):
    start_response('201 Created', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'User Created']


@app.route('^/user/(?P<name>\w+)/$', 'GET')
def user_detail(request, start_response, name):
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    body = 'Hello {name}'.format(name=name)
    return [body.encode('utf-8')]


@app.route('^/user/(?P<name>\w+)/follow/$', 'POST')
def create_user(request, start_response, name):
    start_response('201 Created', [('Content-type', 'text/plain; charset=utf-8')])
    body = 'Followed {name}'.format(name=name)
    return [body.encode('utf-8')]

