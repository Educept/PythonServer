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
AQuestions = []
# class DQuestions(object):
#     correct = JSONEncoder().encode({
#         "q" : "",
#         "a" : ""
#     })
#     false1 = ""
#     false2 = ""
#     false3 = ""
def generateAlgebraQuestion():
    eng1 = matlab.engine.connect_matlab('love')
    AQuestions = []
    question = ['sqrt(32*x^3)*sqrt(2*x^3);' , 'sqrt(32*x^5)*sqrt(2*x^3);' , '(-2*x-3)*(-4*x^2+3*x+7);' , 'x+6-(9*3);', 'x*(7+12)-12/2;', '(x/7)*(x/5+9);', 'x-5+9*(3/4)+6*2' , 'x+9-5/4', '9*3-6+6*x' , 'x/7+6*x-9+2' , '5*x+(x/7)-2']
    counter = random.randrange(0,9);
    eng1.eval("syms x;",nargout=0);
    eng1.workspace['y'] = question[counter];
    ans = eng1.eval('char(eval(y))',nargout=1);
    # print('ans ',ans)
    ans1 = eng1.eval('char(-eval(y))',nargout=1)
    ans2 = eng1.eval('char(eval(y)+1)',nargout=1)
    ans3 = eng1.eval('char(eval(y)*1/2)',nargout=1)
    AQuestions.append(question[counter])
    AQuestions.append(ans)
    AQuestions.append(ans1)
    AQuestions.append(ans2)
    AQuestions.append(ans3)
    eng1.quit()
    return AQuestions



def generateIntegralQuestion():
    eng1 = matlab.engine.connect_matlab('love')
    IQuestions = []
    question = ['sqrt(x) - (1/(sqrt(x)));' , 'sqrt(x)*(x^2+1);' , 'sin(x)/(7*x);' , '(5*x^2)-(5*sqrt(x)-(3/x));', 'tan(3*x-2)*(2*x+1);', '(5*x*sqrt(x))/2 + (1/2*sqrt(x));', '2*cos(x)/sqrt(x) + sqrt(x)/2' , '-7*x^5/(1-x^3)', '12*x^2-6*x+2*sec(x)' , '2*x/(3*sin(x)) + (6/x^3)' , 'sqrt(x) - 1/sqrt(x)']
    # result = {}
    # question = DQuestions()
    # for counter in range(0, 4):
    counter = random.randrange(0,9);
    # print(counter)
    eng1.eval("syms x;",nargout=0);
    eng1.workspace['y'] = question[counter];
    ans = eng1.eval('char(int(y,x))',nargout=1);
    ans1 = eng1.eval('char(-int(y,x))',nargout=1)
    ans2 = eng1.eval('char(int(y,x)+1)',nargout=1)
    ans3 = eng1.eval('char(int(y,x)*1/2)',nargout=1)
    IQuestions.append(question[counter])
    IQuestions.append(ans)
    IQuestions.append(ans1)
    IQuestions.append(ans2)
    IQuestions.append(ans3)
    eng1.quit()
    return IQuestions

# print('Integral ', generateIntegralQuestion())

def generateDerivativeQuestion():
    # eng = matlab.engine.start_matlab()
    eng1 = matlab.engine.connect_matlab('love')
    DQuestions = []
    question = ['y = sqrt(x) - (1/(sqrt(x)));' , 'y = sqrt(x)*(x^2+1);' , 'y = 1/(7*x);' , 'y = (5*x^2)-(5*sqrt(x)-(3/x));', 'y = (sin(x))*(2*x+1);', 'y = (5*x*sqrt(x))/2 + (1/2*sqrt(x));', 'y = 2*cos(x)/sqrt(x) + sqrt(x)/2' , 'y = -7/(1-x^3)', 'y = 12*x^2-6*x+2' , 'y = 2*x^2/3 + (6/x^3)' , 'y = sqrt(x) - 1/sqrt(x)']
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



# print('question is ', generateDerivativeQuestion())

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
    # print(temp)
    sio.emit('reply', temp)

@sio.on('questions2', namespace='/')
def connect(sid, environ):
    # print('here')
    temp1 = generateIntegralQuestion()
    # print(temp1)
    sio.emit('reply2', temp1)
#
@sio.on('questions3', namespace='/')
def connect(sid, environ):
    # print('here')
    temp2 = generateAlgebraQuestion()
    # print(temp2)
    sio.emit('reply3', temp2)

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
