from boolean_image.basemanipulator import BaseManipulator


class CenterParameters(object):
    """
    Contain values pertinent to centering a BI
    """
    def __init__(self):
        #Edges; numPixels from edge to find first active pixel
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None
        
        #numPixels to shift each active pixel along respective axis
        self.shiftX = None
        self.shiftY = None

        #Effective direction and starting point to shift pixels
        self.intervalX = None
        self.intervalY = None
        return

    def swapLeftRight(self):
        """
        Swap the values for the right and left edges

        Use to shift pixels left from left to right, or shift right
        from right to left
        """
        self.left, self.right = self.right, self.left
        return

    def swapTopBottom(self):
        """
        Swap the values for the top and bottom edges

        Use to shift pixels up from top to bottom, or shift down from
        bottom to top
        """
        self.top, self.bottom = self.bottom, self.top
        return


class Center(BaseManipulator):
    """
    Center the activated region of a BI
    """
    def __init__(self, array, x=None, y=None):
       #BaseBinaryImageArrayManipulator.__init__(self, array, x, y)
        self._toCenter = CenterParameters()
        self._setCenterParameters()
        return

    def center(self):
        """
        Centers self.image
        """
        #Populate self.toCenter parameters
        self._setCenterParameters()
        self._setShifts()

        #Shift active region of BIA accordingly
        self._shift()
        return

    @staticmethod
    def _getRange(line):
        """
        Return tuple of two coordinates spanning the range of active
        pixels on line

        Return tuple of two Nones when there is no active region; line
        is a 1D array
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

    def _setCenterParameters(self):
        """
        Populate self._toCenter parameters
        """

        #Retrive edge values
        BaseManipulator._setEdges(self)

        #Expect 1:1 correspondance initially
        self._toCenter.left = self._activeEdges.left
        self._toCenter.right = self._activeEdges.right
        self._toCenter.top = self._activeEdges.top
        self._toCenter.bottom = self._activeEdges.bottom

        #Reset retrieved edges
        self._activeEdges.reset()
        return

    def _setShifts(self):
        """
        Populate self._toCenter.shift values
        """
        top = self.height - self._toCenter.top
        right = self.width - self._toCenter.right

        #Subtract 1 before floor division to round down on evens
        self._toCenter.shiftX = (right - self._toCenter.left - 1) // 2
        self._toCenter.shiftY = (top - self._toCenter.bottom - 1) // 2
        self._adjustEdges()
        return

    def _adjustEdges(self):
        """
        Modify edge, and shift values to reflect their role in further
        operations on BI

        Shift operations run in place; to prevent information loss,
        active pixels may only be shifted into regions without active
        pixels; when shifting right, shifting begins with the right
        most column of pixels. 

        i.e:
         _ _ _ _ _      _ _ _ _ _
        | |X|X| | | => | |X| | |X|
         ‾ ‾ ‾ ‾ ‾      ‾ ‾ ‾ ‾ ‾
        the self.interval values store the direction of the shift, 
        i.e. -1 is left to right.
        But, the range iteraterd through is always written right to
        left,
        i.e. range(right, left, 1). So, when the direction is
        negative, swap the axis' edge values
        i.e. range(left, right -1)
        """
        if self._toCenter.shiftX >= 0:
            self._toCenter.left -= 1
            self._toCenter.swapLeftRight()
            self._toCenter.intervalX = -1
        else:
            self._toCenter.right += 1
            self._toCenter.intervalX = 1

        if self._toCenter.shiftY >= 0:
            self._toCenter.bottom -= 1
            self._toCenter.intervalY = -1
        else:
            self._toCenter.top += 1
            self._toCenter.swapTopBottom()
            self._toCenter.intervalY = 1
        return

    def _shift(self):
        """
        Shift active region of BIA in place

        self._adjustEdges() must be called before self._shift()
        """
        #From top to bottom shift each row appropriately
        for i in range(
                self._toCenter.top, 
                self._toCenter.bottom, 
                self._toCenter.intervalY):
            self._shiftRow(self.image[i])

            #If a y-axis shift is required, move current row into
            #inactive region
            if self._toCenter.shiftY != 0:
                for j in range(len(self.image[i])):
                    self.image[i + self._toCenter.shiftY][j] = (
                        self.image[i][j] )
                    self.image[i][j] = 0
        return

    def _shiftRow(self, row):
        """
        Shift active region of line
        """
        #Handle null case
        if self._toCenter.shiftX == 0:
            return

        #Move each pixel left to right into inactive space
        for i in range(
                self._toCenter.left, 
                self._toCenter.right, 
                self._toCenter.intervalX):
            row[i + self._toCenter.shiftX] = row[i]
            row[i] = 0
            pass
        return

    def _resetParameters(self):
        """
        Set each parameter of paramters object to their defaults

        Also, call in initializer to ensure consistency
        """
        #Set top and left edge values to size of row/column; 1 outside
        #of index range
        self._toCenter.top = self.height
        self._toCenter.left = self.width
        self._toCenter.bottom = -1
        self._toCenter.bottom = -1
        self._toCenter.shiftX = None
        self._toCenter.shiftY = None
        self._toCenter.intervalX = None
        self._toCenter.intervalY = None
        return
