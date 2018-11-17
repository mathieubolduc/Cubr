from enum import Enum
import numpy as np

class CubeColor(Enum):
    UNKNOWN = 0
    WHITE = 1
    YELLOW = 2
    RED = 3
    ORANGE = 4
    GREEN = 5
    BLUE = 6

centerMap = {   CubeColor.WHITE:    (2, 2, 0),  # bottom
                CubeColor.YELLOW:   (2, 2, 4),  # top
                CubeColor.RED:      (2, 0, 2),  # front
                CubeColor.ORANGE:   (2, 4, 2),  # back
                CubeColor.GREEN:    (4, 2, 2),  # right
                CubeColor.BLUE:     (0, 2, 2)   # left
            }

class Cube:
    def __init__(self):
        # hypercube is a 5x5x5 with the center 3x3s as the sides
        #
        #  ^ z
        #  |
        #  |   / y
        #  |  /
        #  | /
        #  ----------->  x
        self.hypercube = np.zeros((5, 5, 5))


    """ Takes a side (WHITE, RED, etc) and a 3x3 array and stores it in the hypercube"""
    def setSide(self, side, data):
        center = centerMap[side]
        count = 0
        for x in range(1, 4, 1) if center[0] == 2 else [center[0]]:
            for y in range(1, 4, 1) if center[1] == 2 else [center[1]]:
                for z in range(1, 4, 1) if center[2] == 2 else [center[2]]:
                    self.hypercube[x][y][z] = data[count % 3][count // 3]
                    count += 1

    """ Takes a side (WHITE, RED, etc) and returns the 3x3 array of colors corresponding to it"""
    def getSide(self, side):
        center = centerMap[side]
        count = 0
        data = np.zeros((3, 3))
        for x in range(1, 4, 1) if center[0] == 2 else [center[0]]:
            for y in range(1, 4, 1) if center[1] == 2 else [center[1]]:
                for z in range(1, 4, 1) if center[2] == 2 else [center[2]]:
                    data[count % 3][count // 3] = self.hypercube[x][y][z]
                    count += 1
        return data


    """ 90 deg rotation of a side clockwise """
    def rotate(self, side, angle = 90):
        center = centerMap[side]
        minmax = []
        axes = []
        for _ in range(3):
            minmax.append(0 if center[0] <= 2 else 3)
            minmax.append(4 if center[0] >= 2 else 1)
            axes.append(1 if center[0] == 2 else 0)

        # data is 2x5x5 or 5x2x5 or 5x5x2
        data = self.hypercube[minmax[0] : minmax[1]][minmax[2] : minmax[3]][minmax[4] : minmax[5]]
        self.hypercube[minmax[0] : minmax[1]][minmax[2] : minmax[3]][minmax[4] : minmax[5]] = np.rot90(data, angle / 90, axes)



testCube = Cube()

data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

testCube.setSide(CubeColor.WHITE, data)
testCube.rotate(CubeColor.WHITE)
newData = testCube.getSide(CubeColor.WHITE)
print(newData)