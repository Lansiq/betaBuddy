# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 19:42:16 2022

@author: Dominik Lutchman
"""
#Import Everything Here
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import skimage
from PIL import Image
from skimage.measure import label, regionprops, regionprops_table
import pandas as pd
import imageio

"""
EXAMPLE USE

Results = CV('Wall8.png')

plt.imshow(Results[0])
print(Results[1])

"""



#This Function is all we need to use this CV Shit
def CV(FilePath, Colour = "NA"):
    Original = cv2.imread(FilePath)
    Results = Identify_Holds_Colour_Thresh(Original, Colour)
    
    if Colour!= "NA":
        Filtered_Output_For_Beta = Colour_Filtering(Results[1], Colour, Original)
        return [Results[0], Filtered_Output_For_Beta]
    else:
        UnFiltered_Output_For_Beta = Filter(Results[1], Original)
        return [Results[0], UnFiltered_Output_For_Beta]
    
    return "Something Went Wrong"




#This Function Takes In the Cropped Picture and a Possible Colour to Perform CV
#Returns The Photo with all holds identified and Blob Information NOT FORMATTED
def Identify_Holds_Colour_Thresh(Cropped_Picture, Colour = "NA"):
    #Blur Image
    Blur = cv2.GaussianBlur(Cropped_Picture,[5,5],5)
    
    #Convert to HSV Space
    HSV = cv2.cvtColor(Blur, cv2.COLOR_BGR2HSV)
    if Colour == "NA":
        Target = HSV
    #Colour Mask
    if Colour == "Red":
        mask = cv2.inRange(HSV,(0, 0, 0), (20, 255, 255)) #Red
        Target = cv2.bitwise_and(HSV,HSV, mask=mask)
    if Colour == "Yellow":
        mask = cv2.inRange(HSV,(20, 0, 0), (45, 255, 255)) #Yellow 
        Target = cv2.bitwise_and(HSV,HSV, mask=mask)
    if Colour == "Green":
        mask = cv2.inRange(HSV,(50, 0, 0), (80, 255, 255)) #Green  
        Target = cv2.bitwise_and(HSV,HSV, mask=mask)
    if Colour == "Blue":
        mask = cv2.inRange(HSV,(90, 0, 0), (135, 255, 255)) #Blue
        Target = cv2.bitwise_and(HSV,HSV, mask=mask)
    if Colour == "Pink":
        mask = cv2.inRange(HSV,(160, 0, 0), (180, 255, 255)) #Pink  
        Target = cv2.bitwise_and(HSV,HSV, mask=mask)
    
    #Convert to Image Channels
    H, S, V = cv2.split(Target)
    
    #Do Basic Thresholding
    Basic_Threshold = 50
    BasicS = cv2.threshold(S, Basic_Threshold, 255, cv2.THRESH_BINARY)[1]
    
    #Morphing To Clean Up The Image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    Morph_Closing = cv2.morphologyEx(BasicS,cv2.MORPH_CLOSE, kernel, iterations=1)
    Morph_Opening = cv2.morphologyEx(Morph_Closing, cv2.MORPH_OPEN, kernel, iterations=1)
    
    #Identify Blobs
    Climbing_Holds = label(Morph_Opening)
    #plt.imshow(Climbing_Holds)
    
    #Create the Hold Properties into a Dataframe
    Properties = [
    'area',
    'bbox',
    'convex_area',
    'bbox_area',
    'major_axis_length',
    'minor_axis_length',
    'eccentricity',
    'orientation',
    'centroid',
    ]
    df = pd.DataFrame(regionprops_table(Climbing_Holds, properties = Properties))

    #Perform Filtering to Remove Outliers
    Height, Width, Dim = Cropped_Picture.shape
    df_filtered = df[df['eccentricity'] < 0.983]
    df_filtered = df_filtered[df_filtered['bbox_area'] > 0.00015*(Height*Width)]
    df_filtered = df_filtered[df_filtered['bbox_area'] < 0.70*(Height*Width)]
    
    #Copy Original Image to Draw Stuff On It
    Original_With_Labels_After_Filtering = Cropped_Picture.copy()
    
    #Convert the DF into a list with the order I would like
    blob_coordinates = []
    pixel_colours = []
    for index, row in df_filtered.iterrows():
        blob_coordinates.append([row['bbox-0'],
                                 row['bbox-1'],
                                 row['bbox-2'],
                                 row['bbox-3'],
                                 row['centroid-0'],
                                 row['centroid-1'],
                                 row['major_axis_length'],
                                 row['minor_axis_length'],
                                 row['orientation'],
                                 "Picture of Hold Goes Here",
                                 "N/A",
                                 (0,0,0),
                                 index])
    
    #For each Blob Find The coordinates to Draw Stuff with
    for blob in blob_coordinates:
        if isinstance(blob[1],int) or isinstance(blob[1], float):
            start = (int(blob[1]),int(blob[0]))
            end = (int(blob[3]),int(blob[2]))
            Text_Label = (int(blob[1]),int(blob[0]) + 20)
            Center = (int(blob[5]),int(blob[4]))
        else:
            start = (blob[1].astype(int),blob[0].astype(int))
            end = (blob[3].astype(int),blob[2].astype(int))
            Text_Label = (blob[1].astype(int),blob[0].astype(int) + 10)
            Center = (blob[5].astype(int),blob[4].astype(int))
    
        #Store the individual picture of the hold
        Hold = Cropped_Picture[int(blob[0]):int(blob[2]), int(blob[1]):int(blob[3])]
        blob[9] = Hold
        
        #Convert the Small Picture to HSV to Identify Colour
        Hold_HSV = cv2.cvtColor(Hold, cv2.COLOR_BGR2HSV)
        Hold_HSV_Mask_Red = [cv2.inRange(Hold_HSV,(0, 30, 30), (20, 255, 255)), (0,0,255), "Red"]
        Hold_HSV_Mask_Green = [cv2.inRange(Hold_HSV,(55, 30, 30), (70, 255, 255)), (0,255,0), "Green"]
        Hold_HSV_Mask_Yellow = [cv2.inRange(Hold_HSV,(20, 30, 30), (45, 255, 255)), (0,255,255), "Yellow"]
        Hold_HSV_Mask_Pink = [cv2.inRange(Hold_HSV,(160, 30, 30), (170, 255, 255)), (203,192,255), "Pink"]
        Hold_HSV_Mask_Blue = [cv2.inRange(Hold_HSV,(90, 30, 30), (135, 255, 255)), (255,0,0), "Blue"]
    
        Hold_Masks = [Hold_HSV_Mask_Red, Hold_HSV_Mask_Green, Hold_HSV_Mask_Yellow, Hold_HSV_Mask_Pink, Hold_HSV_Mask_Blue]
    
        Size = Hold.size
        Max = 0
        for mask in Hold_Masks:
            Percentage = np.sum(mask[0] == 255)/Size
        
            if Percentage > Max:
                Max = Percentage
                blob[-2] = mask[1]
                blob[-3] = mask[2]
            
        cv2.rectangle(Original_With_Labels_After_Filtering, start, end, blob[-2], 2)
        cv2.putText(Original_With_Labels_After_Filtering, str(blob[-1]), Text_Label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 3)
        cv2.circle(Original_With_Labels_After_Filtering, Center, 5, (255,255,255), -1)
    
    
    return [Original_With_Labels_After_Filtering,blob_coordinates]



#This function takes in the NON FORMATTED Blob info and a desired colour
#Outputs the image with only that colour selected and the FORMATTED Blob Data with the colour
def Colour_Filtering(Blob_Information, Colour, Original):
    Original_With_Colour_Filtering = Original.copy()
    Output_Beta = []
    for blob in Blob_Information:
        if blob[-3] == Colour:
            Output_Beta.append([[int(blob[5]),int(blob[4])],blob[-3],blob[-1]])
            
            if isinstance(blob[1],int) or isinstance(blob[1], float):
                start = (int(blob[1]),int(blob[0]))
                end = (int(blob[3]),int(blob[2]))
                Text_Label = (int(blob[1]),int(blob[0]) + 20)
                Center = (int(blob[5]),int(blob[4]))
            else:
                start = (blob[1].astype(int),blob[0].astype(int))
                end = (blob[3].astype(int),blob[2].astype(int))
                Text_Label = (blob[1].astype(int),blob[0].astype(int) + 10)
                Center = (blob[5].astype(int),blob[4].astype(int))
            
            cv2.rectangle(Original_With_Colour_Filtering, start, end, blob[-2], 2)
            cv2.putText(Original_With_Colour_Filtering, str(blob[-1]), Text_Label, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)
            cv2.circle(Original_With_Colour_Filtering, Center, 5, (255,255,255), -1)
            
    return [Original_With_Colour_Filtering, Output_Beta]


#This function takes in the NON FORMATTED Blob info 
#Outputs the FORMATTED Blob Data with no colour specification
def Filter(Blob_Information, Original):
    Output_Beta = []
    for blob in Blob_Information:
        Output_Beta.append([[int(blob[5]),int(blob[4])],blob[-3],blob[-1]])
        
    return Output_Beta



Results = CV('Wall8.png')

plt.imshow(Results[0])
print(Results[1])