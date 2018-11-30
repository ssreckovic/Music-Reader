from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv

def main():
    undetermined = []
    for i in range(len(bBoxes)):
        undetermined.append(i)
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

    return 0

def NoteHeads(bBoxes):
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param3=30,minRadius=0,maxRadius=0)

    numNoteHeads = len(circles)
    
if __name__ == "__main__":
    main()
