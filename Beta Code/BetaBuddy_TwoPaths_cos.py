# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 20:30:36 2021

@author: paule
"""

# Import needed libaries
import pygame
import math
import util as U
import itertools
import body as B

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

# Wall Height
wall_height = 3

# Height
climber_height = 1.76
# short person
climber_height = 1.56
# Tall person
# climber_height = 1.82


## Different routes - would be given as output to another route
### Yellow
yellow_route = [[[661, 478], 'Yellow', 0], [[663, 676], 'Yellow', 2], [[962, 968], 'Yellow', 3],
                [[847, 1117], 'Yellow', 4], [[1030, 1393], 'Yellow', 6], [[765, 1674], 'Yellow', 11],
                [[941, 1728], 'Yellow', 14], [[705, 2182], 'Yellow', 18], [[365, 2112], 'Yellow', 19],
                [[1031, 2277], 'Yellow', 26], [[709, 2709], 'Yellow', 32], [[697, 2892], 'Yellow', 37],
                [[578, 3054], 'Yellow', 38], [[239, 3230], 'Yellow', 39]]

yellow_height = 3537

# Yellow IDs
start_left_id = 18
start_right_id = 18
end_id = 0
right_foot_id = 38
left_foot_id = 39

### Purple
purple_route = [[[556, 513], 'Yellow', 1], [[588, 922], 'Yellow', 2], [[1080, 979], 'Yellow', 3],
                [[644, 1356], 'Yellow', 4], [[1020, 1535], 'Yellow', 5],[[862, 1739], 'Yellow', 6],
                [[1154, 1984], 'Yellow', 7], [[1054, 2079], 'Yellow', 8], [[1325, 2176], 'Yellow', 9],
                [[1013, 2342], 'Yellow', 10], [[518, 2423], 'Yellow', 11], [[1513, 2552], 'Yellow', 12],
                [[979, 2700], 'Yellow', 13], [[607, 2818], 'Yellow', 14], [[1320, 2975], 'Yellow', 15],
                [[592, 3016], 'Yellow', 16], [[1173, 3207], 'Yellow', 17]]

purple_height = 3345

# Purple IDs
start_left_id = 10
start_right_id = 12
end_id = 1
right_foot_id = 17
left_foot_id = 16

# Wall1 = Yellow 1
wall1 = [[[395, 140], 'Yellow', 0], [[422, 309], 'Yellow', 1], [[218, 487], 'Yellow', 2], [[414, 665], 'Yellow', 3],
         [[344, 846], 'Yellow', 4], [[528, 1030], 'Yellow', 5], [[436, 1122], 'Yellow', 6], [[618, 1299], 'Yellow', 7],
         [[77, 1299], 'Yellow', 8], [[510, 1599], 'Yellow', 10], [[609, 1698], 'Yellow', 11], [[698, 1915], 'Yellow', 12],
         [[340, 1921], 'Yellow', 13], [[426, 2252], 'Yellow', 14], [[792, 2293], 'Yellow', 15], [[328, 2598], 'Yellow', 16]]

wall1_height = 2666

start_left_id = 10; start_right_id = 11
end_id = 0
right_foot_id = 15; left_foot_id = 16

# Wall2 = Pink 1
wall2 = [[[522, 365], 'Red', 0], [[536, 463], 'Red', 1], [[442, 550], 'Red', 2], [[555, 669], 'Red', 3], [[500, 725], 'Red', 4],
        [[562, 892], 'Red', 7], [[561, 1006], 'Red', 8], [[510, 1073], 'Red', 9], [[628, 1188], 'Red', 10],[[517, 1342], 'Red', 11],
         [[646, 1467], 'Red', 12]]

wall2_height = 1614

start_left_id = 7; start_right_id = 7
end_id = 0
right_foot_id = 12; left_foot_id = 11

# Wall3 = Green 1
wall3 = [[[369, 497], 'Green', 19], [[418, 569], 'Green', 20], [[367, 609], 'Green', 22], [[304, 717], 'Green', 26], [[338, 780], 'Green', 29],
         [[299, 830], 'Green', 31], [[222, 949], 'Green', 39], [[254, 1005], 'Green', 41], [[368, 1070], 'Green', 42], [[164, 1157], 'Green', 45],
         [[330, 1225], 'Green', 49], [[165, 1376], 'Green', 53], [[248, 1502], 'Green', 55], [[48, 1681], 'Green', 59]]

wall3_height = 1718

# start_left_id = 45; start_right_id = 45
# end_id = 19
# right_foot_id = 55; left_foot_id = 59

wall4 = [[[316, 114], 'Red', 0], [[359, 242], 'Red', 1], [[405, 290], 'Red', 2], [[402, 396], 'Red', 3], [[434, 519], 'Red', 4], [[312, 617], 'Red', 5],
         [[175, 800], 'Red', 6], [[363, 907], 'Red', 7], [[376, 1042], 'Red', 8], [[120, 1164], 'Red', 9], [[343, 1231], 'Red', 10],[[68, 1379], 'Red', 11]]

wall4_height = 1453

start_left_id = 6; start_right_id = 6
end_id = 0
right_foot_id = 10; left_foot_id = 11

# Hold class
class Hold:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.colour = RED

    def get_position(self):
        return self.x, self.y

    def get_id(self):
        return self.id

    def is_start(self):
        return self.colour == GREEN

    def is_end(self):
        return self.colour == BLUE

    def make_start(self):
        self.colour = GREEN

    def make_orange(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = BLUE

    # Method to draw hold
    def draw(self, window, scale):
        pygame.draw.circle(window, self.colour, (self.x * scale, self.y * scale), 5)

    def __lt__(self, other):
        return False

## Functions for testing purposes
# Draws a list of hold objects onto the screen
def drawHolds(window, holdlist, height):
    # window.fill(WHITE)
    scale = height / wall_height
    for hold in holdlist:
        hold.draw(window, scale)
    pygame.display.update()

# Draws a single path on screen
def drawPath(window, path, colour, scale):
    # window.fill(WHITE)
    # path = list(path.values())
    for i in range(len(path) - 1):
        pygame.draw.line(window, colour, (path[i].get_position()[0] * scale, path[i].get_position()[1] * scale),
                         (path[i + 1].get_position()[0] * scale, path[i + 1].get_position()[1] * scale), 5)
    pygame.display.update()

# Set hold colour to start
def set_start(start):
    start.make_start()

# Set hold color to end
def set_end(end):
    end.make_end()

def screen_setup(width, height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Simple Path')
    screen.fill(WHITE)
    pygame.display.flip()
    return screen

def draw_stance(stance, height, window):
    scale = height / wall_height
    hand_left = stance[0];foot_left = stance[2];hand_right = stance[1];foot_right = stance[3]

    pygame.draw.circle(window, TURQUOISE, (hand_left.get_position()[0] * scale, hand_left.get_position()[1] * scale), 10)
    pygame.draw.circle(window, ORANGE, (hand_right.get_position()[0] * scale, hand_right.get_position()[1] * scale), 10)
    pygame.draw.circle(window, PURPLE, (foot_left.get_position()[0] * scale, foot_left.get_position()[1] * scale), 10)
    pygame.draw.circle(window, GREY, (foot_right.get_position()[0] * scale, foot_right.get_position()[1] * scale), 10)
    pygame.display.update()

######## Fuctions for beta function
# Takes a list of corridantes and makes them into hold objects
def make_holds(hold_coords, hold_id):
    hold_list = []
    for i in range(len(hold_coords)):
        newHold = Hold(hold_coords[i][0], hold_coords[i][1], hold_id[i])
        hold_list.append(newHold)
    return hold_list

# Hurestic function (Are we getting closer to the goal?)
def heuristic(p1, p2):  # p1, p2 are cooridantes ie (x,y)
    x1, y1 = p1.get_position()
    x2, y2 = p2.get_position()
    return abs(x1 - x2) + abs(y1 - y2)  # Manhatten distance

def g(p1, p2):  # p1, p2 are holds
    x1, y1 = p1.get_position()
    x2, y2 = p2.get_position()
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # Eculidan Distance

# Take cv Output and make a list of Hold objects
def get_holds(cv_list, img_height, wall_h):
    coords = []
    id = []
    # Get coords and id seprate
    for i in cv_list:
        coords.append(i[0])
        id.append(i[2])

    # Scale coords
    scale = img_height / wall_h
    for i in coords:
        i[0] = i[0] / scale
        i[1] = i[1] / scale

    classHoldsList = make_holds(coords, id)
    return classHoldsList

# Given a list of ids return the start stance and end hold
def get_startstance_end(classHoldsList, start_left_id, start_right_id, end_id, left_foot_id, right_foot_id):
    for i in classHoldsList:
        if i.get_id() == start_left_id:
            start_left = i
            set_start(i)
        if i.get_id() == start_right_id:
            start_right = i
            set_start(i)
        if i.get_id() == end_id:
            end = i
            set_end(i)
        if i.get_id() == left_foot_id:
            left_foot = i
            set_start(i)
        if i.get_id() == right_foot_id:
            right_foot = i
            set_start(i)

    start_stance = [start_left, start_right,left_foot,right_foot ]
    return start_stance, end

# Find all stances that have 3 holds in common with one another
def match_stances(current_stance,stance_list):
    # Find stances with max number of same hold posistions
    stance_matches = []
    for i, stance in enumerate(stance_list):
        count = 0
        for j in range(4):
            if current_stance[j] == stance[j]:
                count += 1
        if count == 3:
            stance_matches.append(stance)

    return stance_matches

# Get index of hold different bt two stances
def get_diff_index(stance1,stance2):
    for i in range(4):
        if stance1[i] != stance2[i]:
            return i

# Get cost of moving to next stance
def stance_cost(current_stance, next_stance,end, beta_list,person_h):
    cost = 0
    if len(beta_list)>2:
        if next_stance == beta_list[-2]:
            cost += 10000000

    if len(beta_list)>3:
        if next_stance == beta_list[-3]:
            cost += 10000000

    #get index of segment moved
    index_moved = get_diff_index(current_stance,next_stance)

    # make body for this stance
    body = B.Body(current_stance[0].get_position(),current_stance[1].get_position(),current_stance[2].get_position(),current_stance[3].get_position(), person_h)

    is_balance = body.offBalance()
    if is_balance:
        cost += 10000000

    next_hold = next_stance[index_moved]
    current_hold = current_stance[index_moved]

    x1, y1 = next_hold.get_position()
    x2, y2 = current_hold.get_position()

    if y1 < y2:
        upwards = 0
    else:
        upwards = 10000000

    cost += g(current_stance[index_moved], next_stance[index_moved]) + heuristic(next_stance[index_moved],end) + upwards
    return cost

# Find all feasibale 4 combintaion of holds in problem
def stable_stances(hold_list,start_left_id, start_right_id,person_height):
    # This function is to retun all combination of possible 4 points of contant
    # for a stance to be stable it must be in region of "reachability"
    # min and max distance between hands and foot
    # left hand/foot must be to left of right and right to right of left
    # make combintaions of all possible 4 combinations of holds

    # left hand, right hand, left foot, right foot
    allcombo_hold = list(itertools.combinations(hold_list, 4))
    for i, current in enumerate(allcombo_hold):
        allcombo_hold[i] = list(current)

    # max_foothand_dist = 0.5 + segL_height['upperExtremity']*body_height + segL_height['lowerExtremity']*body_height + segL_height['trunk']*body_height
    # max_foothand_dist = 2.5; min_foothand_dist = 0.5
    max_foothand_dist = person_height*1.2;
    min_foothand_dist = 0.5

    # print("Len1 all combo: ", len(allcombo_hold))

    # get start left and right y value
    for i in hold_list:
        if i.get_id() == start_left_id:
            start_left_y = i.get_position()[1]
        if i.get_id() == start_right_id:
            start_right_y = i.get_position()[1]

    # Switch hands and feet if they are not to the left/right
    for i,current in enumerate(allcombo_hold):
        hand_left = current[0]; hand_right = current[1]
        foot_left = current[2]; foot_right = current[3]

        lh_x = hand_left.get_position()[0]; rh_x = hand_right.get_position()[0]
        ll_x = foot_left.get_position()[0]; rl_x = foot_right.get_position()[0]

        if lh_x > rh_x:
            allcombo_hold[i][0] = hand_right
            allcombo_hold[i][1] = hand_left

        if ll_x > rl_x:
            allcombo_hold[i][2] = foot_right
            allcombo_hold[i][3] = foot_left

    # First filter is to take out posistions too close and too far away
    filter1 = []
    filter2 = []
    for i, current in enumerate(allcombo_hold):
        hand_left = current[0]; foot_left = current[2]; hand_right = current[1];foot_right = current[3]
        dist1 = g(hand_left, foot_left);dist2 = g(hand_right, foot_right);dist3 = g(hand_left, foot_right);dist4 = g(hand_right, foot_left)

        if (dist1>min_foothand_dist) and (dist2>min_foothand_dist) and (dist3>min_foothand_dist) and (dist4>min_foothand_dist):
            filter1.append(list(current))
            if (dist1<max_foothand_dist) and (dist2<max_foothand_dist) and (dist3<max_foothand_dist) and (dist4<max_foothand_dist):
                filter2.append(list(current))

    # print("Len3: ", len(filter1))
    # print("Len4: ", len(filter2))

    stable_stances = filter2
    return stable_stances

# Find string of stances that make beta
def beta_stances(start_stance, stance_list,end,person_h):
    current_stance = start_stance

    beta_stance_list = [start_stance]

    # Want to minmize cost
    # Cost = manhatten diatnce + eculdian distance
    counter = 0
    run = True
    # while (current_stance[0] != end or current_stance[1] != end) or counter < 20:
    # while counter < 19:
    while run:
        print()
        print("count: ",counter)

        if counter>30:
            error_statemnt = "Error Beta not found"
            break
            return error_statemnt

        lowest_score = 1000000000
        next_stance = None
        next_pos_stances = match_stances(current_stance, stance_list)
        print("len next stnaces: ",len(next_pos_stances))

        for int, i in enumerate(next_pos_stances):
            if i != current_stance:
                current_score = stance_cost(current_stance, i, end, beta_stance_list,person_h)
                print(int, ": ", current_score)
                if current_score < lowest_score:
                    lowest_score = current_score
                    next_stance = i

        current_stance = next_stance
        beta_stance_list.append(next_stance)

        run = ((next_stance[0] != end) and (next_stance[1] != end))
        counter += 1

    return beta_stance_list

def sort_beta(beta_stances, end_id):
    # print("look here: ", beta_stances[0][0].get_id())
    # id = int(beta_stances[0][0].get_id())
    # print(int(id))

    left_hand = {1: beta_stances[0][0].get_id()}
    right_hand = {1: beta_stances[0][1].get_id()}
    left_foot = {1: beta_stances[0][2].get_id()}
    right_foot = {1: beta_stances[0][3].get_id()}

    last_stance = beta_stances[0]

    counter = 2
    for i in range(1,len(beta_stances)):
        index = get_diff_index(last_stance,beta_stances[i])
        if index == 0:
            left_hand[counter] = beta_stances[i][0].get_id()
        if index == 1:
            right_hand[counter] = beta_stances[i][1].get_id()
        if index == 2:
            left_foot[counter] = beta_stances[i][2].get_id()
        if index == 3:
            right_foot[counter] = beta_stances[i][3].get_id()

        counter += 1
        last_stance = beta_stances[i]

    if list(left_hand.values())[-1] != end_id:
        left_hand[counter] = end_id

    if list(right_hand.values())[-1] != end_id:
        right_hand[counter] = end_id

    return left_hand, right_hand, left_foot, right_foot


# Take climber height and wall height
def beta(cv_route,image_height,start_left_id, start_right_id, end_id, left_foot_id, right_foot_id, climber_h, wall_h):
    hold_objects = get_holds(cv_route, image_height,wall_h)
    start_stance, end_hold = get_startstance_end(hold_objects,start_left_id, start_right_id, end_id, left_foot_id, right_foot_id)
    all_stances = stable_stances(hold_objects, start_left_id, start_right_id, climber_h)
    beta_stance_list = beta_stances(start_stance, all_stances, end_hold,climber_h)
    final = sort_beta(beta_stance_list,end_id)

    return final, beta_stance_list, hold_objects, all_stances

def main():
    print("Hello World")
    # Only line needed to get beta output for app
    for_alex, beta_stances_list, holds, stances = beta(wall4,wall4_height,start_left_id, start_right_id, end_id, left_foot_id, right_foot_id, climber_height, wall_height)
    print(beta_stances_list[0][0].get_id())

    ### Draw suff for testing
    # Set up screen
    (width, height) = (400, 780)
    screen = screen_setup(width, height)

    # Draw holds
    drawHolds(screen, holds, height)

    running = True
    i = 0
    while running:
        # If the X button is clicked quit pygame screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.fill(WHITE)
                    drawHolds(screen, holds, height)
                    i += 1

                if event.key == pygame.K_BACKSPACE:
                    screen.fill(WHITE)
                    drawHolds(screen, holds, height)
                    i -= 1

        if i > len(beta_stances_list) - 1:
            i = 0

        draw_stance(beta_stances_list[i], height, screen)
        # body = B.Body(beta_stances_list[i][0].get_position(),beta_stances_list[i][1].get_position(),beta_stances_list[i][2].get_position(),beta_stances_list[i][3].get_position(),person_height)
        # body.drawBody()
    pygame.quit()

main()