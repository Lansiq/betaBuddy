import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

## Opens image from "testWalls" folder
# string filePath = location of image to open
# bool color = [0] for grayscale image
#       = [1] for color image
def inputImage(fileName,colour = 1):
    return cv2.imread("testWalls/"+fileName,colour)

## Opens image from "fileName"
# string filePath = ABSOLUTE filepath of image to open
# bool color = [0] for grayscale image
#       = [1] for color image
def inputImageFile(fileName,colour = 1):
    return cv2.imread(fileName,colour)

## Displays image in seperate window
# cv2 img = cv2 object of image
def printImage(img, Window_Name = "Output Window"):
    cv2.imshow(Window_Name, img)
    cv2.waitKey(0)

## Plots image via MATLAB
# cv2 img = cv2 object of image
def plotImage(img):
    return plt.imshow(img)

## Saves image to local directory, will nest it in folder "output"
# string fileName = name of jpg to save
# cv2 img = cv2 object of image
def saveImage(img,fileName = "Output"):
    cv2.imwrite("output/"+fileName+".jpg",img)  
    
#Apply A Guassian Blur to the Input Picture
#Kernal Size is the size of the Kernal that is used to find the average pixel
#Sigma defines the amount of variance when calculating the mean durring blurring
def Blur (Image, Kernal_Size, Sigma = 0):
    Blurred_Image = cv2.GaussianBlur(Image,[Kernal_Size,Kernal_Size],Sigma)
    return Blurred_Image

#Converts Image to RGB Color Space
def RGB (Image):
    RGB_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    return RGB_Image

#Converts Image to Black and White
#Assumes Image is BGR unless Specified
def Gray (Image, BGR = True):
    if BGR:
        Gray_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    else:
        Gray_Image = cv2.cvtColor(Image, cv2.COLOR_RGB2GRAY)
        
    return Gray_Image

#Performs Thresholding
#Threshold is the Miniumum intensity that a pixel must. If < they will be black
#Output_Pixel is the Pixel value that will be assigned to pixels > Threshold
def Threshold_Basic (Image,Threshold,Output_Pixel=255):
    T_Value,Threshold_Image = cv2.threshold (Image,Threshold,Output_Pixel,cv2.THRESH_BINARY_INV)
    return Threshold_Image

def Threshold (Image,Output_Pixel=255):
    T_Value,Threshold_Image = cv2.threshold (Image,0,Output_Pixel,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return T_Value,Threshold_Image

def Mask (Input_Image, Mask):
    Masked_Image = cv2.bitwise_and(Input_Image,Input_Image,mask = Mask)
    return Masked_Image

def Canny (Image,Low_Threshold,High_Threshold):
    Canny_Image = cv2.Canny(Image,Low_Threshold,High_Threshold)
    return Canny_Image

def Find_Contours (Image,Target_Image):
    Contours, Heirarchy = cv2.findContours(Image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(Target_Image,Contours,-1,(224,245,66),2)
       
    return Target_Image

def Find_Contours_Optimal (Image,Target_Image,Filled = True):
    Contours, Heirarchy = cv2.findContours(Image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       
    Hulls = map(cv2.convexHull,Contours)
    Hulls = list(Hulls)
    
    if Filled:
        cv2.drawContours(Target_Image,Hulls,-1,(224,245,66),-1)
    else:
        cv2.drawContours(Target_Image,Hulls,-1,(224,245,66),2)
                
    return Target_Image

def Find_Contours_Optimal_Binary (Image,Target_Image,Filled = True):
    Contours, Heirarchy = cv2.findContours(Image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       
    Hulls = map(cv2.convexHull,Contours)
    Hulls = list(Hulls)
    
    Mask = np.zeros(Target_Image.shape,np.uint8)
    
    if Filled:
        cv2.drawContours(Mask,Hulls,-1,(255,255,255),-1)
    else:
        cv2.drawContours(Mask,Hulls,-1,(255,255,255),2)
                
    return Mask

def Find_Contours_Optimal_Moment (Image,Target_Image,Filled = True):
    Contours, Heirarchy = cv2.findContours(Image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       
    Hulls = map(cv2.convexHull,Contours)
    Hulls = list(Hulls)
    
    if Filled:
        cv2.drawContours(Target_Image,Hulls,-1,(224,245,66),-1)
    else:
        cv2.drawContours(Target_Image,Hulls,-1,(224,245,66),2)
        
    Centr = []
    for H in Hulls:
        M = cv2.moments(H)
        
        if (int(M["m00"]))!= 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        
            #Uncomment to show pre-clustering centroids
            #cv2.circle(Target_Image, (cX, cY), 5, (0, 0, 255), -1)

            Centr.append([cX, cY])

    Coords = kMeansCluster(Centr)

    for C in Coords:
        cv2.circle(Target_Image, (C[0], C[1]), 5, (0, 0, 255), -1)
    
    return Target_Image, Coords

# Clustering algorithm to eliminate repeated coordinates within the same hold
# int Centroids = calculated centroid coordinates (x,y pairs) from contours
# int holdNum = number of holds for wall, will aim to isolate only that many coordinate pairs
def kMeansCluster(Centroids, holdNum = 15):     # update to ask for user input for number of holds
    X = np.array(Centroids)
    kmeans = KMeans(n_clusters=holdNum, random_state=0).fit(X)

    return np.int_(kmeans.cluster_centers_)

# Rescales pixels value of hold coordinates into distance from floor to use for beta algorithm
# int coords = 2D array holding x,y pairs of coordinates for holds
# cv2 img = image of wall
# float scale = x pixel/meters
def scaleCoords(coords, img, scale = None):

    if scale == None:
        height, width, channel = img.shape
        scale = height/8                        # Assumes 8 meter wall, 
    
    coordsDist =[[j/scale for j in i] for i in coords] # Distance from ground

    return coordsDist

## Flips pixels value of hold coordinates so origin goes from top left -> bottom left
# int coords = 2D array holding x,y pairs of coordinates for holds
# cv2 img = image of wall
# float scale = x pixel/meters
def flipCoords(coords, img):
    height, width, channel = img.shape

    flip = coords
    for i in range(len(coords)):
        flip[i,1] = height - coords[i,1]

    return flip


## Takes an image and provides points of holds (units of distance), assumes origin is top left
# cv2 testImg = image of wall
def photoToDist(testImg):
    # Preprocessing - Gaussian Blur 
    GBlur = Blur(testImg, 15) # Change kernal size (2nd input) for more blur
       
    # Convert to greyscale
    Picture_Gray = Gray(testImg)

    # Threshold/Mask
    T,Threshold_Adaptive = Threshold(Picture_Gray)
    Mask_Adaptive = Mask(testImg,Threshold_Adaptive)

    #Uncomment if you want to see image
    #U.printImage(Mask_Adaptive)
        
    # Canny
    Canny = Canny(Picture_Gray,T/2,T)

    # Contour
    Contours_Outline = Find_Contours_Optimal(Canny,testImg,False)

    #Uncomment if you want to see image
    #U.printImage(Contours_Outline)

    # Centroid
    Contours_Filled_Binary = Find_Contours_Optimal_Binary(Canny,testImg)
    Canny = Canny(Contours_Filled_Binary,T/2,T)
    Contours_Filled_Moment, coords = Find_Contours_Optimal_Moment(Canny,testImg)

    #Uncomment if you want to see image
    #U.printImage(Contours_Filled_Moment)

    # Scaling
    holdDist = scaleCoords(coords,testImg)
        
    return coords

## Takes an image and provides points of holds (units of distance), assumes origin is top left
# cv2 testImg = image of wall
def photoToAppCoords(testImg, appHeight, appWidth):
    # Preprocessing - Gaussian Blur 
    GBlur = Blur(testImg, 15) # Change kernal size (2nd input) for more blur
       
    # Convert to greyscale
    Picture_Gray = Gray(GBlur)

    # Threshold/Mask
    T,Threshold_Adaptive = Threshold(Picture_Gray)
    Mask_Adaptive = Mask(testImg,Threshold_Adaptive)

    #Uncomment if you want to see image
    #printImage(Mask_Adaptive)
        
    # Canny
    CannyImg = Canny(Picture_Gray,T/2,T)

    # Contour
    Contours_Outline = Find_Contours_Optimal(CannyImg,testImg,False)

    #Uncomment if you want to see image
    #printImage(Contours_Outline)

    # Centroid
    Contours_Filled_Binary = Find_Contours_Optimal_Binary(CannyImg,testImg)
    CannyImg = Canny(Contours_Filled_Binary,T/2,T)
    Contours_Filled_Moment, coords = Find_Contours_Optimal_Moment(CannyImg,testImg)

    #Uncomment if you want to see image
    #printImage(Contours_Filled_Moment)

    #PUT INTO OWN FUNCTION
    #=======================
    # Scaling
    appCoords = flipCoords(coords,testImg)
    print(appCoords)
    appCoords = scaleCoords(appCoords, testImg, testImg.shape[0]/appHeight)
    appCoords = offsetCoords(appCoords, testImg, appWidth, appHeight)
    
    return appCoords

#Offsets the horizontal coordinates based on the application width

def offsetCoords(coords, testImg, appWidth, appHeight):
    offset = ( appWidth - (testImg.shape[1])*(appHeight/testImg.shape[0]) )/2.0

    offsetCoords = coords
    for i in range(len(coords)):
        offsetCoords[i][0] = coords[i][0] + offset

    return offsetCoords