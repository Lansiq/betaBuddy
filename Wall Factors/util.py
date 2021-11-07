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
def printImage(img):
    cv2.imshow('', img)

## Plots image via MATLAB
# cv2 img = cv2 object of image
def plotImage(img):
    return plt.imshow(img)

## Saves image to local directory, will nest it in folder "output"
# string fileName = name of jpg to save
# cv2 img = cv2 object of image
def saveImage(fileName, img):
    cv2.imwrite("output/"+fileName+".jpg",img)  