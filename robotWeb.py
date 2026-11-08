import time

import serial
from flask import render_template, Response
from flask import Flask
import cameraIpcTestModule
import cameraIPC
import logging

NO_ACTION = 0
FORWARD = 1
BACKWARDS = 2
LEFT = 3
RIGHT = 4
TURN_LEFT = 5
TURN_RIGHT = 6
BODY_UP = 7
BODY_DOWN = 8

#setup serial connection
ser = serial.Serial('/dev/serial0', 115200)
ser.write(NO_ACTION.to_bytes(1, 'big'))
ser.timeout = 0

#setup flask
app = Flask("robotWeb")
logging.getLogger('werkzeug').disabled = True

#setup cam
cameraIPC.initCamera()

#main page
@app.route('/')
def controlBot():
    return render_template("robotRequestHTML.html")

#movement commands -------------------------------------------------------

@app.route('/left')
def goLeft():
    return movement(LEFT)

@app.route('/forward')
def goForward():
    return movement(FORWARD)

@app.route('/back')
def goBackwards():
    return movement(BACKWARDS)

@app.route('/right')
def goRight():
    return movement(RIGHT)

@app.route('/turnLeft')
def turnLeft():
    return movement(TURN_LEFT)

@app.route('/turnRight')
def turnRight():
    return movement(TURN_RIGHT)

def movement(move):
    response = [b'', b'']
    response[0] = ser.read(1)
    if response[0] == b'K':
        response[0] = ser.read(1)
    print(response[0])
    response[1] = ser.read(1)
    print(response[1])
    if response[0] == b'O' and response[1] == b'K':
        print("OK")
        ser.write(move.to_bytes(1, 'big'))
        return "OK"
    else:
        print("BUSY")
        return "BUSY"


#get frame
@app.route('/nextframe')
def getNextFrame():

    frameData = cameraIPC.getCurrentFrame()
    r = Response(frameData, mimetype='image/jpeg')

    with open("test.jpg", "wb") as f:
        f.write(frameData)

    return frameData


# main --------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)