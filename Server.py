import socketio
import eventlet
import eventlet.wsgi
import matlab.engine
from sympy import *
import numpy as np
import random
from json import JSONEncoder
import json
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

# answer = py.eval()

# @app.route('/')
# def index():
#     """Serve the client-side application."""
#     return render_template('index.html')
DQuestions = []
IQuestions = []
# class DQuestions(object):
#     correct = JSONEncoder().encode({
#         "q" : "",
#         "a" : ""
#     })
#     false1 = ""
#     false2 = ""
#     false3 = ""
def generateIntegralQuestion():
    # eng = matlab.engine.start_matlab()
    eng1 = matlab.engine.connect_matlab('love')
    IQuestions = []
    IQuestions = ['f = sqrt(x) - (1/(sqrt(x)));' , 'f = sqrt(x)*(x^2+1);' , 'f = 1/(7*x);' , 'f = (5*x^2)-(5*sqrt(x)-(3/x));', 'f = (3*x-2)*(2*x+1);', 'f = (5*x*sqrt(x))/2 + (1/2*sqrt(x));', 'f = 2/sqrt(x) + sqrt(x)/2' , 'f = -7/(1-x^3)', 'f = 12*x^2-6*x+2' , 'f = 2*x/3 + (6/x^3)' , 'f = sqrt(x) - 1/sqrt(x)']
    # result = {}
    # question = DQuestions()
    # for counter in range(0, 4):
    counter = random.randrange(0,9);
    # print(counter)
    eng1.eval("syms x;",nargout=0);
    eng1.eval(IQuestions[counter],nargout=0);
    ans = eng1.eval('char(diff(f))',nargout=1)
    ans1 = eng1.eval('char(-diff(f))',nargout=1)
    ans2 = eng1.eval('char(diff(f)+1)',nargout=1)
    ans3 = eng1.eval('char(diff(f)*1/2)',nargout=1)
    IQuestions.append(IQuestions[counter])
    IQuestions.append(ans)
    IQuestions.append(ans1)
    IQuestions.append(ans2)
    IQuestions.append(ans3)
        # a = eng1.eval('sqrt(5)')
        # print(a)
        # res
        # print(ans)
    eng1.quit()


    return IQuestions



def generateDerivativeQuestion():
    # eng = matlab.engine.start_matlab()
    eng1 = matlab.engine.connect_matlab('love')
    DQuestions = []
    question = ['y = sqrt(x) - (1/(sqrt(x)));' , 'y = sqrt(x)*(x^2+1);' , 'y = 1/(7*x);' , 'y = (5*x^2)-(5*sqrt(x)-(3/x));', 'y = (3*x-2)*(2*x+1);', 'y = (5*x*sqrt(x))/2 + (1/2*sqrt(x));', 'y = 2/sqrt(x) + sqrt(x)/2' , 'y = -7/(1-x^3)', 'y = 12*x^2-6*x+2' , 'y = 2*x/3 + (6/x^3)' , 'y = sqrt(x) - 1/sqrt(x)']
    # result = {}
    # question = DQuestions()
    # for counter in range(0, 4):
    counter = random.randrange(0,9);
    # print(counter)
    eng1.eval("syms x;",nargout=0);
    eng1.eval(question[counter],nargout=0);
    ans = eng1.eval('char(diff(y))',nargout=1)
    ans1 = eng1.eval('char(-diff(y))',nargout=1)
    ans2 = eng1.eval('char(diff(y)+1)',nargout=1)
    ans3 = eng1.eval('char(diff(y)*1/2)',nargout=1)
    DQuestions.append(question[counter])
    DQuestions.append(ans)
    DQuestions.append(ans1)
    DQuestions.append(ans2)
    DQuestions.append(ans3)
        # a = eng1.eval('sqrt(5)')
        # print(a)
        # res
        # print(ans)
    eng1.quit()


    return DQuestions



print('question is ', generateDerivativeQuestion())

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)


# @sio.on('clientQ', namespace='/')
# def connect(sid, environ):
#     print(sid)
#     print(environ)
    # sio.emit('reply', generateDerivativeQuestion())

@sio.on('questions', namespace='/')
def connect(sid, environ):
    # print('here')
    temp = generateDerivativeQuestion()
    print(temp)
    sio.emit('reply', temp)

    # print("connect ", sid)
    # print("environ ", environ);
    # print environ[0]

# @sio.on('chat message', namespace='/chat')
# def message(sid, data):
#     print("message ", data)
#     sio.emit('reply', room=sid)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
