# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 20:30:36 2021

@author: paule

modified from: https://www.pythonpool.com/a-star-algorithm-python/
pygame tutorial: https://www.youtube.com/watch?v=8dfePlONtls
"""


# Import needed libaries
import pygame
import math
import util as U
import cv2

# Define different colours for convience
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# A list of the corridants of the holds
holdsList1 = [[70,770],[225,650],[150,580],[175,450],[290,480],[310,410],[225,375],[210,350],[275,275],[300,225],[275,190],[325,130],[350,120],[325,75]]
holdsList11 = [[175,450],[290,480],[310,410],[225,375],[210,350],[275,275],[300,225],[275,190]]
holdsList2 = [[210,720],[300,720],[180,620],[80,550],[300,500],[190,490],[120,370],[75,320],[190,300],[100,220],[120,120]]

class Body:
    def __init__(self, rax, ray, lax, lay, rlx, rly, llx, lly,bx,by):
        
        self.bx = bx
        self.by = by
        self.rax = rax
        self.ray = ray
        self.lax = lax
        self.lay = lay
        self.rlx = rlx
        self.rly = rly
        self.llx = llx
        self.lly = lly
        
        self.arm_weight = 1/16
        self.leg_weight = 3/16
        self.body_weight = 1/2
        
        self.cm_x = None
        self.cm_y = None
        
        self.body_centre_x = None
        self.body_centre_y = None
        
        self.armR_centre_x = None
        self.armR_centre_y = None
        
        self.armL_centre_x = None
        self.armL_centre_y = None
        
        self.legR_centre_x = None
        self.legR_centre_y = None
        
        self.legL_centre_x = None
        self.legL_centre_y = None
        
        self.scale = 200
        
        self.max_arm_length = 0.7525*self.scale
        self.max_leg_length = 0.8775*self.scale
        self.body_width = 0.3913*self.scale
        self.body_length = 0.51*self.scale
        self.density = 0.5*self.scale
        
    def get_midpoint(self, x1,x2,y1,y2):
        Mx = (x1 + x2)/2
        My = (y1 + y2)/2
        
        return Mx, My
        
    def make_centres(self):
        self.body_centre_x = self.bx + self.body_width/2
        self.body_centre_y = self.by + self.body_length/2
        
        self.armR_centre_x, self.armR_centre_y = self.get_midpoint(self.rax, self.bx + self.body_width, self.ray, self.by) 
        
        self.armL_centre_x, self.armL_centre_y = self.get_midpoint(self.lax,self.bx,self.lay,self.by) 
        
        self.legR_centre_x, self.legR_centre_y = self.get_midpoint(self.rlx,self.bx+self.body_width,self.rly,self.by+self.body_length) 
        
        self.legL_centre_x, self.legL_centre_y = self.get_midpoint(self.llx,self.bx,self.lly,self.by+self.body_length) 
    
    def centre_mass(self):
#        self.cm_x = self.body_weight*self.body_centre_x + self.arm_weight*(self.armR_centre_x + self.armL_centre_x) + self.leg_weight*(self.legR_centre_x + self.legL_centre_x)           
#        self.cm_y = self.body_weight*self.body_centre_y + self.arm_weight*(self.armR_centre_y + self.armL_centre_y) + self.leg_weight*(self.legR_centre_y + self.legL_centre_y)           
        
        self.cm_x = self.body_weight*self.body_centre_x + self.arm_weight*(self.rax + self.lax) + self.leg_weight*(self.rlx + self.llx)           
        self.cm_y = self.body_weight*self.body_centre_y + self.arm_weight*(self.ray + self.lay) + self.leg_weight*(self.rly + self.lly)
        
    def get_cm(self):
        return self.cm_x, self.cm_y
    
    def draw_right_arm(self, window):
        pygame.draw.line(window, BLACK, (self.rax, self.ray), (self.bx+self.body_width, self.by),3)
        
    def draw_left_arm(self, window):
        pygame.draw.line(window, BLACK, (self.lax, self.lay), (self.bx, self.by),3)
        
    def draw_right_leg(self, window):
        pygame.draw.line(window, BLACK, (self.rlx, self.rly), (self.bx+self.body_width, self.by+self.body_length),3)
    
    def draw_left_leg(self, window):
        pygame.draw.line(window, BLACK, (self.llx, self.lly), (self.bx, self.by+self.body_length),3)
        
    def draw_body(self, window):
        pygame.draw.line(window, BLACK, (self.bx, self.by), (self.bx+self.body_width, self.by),3)        
        pygame.draw.rect(window, BLACK, (self.bx,self.by,self.body_width,self.body_length), 3)
        
    def draw_whole_body(self, window):
        self.draw_right_arm(window); self.draw_left_arm(window); self.draw_right_leg(window); self.draw_left_leg(window); self.draw_body(window)
        
    def draw_cm(self,window):
        pygame.draw.circle(window, RED,(self.cm_x, self.cm_y), 5)

# Define class Hold
class Hold:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.colour = RED
        self.close = []
        self.twohands = False
        self.foot_holds = []
        
    def get_position(self):
        return self.x, self.y

    def is_start(self):
        return self.colour == GREEN
    
    def is_end(self):
        return self.colour == BLUE
    
    def make_start(self):
        self.colour = GREEN
    
    def make_end(self):
        self.colour = BLUE
        
    def make_neighbor(self):
        self.colour = TURQUOISE
        
    def update_parent(self, theparent):
        self.parent = theparent
    
    #Method to draw hold
    def draw(self, window, scale):
        pygame.draw.circle(window, self.colour,(self.x*scale, self.y*scale), 5)
    
    def draw_edge(self, window, p):
        pygame.draw.line(window, ORANGE, (self.x, self.y), p.get_posistion())
    
    def update_neighbors(self, holdsList):
        self.neighbors = []
        for hold in holdsList:
            if hold != self:
                x,y = hold.get_position()
                if abs(self.x - x) < 1 and abs(self.y - y) < 2 and (y - self.y) < 0:
                    self.neighbors.append(hold)
                    #hold.make_neighbour()
    
    def update_feet(self, holdsList):
        self.foot_holds = []
        for hold in holdsList:
            if hold != self:
                x,y = hold.get_position()
                if y > self. y and abs(self.y - y) < 350 and abs(self.y - y) > 150: # abs(self.x - x) < 125 and abs(self.y - y) < 125 and (y - self.y) < 0:
                    self.foot_holds.append(hold)
#                    hold.make_neighbor()
    
    def is_close(self,holdsList):
        # for path1 x = 25 y = 35
        # for path2
        self.close = []
        for hold in holdsList:
            if hold != self:   
                x,y = hold.get_posistion()
                if abs(self.x - x) <= 25 and abs(self.y - y) <= 35:
                    self.close.append(hold)
                    hold.make_neighbour()
        
    def __lt__(self, other):
        return False
    
    
class Path:
    
    def __init__(self, start):
        self.holds = [start]

#####################################################################################################################
############################################ Functions for Beta Buddy #############################################
#####################################################################################################################

# Takes a list of corridantes and makes them into hold objects
def make_holds(hold_coords):
    hold_list = []
    for i in hold_coords:
        newHold = Hold(i[0],i[1])
        hold_list.append(newHold)
    return hold_list

# Draws a list of hold objects onto the screen
def drawHolds(window,holdlist, height):
    #window.fill(WHITE)
    scale = height/8
    for hold in holdlist:
        hold.draw(window, scale)
    pygame.display.update()

def drawPath(window, path,colour,scale):
    #window.fill(WHITE)
    path = list(path.values())
    for i in range(len(path)-1):
        pygame.draw.line(window, colour, (path[i].get_position()[0]*scale,path[i].get_position()[1]*scale),
                         (path[i+1].get_position()[0]*scale,path[i+1].get_position()[1]*scale), 5)
    pygame.display.update()

def printFont(window,font,text,x,y):
    text = font.render(text, False, BLACK, WHITE) #No clue what False/True does
    window.blit(text,(x,y))

def printHoldNumber(window,path,font):
    key_list = list(path)
    value_list = list(path.values())

    for i in range(len(value_list)):
        x,y = value_list[i].get_position()
        text = str(key_list[i])
        printFont(window,font,text,x,y)
        
def update_neighbours(classHoldsList):
    for i in classHoldsList:
        i.update_neighbors(classHoldsList)
        i.update_feet(classHoldsList)

def draw_paths(colours,paths,screen,scale):
    for j, path in enumerate(paths):
            col = colours[j]
            drawPath(screen,path,col,scale)
            
# Hurestic function (Are we getting closer to the goal?)
def heuristic(p1, p2):  #p1, p2 are cooridantes ie (x,y)
	x1, y1 = p1.get_position()
	x2, y2 = p2.get_position()
	return abs(x1 - x2) + abs(y1 - y2) # Manhatten distance


def g(p1, p2):  #p1, p2 are cooridantes ie (x,y)
	x1, y1 = p1.get_position()
	x2, y2 = p2.get_position()
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) # Eculidan Distance

def find_paths(start_left, start_right, end, holdList):
    

    left_path = {1: start_left}
    right_path = {1: start_right}
    
    #Define list of all paths
    paths = [left_path, right_path]
    
    last_hold_in_path = start_left
    count = 1
    while last_hold_in_path != end:
        lowest_score = 100000000
        path_index = -1
        best_next_hold = None

        for i, path in enumerate(paths):
                
            last_hold = list(path.values())[-1]

            
            for pos_hold in last_hold.neighbors:

                is_good = True

                #Determine if this hold can still be held by a hand
                for path_x in paths:
                    if path_x != path:
                        last_x_hold = list(path_x.values())[-1]
                      
                        if last_x_hold == pos_hold:
                            if not last_x_hold.twohands:
                                is_good = False
                                
                        if g(last_x_hold, pos_hold) > 100:
                            is_good = False

                if is_good:
#                    print("FOUND A GOOD HOLD")
                    score = g(last_hold, pos_hold) + heuristic(end, pos_hold)
                    
                    if score < lowest_score:
                        lowest_score = score
                        
                        path_index = i
                        best_next_hold = pos_hold

        count = count + 1
        currentPath = paths[path_index]
        currentPath[count] = best_next_hold
        last_hold_in_path = best_next_hold
    
    # Check to add last hold to missing path
    if list(paths[0].values())[-1] != end:
        count = count + 1
        currentPath = paths[0]
        currentPath[count] = end
    
    if list(paths[1].values())[-1] != end:
        count = count + 1
        currentPath = paths[1]
        currentPath[count] = end        
    
    return paths
  

def get_left_right_feet(feet):
    
    if feet[0].x < feet[1].x:
        left = feet[0]
        right = feet[1]
    else:
        left = feet[1]
        right = feet[0]
        
    return left, right

def max_dist_feet(pos_feet):
    max_dist = -1
    foot_list = []
    
    for i in pos_feet:
        for j in pos_feet:
            x1,y1 = i.get_position()
            x2,y2 = j.get_position()
            
            dist = abs(x1-x2)
            
            if dist > max_dist:
                max_dist = dist
                hold1 = i
                hold2 = j
    
    foot_list = [hold1,hold2]
    
    return foot_list

def get_feet(hand_paths, start_foot_left, start_foot_right):
    
    left_foot_path = {1: start_foot_left}
    right_foot_path = {1: start_foot_right}
    
    count = 2
    
    # make copy of left  hand path
    all_hands = hand_paths[0].copy()
    
    # Merge left and right hands
    all_hands.update(hand_paths[1])
    
    # Loop through all hands after start hold
    for i in range(2,len(all_hands)+1):
        # Get currnt hand
        current_hand = all_hands[i]
        
        # Get possible feet and current feet to determine if they should move
        pos_feet = current_hand.foot_holds
        current_left_foot = list(left_foot_path.values())[-1]
        current_right_foot = list(right_foot_path.values())[-1]
        
        # If current foot is not in possible feet foot needs to move
        is_left = not(current_left_foot in pos_feet)
        is_right = not(current_right_foot in pos_feet)
        
        # If both left and right are not in pos_feet
        if is_left and is_right:
            # If left and right are not in pos feet
            if len(pos_feet) == 2: # If only two feet options put left to left and right ti right
                left, right = get_left_right_feet(pos_feet)
                left_foot_path[count] = left
                right_foot_path[count] = right
                count +=1 
                
            else:
                # Find max x disatnce between possible feet for best stability
                two_foots = max_dist_feet(pos_feet)
                
                # Pick left and right
                left, right = get_left_right_feet(two_foots)
                left_foot_path[count] = left
                right_foot_path[count] = right
                count +=1
        
        elif is_left:
            pos_feet.remove(current_right_foot)
            
            if len(pos_feet) == 2: # If only two feet options put left to left and right ti right
                left, right = get_left_right_feet(pos_feet)
                left_foot_path[count] = left
                right_foot_path[count] = right
                count +=1
                
            else:
                # Find max x disatnce between possible feet for best stability
                two_foots = max_dist_feet(pos_feet)
                
                # Pick left and right
                left, right = get_left_right_feet(two_foots)
                left_foot_path[count] = left
                right_foot_path[count] = right
                count +=1
        
        elif is_right:
            pos_feet.remove(current_left_foot)
            if len(pos_feet) == 2: # If only two feet options put left to left and right ti right
                left, right = get_left_right_feet(pos_feet)
                left_foot_path[count] = left
                right_foot_path[count] = right
                count +=1
                
            else:
                # Find max x disatnce between possible feet for best stability
                two_foots = max_dist_feet(pos_feet)
                
                # Pick left and right
                left, right = get_left_right_feet(two_foots)
                left_foot_path[count] = left
                right_foot_path[count] = right
                count +=1
        
    return left_foot_path, right_foot_path


def scale_coords(cords_m,h):
    ratio = h/8
    cords = cords_m.copy()
    for i in cords:
        i[0] = i[0]*ratio
        i[1] = i[1]*ratio

    return cords, ratio

def set_start(start):
    start.make_start()

def set_end(end):
    end.make_end()

def get_holds(path):
    testImg = cv2.imread(path)

    coords = U.photoToCoords(testImg)
    coords.sort()

    classHoldsList = make_holds(coords)
    return classHoldsList

def screen_setup(width,height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simple Path')
    screen.fill(WHITE)
    pygame.display.flip()

    return screen
##############################################################################    
####################### Main to test Beta Stuff ##############################
##############################################################################
# def main():
#     path = r"C:\Users\paule\PycharmProjects\Capstone\Wall Factors\testWalls\Wall9.JPEG"
#     testImg = cv2.imread(path)
#     coords = U.photoToCoords(testImg)
#     print(coords)
#     scaled = scale_coords(coords, 780, 400)
#     print(scaled)
#
#     # Screen Setup
#     (width, height) = (400, 780)
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption('Simple Path')
#     screen.fill(WHITE)
#     pygame.display.flip()
#
#     # Take hold cooridantes and make them into Hold Class objects
#    ############# Can change holds list used in this line #################
#     # classHoldsList = make_holds(holdsList1)
#
#    # Set start and end holds
#     start = classHoldsList[3]
#     start.make_start()
#
#     left_foot = classHoldsList[0]
#     right_foot = classHoldsList[1]
#
#     # print(start.get_position())
#     # print(classHoldsList[2].get_position())
#     # print(left_foot.get_position())
#     # print(right_foot.get_position())
#
#     classHoldsList[13].update_feet(classHoldsList)
#
#     classHoldsList[8].twohands = True
#
#     end = classHoldsList[-1]
#     end.make_end()
#
#     # Get neighbours for each hold
#     update_neighbours_feet(classHoldsList)
#
#     # Find paths
#     hand_paths, foot_paths = find_paths(start, start, left_foot, right_foot, end, classHoldsList)
#     # print(paths)
#     # print(list(hand_paths[0]))
#     # print(list(hand_paths[1]))
#
#     left_feet, right_feet = get_feet(hand_paths, left_foot, right_foot)
#
#     # print(left_feet)
#     # print(right_feet)
#
#     feet_paths = [left_feet,right_feet]
#
#     pygame.init() # intilize font
#     font=pygame.font.SysFont('helvetica',20) #define the font and size
#
# #    printHoldNumber(screen,hand_paths[0],font)
# #    printHoldNumber(screen,hand_paths[1],font)
#
#     printHoldNumber(screen,feet_paths[0],font)
#     printHoldNumber(screen,feet_paths[1],font)
#
# #    for i in paths[1].holds:
# #        i.make_neighbor()
#
#    # Use a loop so the window stays open
#    # But this means that pygame is always redrawing
#     running = True
#     while running:
#        # If the X button is clicked quit pygame screen
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                running = False
#
#        # Draw holds on screen
#        drawHolds(screen,classHoldsList)
#
#        #Draw Paths
#        colours = [PURPLE, GREY]
# #        draw_paths(colours,hand_paths,screen)
#        draw_paths(colours,feet_paths,screen)
#
#
#     pygame.quit()
    
############################################################################
####################### Main to test CM Stuff ##############################
############################################################################
    
# def main():
#     # Screen Setup
#     (width, height) = (400, 780)
#     screen = pygame.display.set_mode((width, height))
#     pygame.display.set_caption('Simple Path')
#     screen.fill(WHITE)
#     pygame.display.flip()
#
#     pygame.init() # intilize font
#     font=pygame.font.SysFont('helvetica',20) #define the font and size
#
#     rax = 325
#     ray = 275
#     lax = 275
#     lay = 275
#     rlx = 325
#     rly = 500
#     llx = 275
#     lly = 500
#     bx = 160
#     by = 300
#
#
#     body = Body(rax, ray, lax, lay, rlx, rly, llx, lly,bx,by)
#
#     # Use a loop so the window stays open
#     # But this means that pygame is always redrawing
#     running = True
#     while running:
#         # If the X button is clicked quit pygame screen
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         # Draw holds on screen
# #        drawHolds(screen,classHoldsList)
#
#         body.draw_whole_body(screen)
#         body.make_centres()
#         body.centre_mass()
#         body.draw_cm(screen)
#         pygame.display.update()
#
#
#         #Draw Paths
#         colours = [PURPLE, GREY]
# #        draw_paths(colours,hand_paths,screen)
# #        draw_paths(colours,feet_paths,screen)
#
#
#     pygame.quit()

def main():
    # choose image
    path = r"C:\Users\paule\PycharmProjects\Capstone\Wall Factors\testWalls\Wall9.JPEG"

    # make image into list of hold objects
    classHoldsList = get_holds(path)

    # Set start and end holds
    start = classHoldsList[0]
    end = classHoldsList[12]
    set_start(start)
    set_end(end)

    # Get neighbours for each hold
    update_neighbours(classHoldsList)

    hand_paths = find_paths(start, start, end, classHoldsList)
    print(hand_paths)

    # Screen Setup
    (width, height) = (300, 780)
    screen = screen_setup(width,height)

    scale = height/780

    # Draw holds
    drawHolds(screen, classHoldsList, height)

    # Draw Paths
    colours = [PURPLE, GREY]
    draw_paths(colours, hand_paths, screen, scale)
    # draw_paths(colours,feet_paths,screen)

    running = True
    while running:
        # If the X button is clicked quit pygame screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

    # Get neighbours for each hold
    # update_neighbours(classHoldsList)

    # classHoldsList[8].twohands = True

   #
   #  left_foot = classHoldsList[0]
   #  right_foot = classHoldsList[1]
   #
   #  classHoldsList[13].update_feet(classHoldsList)
   #
   #  classHoldsList[8].twohands = True

    # Find paths
    # hand_paths = find_paths(start, start, end, classHoldsList)
   #
   #  left_feet, right_feet = get_feet(hand_paths, left_foot, right_foot)
   #
   #  feet_paths = [left_feet,right_feet]
   #
   #  pygame.init() # intilize font
   #  font=pygame.font.SysFont('helvetica',20) #define the font and size
   #
   #  printHoldNumber(screen,feet_paths[0],font)
   #  printHoldNumber(screen,feet_paths[1],font)

   # Use a loop so the window stays open
   # But this means that pygame is always redrawing


main()