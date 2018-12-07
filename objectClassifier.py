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

    undetermined = []
    for i in range(len(bBoxes)):
        undetermined.append(i)

    imageFilePath = "Test Pictures/singleNote.png"
    img = cv.imread(imageFilePath,0)
    testBoxes = readInTest(img)

    #NoteHeads(bBoxes) # does this actually change the values? (side effect)
    testBoxImg = np.array(testBoxes[0].grid)
    circles = NoteHeads(testBoxes)
    #cv.imwrite('singleOutput.png', testBoxImg)
    #cv.imshow("image",testBoxImg)
    for box in bBoxes:
        if box.noteHeads == 0:
            #do other things to determine what it is!
        else:
            #do things that you do with notes?
            1. determine type of note (filled or not)
            2. if not filled, num of tails
            3. multi or single note!

    #does it make sense to do all notes in a category first? or loop through
    #and determine as you go which find in where
def readInTest(img):
    ret2,bw = cv.threshold(img,170,255,cv.THRESH_BINARY)
    pixels = np.array(bw)
    #cv.imwrite('singleOutput.png', pixels)
    col = 0
    boxes = []
    picHeight = len(bw)
    picWidth = len(bw[0])

    for col in range(picWidth):
        for row in range(picHeight):
            #if a black pixel is found traverse through the neighboring ones to find the edges of the object
            #and then make a bounding box for it.
            if pixels.item(row,col) == 0:
                [minCol, maxCol, minRow, maxRow, pixLocations] = staffSegmentation.pixelTraversal(pixels, col, row)

                box = BoundingBox([minRow,minCol], (maxCol - minCol), (maxRow - minRow), pixLocations)
                boxes.append(box)
                break

    return boxes


def NoteHeads(bBoxes):


    imageFilePath = 'Test Pictures/SingleNoteSpace.png'
    img = cv.imread(imageFilePath,0)
    sets = [
            [1,60,50,200,5,2],
            [1,60,50,200,3,1],
            [1,60,300,300,5,1],
            [1,60,50,200,5,10],
            [1,60,50,200,1,3]
        ]
    #tempImg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
    for i in range(len(sets)):
        cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
        circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,sets[i][0],sets[i][1],sets[i][2],sets[i][3],sets[i][4],sets[i][5])
        #circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,100,50,200,1,10)
        circles = np.uint16(np.around(circles))
        for j in circles[0,:]:
            cv.circle(cimg,(j[0],j[1]),j[2],(0,255,0))

        fileName = "Output Pictures/outPic" + str(i) + ".png"
        cv.imwrite(fileName, cimg)
        print fileName + " printed"
    # for box in bBoxes:
    #     # img = np.array(box.grid)
    #     # cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
    #     #definitely needs to be changed
    #     circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,100,50,200,1,10)
    #     print circles
    #
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0,:]:
    #         # draw the outer circle
    #         cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    #     #note where the heads are! and save them for placement later
    #     box.numNoteHeads = len(circles)
    #


    return circles



if __name__ == "__main__":
    main()
