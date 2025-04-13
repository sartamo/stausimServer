import numpy as np
from scipy.spatial import KDTree

size = 1000

class Track:
    def __init__(self): # Must be inherited
        self.points = np.argwhere(self.track > 0)
        self.tree = KDTree(self.points)

    def nearest(self, point):
        distance, index = self.tree.query(point)
        return (distance, self.points[index])


class Circle(Track):
    def __init__(self, radius):
        self.radius = radius
        self.track = self.circle()
        super().__init__()        
        
    def circle(self):
        center = size // 2
        y, x = np.ogrid[:size, :size]
        distance_center = np.sqrt((x - center) ** 2 + (y - center) ** 2)
        mask = abs(distance_center - self.radius) <= 2
        matrix = np.zeros((size, size), dtype=float)
        for x0, y0 in zip(*np.where(mask)):
            angle = np.atan2(y0 - center, x0 - center) # Calculates angle of circle radius towards x-axis
            if angle <= -np.pi/2:
                angle += 2 * np.pi
            matrix[x0, y0] = angle + np.pi/2 # Rotate the angle by 90 degrees: Angle of tangent line towards x-axis
            if matrix[x0, y0] == 0:
                print("Angle is 0")
        return matrix


if __name__ == "__main__":
    track = Circle(400)
    print(track.nearest((503,103)))
    print(track.track[100, 500])
