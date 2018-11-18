from Cube import *
from collections import deque
from Algorithms import *
from Display import plotCube

elliMap = { CubeColor.RED: 'F',
            CubeColor.BLUE: 'L',
            CubeColor.GREEN: 'R',
            CubeColor.ORANGE: 'B',
            CubeColor.WHITE: 'D',
            CubeColor.YELLOW: 'U',
}


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
            # if len(self.moves) > 0 and self.moves[-1].side == move.side:
            #     self.moves[-1].angle = (self.moves[-1].angle + move.angle) % 360
            #     if self.moves[-1].angle == 0:
            #         self.moves.pop()
            # else:
            self.moves.append(move)

    def _addAlgorithm(self, cube, algorithm):
        for move in algorithm:
            self._addMove(cube, move)



    def toElli(self):
        s = ""
        for move in self.moves:
            if move.angle != 0:
                s += elliMap[move.side]
                move.angle %= 360
                if move.angle == 180:
                    s += '2'
                elif move.angle == -90 or move.angle == 270:
                    s += 'i'
        return s


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

        # F2L
        for edge in [   [CubeColor.RED, CubeColor.BLUE],
                        [CubeColor.BLUE, CubeColor.ORANGE],
                        [CubeColor.ORANGE, CubeColor.GREEN],
                        [CubeColor.GREEN, CubeColor.RED]]:
            edgePos = cube.find(edge)
            desiredPos = solvedCube.find(edge)
            if not np.all([edgePos[i] == desiredPos[i] for i in range(2)]):
                if edgePos[0][2] == 2:
                    # already in the F2L, move it out
                    x = edgePos[0][0]
                    y = edgePos[0][1]
                    currentSide = 0
                    if x < 2 and y < 2:
                        currentSide = CubeColor.BLUE
                    elif x > 2 and y < 2:
                        currentSide = CubeColor.RED
                    elif x > 2 and y > 2:
                        currentSide = CubeColor.GREEN
                    elif x < 2 and y > 2:
                        currentSide = CubeColor.ORANGE
                    
                    algo = rotateAlgo(F2L, currentSide)
                    self._addAlgorithm(cube, algo)
                    edgePos = cube.find(edge)

                # on top, add it in
                j = 0 if edgePos[0][2] == 3 else 1
                while getSideFromPosition(edgePos[j]) != edge[j]:
                    self._addMove(cube, CubeRotation(CubeColor.YELLOW))
                    edgePos = cube.find(edge)
                currentSide = getSideFromPosition(edgePos[j])
                sides = [CubeColor.RED, CubeColor.GREEN, CubeColor.ORANGE, CubeColor.BLUE]
                left = sides[(sides.index(currentSide) + 1) % 4]
                algo = F2L
                if edge[(j+1) % 2] != left:
                    algo = flipAlgo(algo)
                algo = rotateAlgo(algo, currentSide)
                self._addAlgorithm(cube, algo)



        # edge orientation
        yellowFace = cube.getSide(CubeColor.YELLOW)
        if np.all([yellowFace[location[0]][location[1]] != CubeColor.YELLOW for location in [(0, 1), (1, 0), (1, 2), (2, 1)]]):
            # no yellow yet, do the algo anywhere
            self._addAlgorithm(cube, OLL_EDGE)
            yellowFace = cube.getSide(CubeColor.YELLOW)

        currentSide = 0
        if yellowFace[0][1] == CubeColor.YELLOW and yellowFace[1][2] != CubeColor.YELLOW:
            currentSide = CubeColor.ORANGE
        elif yellowFace[1][2] == CubeColor.YELLOW and yellowFace[2][1] != CubeColor.YELLOW:
            currentSide = CubeColor.GREEN
        elif yellowFace[2][1] == CubeColor.YELLOW and yellowFace[1][0] != CubeColor.YELLOW:
            currentSide = CubeColor.RED
        elif yellowFace[1][0] == CubeColor.YELLOW and yellowFace[0][1] != CubeColor.YELLOW:
            currentSide = CubeColor.BLUE
        
        # copycube = cube.copy()
        if currentSide != 0:
            algo = rotateAlgo(OLL_EDGE, currentSide)
            # j = 0
            while not np.all([yellowFace[location[0]][location[1]] == CubeColor.YELLOW for location in [(0, 1), (1, 0), (1, 2), (2, 1)]]):
                self._addAlgorithm(cube, algo)
                yellowFace = cube.getSide(CubeColor.YELLOW)
                # j += 1
                # if j > 10:
                #     print(currentSide)
                #     plotCube(copycube)
                #     plotCube(cube)


        # edge placement
        currentSide = 0
        for i in range(4):
            good = 0
            for side in [CubeColor.RED, CubeColor.BLUE, CubeColor.ORANGE, CubeColor.GREEN]:
                edge = [CubeColor.YELLOW, side]
                edgePos = cube.find(edge)
                desiredPos = solvedCube.find(edge)
                if np.all([edgePos[i] == desiredPos[i] for i in range(2)]):
                    good += 1
                    currentSide = side
            if good == 4 or good == 1:
                break
            cube.rotate(CubeColor.YELLOW)
        else:
            # random sune
            self._addAlgorithm(cube, SUNE)
            for i in range(4):
                good = 0
                for side in [CubeColor.RED, CubeColor.BLUE, CubeColor.ORANGE, CubeColor.GREEN]:
                    edge = [CubeColor.YELLOW, side]
                    edgePos = cube.find(edge)
                    desiredPos = solvedCube.find(edge)
                    if np.all([edgePos[i] == desiredPos[i] for i in range(2)]):
                        good += 1
                        currentSide = side
                if good == 4 or good == 1:
                    break
                cube.rotate(CubeColor.YELLOW)
                    
        if good == 1:
            algo = rotateAlgo(SUNE, currentSide)
            self._addAlgorithm(cube, algo)
            for side in [CubeColor.RED, CubeColor.BLUE, CubeColor.ORANGE, CubeColor.GREEN]:
                edge = [CubeColor.YELLOW, side]
                edgePos = cube.find(edge)
                desiredPos = solvedCube.find(edge)
                if not np.all([edgePos[i] == desiredPos[i] for i in range(2)]):
                    self._addAlgorithm(cube, algo)
                    break


        # corner placement
        sides = [CubeColor.RED, CubeColor.BLUE, CubeColor.ORANGE, CubeColor.GREEN]
        currentSide = 0
        for i in range(4): 
            good = 0
            for i in range(4):
                corner = [CubeColor.YELLOW, sides[i], sides[(i+1)%4]]
                cornerPos = cube.find(corner)
                desiredPos = solvedCube.find(corner)
                if np.any([np.all([cornerPos[(i+j)%3] == desiredPos[i] for i in range(3)]) for j in range(3)]):
                    good += 1
                    currentSide = i
            if good == 4 or good == 1:
                break
            cube.rotate(CubeColor.YELLOW)
        else:
            self._addAlgorithm(cube, PLL_A)
            for i in range(4): 
                good = 0
                for i in range(4):
                    corner = [CubeColor.YELLOW, sides[i], sides[(i+1)%4]]
                    cornerPos = cube.find(corner)
                    desiredPos = solvedCube.find(corner)
                    if np.any([np.all([cornerPos[(i+j)%3] == desiredPos[i] for i in range(3)]) for j in range(3)]):
                        good += 1
                        currentSide = i
                if good == 4 or good == 1:
                    break
                cube.rotate(CubeColor.YELLOW)
        
        if good == 1:
            corner = [CubeColor.WHITE, sides[currentSide], sides[(currentSide+1)%4]]
            desiredPos = solvedCube.find(corner)
            currentSide = getSideFromPosition(desiredPos[2])
            algo = rotateAlgo(PLL_A, currentSide)
            self._addAlgorithm(cube, algo)
            for i in range(4):
                corner = [CubeColor.YELLOW, sides[i], sides[(i+1)%4]]
                cornerPos = cube.find(corner)
                desiredPos = solvedCube.find(corner)
                if not np.any([np.all([cornerPos[(i+j)%3] == desiredPos[i] for i in range(3)]) for j in range(3)]):
                    self._addAlgorithm(cube, algo)
                    break
        

        # corner orientation
        angle = 0
        for i in range(4):
            corner = [CubeColor.YELLOW, sides[i], sides[(i+1)%4]]
            cornerPos = cube.find(corner)
            while cornerPos[0][2] != 4:
                self._addAlgorithm(cube, GHOST)
                cornerPos = cube.find(corner)
            self._addMove(cube, CubeRotation(CubeColor.YELLOW, -90))

        plotCube(cube)





""" tests"""
if(__name__ == "__main__"):
    for _ in range(1):
        testCube = getScrambledCube()
        # testCube = getSolvedCube()
        solver = CubeSolver(testCube)
        solver.computeMoves()
        print(solver.toElli())
        print()
        print(len(solver.moves))
        