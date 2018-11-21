class BoundingBox:
    def __init__(self, origin, width, height, pixLocations):
        self.origin = origin
        self.width = width
        self.height = height
        self.blackPix = pixLocations

        self.grid = self.makeGrid() #pixLocations,width,Height)

    def showInfo(self):
        print "origin " + str(self.origin)
        #print "width " + str(self.width)
        #print "height " + str(self.height)


    #makes a grid of the 
    def makeGrid(self):
        grid = [[255]*(self.width+1)]*(self.height+1)

        blackPix = self.blackPix

        for i in range(len(blackPix)-1):
            grid[blackPix[i][0] - self.origin[0]][blackPix[i][1] - self.origin[1]] = 0

        return grid
