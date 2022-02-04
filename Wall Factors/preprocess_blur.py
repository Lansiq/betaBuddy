## Gaussian Blur
import util as U
import cv2


for k in range(1,8):
    print("Testing Wall",k,":")
    
    testImg = U.inputImage("Wall"+str(k)+".JPEG")
    U.printImage(testImg)

    for i in range(3,23,2):
        
        imgMSF = U.Blur(testImg,i)

        U.saveImage(imgMSF, "Blur/wall"+str(k)+"_output"+str(i))
