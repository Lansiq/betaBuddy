from shapely.geometry import Point, Polygon
import math

# Dictionary for:
    # Segmental Mass / Total Mass
segMass_totalMass = {
    "upperExtremity":0.05,
    "lowerExtremity":0.161
}

    # Center of Mass / Segment Length
COM_segL = {
    "upperExtremity":0.53,
    "lowerExtremity":0.447
}

    # Segment Length / Height
segL_height = {
    "upperExtremity":0.44,
    "lowerExtremity":0.530,
    "shoulder":0.259,
    "hip":0.191,
    "trunk":0.288
}

## Body class containing segment objects
## Body needs to be defined every new move (temporary solution, function to move body to new position WIP)
# Point startLH, startRH, startLF, startRF = left/right hand and left/right foot starting x-y coordinate pairs
# int h = height of the individual
class Body:
    def __init__(self, startLH, startRH, startLF, startRF, h):
        self.height = h
        self.seg = []

        # Body Dimensions
        self.max_arm_length = segL_height["upperExtremity"]*self.height
        self.max_leg_length = segL_height["lowerExtremity"]*self.height
        self.shoulder_width = segL_height["shoulder"]*self.height
        self.hip_width = segL_height["hip"]*self.height
        self.body_length = segL_height["trunk"]*self.height
        self.density = 0.5*self.height ###### Not sure what this is ######

        # Add starting holds as 4 distal endpoints
        #   Arbitrary center of torso (not necessarily COM of body) defined by centroid of distal points
        #   Proximal points defined from center +- offset from body width/length
        arb = Polygon([[p.x, p.y] for p in [startLH, startRH, startLF, startRF,]])
        center = arb.centroid

        #   Left Arm
        self.addSegment("upperExtremity",center-self.shoulder_width/2, center+self.body_length/2, startLH.x, startLH.y)
        #  Right Arm
        self.addSegment("upperExtremity",center+self.shoulder_width/2, center+self.body_length/2, startRH.x, startRH.y)
        #   Left Leg
        self.addSegment("lowerExtremity",center-self.hip_width/2, center-self.body_length/2, startLF.x, startLF.y)
        #   Right Leg
        self.addSegment("lowerExtremity",center+self.hip_width/2, center-self.body_length/2, startRF.x, startRF.y)

        self.torso = self.updateTorso()

    # Define new segment and add it to list
    def addSegment(self, name, xProx, yProx, xDist, yDist):
        self.seg.append(segment(name, xProx, yProx, xDist, yDist, self.height))

    # Calculates full body centre of mass coordinates
    # int[] COM = x-y pair of COM coordinate  
    def fullBody_centreOfMass(self):
        bodyCOMx = 0
        bodyCOMy = 0

        for i in self.seg:
            segCOM = i.centreOfMass
            bodyCOMx = bodyCOMx + i.P*segCOM[0]
            bodyCOMy = bodyCOMy + i.P*segCOM[1]
        
        return Point(bodyCOMx, bodyCOMy)

    # Proximal points of all segments define torso vertices
    #   Simplest case only
    #   Need to redefine if more segments are added (check ids and only add shoulder/hip points)
    def updateTorso(self):
        torsoVertex = []
        for i in self.seg:
            torsoVertex.append(i.proximal)
        return Polygon(torsoVertex)

    # Checks if body's centre of mass is within torso
    def offBalance(self):
        return self.fullBody_centreOfMass().within(self.torso)

    ## WIP ##
    ## Provide new coordinates and body will move while checking constraints of torso and max segment lengths
    #def moveBody(self, newCoords)


## Segment class containing coordinates of proximal and distal locations
##   proximal = closer to trunk/midline. i.e., proximal of arm = shouler joint, distal of arm = hand
# int x_p, y_p, x_d, y_d = x and y pairs of coordinates for proximal and distal points respecitvely
# string name = segment unique identifier (upperExtremity, lowerExtermity, etc.)
# double R = ratio of COM:Segment Length from proximal joint
# double P = ratio of Segment Mass:Total Mass
class segment:
    def __init__(self, name, x_p, y_p, x_d, y_d, height):
        self.id = name
        self.proximal = Point(x_p,y_p)
        self.distal = Point(x_d,y_d)

        # Access dictionary for segment specific information
        self.R = segMass_totalMass[self.id]
        self.P = COM_segL[self.id]

    # Calculates centre of mass coordinates of segment
    # int[] COM = x-y pair of COM coordinate
    def centreOfMass(self):
        COMx = self.proximal[0] + self.R*(self.distal[0]-self.proximal[0])
        COMy = self.proximal[1] + self.R*(self.distal[1]-self.proximal[1])

        return Point(COMx,COMy)
    
    # Getters
    def segmentLength(self):
        return math.sqrt( (self.distal[0]-self.proximal[0])^2 + (self.distal[1]-self.proximal[1])^2 )

    def maxLength(self, height):
        return segL_height[self.id]*height