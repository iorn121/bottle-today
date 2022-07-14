import re
import json
from urllib.parse import parse_qs,urljoin
import cgi
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
        request=Request(env)
        callback,kwargs = self.router.match(request.method,request.path)
        return callback(request,start_response,**kwargs)
    
    
    
class Request:
    def __init__(self,environ,charset="utf-8"):
        self.environ = environ
        self._body=None
        self.charset=charset

    @property
    def path(self):
        return self.environ["PATH_INFO"] or "/"
    
    @property
    def method(self):
        return self.environ["REQUEST_METHOD"].upper()
    
    @property
    def forms(self):
        form=cgi.FieldStorage(
            fp=self.environ["wsgi.input"],
            environ=self.environ,
            keep_blank_values=True,
        )
        params={k: form[k].value for k in form}
        return params

    @property
    def query(self):
        return parse_qs(self.environ["QUERY_STRING"])

    @property
    def body(self):
        if self.body is None:
            content_length = int(self.environ["CONTENT_LENGTH"],0)
            self._body=self.environ["wsgi.input"].read(content_length)
        return self._body
    
    @property
    def text(self):
        return self._body.decode(self.charset)
    
    @property
    def json(self):
        return json.loads(self._body)