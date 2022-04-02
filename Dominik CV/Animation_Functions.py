# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:56:49 2022

@author: Dominik Lutchman
"""

#Import Everything Here
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import skimage
from skimage.measure import label, regionprops, regionprops_table
import pandas as pd
import imageio

"""
EXAMPLE USE

rightArm = {
    '1' : '24',
    '2' : '19',
    '5' : '13',
    '9' : '11',
    '14' : '4',
    '17' : '3'
 }
leftArm = {
    '1' : '24',
    '3' :'21',
    '6' : '13',
    '10' : '11',
    '11': '9',
    '12' : '6',
    '16' : '3'
 }
rightFoot = {
    '1' : '32',
    '4' : '30',
    '8' : '22',
    '15' : '13'
 }
leftFoot = {
    '1' : '30',
    '7' : '24',
    '13' : '19'
 }

Holds = [[[675, 39], 'Yellow', 0], [[933, 2], 'Red', 1], [[574, 28], 'Red', 2], [[334, 53], 'Green', 3], [[383, 125], 'Green', 4], [[571, 134], 'Red', 5], [[333, 165], 'Green', 6], [[831, 202], 'Yellow', 7], [[603, 257], 'Red', 8], [[269, 273], 'Green', 9], [[481, 355], 'Red', 10], [[303, 336], 'Green', 11], [[670, 421], 'Yellow', 12], [[264, 387], 'Green', 13], [[974, 380], 'Yellow', 14], [[949, 551], 'Yellow', 15], [[725, 478], 'Red', 18], [[187, 505], 'Green', 19], [[344, 538], 'Red', 20], [[219, 562], 'Green', 21], [[333, 626], 'Green', 22], [[533, 645], 'Red', 23], [[129, 713], 'Green', 24], [[706, 783], 'Yellow', 25], [[295, 781], 'Green', 26], [[545, 780], 'Red', 27], [[930, 896], 'Pink', 28], [[289, 902], 'Red', 29], [[129, 932], 'Green', 30], [[512, 969], 'Red', 31], [[212, 1055], 'Green', 32], [[930, 1068], 'Yellow', 33], [[242, 1097], 'Red', 34]]

Results = cv2.imread('Wall8.png')
Results2 = Animation(Results, 3, 1.5, Holds,leftArm, rightArm, leftFoot, rightFoot)
imageio.mimsave('videotest.gif', Results2, fps=0.5)

"""


#This Function is all we need to use this Animation Shit
def Animation(Image, Image_Height_Meters, Climber_Height_Meters, Hold_Information_CV, LeftArm_Dict, RightArm_Dict, LeftLeg_Dict, RightLeg_Dict):
    Ordered_Steps = Climbing_Steps(LeftArm_Dict, RightArm_Dict, LeftLeg_Dict, RightLeg_Dict, Hold_Information_CV)
    Sizes_Body = Body_Sizes_Meters(Climber_Height_Meters)
    Body_Sizes_Pixel = Sizes(Image, Image_Height_Meters, Sizes_Body)
    Visual = ImageFrames(Image, Ordered_Steps, Body_Sizes_Pixel)
    
    return Visual



#This Function Draws the Lines for where the next step is going
#Takes in an Image, the Current Step Cords and the Next Step Cords
#Outputs and Image with the Lines
def Next_Step_Lines(Original, Current_Step, Next_Step):
    Original = Original.copy()
    
    if Current_Step[0][0] != Next_Step[0][0] or Current_Step[0][1] != Next_Step[0][1]:
        cv2.arrowedLine(Original, (Current_Step[0][0], Current_Step[0][1]), (Next_Step[0][0], Next_Step[0][1]), (0,179,255), 2)
        return Original
        
    if Current_Step[1][0] != Next_Step[1][0] or Current_Step[1][1] != Next_Step[1][1]:
        cv2.arrowedLine(Original, (Current_Step[1][0], Current_Step[1][1]), (Next_Step[1][0], Next_Step[1][1]), (0,179,255), 2)
        return Original
        
    if Current_Step[2][0] != Next_Step[2][0] or Current_Step[2][1] != Next_Step[2][1]:
        cv2.arrowedLine(Original, (Current_Step[2][0], Current_Step[2][1]), (Next_Step[2][0], Next_Step[2][1]), (0,179,255), 2)
        return Original

    if Current_Step[3][0] != Next_Step[3][0] or Current_Step[3][1] != Next_Step[3][1]:
        cv2.arrowedLine(Original, (Current_Step[3][0], Current_Step[3][1]), (Next_Step[3][0], Next_Step[3][1]), (0,179,255), 2)
        return Original
    return Original



#This Function Creates all The Frames for the Final Output
#Takes in the background photo, a list of all the steps in order, All the Body Sizes in Pixels
#Outputs a list of images of every step
def ImageFrames(Original, Every_Step,Body_Sizes_Pixel):
    All_Frames = []
    i = 0
    for Step in Every_Step:
        Frame = Original.copy()
        
        Body_Center_Optimal = Body_Optimal_Position(Step,Body_Sizes_Pixel)

        Output = Draw_Sandro(Frame, Step, Body_Center_Optimal, Body_Sizes_Pixel)
        
        if i != len(Every_Step)-1:
            Output = Next_Step_Lines(Output, Step, Every_Step[i+1])
        
        
        if i == len(Every_Step)-1:
            Output = Draw_Sandro(Frame, Step, Body_Center_Optimal, Body_Sizes_Pixel, TheEnd = True)
            
        if i == 0:
            Output = Draw_Sandro(Frame, Step, Body_Center_Optimal, Body_Sizes_Pixel, TheStart = True)
            
        
        #cv2.imwrite("Euirkea" + str(i) + ".png", Output)
        
        Output = cv2.cvtColor(Output, cv2.COLOR_BGR2RGB)
        
        All_Frames.append(Output)
        
        i = i + 1
        
    return All_Frames


#This Function Converts a Hold Number (From Beta) to the Cords Associated with that Hold Number
#Takes in the Climbing Holds Info from CV and the desired Hold Number
#Outputs the Cords Associated with that Hold Number
def Hold_Number_To_Cords(Climbing_Holds, Hold_Number):
    for Holds in Climbing_Holds:
        if Holds[2] == int(Hold_Number):
            return Holds[0]
    return "No Hold With That Hold Number"



#This function Converts the Step Number (From Beta) to the Hold Numbers associated with that Step
#Takes in The Dictionaries from all Body Parts and the Step_Number its looking for
#Returns The Hold Number being changed in that step and which Body part it effects
def Step_Number_To_Hold_Number(LeftArm, RightArm, LeftLeg, RightLeg, Step_Number):
    for i in LeftArm:
        if int(i[0])== Step_Number:
            return [i[1], "LA"]
            
    for i in RightArm:
        if int(i[0])== Step_Number:
            return [i[1], "RA"]
            
    for i in LeftLeg:
        if int(i[0])== Step_Number:
            return [i[1], "LL"]

    for i in RightLeg:
        if int(i[0])== Step_Number:
            return [i[1], "RL"]
    
    return "No Step Number Found"


#This Function takes in the Dictionaries from the Beta and the Climbing Holds Info and creates
#a list of list of all the steps in order with the HOLD CORDS
def Climbing_Steps(LeftArm, RightArm, LeftLeg, RightLeg, Climbing_Holds):
    LeftArm = list(LeftArm.items())
    RightArm = list(RightArm.items())
    LeftLeg = list(LeftLeg.items())
    RightLeg = list(RightLeg.items())
    
    #Find Number of Steps
    Steps = 0
    for i in LeftArm:
        if int(i[0])>Steps:
            Steps = int(i[0])
            
    for i in RightArm:
        if int(i[0])>Steps:
            Steps = int(i[0])
            
    for i in LeftLeg:
        if int(i[0])>Steps:
            Steps = int(i[0])

    for i in RightLeg:
        if int(i[0])>Steps:
            Steps = int(i[0])
    
    
    Positions_Order = []
    Left_Arm = Hold_Number_To_Cords(Climbing_Holds, LeftArm[0][1])
    Right_Arm = Hold_Number_To_Cords(Climbing_Holds, RightArm[0][1])
    Left_Leg = Hold_Number_To_Cords(Climbing_Holds, LeftLeg[0][1])
    Right_Leg = Hold_Number_To_Cords(Climbing_Holds, RightLeg[0][1])
    
    Current_Position = [Left_Arm, Right_Arm, Left_Leg, Right_Leg]
    Positions_Order.append(Current_Position)

    #print(Positions_Order)
    
    for i in range(2,Steps+1):
        Hold_Number = Step_Number_To_Hold_Number(LeftArm, RightArm, LeftLeg, RightLeg, i)
        #print(Hold_Number)
        Hold_Cords = Hold_Number_To_Cords(Climbing_Holds, Hold_Number[0])
        #print(Hold_Cords)
        
        if Hold_Number[1] == "LA":
            Left_Arm = Hold_Cords
    
        if Hold_Number[1] == "RA":
            Right_Arm = Hold_Cords
            
        if Hold_Number[1] == "LL":
            Left_Leg = Hold_Cords
            
        if Hold_Number[1] == "RL":
            Right_Leg = Hold_Cords
            
        Current_Position = [Left_Arm, Right_Arm, Left_Leg, Right_Leg]
        
        Positions_Order.append(Current_Position)
    
    return Positions_Order


#This function takes in a climber height and returns Body Sizes in Meteres
def Body_Sizes_Meters(Height):
    
    Arm_Size = Height * 0.44
    Leg_Size = Height * 0.53
    Head_Size = Height * 0.13
    Body_Size = Height * 0.25
    
    return [Arm_Size, Leg_Size, Head_Size, Body_Size]



#This function takes in the Image, The Actual height of the image and Body Sizes in Meters
#This function returns Body Sizes in Pixel
def Sizes(Cropped_Picture, Actual_Height, Sizes):
    Height, Width, Dim = Cropped_Picture.shape
    
    PixelPerMeter = Height//Actual_Height
    
    #Hand_Size_Pixel = int(PixelPerMeter * Hand_Size)
    #Foot_Size_Pixel = int(PixelPerMeter * Foot_Size)
    Body_Size_Pixel = int(PixelPerMeter * Sizes[3])
    Head_Size_Pixel = int(PixelPerMeter * Sizes[2])
    Leg_Size_Pixel = int(PixelPerMeter * Sizes[1])
    Arm_Size_Pixel = int(PixelPerMeter * Sizes[0])
    
    return [Arm_Size_Pixel, Leg_Size_Pixel, Head_Size_Pixel, Body_Size_Pixel]


#This function takes in the image, The sorted body positions, Body Sizes in Pixel
#Returns an Image with Beta Buddy fully drawn for 1 frame
def Draw_Sandro(Cropped_Picture, Positions, Body_Center, Body_Sizes, TheStart = False, TheEnd = False):
    Image = Cropped_Picture.copy()
    
    Left_Arm_Joint = [int(Body_Center[0] - Body_Sizes[3]/2), int(Body_Center[1] - Body_Sizes[3]/2)]
    Right_Arm_Joint = [int(Body_Center[0] + Body_Sizes[3]/2), int(Body_Center[1] - Body_Sizes[3]/2)]
    
    Left_Leg_Joint = [int(Body_Center[0] - Body_Sizes[3]/2), int(Body_Center[1] + Body_Sizes[3]/2)]
    Right_Leg_Joint = [int(Body_Center[0] + Body_Sizes[3]/2), int(Body_Center[1] + Body_Sizes[3]/2)]
    
    Head = [Body_Center[0],int(Body_Center[1] - Body_Sizes[3]/2 - Body_Sizes[2]/2)]
    Head2 = [int(Body_Center[0] + Body_Sizes[2]/2) ,int(Body_Center[1] - Body_Sizes[3]/2 - Body_Sizes[2]/2)]
    
    #Draw Body
    cv2.rectangle(Image,Left_Arm_Joint,Right_Leg_Joint,(0,0,0),4)
    
    #Draw Head
    cv2.circle(Image,Head, int(Body_Sizes[2]/2), (0,0,0),4)
    
    
    #Draw Arms
    #Left Arm
    cv2.line(Image,Left_Arm_Joint,Positions[0],(255,0,0),6)
    
    #Right Arm
    cv2.line(Image,Right_Arm_Joint,Positions[1],(255,0,0),6)


    #Draw Legs
    #Left Leg
    cv2.line(Image,Left_Leg_Joint,Positions[2],(0,0,255),6)
    
    #Right Leg
    cv2.line(Image,Right_Leg_Joint,Positions[3],(0,0,255),6)
    
    #Draw Words
    cv2.putText(Image, "#BetaBuddy", Left_Leg_Joint, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
    
    if TheStart:
        cv2.putText(Image, '"Lets Take This One Step At a Time"', Head2, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
    
    if TheEnd:
        cv2.putText(Image, '"If I Can Do it, You Can Do it. Good Luck Climber"', Head2, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    return Image


#This function takes in the Body Positions for 1 frame and the Body Sizes in Pixesl
#This function returns the Center of the Body for the given Body Positions that minimizes appendage length
def Body_Optimal_Position(Positions,Body_Sizes):
    MinX = Positions[0][0]
    MinY = Positions[0][1]
    MaxX = MinX
    MaxY = MinY
    
    for Position in Positions:
        if Position[0] < MinX:
            MinX = Position[0]
        if Position[1] < MinY:
            MinY = Position[1]
        if Position[0] > MaxX:
            MaxX = Position[0]
        if Position[1] > MaxY:
            MaxY = Position[1]
            
            
    StepX = int((MaxX - MinX)/10)
    StepY = int((MaxY - MinY)/10)
    
    Min_Distance = Body_Position_Sum([MinX,MinY], Body_Sizes, Positions)[0]
    Min_Body_Center = [0,0]
    for x in range(9):
        for y in range(9):
            Body_Center = [(MinX + (StepX*x)), (MinY + (StepY*y))]
            Body_Distance = Body_Position_Sum(Body_Center, Body_Sizes, Positions)
            #print(Body_Distance)
            if (Body_Distance[0] < Min_Distance) and Body_Distance[1]:
                Min_Body_Center = Body_Center
    
    
    return Min_Body_Center



#This function takes in the cords for the center of the body, the Body Sizes in Pixels and the hold positions
#for one frame
#This function returns the Sum of the appendages lengths given the center of the body
def Body_Position_Sum(Body_Center,Body_Sizes,Positions):
    Left_Arm_Joint = [int(Body_Center[0] - Body_Sizes[3]/2), int(Body_Center[1] - Body_Sizes[3]/2)]
    Right_Arm_Joint = [int(Body_Center[0] + Body_Sizes[3]/2), int(Body_Center[1] - Body_Sizes[3]/2)]
    
    Left_Leg_Joint = [int(Body_Center[0] - Body_Sizes[3]/2), int(Body_Center[1] + Body_Sizes[3]/2)]
    Right_Leg_Joint = [int(Body_Center[0] + Body_Sizes[3]/2), int(Body_Center[1] + Body_Sizes[3]/2)]
    
    #print(Left_Arm_Joint)
    #print(Right_Arm_Joint)
    #print(Left_Leg_Joint)
    #print(Right_Leg_Joint)
    
    
    Left_Arm_Distance = Distance_Bw_Points(Left_Arm_Joint, Positions[0])
    Right_Arm_Distance = Distance_Bw_Points(Right_Arm_Joint, Positions[1])
    Left_Leg_Distance = Distance_Bw_Points(Left_Leg_Joint, Positions[2])
    Right_Leg_Distance = Distance_Bw_Points(Right_Leg_Joint, Positions[3])
    
    #print(Left_Arm_Distance)
    #print(Right_Arm_Distance)
    #print(Left_Leg_Distance)
    #print(Right_Leg_Distance)
    
    Possible = True
    if (Left_Arm_Distance > Body_Sizes[0]) or (Right_Arm_Distance > Body_Sizes[0]):
        Possible = False
        
    if (Left_Leg_Distance > Body_Sizes[1]) or (Right_Leg_Distance > Body_Sizes[1]):
        Possible = False
        
    Total_Distance = Left_Arm_Distance + Right_Arm_Distance + Left_Leg_Distance + Right_Leg_Distance
    
    return [Total_Distance, Possible]



#This function takes two points and returns the magnitude of the distance 
def Distance_Bw_Points(Point1, Point2):
    Distance = ((Point1[0]-Point2[0])**2 + (Point1[1]-Point2[1])**2)**(1/2)
    return Distance





