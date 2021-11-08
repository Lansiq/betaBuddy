## Mean Shift Filtering
import util as U
import cv2

for k in range(1,8):
    println("Testing Wall",k,":")
    
    testImg = U.inputImage("Wall"+str(k)+".JPEG")

for i in range(30,40,10):
    for j in range(10,30,10):
        print(i," ", j)
        imgMSF = cv2.pyrMeanShiftFiltering(testImg,i,j)

        U.saveImage(imgMSF, "Blur/wall"+str(k)+"_output"+str(i)+str(j))
