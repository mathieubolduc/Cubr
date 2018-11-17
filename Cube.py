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
        self.hypercube = np.zeros(5, 5, 5)


    """ Takes a side (WHITE, RED, etc) and a 3x3 array and stores it in the hypercube"""
    def setSide(self, side, data):
        center = centerMap[side]
        count = 0
        for x in range(5) if center[0] == 2 else (center[0]):
            for y in range(5) if center[1] == 2 else (center[1]):
                for z in range(5) if center[2] == 2 else (center[2]):
                    self.hypercube[x][y][z] = data[count % 3][count / 3]
                    count += 1

    """ Takes a side (WHITE, RED, etc) and returns the 3x3 array of colors corresponding to it"""
    def getSide(self, side):
        center = centerMap[side]
        count = 0
        data = [[] * 3 for _ in range(3)]
        for x in range(0, 5, 1) if center[0] == 2 else (center[0]):
            for y in range(0, 5, 1) if center[1] == 2 else (center[1]):
                for z in range(0, 5, 1) if center[2] == 2 else (center[2]):
                    data[count % 3][count / 3] = self.hypercube[x][y][z]
                    count += 1


    # 90 deg rotation of a side clockwise
    def rotate(self, side):
        ...