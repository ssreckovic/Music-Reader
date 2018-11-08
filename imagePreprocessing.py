from PIL import Image
import boundingBox

def main(bwImg, horzCount, lineLocations, barLineWidth,spaceSize):

    pixels = bwImg.load()
    picWidth = bwImg.size[0]
    picHeight = bwImg.size[1]
    pixels = removeBarLines(lineLocations, pixels,barLineWidth, picWidth)
    x = verticalSearch(pixels,picWidth, picHeight)
    # as test [minCol, maxCol, minRow, maxRow] = pixelTraversal(pixels, 289, 141)
    #horizontalCuts

                # vertical projection only done after horizontal cuts are made to cut the
                # image into specfic bar lines, it will be done to each section
                # vertCount = verticalProjection(pixels, picWidth,picHeight)

    #propogate vertically when pixel hit turn it red and recursively(BFS?) go through until
    #no more new pixels found. Keep track of min & max x-y values and then create
    #a bounding box object that contains the lineLocations
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

    for col in range(picWidth):
        count = 0
        for row in range(picHeight):
            if pixels[col,row] == 0:
                [minCol, maxCol, minRow, maxRow] = pixelTraversal(pixels, col, row)
                #put these in boundng boxes afterwards
    return 0

def pixelTraversal(pixels, startCol, startRow):

    pixels[startCol,startRow] = 128
    minCol = startCol
    maxCol = startCol
    minRow = startRow
    maxRow = startRow

    directions = [[1,0],[0,-1],[0,1],[-1,0]]#[[0,-1],[-1,0],[0,1],[1,0]]

    for i in range(len(directions)):

        if pixels[(startCol + directions[i][0]), (startRow + directions[i][1])] == 0:
            [tempMinCol, tempMaxCol, tempMinRow, tempMaxRow] = pixelTraversal(pixels, (startCol + directions[i][0]), (startRow + directions[i][1]))
            #print 'col and row ' + str(startCol + directions[i][0]) + ',' + str(startRow + directions[i][1])
            if tempMinCol > minCol:
                minCol = tempMinCol
            if tempMaxCol > maxCol:
                maxCol = tempMaxCol
            if tempMinRow < minRow:
                minRow = tempMinRow
            if tempMaxRow > maxRow:
                maxRow = tempMaxRow

    return [minCol,maxCol, minRow, maxRow]


if __name__ == "__main__":
    main()
