import subprocess
import socket
import atomicBytes
import threading
import cv2
import time

#----------------------- Camera Options --------------------------

frameWidth = 640
frameHeight = 480
jpegQuality = 90

#-----------------------------------------------------------------

#timeouts in seconds
INIT_SOCKET_TIMEOUT = None
WORKING_SOCKET_TIMEOUT = 1

# setup global variables
currentImageData = atomicBytes.AtomicBytes()
receivingImages = False
disconnectedImage = None


def initDisconnectedImage():

    global disconnectedImage

    with open("connError.jpg", "rb") as f:
        disconnectedImage = f.read()


def initCamera():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
    t = threading.Thread(target=getFrames, args=(cap,))
    t.start()

def getFrames(cap):

    global currentImageData
    global receivingImages
    global jpegQuality

    while True:
        try:
            status, img = cap.read()
            encodeParameters = [int(cv2.IMWRITE_JPEG_QUALITY), jpegQuality]
            status, jpegImage = cv2.imencode('.jpg', img, encodeParameters)
            currentImageData.writeBytes(jpegImage.data.tobytes())
            receivingImages =  True
        except:
            receivingImages = False


def getCurrentFrame():

    global currentImageData
    global disconnectedImage
    global receivingImages

    if receivingImages:
        return currentImageData.readBytes()

    return disconnectedImage


# kill camera process on exit ------------------------------

def killChild():

    global child

    if (not child is None) and child.poll() is None:
        child.kill()


#atexit.register(killChild)
#/usr/local/bin/pycheck/pycheck.sh