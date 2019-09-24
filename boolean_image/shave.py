from boolean_image.basemanipulator import BaseManipulator

class Shave(BaseManipulator):
    """
    BI manipulator which removes as much inactive region as possible
    while returning a square
    """
    def __init__(self, *args, **kwargs):
        return

    def shave(self):
        """
        Remove, in place, rows and columns surrounding BI without
        active pixels
        """
        #Populate self._toCenter edge values to find area to preserve
        self._setEdges()

        #Find max number of rows/columns to be removed around square
        #active region
        extra = (len(self.image) - 
            max(abs(self._toCenter.left - self._toCenter.right), 
                abs(self._toCenter.top - self._toCenter.bottom) ) )

        #Until that many rows and columns have been removed
        for i in range(extra - 1):

            #Remove either a bottom or top row depending on which is
            #available
            if self._toCenter.bottom:
                del self.image[0]
                self._toCenter.bottom -= 1
            else:
                del self.image[-1]

            #Remove either a left or right column depending on which
            #is available
            if self._toCenter.left:
                for eachRow in self.image:
                    del eachRow[0]
                self._toCenter.left -= 1
            else:
                for eachRow in self.image:
                    del eachRow[-1]

        #Re-assign height and width values given the size of image has
        #changed
        self.height = len(self.image)
        self.width = len(self.image[0])

        #Since _setEdges() was called
        self._resetParameters()
        return

