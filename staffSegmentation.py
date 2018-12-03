from PIL import Image
import numpy as np
import cv2 as cv
from boundingBox import BoundingBox

def main(bwImg, lineLocations, barLineWidth,spaceSize,spaceBetweenBars):


    pixels = np.array(bwImg) #pixels(row, col)
    picWidth = len(bwImg[0]) #bwImg.size[0]
    picHeight = len(bwImg)   #bwImg.size[1]

    pixels = removeBarLines(lineLocations, pixels,barLineWidth, picWidth)
    #[minCol, maxCol, minRow, maxRow, pixLocations] = pixelTraversal(pixels, 26, 88)
    # print [minCol, maxCol, minRow, maxRow, pixLocations]
    bBoxes = findObjects(pixels,picWidth, picHeight)
    drawBoundingBox(pixels, bBoxes)
    #bBoxes = sortObjects(bBoxes,spaceBetweenBars, spaceSize, lineLocations)

    # for box in bBoxes:
    #     box.showInfo()

    #pixels.save('testOutput.png')
    cv.imwrite('testOutput.png', pixels)
    #cv.imshow("image", pixels);
    #cv.waitKey();


#removes the bar lines from the sheet music
def removeBarLines(lineLocations,pixels, barLineWidth, picWidth):

    oneLineThickness = (len(barLineWidth) == 1)
    lineThickness = barLineWidth[0]

    lineNum = 0
    lineCounter = 0
    while lineNum < len(lineLocations):
        if not oneLineThickness:
            lineThickness = barLineWidth[lineCounter]

        pixels = eraseLine(lineThickness, lineLocations[lineNum],pixels, picWidth)
        #lineNum+=lineThickness
        lineNum+=1
        lineCounter +=1


    return pixels

#removes a single line with given thickness from the sheet music without
#effecting any other objects on the sheet
def eraseLine(thickness, startLine, image, picWidth):

    #************************************************************
    #can be improved! some notes dont look the same as before etc!
    #***********************************************************

    topLine = startLine
    botLine = startLine + thickness -1
    for col in range(picWidth):
        if image.item(topLine,col) == 0 or image.item(botLine,col) == 0:
            if image.item(topLine-1, col) == 255 and image.item(botLine+1,col) == 255:
                for j in range(thickness):
                    image.itemset((topLine+j,col),255)
            elif image.item(topLine - 1, col) == 255 and image.item(botLine+1,col) == 0:
                thick = thickness/2
                if thick < 1:
                    thick = 1
                for j in range(thick):
                    image.itemset((topLine + j, col),255)

            elif image.item(topLine - 1, col) == 0 and image.item(botLine+1,col) == 255:
                thick = thickness/2
                if thick < 1:
                    thick = 1
                for j in range(thick):
                    image.itemset((botLine - j, col),255)

    return image

#makes a vertical projection of the pixels in the pictures
def findObjects(pixels, picWidth, picHeight):

    vertCount = [0] * picWidth
    boxList = []

    for col in range(picWidth):
        count = 0
        for row in range(picHeight):

            #if a black pixel is found traverse through the neighboring ones to find the edges of the object
            #and then make a bounding box for it.
            if pixels.item(row,col) == 0:
                [minCol, maxCol, minRow, maxRow, pixLocations] = pixelTraversal(pixels, col, row)
                #if its just 1 pixel found
                # if [minCol, maxCol, minRow, maxRow] == [col,col,row,row]:
                #     pixels[col,row] = 255
                # else:
                box = BoundingBox([minRow,minCol], (maxCol - minCol), (maxRow - minRow), pixLocations)
                boxList.append(box)

    return boxList

#recursively traverses nearby pixels that are black and finds the minimum and maximum column
#and row values for the object
def pixelTraversal(pixels, startCol, startRow):

    up = [-1,0]
    down = [1,0]
    left = [0,-1]
    right = [0,1]

    pixels.itemset((startRow,startCol),100)
    minCol = startCol
    maxCol = startCol
    minRow = startRow
    maxRow = startRow
    pixLocations = [[startRow, startCol]]
    directions = [left,right, up, down]
    height,width = pixels.shape


    for i in range(len(directions)):
        if (startRow + directions[i][0]) >=0 and (startRow + directions[i][0]) < height and (startCol + directions[i][1]) >=0 and (startCol + directions[i][1]) < width:
            if pixels.item((startRow + directions[i][0]), (startCol + directions[i][1])) == 0:
                [tempMinCol, tempMaxCol, tempMinRow, tempMaxRow, location] = pixelTraversal(pixels, (startCol + directions[i][1]), (startRow + directions[i][0]))

                if tempMinCol < minCol:
                    minCol = tempMinCol
                if tempMaxCol > maxCol:
                    maxCol = tempMaxCol
                if tempMinRow < minRow:
                    minRow = tempMinRow
                if tempMaxRow > maxRow:
                    maxRow = tempMaxRow
                pixLocations += location

    return [minCol,maxCol, minRow, maxRow, pixLocations]

#draws bounding boxes around the found objects
def drawBoundingBox(pixels, boxList):

    for box in boxList:
        origin = box.origin
        height = box.height
        width = box.width
        i = 0
        while i <= height:
            pixels.itemset((origin[0] + i, origin[1]), 0)
            pixels.itemset((origin[0] + i, origin[1]+width),0)
            i+=1
        i=0
        while i <= width:
            pixels.itemset((origin[0],origin[1] + i),0)
            pixels.itemset((origin[0] + height, origin[1] + i ),0)
            i+=1

#sort the object in order from top left to top right, then down to the next row
def sortObjects(boxList, barSpace, spaceSize, lineLocations):

    boxList = quickSort(boxList,0,len(boxList)-1)

    sortedBoxes = []
    for i in range(len(lineLocations)/5):
        lineBoxes = []
        start = lineLocations[i*5]
        print lineLocations[i*5]
        upper = start - spaceSize[0] * 6
        lower = start + spaceSize[0] * 10
        for j in range(len(boxList)):
            if boxList[j].origin[0] >= upper and boxList[j].origin[0] <= lower:
                lineBoxes.append(boxList[j])

        sortedBoxes +=lineBoxes

    return sortedBoxes



def quickSort(alist,first,last):

    if first<last:

       splitpoint = partition(alist,first,last)

       quickSort(alist,first,splitpoint-1)
       quickSort(alist,splitpoint+1,last)

    return alist



def partition(alist,first,last):
   pivotvalue = alist[first]

   leftmark = first+1
   rightmark = last

   done = False
   while not done:

       while leftmark <= rightmark and (alist[leftmark].origin[1] <= pivotvalue.origin[1]):
           leftmark = leftmark + 1

       while rightmark >= leftmark and (alist[rightmark].origin[1] >= pivotvalue.origin[1]):
           rightmark = rightmark -1

       if rightmark < leftmark:
           done = True
       else:
           temp = alist[leftmark]
           alist[leftmark] = alist[rightmark]
           alist[rightmark] = temp

   temp = alist[first]
   alist[first] = alist[rightmark]
   alist[rightmark] = temp

   return rightmark



if __name__ == "__main__":
    main()
