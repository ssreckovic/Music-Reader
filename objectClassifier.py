from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv

def main():






    # img = cv.imread('oneLine.png',0)
    # th3 =  cv.GaussianBlur(img, (3,3),4)
    # th4 =  cv.GaussianBlur(img, (3,3),2)
    # ret2,th3 = cv.threshold(th3,150,255,cv.THRESH_BINARY)
    # ret3,th4 = cv.threshold(th4,150,255,cv.THRESH_BINARY)
    # #img = cv.medianBlur(img,3)
    # # th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
    # #         cv.THRESH_BINARY,23,2)
    # ret,th1 = cv.threshold(img,200,255,cv.THRESH_BINARY)
    # # th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
    # #     cv.THRESH_BINARY,17,2)
    #
    # #th2 = cv.medianBlur(th1,2)
    # th2 = cv.GaussianBlur(th1, (3,3),3)
    # #ret3,th4 = cv.threshold(th2,200,255,cv.THRESH_BINARY)
    # plt.subplot(2,2,1),plt.imshow(th1,'gray')
    # plt.title("Binary Threshold")
    # plt.subplot(2,2,2),plt.imshow(th2,'gray')
    # plt.title("Binary + Gauss Blur")
    # plt.subplot(2,2,3),plt.imshow(th3,'gray')
    # plt.title("Gauss + Binary")
    # plt.subplot(2,2,4),plt.imshow(th4,'gray')
    # plt.title("Binary + Gauss + Binary")
    # #plt.imshow(th1,'gray')
    # plt.show()
    return 0

if __name__ == "__main__":
    main()
