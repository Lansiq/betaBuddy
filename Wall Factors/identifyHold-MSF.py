## Mean Shift Filtering; overlay of result of Canny edge detection
import util as U

testImg = U.inputImage("IMG_6354.JPEG")

#U.printImage(testImg)

U.plotImage(testImg)

testImg = U.Gray(testImg)

U.plotImage(testImg)

U.saveImage(testImg)