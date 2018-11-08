from PIL import Image
from boundingBox import BoundingBox

def main(bwImg, horzCount, lineLocations, barLineWidth,spaceSize):

    pixels = bwImg.load()
    picWidth = bwImg.size[0]
    picHeight = bwImg.size[1]
    pixels = removeBarLines(lineLocations, pixels,barLineWidth, picWidth)
    bBoxes = verticalSearch(pixels,picWidth, picHeight)
    drawBoundingBox(pixels, bBoxes)

    # [minCol, maxCol, minRow, maxRow,location] = pixelTraversal(pixels, 479, 102)
    # box = BoundingBox([minCol,minRow], (maxCol - minCol), maxRow - minRow)
    # print minCol, maxCol, minRow, maxRow
    # print len(location)
    #box.showInfo()
    bwImg.save('testOutput.png')


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
        lineNum+=lineThickness
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
        if image[col,topLine] == 0 or image[col,botLine] == 0:
            if image[col,topLine-1] == 255 or image[col,botLine+1] == 255:
                for j in range(thickness):
                        image[col,topLine+j] = 255

    return image

#makes a vertical projection of the pixels in the pictures
def verticalSearch(pixels, picWidth, picHeight):

    vertCount = [0] * picWidth
    boxList = []

    for col in range(picWidth):
        count = 0
        for row in range(picHeight):

            #if a black pixel is found traverse through the neighboring ones to find the edges of the object
            #and then make a bounding box for it.
            if pixels[col,row] == 0:
                [minCol, maxCol, minRow, maxRow, pixLocations] = pixelTraversal(pixels, col, row)
                box = BoundingBox([minCol,minRow], (maxCol - minCol), maxRow - minRow, pixLocations)
                boxList.append(box)

    return boxList

#recursively traverses nearby pixels that are black and finds the minimum and maximum column
#and row values for the object
def pixelTraversal(pixels, startCol, startRow):

    pixels[startCol,startRow] = 100
    minCol = startCol
    maxCol = startCol
    minRow = startRow
    maxRow = startRow
    pixLocations = [[startCol, startRow]]
    directions = [[1,0],[0,-1],[0,1],[-1,0]]#[[0,-1],[-1,0],[0,1],[1,0]]

    for i in range(len(directions)):

        if pixels[(startCol + directions[i][0]), (startRow + directions[i][1])] == 0:
            [tempMinCol, tempMaxCol, tempMinRow, tempMaxRow, location] = pixelTraversal(pixels, (startCol + directions[i][0]), (startRow + directions[i][1]))
            
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
            pixels[origin[0],origin[1] + i] = 0
            pixels[origin[0]+width,origin[1] + i] = 0
            i+=1

        i=0
        while i <= width:
            pixels[origin[0]+i,origin[1]] = 0
            pixels[origin[0]+i,origin[1]+height] = 0
            i+=1




if __name__ == "__main__":
    main()
