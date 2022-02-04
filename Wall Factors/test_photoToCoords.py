## Uses 7 test images and performs edge detection
import util as U
import cv2
import numpy as np

def main():
    ## Fix file path issue ##
    #wallNum = input("Please enter Wall Number: ")
    #testImg = U.inputImage("Wall"+str(wallNum)+".JPEG")
    path = r"C:\Users\lance\Desktop\testWalls\Wall9.JPEG"

    testImg = cv2.imread(path)
    U.printImage(testImg)

    # Preprocessing - Gaussian Blur 
    GBlur = U.Blur(testImg, 15) # Change kernal size (2nd input) for more blur

    # Run edge detection algorithm and return coordinates
    coordinates, scaled, outputImg = edgeDetect(GBlur)

    # Output Check
    print(scaled)
    U.printImage(outputImg)
    cv2.waitKey(0)

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

    # Scaling
    holdDist = U.scaleCoords(coords,Picture)
        
    return coords, holdDist, Contours_Filled_Moment

main()