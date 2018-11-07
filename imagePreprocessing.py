from PIL import Image

def main(bwImg, pixCountArr, lineLocations, barLineWidth,spaceSize):

    pixels = bwImg.load()
    picWidth = bwImg.size[0]
    pixels = removeBarLines(lineLocations, pixels,barLineWidth, picWidth)

    bwImg.save('testOutput.png')


def removeBarLines(lineLocations,pixels, barLineWidth, picWidth):

    oneLineThickness = (len(barLineWidth) == 1)
    lineThickness = barLineWidth[0]

    lineNum = 0

    while lineNum < len(lineLocations):
        lines = []#holds the vertical coord value of the line
        if not oneLineThickness:
            lineThickness = barLineWidth[lineNum %5]
        
        pixels = eraseLine(lineThickness, lineLocations[lineNum],pixels, picWidth)
        lineNum+=lineThickness


    return pixels


def eraseLine(thickness, startLine, image, picWidth):

    topLine = startLine
    botLine = startLine + thickness -1

    for col in range(picWidth):
        if image[col,topLine] == 0 and image[col,botLine] == 0:
                #if image[col,topLine-1] == 255 or image[col,botLine+1] == 255:
            for j in range(thickness):
                    image[col,topLine+j] = 255


    return image





if __name__ == "__main__":
    main()
