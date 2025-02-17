import socket
# import time
import logging
import threading

class Socket:
    def __init__(self, port):
        self.port = port
        self.conn = False
        self.addr = False
        self.sock = False
        self.sendBuffer = []
        self.receiveBuffer = []
        self.status = 0 # 0: Not initialized, 1: Not connected, 2: Connected
        logging.info(f"Created Socket object on port {self.port}")
    
    def _setup(self): # Must be started in additional thread
        assert self.status == 0 # Raise AssertionError if socket has already been set up
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", self.port))
        self.sock.listen()
        self.status = 1
        logging.info(f"Listening on port {self.port}")
        self.conn, self.addr = self.sock.accept()
        self.status = 2
        logging.info(f"Connected on port {self.port} by {self.addr}")
        while True:
            if self.status != 2: # Something else has closed the connection and will handle it
                break
            data = self.conn.recv(1024)
            if not data: # This thread has detected a pipe break
                logging.info(f"Connection on port {self.port} by {self.addr} has been lost, reconnecting ...")
                self.close() # If the connection is lost, close and retry
                self.setup()
                break 
            logging.info(f"Received {data} from {self.addr} on port {self.port}")
            if self.sendBuffer:
                self.conn.sendall(self.sendBuffer[0])
                logging.info(f"Sent {self.sendBuffer[0]} to {self.addr} on port {self.port}")
                self.sendBuffer.pop(0)
    
    def setup(self):
        x = threading.Thread(target=self._setup)
        x.start()
    
    def send(self, data):
        self.sendBuffer.append(data)
    
    def close(self):
        self.status = 0
        if self.conn:
            self.conn.close()
            logging.info(f"Closed conn for port {self.port}")
        if self.sock:
            self.sock.close()
            logging.info(f"Closed sock for port {self.port}")