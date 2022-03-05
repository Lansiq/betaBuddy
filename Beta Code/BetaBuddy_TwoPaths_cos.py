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
    def draw(self, window):
        pygame.draw.circle(window, self.colour,(self.x, self.y), 5)
    
    def draw_edge(self, window, p):
        pygame.draw.line(window, ORANGE, (self.x, self.y), p.get_posistion())
    
    def update_neighbors(self, holdsList):
        self.neighbors = []
        for hold in holdsList:
            if hold != self:
                x,y = hold.get_position()
                if abs(self.x - x) < 125 and abs(self.y - y) < 125 and (y - self.y) < 0:
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


# Functions for Beta Buddy #


# Takes a list of corridantes and makes them into hold objects
def make_holds(hold_coords):
    hold_list = []
    for i in hold_coords:
        newHold = Hold(i[0],i[1])
        hold_list.append(newHold)
    return hold_list

# Draws a list of hold objects onto the screen
def drawHolds(window,holdlist):
    #window.fill(WHITE)
    for hold in holdlist:
        hold.draw(window)
    pygame.display.update()

def drawPath(window, path,colour):
    #window.fill(WHITE)
    path = list(path.values())
    for i in range(len(path)-1):
        pygame.draw.line(window, colour, path[i].get_position(), path[i+1].get_position(), 5)
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
        
def update_neighbours_feet(classHoldsList):
    for i in classHoldsList:
        i.update_neighbors(classHoldsList)
        i.update_feet(classHoldsList)

def draw_paths(colours,paths,screen):
    for j, path in enumerate(paths):
            col = colours[j]
            drawPath(screen,path,col) 
            
# Hurestic function (Are we getting closer to the goal?)
def heuristic(p1, p2):  #p1, p2 are cooridantes ie (x,y)
	x1, y1 = p1.get_position()
	x2, y2 = p2.get_position()
	return abs(x1 - x2) + abs(y1 - y2) # Manhatten distance


def g(p1, p2):  #p1, p2 are cooridantes ie (x,y)
	x1, y1 = p1.get_position()
	x2, y2 = p2.get_position()
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) # Eculidan Distance

def find_paths(start_left, start_right, start_foot_left, start_foot_right, end, holdList):
    

    left_path = {1: start_left}
    right_path = {1: start_right}
    
    left_foot_path = {1: start_foot_left}
    right_foot_path = {1: start_foot_right}
    
    #Define list of all paths
    paths = [left_path, right_path]
    foot_paths = [left_foot_path, right_foot_path]
    
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
    
    return paths, foot_paths
  

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
        
#    left_foot_path = {1: start_foot_left}
#    right_foot_path = {1: start_foot_right}
#    
#    foot_paths = [left_foot_path, right_foot_path]
    
    pass
    

def main():
    # Screen Setup
    (width, height) = (400, 780)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simple Path')
    screen.fill(WHITE)
    pygame.display.flip()
    
    # Take hold cooridantes and make them into Hold Class objects
    ############# Can change holds list used in this line #################
    classHoldsList = make_holds(holdsList1)
    
    # Set start and end holds
    start = classHoldsList[3]
    start.make_start()
    
    
    left_foot = classHoldsList[0]
    right_foot = classHoldsList[1]
    
    print(start.get_position())
    print(classHoldsList[2].get_position())
    print(left_foot.get_position())
    print(right_foot.get_position())
    
    classHoldsList[13].update_feet(classHoldsList)
    
    classHoldsList[8].twohands = True
    
    end = classHoldsList[-1]
    end.make_end()
    
    # Get neighbours for each hold
    update_neighbours_feet(classHoldsList)
    
    # Find paths
    hand_paths, foot_paths = find_paths(start, start, left_foot, right_foot, end, classHoldsList)
#    print(paths)
    print(list(hand_paths[0]))
    print(list(hand_paths[1]))
    
    
    left_feet, right_feet = get_feet(hand_paths, left_foot, right_foot)
    
    print(left_feet)
    print(right_feet)
    
    feet_paths = [left_feet,right_feet]
    
    pygame.init() # intilize font
    font=pygame.font.SysFont('helvetica',20) #define the font and size
    
#    printHoldNumber(screen,hand_paths[0],font)
#    printHoldNumber(screen,hand_paths[1],font)
    
    printHoldNumber(screen,feet_paths[0],font)
    printHoldNumber(screen,feet_paths[1],font)
    
#    for i in paths[1].holds:
#        i.make_neighbor()
    
    # Use a loop so the window stays open
    # But this means that pygame is always redrawing
    running = True
    while running:
        # If the X button is clicked quit pygame screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw holds on screen
        drawHolds(screen,classHoldsList)
        
        #Draw Paths
        colours = [PURPLE, GREY]
#        draw_paths(colours,hand_paths,screen)
        draw_paths(colours,feet_paths,screen)
    
    
    pygame.quit()

main()