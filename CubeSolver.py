from Cube import *
from collections import deque

class CubeRotation:
    def __init__(self, side, angle=90):
        self.side = side
        self.angle = angle
        
def _doMove(cube, move):
    cube.rotate(move.side, move.angle)

class CubeSolver:
    def __init__(self, cube):
        self.cube = cube
        self.moves = deque()

    def nextMove(self):
        _doMove(self.cube, self.moves.popleft())

    
    def _addMove(self, cube, move):
        if move.angle != 0:
            _doMove(cube, move)
            if len(self.moves) > 0 and self.moves[-1].side == move.side:
                self.moves[-1].angle = (self.moves[-1].angle + move.angle) % 360
                if self.moves[-1].angle == 0:
                    self.moves.pop()
            else:
                self.moves.append(move)


    def computeMoves(self):
        # copy the cube
        cube = self.cube.copy()
        solvedCube = getSolvedCube()

        # do the white side

        # white edges
        for side in [CubeColor.RED, CubeColor.GREEN, CubeColor.ORANGE, CubeColor.BLUE]:
            edge = [CubeColor.WHITE, side]
            edgePos = cube.find(edge)
            desiredPos = solvedCube.find(edge)
            if not np.all([edgePos[i] == desiredPos[i] for i in range(2)]):
                whiteSide = getSideFromPosition(edgePos[0])
                otherSide = getSideFromPosition(edgePos[1])
                # side facing
                if whiteSide != CubeColor.WHITE and whiteSide != CubeColor.YELLOW:
                    # turn side until up
                    angle = 0
                    while(otherSide != CubeColor.YELLOW):
                        self._addMove(cube, CubeRotation(whiteSide))
                        edgePos = cube.find(edge)
                        otherSide = getSideFromPosition(edgePos[1])
                        angle += 90

                    # move outa the way
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                    self._addMove(cube, CubeRotation(whiteSide, -angle))

                    # put the edge in the right place
                    edgePos = cube.find(edge)
                    whiteSide = getSideFromPosition(edgePos[0])
                    while(whiteSide != side):
                        self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                        edgePos = cube.find(edge)
                        whiteSide = getSideFromPosition(edgePos[0])
                    
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                    edgePos = cube.find(edge)
                    whiteSide = getSideFromPosition(edgePos[0])
                    self._addMove(cube, CubeRotation(whiteSide))
                    self._addMove(cube, CubeRotation(side, -90))
                    self._addMove(cube, CubeRotation(whiteSide, -90))

                # vertically facing
                else:
                    # turn it up if down
                    if(whiteSide == CubeColor.WHITE):
                        self._addMove(cube, CubeRotation(otherSide, 180))

                    # put the edge in the right place
                    edgePos = cube.find(edge)
                    otherSide = getSideFromPosition(edgePos[1])
                    while(otherSide != side):
                        self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                        edgePos = cube.find(edge)
                        otherSide = getSideFromPosition(edgePos[1])

                    self._addMove(cube, CubeRotation(side, 180))


        # White corners
        for corner in [ [CubeColor.WHITE, CubeColor.RED, CubeColor.BLUE],
                        [CubeColor.WHITE, CubeColor.BLUE, CubeColor.ORANGE],
                        [CubeColor.WHITE, CubeColor.ORANGE, CubeColor.GREEN],
                        [CubeColor.WHITE, CubeColor.GREEN, CubeColor.RED]]:
            cornerPos = cube.find(corner)
            desiredPos = solvedCube.find(corner)
            if not np.all([cornerPos[i] == desiredPos[i] for i in range(3)]):
                if cornerPos[0][2] < 2:
                    # on white side, move it to the top layer
                    x = cornerPos[0][0]
                    y = cornerPos[0][1]
                    currentSide = 0
                    if x < 2 and y < 2:
                        currentSide = CubeColor.RED
                    elif x > 2 and y < 2:
                        currentSide = CubeColor.GREEN
                    elif x > 2 and y > 2:
                        currentSide = CubeColor.ORANGE
                    elif x < 2 and y > 2:
                        currentSide = CubeColor.BLUE
                    self._addMove(cube, CubeRotation(currentSide))
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW, -90))
                    self._addMove(cube, CubeRotation(currentSide, -90))
                    cornerPos = cube.find(corner)

                
                # on top side
                if cornerPos[0][2] == 4:
                    # white on top, move it to the side
                    while getSideFromPosition(cornerPos[1]) != corner[2]:
                        self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                        cornerPos = cube.find(corner)
                    currentSide = getSideFromPosition(cornerPos[2])
                    self._addMove(cube, CubeRotation(currentSide))
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW, -90))
                    self._addMove(cube, CubeRotation(currentSide, -90))
                    cornerPos = cube.find(corner)

                # white on the side
                if cornerPos[1][2] == 3:
                    # white and 1st other color are on the side
                    while getSideFromPosition(cornerPos[1]) != corner[1]:
                        self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                        cornerPos = cube.find(corner)
                    self._addMove(cube, CubeRotation(corner[2], -90))
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW, -90))
                    self._addMove(cube, CubeRotation(corner[2]))
                else:
                    # white and 2nd other color are on the side
                    while getSideFromPosition(cornerPos[2]) != corner[2]:
                        self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                        cornerPos = cube.find(corner)
                    self._addMove(cube, CubeRotation(corner[1]))
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                    self._addMove(cube, CubeRotation(corner[1], -90))


        print(cube.hypercube)







""" tests"""
if(__name__ == "__main__"):
    for _ in range(1):
        testCube = getScrambledCube()
        # testCube = getSolvedCube()
        # testCube.rotate(CubeColor.RED, -90)
        # testCube.rotate(CubeColor.YELLOW, -90)
        # testCube.rotate(CubeColor.RED, 90)
        # testCube.rotate(CubeColor.ORANGE, -90)
        # testCube.rotate(CubeColor.YELLOW, -90)
        # testCube.rotate(CubeColor.ORANGE, 90)
        solver = CubeSolver(testCube)
        solver.computeMoves()
        print(len(solver.moves))