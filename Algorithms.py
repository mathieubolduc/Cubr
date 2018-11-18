from Cube import CubeColor, Cube



class CubeRotation:
    def __init__(self, side, angle=90):
        self.side = side
        self.angle = angle
        

def rotateAlgo(algorithm, facing=CubeColor.RED):
    algo = []
    rotation = [CubeColor.RED, CubeColor.GREEN, CubeColor.ORANGE, CubeColor.BLUE]
    offset = rotation.index(facing)
    for move in algorithm:
        newSide = move.side
        if move.side in rotation:
            newSide = rotation[(rotation.index(move.side) + offset) % 4]
        algo.append(CubeRotation(newSide, move.angle))
    return algo

def flipAlgo(algorithm):
    algo = []
    for move in algorithm:
        newSide = move.side
        if move.side == CubeColor.BLUE:
            newSide = CubeColor.GREEN
        elif move.side == CubeColor.GREEN:
            newSide = CubeColor.BLUE
        algo.append(CubeRotation(newSide, -move.angle))
    return algo


# right hand side F2L
F2L         = [ CubeRotation(CubeColor.YELLOW, 90),
                CubeRotation(CubeColor.GREEN, 90),
                CubeRotation(CubeColor.YELLOW, -90),
                CubeRotation(CubeColor.GREEN, -90),
                CubeRotation(CubeColor.YELLOW, -90),
                CubeRotation(CubeColor.RED, -90),
                CubeRotation(CubeColor.YELLOW, 90),
                CubeRotation(CubeColor.RED, 90)
                ]

# right hand side edge orienter
OLL_EDGE    = [ CubeRotation(CubeColor.RED, -90),
                CubeRotation(CubeColor.YELLOW, -90),
                CubeRotation(CubeColor.BLUE, -90),
                CubeRotation(CubeColor.YELLOW, 90),
                CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.RED, 90),
                ]

SUNE        = [ CubeRotation(CubeColor.GREEN, 90),
                CubeRotation(CubeColor.YELLOW, 90),
                CubeRotation(CubeColor.GREEN, -90),
                CubeRotation(CubeColor.YELLOW, 90),
                CubeRotation(CubeColor.GREEN, 90),
                CubeRotation(CubeColor.YELLOW, 180),
                CubeRotation(CubeColor.GREEN, -90),
                ]

PLL_A       = [ CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.RED, -90),
                CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.ORANGE, 180),
                CubeRotation(CubeColor.BLUE, -90),
                CubeRotation(CubeColor.RED, 90),
                CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.ORANGE, 180),
                CubeRotation(CubeColor.BLUE, 180),
                ]

GHOST       = [ CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.WHITE, 90),
                CubeRotation(CubeColor.BLUE, -90),
                CubeRotation(CubeColor.WHITE, -90),
                CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.WHITE, 90),
                CubeRotation(CubeColor.BLUE, -90),
                CubeRotation(CubeColor.WHITE, -90),
                ]

PLL_H       = [ CubeRotation(CubeColor.BLUE, 180),
                CubeRotation(CubeColor.GREEN, 180),
                CubeRotation(CubeColor.WHITE, 90),
                CubeRotation(CubeColor.BLUE, 90),
                CubeRotation(CubeColor.GREEN, -90),
                CubeRotation(CubeColor.ORANGE, 180),
                CubeRotation(CubeColor.BLUE, -90),
                CubeRotation(CubeColor.GREEN, 90),
                CubeRotation(CubeColor.WHITE, 90),
                CubeRotation(CubeColor.BLUE, 180),
                CubeRotation(CubeColor.GREEN, 180)
                ]