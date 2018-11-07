from PIL import Image
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

#make the image exclusively 0 or 1 (black or white)
def binaryTransform(image):
    gray = image.convert('L')  #conversion to gray scale
    bw = gray.point(lambda x: 0 if x<128 else 255, '1')  #binarization

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

    #********************************************************
    #ASSUMING THAT THE FIRST LINE IN LIST IS A BARLINE!!!!!!
    #********************************************************
    lineWidths = []
    barCounter = 0
    i=0

    while barCounter < 5: #num bar Lines
        widthSum = 1
        while True:
            if lineArray[i] == (lineArray[i+1]-1):
                widthSum +=1
                i+=1
            else:
                break
        lineWidths.append(widthSum)
        i+=1
        barCounter +=1


    print "Linewidths:" + str(lineWidths)

    if all(val==lineWidths[0] for val in lineWidths):
        return [lineWidths[0]]

    return lineWidths


def findSpacesSize(lineArray):

    lineDistances =[]

    for i in range(len(lineArray)-1):
        lineDistances.append(lineArray[i+1] - lineArray[i])

    #gets the mode of the array(most common space size)
    print "Line distances" + str(lineDistances)
    spacesCount = Counter(lineDistances)
    tempSpaceInfo = spacesCount.most_common(1)

    commonSize = tempSpaceInfo[0][0]
    occurances = tempSpaceInfo[0][1]

    #if >70% of line distances are commonSize then all space sizes are the same
    if occurances / len(lineDistances) > 0.7:
        print "Spaces Size: " + str(commonSize)
        return [commonSize]
    else:
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
    imageFilePath = 'easyTestSheetMusic.png'
    image = Image.open(imageFilePath)
    imageArray = np.array(image)

    # pixels = image.load() # create the pixel map
    #
    # for i in range(image.size[0]):    # for every col:
    #     for j in range(image.size[1]):    # For every row
    #         print pixels[i,j]

    bw = binaryTransform(image)
    bwArray = np.array(bw)
    #print bwArray
    picWidth = len(bwArray[0])

    pixCountArr = horizontalProjection(bwArray)
    lineArray = getLines(pixCountArr,picWidth)
    barLineWidth = findBarLineWidth(lineArray)
    spaceSize = findSpacesSize(lineArray)

    import imagePreprocessing
    imagePreprocessing.main(bw,pixCountArr, lineArray, barLineWidth,spaceSize)


    # imgplot = plt.imshow(bw)
    # plt.show()

if __name__ == "__main__":
    main()
