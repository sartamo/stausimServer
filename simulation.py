import random
import time
import logging
import matplotlib.pyplot as plt

class Simulation():
    def __init__(self):
        self.positions = [0, 5, 10]
        self.velocities = [0, 0, 0]
        self.L = 200
        self.N = 3
        self.vmax = 3
        self.p = 0.7
        self.steps = 100
        self.interval = 0.5
        self.history = []

    def _simulation(self):
        for t in range(self.steps):
            new_velocities = self.velocities[:]

            # Acceleration
            for i in range(self.N):
                new_velocities[i] = min(new_velocities[i] + 1, self.vmax)

            # Braking
            gap2 = self.L - self.positions[2] - 1
            new_velocities[2] = min(new_velocities[2], gap2 - 1) # Car 2 only brakes if at end of road
            
            gap1 = self.positions[2] - self.positions[1] - 1
            if gap1 < new_velocities[1]:
                new_velocities[1] = max(gap1 - 1, 0) # Car 1 brakes less aggressively

            gap0 = self.positions[1] - self.positions[0] - 1
            if gap0 < new_velocities[0]:
                new_velocities[0] = max(gap0 - 2, 0) # Car 0 brakes more aggressively

            # Randomization (only for first car)
            if new_velocities[2] > 0 and random.random() < self.p:
                new_velocities[2] -= 1

            # Movement
            for i in range(self.N):
                self.positions[i] += new_velocities[i]

            self.velocities = new_velocities
            self.history.append(self.positions[:])
            logging.info(f"Simulation: positions {self.positions}, velocities {self.velocities}")
            #time.sleep(interval)

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    simulation = Simulation()
    simulation._simulation()

    plt.figure(figsize=(20, 10))
    colors = ["red", "blue", "green"]
    for car in range(simulation.N):
        x = [simulation.history[t][car] for t in range(simulation.steps)]
        y = list(range(simulation.steps))
        plt.scatter(x, y, color=colors[car], s=20, label=f"Car {car+1}")

    plt.xlabel("Position")
    plt.ylabel("Time step")
    plt.title("Nagel–Schreckenberg Simulation (3 Cars)")
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()