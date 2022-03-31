from shapely.geometry import Point, Polygon
import math
import matplotlib.pyplot as plt


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
        arb = Polygon([[p[0], p[1]] for p in [startLH, startRH, startLF, startRF]])
        center = arb.centroid

        print(self.shoulder_width,self.hip_width,self.body_length)

        #   Left Arm
        self.addSegment("upperExtremity", \
            (center.x-self.shoulder_width)/2, \
            (center.y+self.body_length)/2, startLH[0], startLH[1])
        #  Right Arm
        self.addSegment("upperExtremity", \
            (center.x+self.shoulder_width)/2, (center.y+self.body_length)/2, \
            startRH[0], startRH[1])
        #   Left Leg
        self.addSegment("lowerExtremity",\
            (center.x-self.hip_width)/2, (center.y-self.body_length)/2, \
            startLF[0], startLF[1])
        #   Right Leg
        self.addSegment("lowerExtremity",\
            (center.x+self.hip_width)/2, (center.y-self.body_length)/2, \
            startRF[0], startRF[1])

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
            segCOM = i.centreOfMass()
            bodyCOMx = bodyCOMx + i.P*segCOM.x
            bodyCOMy = bodyCOMy + i.P*segCOM.y
        
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
        return not (self.fullBody_centreOfMass().within(self.torso))

    def drawBody(self):
        plt.figure()

        # Torso
        xt = [ self.seg[0].proximal.x, self.seg[1].proximal.x, self.seg[3].proximal.x, self.seg[2].proximal.x ]
        xt.append(xt[0])
  
        yt = [ self.seg[0].proximal.y, self.seg[1].proximal.y, self.seg[3].proximal.y, self.seg[2].proximal.y ]
        yt.append(yt[0])

        plt.plot(xt,yt) 

        #Draw Limbs
        RHx = [ self.seg[0].proximal.x,self.seg[0].distal.x ]
        RHy = [ self.seg[0].proximal.y,self.seg[0].distal.y ]
        plt.plot(RHx,RHy) 

        LHx = [ self.seg[1].proximal.x,self.seg[1].distal.x ]
        LHy = [ self.seg[1].proximal.y,self.seg[1].distal.y ]
        plt.plot(LHx,LHy) 

        RLx = [ self.seg[3].proximal.x,self.seg[3].distal.x ]
        RLy = [ self.seg[3].proximal.y,self.seg[3].distal.y ]
        plt.plot(RLx,RLy) 

        LLx = [ self.seg[2].proximal.x,self.seg[2].distal.x ]
        LLy = [ self.seg[2].proximal.y,self.seg[2].distal.y ]
        plt.plot(LLx,LLy) 

        # Full Body COM
        COM = self.fullBody_centreOfMass()
        plt.plot(COM.x, COM.y,'o')

        # Plot
        print(COM)
        print(self.torso)
        plt.show()  

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
        COMx = self.proximal.x + self.R*(self.distal.x-self.proximal.x)
        COMy = self.proximal.y + self.R*(self.distal.y-self.proximal.y)

        return Point(COMx,COMy)
    
    # Getters
    def segmentLength(self):
        return math.sqrt( (self.distal[0]-self.proximal[0])^2 + (self.distal[1]-self.proximal[1])^2 )

    def maxLength(self, height):
        return segL_height[self.id]*height