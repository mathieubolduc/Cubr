import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import pylab as pl
from Cube import *

colorMap = {CubeColor.WHITE: 'w',
            CubeColor.YELLOW: 'y',
            CubeColor.RED: 'r',
            CubeColor.ORANGE: '#FFA500',
            CubeColor.GREEN: 'g',
            CubeColor.BLUE: 'b',}

def plotCube(cube):
    ax = a3.Axes3D(pl.figure())
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_zlim(0, 5)
    for side in CubeColor.ALL:
        center = centerMap[side]
        for z in range(1, 4, 1) if center[2] == 2 else [center[2]]:
            for y in range(1, 4, 1) if center[1] == 2 else [center[1]]:
                for x in range(1, 4, 1) if center[0] == 2 else [center[0]]:
                    color = cube.hypercube[x][y][z]
                    xmin = x - 0.5
                    xmax = x + 0.5
                    ymin = y - 0.5
                    ymax = y + 0.5
                    zmin = z - 0.5
                    zmax = z + 0.5

                    verts = []
                    if center[0] != 2:
                        xset = x + 0.5 if x == 0 else 3.5
                        verts.append([xset, ymin, zmin])
                        verts.append([xset, ymin, zmax])
                        verts.append([xset, ymax, zmax])
                        verts.append([xset, ymax, zmin])
                    elif center[1] != 2:
                        yset = y + 0.5 if y == 0 else 3.5
                        verts.append([xmin, yset, zmin])
                        verts.append([xmin, yset, zmax])
                        verts.append([xmax, yset, zmax])
                        verts.append([xmax, yset, zmin])
                    elif center[2] != 2:
                        zset = z + 0.5 if z == 0 else 3.5
                        verts.append([xmin, ymin, zset])
                        verts.append([xmin, ymax, zset])
                        verts.append([xmax, ymax, zset])
                        verts.append([xmax, ymin, zset])

                    tri = a3.art3d.Poly3DCollection([verts])
                    tri.set_color(colorMap[color])
                    tri.set_edgecolor('k')
                    ax.add_collection3d(tri)

    pl.show()


    
""" tests"""
if(__name__ == "__main__"):
    ...