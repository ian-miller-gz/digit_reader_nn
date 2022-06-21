class ActiveEdges(object):
    #Edges of active region
    def __init__(self):
        #Edges; numPixels from edge to find first active pixel
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

    def reset(self):
        self.__init__()


class BaseManipulator(object):
    #Crop Black/White field based on activity.
    def __init__(self, array, x=None, y=None):
        if not x or not y:
            self.image = array
            self.height = len(array)
            self.width = len(array[0])
        else:
            self.image = BaseManipulator._construct(array, x, y)
            self.height = y
            self.width = x
        self._activeEdges = ActiveEdges()
        return

    @property
    def flatImage(self):
        return [item for row in self.image for item in row]

    @staticmethod
    def _construct(array, x, y):
        #Populate field
        assert len(array) == x * y, "{} is not the correct size; {} * {}".format(
            array, x, y)

        result = [[] for i in range(x)]

        #Iterate in reverse to flip y-axis to fix both axis origins
        #on top of each other
        i = 0
        for j, each in enumerate(array[::-1]):
            if each:
                result[i].insert(0, 1)
            else:
                result[i].insert(0, 0)
            i += 1 if (j + 1) % y == 0 else 0
        return result

    @staticmethod
    def _getRange(line):
        #Return coordinates spanning the range of active pixels on line
        left = len(line) + 1
        right = -1
        isFound = False
        for i, eachItem in enumerate(line):

            #Update the right-most coordinate when a active pixel is found
            if eachItem:
                right = i

                #Left-most coordinate is the first active pixel
                if not isFound:
                    isFound = True
                    left = i

        #If right is still -1, then no active pixel exists in region
        return (left, right) if right >= 0 else (None, None)

    def _setEdges(self):
        #Set edge values stored in self._activeEdges
        
        #Initialize egdge values to their limits
        self._activeEdges.bottom, self._activeEdges.top = (
            -1, self.height)
        self._activeEdges.right, self._activeEdges.left = (
            -1, self.width)
        isFoundBottom = False
        for i, eachRow in enumerate(self.image):

            #Get range of active pixels for each row
            newLeft, newRight = self._getRange(eachRow)
            if (newLeft != None):

                #Update x-axis edges if found
                if newLeft < self._activeEdges.left:
                    self._activeEdges.left = newLeft
                if newRight > self._activeEdges.right:
                    self._activeEdges.right = newRight

                #reading upward, the first row with an active pixel
                #finds self.bottom
                if not isFoundBottom:
                    self._activeEdges.bottom = i
                    isFoundBottom = True

                #Every row with an active pixel updates top-most pixel
                self._activeEdges.top = i
        return

