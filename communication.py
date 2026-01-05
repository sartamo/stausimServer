import socket
import time
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
        logging.info(f"Created Socket server object on port {self.port}")
    
    def _setup(self): # Must be started in additional thread
        assert self.status == 0 # Raise AssertionError if socket has already been set up
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", self.port))
        self.sock.listen()
        self.status = 1
        logging.info(f"Listening on port {self.port}")
        self.conn, self.addr = self.sock.accept()
        self.status = 2
        logging.info(f"Connected on port {self.port} by {self.addr}")
        s = threading.Thread(target=self._send)
        s.start()
        #r = threading.Thread(target=self._receive)
        #r.start()
    
    def _receive(self):
        while self.status == 2: # status != 2: Something else has closed the connection and will handle it
            data = self.conn.recv(1024)
            if not data: # Pipe break detected
                logging.info(f"Received empty data on port {self.port} by {self.addr}")
                self.close() # If the connection is lost, close and retry
                self.setup()
                break
            self.receiveBuffer.append(data)
            logging.info(f"Received {data} from {self.addr} on port {self.port}")
    
    def _send(self):
        while self.status == 2: # status != 2: Something else has closed the connection and will handle it
            if self.sendBuffer:
                try:
                    self.conn.sendall(self.sendBuffer[0])
                    logging.info(f"Sent {self.sendBuffer[0]} to {self.addr} on port {self.port}")
                    self.sendBuffer.pop(0)
                except BrokenPipeError:
                    logging.info(f"Couldn't send data to {self.addr} on port {self.port}")
                    self.close()
                    self.setup()
                    break
            time.sleep(0.05)
    
    def setup(self):
        t = threading.Thread(target=self._setup)
        t.start()
        return t
    
    def receive(self):
        if self.receiveBuffer:
            data = self.receiveBuffer[0]
            self.receiveBuffer.pop(0)
            return data
        else:
            return False
    
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