from flask import Flask, escape, request
from flask_socketio import SocketIO, emit
from threading import Thread, Lock
from gpiozero import Button
import time

app = Flask(__name__)
socketio = SocketIO(app)
lock = Lock()
num = 0
lap_lock = Lock()
laps = []

btn = Button(2)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/style.css')
def style():
    return app.send_static_file('style.css')

@app.route('/script.js')
def script():
    return app.send_static_file('script.js')

@app.route('/current')
def current():
    lock.acquire()
    out = str(num)
    lock.release()
    return out

@socketio.on('reset')
def reset():
    global num
    lock.acquire()
    num = 0
    socketio.emit('num', {'num': num}, broadcast = True)
    lock.release()

@socketio.on('connect')
def connect():
    socketio.emit('data', {'num': num, 'laps': laps})

@socketio.on('lap')
def lap():
    print('lap')
    global laps
    global num
    lap_lock.acquire()
    laps.append({'num': num})
    lap_lock.release()
    lock.acquire()
    num = 0
    socketio.emit('data', {'num': num, 'laps': laps}, broadcast = True)
    lock.release()

@socketio.on('clear')
def clear():
    global laps, num
    lap_lock.acquire()
    laps = []
    lap_lock.release()
    lock.acquire()
    num = 0
    socketio.emit('data', {'num': num, 'laps': laps}, broadcast = True)
    lock.release()

def count():
    state = btn.value
    while True:
        if(btn.value == 1 or btn.value == state):
            state = btn.value
            continue
        state = btn.value
        print('yo')
        global num
        lock.acquire()
        num += 1
        lock.release()
        socketio.emit('num', {'num': num}, broadcast = True)
        time.sleep(0.01)

if __name__ == '__main__':
    socketio.run(app)

t = Thread(target = count)
t.start()
