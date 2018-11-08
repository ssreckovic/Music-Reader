from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

#make the image exclusively 0 or 1 (black or white)
def binaryTransform(image):
    gray = image.convert('L')  #conversion to gray scale
    bw = gray.point(lambda x: 0 if x<200 else 255, '1')  #binarization

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
    i=0
    thickness = 1
    while i< len(lineArray)-1:
        if lineArray[i] + 1 == lineArray[i+1]:
            thickness +=1
        else:
            lineThicknesses.append(thickness)
            thickness = 1
        i+=1
    lineThicknesses.append(thickness+1)
    print "Linewidths:" + str(lineThicknesses)

    if all(val==lineThicknesses[0] for val in lineThicknesses):
        return [lineThicknesses[0]]

    return lineThicknesses


def findSpacesSize(lineArray, lineThickness):

    lineDistances =[]

    for i in range(len(lineArray)-1):
        lineDistances.append(lineArray[i+1] - lineArray[i])

    #gets the mode of the array(most common space size)
    print "Line distances" + str(lineDistances)
    spacesCount = Counter(lineDistances)
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
            return spaceSizeArr
        i+=1

    #shouldnt happen
    #raise
    print "I should not be here!!!!! (findSpacesSize)"
    return 0


def main():
    imageFilePath = 'oneLine.png'#'easyTestSheetMusic.png'
    image = Image.open(imageFilePath)
    imageArray = np.array(image)


    bw = binaryTransform(image)
    bwArray = np.array(bw)
    picWidth = len(bwArray[0])

    horzPicCount = horizontalProjection(bwArray)
    lineArray = getLines(horzPicCount,picWidth)
    lineThickness = findBarLineWidth(lineArray)
    spaceSize = findSpacesSize(lineArray,lineThickness)

    import imagePreprocessing
    imagePreprocessing.main(bw,horzPicCount, lineArray, lineThickness,spaceSize)


    # imgplot = plt.imshow(bw)
    # plt.show()

if __name__ == "__main__":
    main()
