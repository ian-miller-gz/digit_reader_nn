class ActiveEdges(object):
    """
    Contain values pertinent to centering a BI
    """
    def __init__(self):
        #Edges; numPixels from edge to find first active pixel
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

    def reset(self):
        """
        Set each edge to None

        Hopefully invoke an error, or be traceable since these values
        should never be called without being immediately determined
        prior

        Determining these values is expensive. So, do not wrap their
        generation in a property; it is not obvious they are
        expensive
        """
        self.__init__()


class BaseManipulator(object):
    """
    Two-dimensional array of 1's and 0's which represent the active
    and inactive regions of depictive images / characters

    Can define an active region, a smallest possible square capable of
    containing the active region. Define by finding distance inward
    the total image size to the active region from each eadge - store
    as ActiveEdges object
    """
    def __init__(self, array, x=None, y=None):
        if not x or not y:
            assert len(array[0]), "{} is flat; Require dimensions".format(array)
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
        """
        Populate two-dimensional array from elements in a
        one-dimensional array

        width and height are determined by x and y parameters
        """
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
        """
        Return tuple of two coordinates spanning the range of active
        pixels on line

        Return tuple of two Nones when there is no active region;
        line is a 1D array
        """
        left = len(line) + 1
        right = -1
        isFound = False
        for i, eachItem in enumerate(line):

            #Update the right-most pixel coordinate with each
            #new-found active pixel
            if eachItem:
                right = i

                #Only check for the left-most pixel until the first
                #pixel is found
                if not isFound:
                    isFound = True
                    left = i

        #If right is still -1, then no active pixel exists in region
        return (left, right) if right >= 0 else (None, None)

    def _setEdges(self):
        """
        Set edge values stored in self._activeEdges

        Edge values are distance inward from 0, size of array in
        either dimension to the first row or column containing an
        active pixel
        """
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

