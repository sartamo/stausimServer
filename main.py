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

    '''sim = simulation.Simulation()
    ts = sim.start()

    while ts.is_alive():
        v0 = speeds[sim.velocities[0]]
        s0.send(pickle.dumps((0, sim.velocities[0])))
        v1 = speeds[sim.velocities[1]]
        s1.send(pickle.dumps((0, sim.velocities[1])))
        v2 = speeds[sim.velocities[2]]
        s2.send(pickle.dumps((0, sim.velocities[2])))
    
    s0.status = 0
    s1.status = 0
    s2.status = 0'''

    while True:
        s2.send(pickle.dumps((0, 3))) # speed 1 -> 0.6 speed 2 -> 0.75 speed 3 -> 1 ???
        s0.send(pickle.dumps((0, 3)))
        s1.send(pickle.dumps((0, 3)))