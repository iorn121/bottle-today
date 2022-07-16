from glass import App,Response
app = App()


@app.route('^/$', 'GET')
def hello(request):
    return Response("Hello, world!")


@app.route('^/user/$', 'POST')
def create_user(request):
    return Response("User created")

@app.route('^/user/(?P<name>\w+)/$', 'GET')
def user_detail(request, name):
    return Response(f"Hello {name}")
# @app.route('^/user/(?P<name>\w+)/follow/$', 'POST')
# def create_user(request, start_response, name):
#     start_response('201 Created', [('Content-type', 'text/plain; charset=utf-8')])
#     body = 'Followed {name}'.format(name=name)
#     return [body.encode('utf-8')]

