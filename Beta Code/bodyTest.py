import body as b
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt

torso = [[0,1],[1,1],[0,0],[1,0]]
test = b.Body(torso[0],torso[1],torso[2],torso[3],2)
print(test.offBalance())

test.drawBody()