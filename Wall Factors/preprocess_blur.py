## Gaussian Blur
import util as U
import cv2


for k in range(1,8):
    println("Testing Wall",k,":")
    
    testImg = U.inputImage("Wall"+str(k)+".JPEG")

    for i in range(3,23,2):
        
        imgMSF = U.Blur(testImg,i)

        U.saveImage(imgMSF, "Blur/wall"+str(k)+"_output"+str(i))
