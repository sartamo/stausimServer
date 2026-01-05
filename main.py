import logging
import atexit
import time
import pickle

import communication

def exit_handler():
    logging.info("Exiting program")
    s0.close()
    s2.close()

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    atexit.register(exit_handler)

    s0 = communication.Socket(50000)
    s0.setup()
    
    s1 = communication.Socket(50001)
    s1.setup()

    s2 = communication.Socket(50002)
    s2.setup()

    while True:
        time.sleep(1)
        s0.send(pickle.dumps((0, 1)))
        s1.send(pickle.dumps((0, 1)))
        s2.send(pickle.dumps((0, 1)))