import numpy as np
from scipy.spatial import KDTree
import configparser

class Track:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.width = config.getint('track', 'width')
        self.height = config.getint('track', 'height')
        self.radius = config.getint('track', 'radius')
        self.width_track = config.getint('track', 'width_track')
        
        self.track = self.circle()
        
        self.points = np.argwhere(self.track > 0)
        self.tree = KDTree(self.points)

    def nearest(self, point):
        distance, index = self.tree.query(point)
        return (distance, self.points[index])
        
    def circle(self):
        y, x = np.ogrid[:self.width, :self.height]
        distance_center = np.sqrt((x - (self.width//2)) ** 2 + (y - (self.height//2)) ** 2)
        mask = abs(distance_center - self.radius) <= 2
        matrix = np.zeros((self.width, self.height), dtype=float)
        for x0, y0 in zip(*np.where(mask)):
            angle = np.atan2(y0 - (self.height//2), x0 - (self.width//2)) # Calculates angle of circle radius towards x-axis
            if angle <= -np.pi/2:
                angle += 2 * np.pi
            matrix[x0, y0] = angle + np.pi/2 # Rotate the angle by 90 degrees: Angle of tangent line towards x-axis
            if matrix[x0, y0] == 0:
                print("Angle is 0")
        return matrix


if __name__ == "__main__":
    track = Track()
    print(track.nearest((503,103)))
    print(track.track[100, 500])
