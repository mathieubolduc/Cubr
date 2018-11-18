import numpy as np

class CubeColor:
    UNKNOWN = 0
    WHITE = 1
    YELLOW = 2
    RED = 3
    ORANGE = 4
    GREEN = 5
    BLUE = 6

    ALL = [WHITE, YELLOW, RED, ORANGE, GREEN, BLUE]
    

centerMap = {   CubeColor.WHITE:    (2, 2, 0),  # bottom
                CubeColor.YELLOW:   (2, 2, 4),  # top
                CubeColor.RED:      (2, 0, 2),  # front
                CubeColor.ORANGE:   (2, 4, 2),  # back
                CubeColor.GREEN:    (4, 2, 2),  # right
                CubeColor.BLUE:     (0, 2, 2)   # left
            }

def getSolvedCube():
    cube = Cube()
    for side in CubeColor.ALL:
        cube.setSide(side, np.full((3, 3), side))
    return cube

def getScrambledCube():
    cube = getSolvedCube()
    for _ in range(100):
        cube.rotate(np.random.randint(1, 6), np.random.randint(-1, 1) * 90)
    return cube

def getSideFromPosition(pos):
    if pos[0] == 0:
        return CubeColor.BLUE
    elif pos[0] == 4:
        return CubeColor.GREEN
    elif pos[1] == 0:
        return CubeColor.RED
    elif pos[1] == 4:
        return CubeColor.ORANGE
    elif pos[2] == 0:
        return CubeColor.WHITE
    elif pos[2] == 4:
        return CubeColor.YELLOW
    else:
        return CubeColor.UNKNOWN

class Cube:
    def __init__(self, hypercube=None):
        # hypercube is a 5x5x5 with the center 3x3s as the sides
        #
        #  ^ z
        #  |
        #  |   / y
        #  |  /
        #  | /
        #  ----------->  x
        if hypercube is None:
            hypercube = np.zeros((5, 5, 5))
        self.hypercube = hypercube

    def copy(self):
        return Cube(np.copy(self.hypercube))


    """ Takes a side (WHITE, RED, etc) and a 3x3 array and stores it in the hypercube"""
    def setSide(self, side, data):

        if side == CubeColor.WHITE:
            data = np.rot90(data)
        elif side == CubeColor.RED:
            data = np.rot90(data, -1)
            data = np.flip(data, axis = (1))
        elif side == CubeColor.GREEN:
            data = np.rot90(data, -1)
            data = np.flip(data, axis = (1))
        elif side == CubeColor.ORANGE:
            data = np.rot90(data, -1)
        elif side == CubeColor.BLUE:
            data = np.rot90(data, -1)
        elif side == CubeColor.YELLOW:
            data = np.rot90(data, -1)
            data = np.flip(data, axis = (1))

        center = centerMap[side]
        count = 0
        for z in range(1, 4, 1) if center[2] == 2 else [center[2]]:
            for y in range(1, 4, 1) if center[1] == 2 else [center[1]]:
                for x in range(1, 4, 1) if center[0] == 2 else [center[0]]:
                    self.hypercube[x][y][z] = data[count % 3][count // 3]
                    count += 1

    """ Takes a side (WHITE, RED, etc) and returns the 3x3 array of colors corresponding to it"""
    def getSide(self, side):
        center = centerMap[side]
        count = 0
        data = np.zeros((3, 3))
        for z in range(1, 4, 1) if center[2] == 2 else [center[2]]:
            for y in range(1, 4, 1) if center[1] == 2 else [center[1]]:
                for x in range(1, 4, 1) if center[0] == 2 else [center[0]]:
                    data[count % 3][count // 3] = self.hypercube[x][y][z]
                    count += 1
        return data


    """ 90 deg rotation of a side clockwise """
    def rotate(self, side, angle = 90):
        if side == CubeColor.YELLOW or side == CubeColor.RED or side == CubeColor.GREEN:
            angle *= -1

        center = centerMap[side]
        minmax = []
        axes = []
        for i in range(3):
            minmax.append(0 if center[i] <= 2 else 3)
            minmax.append(5 if center[i] >= 2 else 2)
            if(center[i] == 2):
                axes.append(i)

        # data is 2x5x5 or 5x2x5 or 5x5x2
        data = self.hypercube[minmax[0] : minmax[1], minmax[2] : minmax[3], minmax[4] : minmax[5]]
        self.hypercube[minmax[0] : minmax[1], minmax[2] : minmax[3], minmax[4] : minmax[5]] = np.rot90(data, angle / 90, axes)

    """ Finds a cubie and returns its position. Cubies can be centers (len = 1), edges (len = 2) or corners (len = 3)"""
    """ The position is an array with the same size as the cubie, containing the positions (x, y, z)"""
    def find(self, cubie):
        if(len(cubie) == 2):
            # edges
            edges = [   [(2, 1, 0), (2, 0, 1)],
                        [(1, 2, 0), (0, 2, 1)],
                        [(3, 2, 0), (4, 2, 1)],
                        [(2, 3, 0), (2, 4, 1)],
                        [(1, 0, 2), (0, 1, 2)],
                        [(3, 0, 2), (4, 1, 2)],
                        [(0, 3, 2), (1, 4, 2)],
                        [(4, 3, 2), (3, 4, 2)],
                        [(2, 1, 4), (2, 0, 3)],
                        [(1, 2, 4), (0, 2, 3)],
                        [(3, 2, 4), (4, 2, 3)],
                        [(2, 3, 4), (2, 4, 3)]]
            
            result = [0, 0]
            for edge in edges:
                for i in range(2):
                    color = self.hypercube[edge[i][0]][edge[i][1]][edge[i][2]]
                    if(color in cubie):
                        result[cubie.index(color)] = edge[i]
                    else:
                        break
                else:
                    return result

        elif(len(cubie) == 3):
            # corners
            result = [0, 0, 0]
            for x in [1, 3]:
                for y in [1, 3]:
                    for z in [1, 3]:
                        positions = [(x, y, 0 if z==1 else 4), (x, 0 if y==1 else 4, z), (0 if x==1 else 4, y, z)]
                        for i in range(3):
                            color = self.hypercube[positions[i][0]][positions[i][1]][positions[i][2]]
                            if(color in cubie):
                                result[cubie.index(color)] = positions[i]
                            else:
                                break
                        else:
                            return result

        return None




""" tests"""
if(__name__ == "__main__"):
    testCube = getSolvedCube()
    testCube.rotate(CubeColor.WHITE)
    testCube.rotate(CubeColor.YELLOW)