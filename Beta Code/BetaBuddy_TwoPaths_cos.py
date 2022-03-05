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
    
    # Currently adds self to neighbour list
    def update_neighbors(self, holdsList):
        self.neighbors = []
        for hold in holdsList:
            if hold != self:
                x,y = hold.get_position()
                if abs(self.x - x) < 125 and abs(self.y - y) < 125 and (y - self.y) < 0:
                    self.neighbors.append(hold)
                    #hold.make_neighbour()
    
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
    

    left_path = {1: start_left}#Path(start_left)
    right_path = {1: start_right}#Path(start_right)
    
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

def update_neighbours(classHoldsList):
    for i in classHoldsList:
        i.update_neighbors(classHoldsList)

def draw_paths(colours,paths,screen):
    for j, path in enumerate(paths):
            col = colours[j]
            drawPath(screen,path,col)   

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
    
    classHoldsList[8].twohands = True
    
    end = classHoldsList[-1]
    end.make_end()
    
    # Get neighbours for each hold
    update_neighbours(classHoldsList)
    
    # Find paths
    paths = find_paths(start, start, end, classHoldsList)
#    print(paths)
    print(list(paths[0]))
    print(list(paths[1]))
    
    pygame.init() # intilize font
    font=pygame.font.SysFont('helvetica',20) #define the font and size
    
#    printHoldNumber(screen,paths[0],font)
    printHoldNumber(screen,paths[1],font)
    
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
        draw_paths(colours,paths,screen)
    
    
    pygame.quit()

main()