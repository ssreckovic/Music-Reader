from PIL import Image
from collections import Counter
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import staffSegmentation

PIXEL_THRESHOLD = 170
#make the image exclusively 0 or 1 (black or white)
def binaryTransform(image):

    img =  cv.GaussianBlur(image, (3,3),4) #these values determined by trial
    ret2,bw = cv.threshold(img,PIXEL_THRESHOLD,255,cv.THRESH_BINARY)

    # gray = image.convert('L')  #conversion to gray scale
    # bw = gray.point(lambda x: 0 if x<200 else 255, '1')  #binarization

    return bw

#returns an array of the number of black pixels in each row of the picture
def horizontalProjection(bwArray):
    rows = len(bwArray)
    cols = len(bwArray[0])
    print "Rows:" + str(rows)
    print "Cols:" + str(cols)
    pixCount = [0] * rows

    for row in range(rows):
        for col in range(cols):
            if not bwArray[row][col]:
                pixCount[row] +=1

    return pixCount

#finds the rows that have black pixels along most of the picture
def getLines(pixArray, picWidth):
    lineArray = []
    for row in range(len(pixArray)):
        if pixArray[row] >= (picWidth * 0.8):
            lineArray.append(row) #append the row that the line is found in

    print "Lines found at: " + str(lineArray)
    return lineArray


def findBarLineWidth(lineArray):

    lineThicknesses = []
    newLineArray = []
    i=0
    thickness = 1
    while i< len(lineArray)-1:
        if thickness == 1:
            newLineArray.append(lineArray[i])

        if lineArray[i] + 1 == lineArray[i+1]:
            thickness +=1
        else:
            lineThicknesses.append(thickness)
            thickness = 1
        i+=1
    lineThicknesses.append(thickness+1)
    print "Linewidths:" + str(lineThicknesses)

    if all(val==lineThicknesses[0] for val in lineThicknesses):
        return [lineThicknesses[0],newLineArray]

    return [lineThicknesses,newLineArray]


def findSpacesSize(lineArray, lineThickness):

    lineDistances =[]

    for i in range(len(lineArray)-1):
        lineDistances.append(lineArray[i+1] - lineArray[i])

    #gets the mode of the array(most common space size)
    print "Line distances" + str(lineDistances)
    spacesCount = Counter(lineDistances)
    spaceBetweenBars = max(lineDistances)
    tempSpaceInfo = spacesCount.most_common(1)


    commonSize = tempSpaceInfo[0][0]
    tempCommon = 0
    if commonSize == 1:
        j=0
        while j<len(lineDistances):
            if lineDistances[j] != 1:
                tempCommon = lineDistances[j]
                if lineDistances[j+lineThickness[0]] > (tempCommon-1)*0.9 and lineDistances[j+lineThickness[0]] < (tempCommon+1)*1.1:
                    commonSize = tempCommon
                    break
            j+=1


    i=0
    count = 0
    spaceSizeArr = []

    while i < len(lineDistances):
        #space sizes can be inconsistent, so if its within ~10% then its accepted
        if lineDistances[i] > (commonSize-1)*0.9 and lineDistances[i] < (commonSize+1)*1.1:

            spaceSizeArr.append(lineDistances[i])
            count+=1
        else:
            if lineDistances[i] != 1: #if its 1 then its part of the same line so dont reset
                count = 0
                spaceSizeArr = []

        if count == 4:
            print "Spaces size:" + str(spaceSizeArr)
            return [spaceSizeArr,spaceBetweenBars]
        i+=1

    #shouldnt happen
    #raise
    print "I should not be here!!!!! (findSpacesSize)"
    return []



def main():
    #imageFilePath = 'oneLine.png'
    imageFilePath = 'easyTestSheetMusic.png'
    #image = Image.open(imageFilePath)
    image = cv.imread(imageFilePath,0)

    #image = cv2.medianBlur(image,2)

    bw = binaryTransform(image)
    #bw =
    bwArray = np.array(bw)
    picWidth = len(bwArray[0])

    horzPicCount = horizontalProjection(bwArray)
    lineArray = getLines(horzPicCount,picWidth)
    lineThickness, newLineArray = findBarLineWidth(lineArray)
    lineArray = newLineArray
    print lineArray
    spaceSize, spaceBetweenBars = findSpacesSize(lineArray,lineThickness)

    # plt.imshow(bw,'gray')
    # plt.show()
    # for i in range(len(bwArray[0])):
    #     print bwArray.item(i,10)
    staffSegmentation.main(bw, lineArray, lineThickness,spaceSize, spaceBetweenBars)



if __name__ == "__main__":
    main()
