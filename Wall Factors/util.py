import cv2
import matplotlib.pyplot as plt

## Opens image from "Climbing Photos" folder
# string filePath = location of image to open
# bool color = [0] for grayscale image
#       = [1] for color image
def inputImage(fileName,colour = 1):
    return cv2.imread(fileName,colour)

## Displays image in seperate window
# cv2 img = cv2 object of image
def printImage(img, Window_Name = "Output Window"):
    cv2.imshow(Window_Name, img)

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
def Gray (Image):
    Gray_Image = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    return Gray_Image