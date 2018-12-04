from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

import staffSegmentation #for sake of testing
from boundingBox import BoundingBox


def main():
    #classifier split into categories:
    # 1. has note head
    #     a. single note head
    #     b. multiple note heads
    #         i. single line
    #         ii. connected line
    #     Determining tail type, if any
    # 2. no note head
    #     a. sharp, natural, flat
    #     b. clef
    #     c. barlines/double barline
    #     d. other (cota, time signature, crecendo accents etc)

    # undetermined = []
    # for i in range(len(bBoxes)):
    #     undetermined.append(i)

    imageFilePath = "singleNote.png"
    img = cv.imread(imageFilePath,0)
    testBoxes = readInTest(img)

    #NoteHeads(bBoxes) # does this actually change the values? (side effect)
    print testBoxes[0].grid
    testBoxImg = np.array(testBoxes[0].grid)
    cv.imwrite('singleOutput.png', testBoxImg)
    #cv.imshow("image",testBoxImg)
    # for box in bBoxes:
    #     if box.noteHeads == 0:
    #         #do other things to determine what it is!
    #     else:
    #         #do things that you do with notes?
            # 1. determine type of note (filled or not)
            # 2. if not filled, num of tails
            # 3. multi or single note!

    #does it make sense to do all notes in a category first? or loop through
    #and determine as you go which find in where
def readInTest(img):
    ret2,bw = cv.threshold(img,170,255,cv.THRESH_BINARY)
    pixels = np.array(bw)
    #cv.imwrite('singleOutput.png', pixels)
    col = 0
    boxes = []
    picHeight = len(bw)
    for row in range(picHeight):
        #if a black pixel is found traverse through the neighboring ones to find the edges of the object
        #and then make a bounding box for it.
        if pixels.item(row,col) == 0:
            [minCol, maxCol, minRow, maxRow, pixLocations] = staffSegmentation.pixelTraversal(pixels, col, row)

            box = BoundingBox([minRow,minCol], (maxCol - minCol), (maxRow - minRow), pixLocations)
            #print pixLocations
            print len(pixLocations) #shows actual locations
            boxes.append(box)
            break

    return boxes


def NoteHeads(bBoxes):

    for box in bBoxes:
        #definitely needs to be changed
        circles = cv2.HoughCircles(box.grid,cv2.HOUGH_GRADIENT,1,20,param1=50,param3=30,minRadius=0,maxRadius=0)
        #note where the heads are! and save them for placement later
        box.numNoteHeads = len(circles)


if __name__ == "__main__":
    main()
