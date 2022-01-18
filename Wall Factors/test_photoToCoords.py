## Uses 7 test images and performs edge detection
import util as U
import cv2
import numpy as np

def main():
    imgName = input("Please enter image filename: ")
    testImg = U.inputImage(imgName)
    U.plotImage(testImg)

    # Preprocessing - Gaussian Blur 
    GBlur = u.Blur(testImg, 15) # Change kernal size (2nd input) for more blur

    # Run edge detection algorithm
    edgeDetect(GBlur)


# Edge Detection
def edgeDetect(Picture):    
        
    # Convert to greyscale
    Picture_Gray = U.Gray(Picture)

    # Threshold/Mask
    T,Threshold_Adaptive = U.Threshold(Picture_Gray)
    Mask_Adaptive = U.Mask(Picture,Threshold_Adaptive)

    #Uncomment if you want to see image
    #U.printImage(Mask_Adaptive)
        
    # Canny
    Canny = U.Canny(Picture_Gray,T/2,T)

    # Contour
    Contours_Outline = U.Find_Contours_Optimal(Canny,Picture,False)

    #Uncomment if you want to see image
    #U.printImage(Contours_Outline)

    # Centroid
    Contours_Filled_Binary = U.Find_Contours_Optimal_Binary(Canny,Picture)
    Canny = U.Canny(Contours_Filled_Binary,T/2,T)
    Contours_Filled_Moment, coords = U.Find_Contours_Optimal_Moment(Canny,Picture)

    #Uncomment if you want to see image
    #U.printImage(Contours_Filled_Moment)
    
    return coords

main()
