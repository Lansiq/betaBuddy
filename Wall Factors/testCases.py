## Uses 7 test images and performs edge detection
import util as U
import cv2
import numpy as np

def main():
    for k in range(1,8):
        # Loading image of wall
        print("Testing Wall",k,":")
        testImg = U.inputImage("Wall"+str(k)+".JPEG")
        U.plotImage(testImg)
        # Testing two different preprocessing algorithms
        #   both have parameters to vary, will test multiple to see
        #   optimal/most consistent value
        meanSquareFilter, msfSuffix = msf(testImg,k)
        msf_size = len(meanSquareFilter)
        
        gaussianBlur, blurSuffix = gBlur(testImg,k)
        blur_size = len(gaussianBlur)
    
        tests = meanSquareFilter+gaussianBlur
        testsSuffix = msfSuffix+blurSuffix
    
        # Run edge detection algorithm
        edgeDetect(tests,testsSuffix,msf_size,blur_size,k)


# Testing Preprocessing
def msf(img,num):
    print("Running Mean Shift Filtering")
    msf = []
    msfSuff = []

    for i in range(10,40,10):
        for j in range(10,40,10):
            #Image suffix for file naming
            print("Space Radius: ", i)
            print("Colour Radius: ", j)
            suffix = "msf"+str(i)+str(j)
            msfSuff.append(suffix)
                    
            imgMSF = cv2.pyrMeanShiftFiltering(img,i,j)
            
            U.saveImage(imgMSF, "MSF/wall"+str(num)+"_"+suffix)
            msf.append(imgMSF)

    return msf, msfSuff

def gBlur(img,num):
    print("Running Mean Shift Filtering")
    gBlur = []
    blurSuff = []

    for i in range(3,23,2):
        #Image suffix for file naming
        print("Blur Kernal Size: ",i)        
        suffix = "blur"+str(i)
        blurSuff.append(suffix)

        imgBlur = U.Blur(img,i)
        U.saveImage(imgBlur, "Blur/wall"+str(num)+suffix)
        gBlur.append(imgBlur)
            
    return gBlur, blurSuff

# Edge Detection
def edgeDetect(imgArray,suffixArray,msfSize,gBlurSize,num):    
    # Perform on all varrying parameter images
    for i in range(len(imgArray)):
        Picture = imgArray[i]
        
        # Convert to greyscale
        Picture_Gray = U.Gray(Picture)

        # Threshold/Mask
        T,Threshold_Adaptive = U.Threshold(Picture_Gray)
        Mask_Adaptive = U.Mask(Picture,Threshold_Adaptive)
        
        U.saveImage(Mask_Adaptive,"edgeDetect/mask/Wall"+str(num)+"/"+suffixArray[i])

        # Canny
        Canny = U.Canny(Picture_Gray,T/2,T)

        # Contour
        Contours_Outline = U.Find_Contours_Optimal(Canny,Picture,False)

        U.saveImage(Contours_Outline,"edgeDetect/contour/Wall"+str(num)+"/"+suffixArray[i])


        # Centroid
        Contours_Filled_Binary = U.Find_Contours_Optimal_Binary(Canny,Picture)
        Canny = U.Canny(Contours_Filled_Binary,T/2,T)
        Contours_Filled_Moment = U.Find_Contours_Optimal_Moment(Canny,Picture)
        
        U.saveImage(Contours_Filled_Moment,"edgeDetect/moment/Wall"+str(num)+"/"+suffixArray[i])



main()