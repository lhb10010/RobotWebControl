import threading

class AtomicBytes:

    def __init__(self):
        self.bytes = b''
        self.lock = threading.Lock()

    def readBytes(self):
        with self.lock:
            return self.bytes

    def writeBytes(self, newArray):
        with self.lock:
            self.bytes = newArray
