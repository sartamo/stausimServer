import logging
import atexit
import pickle

import communication
import simulation

def exit_handler():
    logging.info("Exiting program")
    s0.close()
    s1.close()
    s2.close()

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    atexit.register(exit_handler)

    s0 = communication.Socket(50000)
    t0 = s0.setup()
    
    s1 = communication.Socket(50001)
    t1 = s1.setup()

    s2 = communication.Socket(50002)
    t2 = s2.setup()

    t0.join()
    t1.join()
    t2.join()

    sim = simulation.Simulation()
    ts = sim.start()

    while ts.is_alive():
        v0 = sim.velocities[0] / 4
        s0.send(pickle.dumps((0, v0)))
        v1 = sim.velocities[1] / 4
        s1.send(pickle.dumps((0, v1)))
        v2 = sim.velocities[2] / 4
        s2.send(pickle.dumps((0, v2)))
    
    s0.status = 0
    s1.status = 0
    s2.status = 0