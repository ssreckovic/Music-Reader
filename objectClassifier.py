from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv


def main(bBoxes):
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

    NoteHeads(bBoxes) # does this actually change the values? (side effect)

    for box in bBoxes:
        if box.noteHeads == 0:
            #do other things to determine what it is!
        else:
            #do things that you do with notes?
            # 1. determine type of note (filled or not)
            # 2. if not filled, num of tails
            # 3. multi or single note!

    #does it make sense to do all notes in a category first? or loop through
    #and determine as you go which find in where

def NoteHeads(bBoxes):

    for box in bBoxes:
        #definitely needs to be changed
        circles = cv2.HoughCircles(box.grid,cv2.HOUGH_GRADIENT,1,20,param1=50,param3=30,minRadius=0,maxRadius=0)
        #note where the heads are! and save them for placement later
        box.numNoteHeads = len(circles)


if __name__ == "__main__":
    main()
