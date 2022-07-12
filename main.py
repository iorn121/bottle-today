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
            "callback":callback
        })
    def match(self,method,path):
        for r in self.routes:
            matched=re.compile(r["path"]).match(path)
            if matched and r["method"]==method:
                url_vars=matched.groupdict()
                return r["callback"], url_vars
        return http404,{}

import re

def http404(env,start_response):
    start_response("200 OK",[("Content-Type", "text/plain; charset=utf-8")])
    return [b"404 Not Found"]
    