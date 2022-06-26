from bottle import Bottle,route,run

app=Bottle()

@app.route('/hello')
def hello():
    return 'Hello world'

run(app,host='localhost',port=8080,debug=True)