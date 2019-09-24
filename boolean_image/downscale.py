from boolean_image.simplemanipulator import SimpleManipulator


class Downscale(SimpleManipulator):
    def __init__(self, array, x=None, y=None):
        return

    @staticmethod
    def padArray(array, pad, numPads):
        """
        Insert stratified rows and columns of pad data into array in
        place
        """
        #Check for 0 value to avoid division by zero
        if not numPads:
            return

        #Find interval for stratification
        length = len(array)
        interval = -(length // numPads)

        #If there is more padding than length, ensure interval is > 0
        if not interval:
            interval = -1

        #Temporarily check for abs value, must test this
        stop = 1 if (interval * len(array)) < -length else 0

        #Insert stratified pads
        for i in range(length - 1, 1, interval):
            array.insert(i, pad)
        return

    def recursivePadDownscale(self, targetHeight, factor=2):
        """
        Downscale BI using fixed max pool downscaling
        interplaced with in place array padding operations
        """
        originalHeight, originalWidth = self.height, self.width

        #Necessesary to enlarge model of active region by shaving
        #excess inactive pixels
        self.shave()

        #Until the image is the target size by height
        #(both certain in square case)
        while len(self.image) != targetHeight:

            #Find pad size for each axis
            padX = originalWidth - len(self.image[0])
            padY = originalHeight - len(self.image)

            #Insert columns of padding
            for eachRow in self.image:
                self.padArray(eachRow, 0, padX)

            #Insert rows of padding
            self.padArray(self.image,
                [0 for x in range(len(self.image[0]))],
                padY)
            self.maxPoolDownscale(factor)

            #Enlarge active region
            self.shave()

        #Re-assign width and height values
        self.height, self.width = len(self.image), len(self.image[0])
        return

    def maxPoolDownscale(self, factor):
        """
        Use copy/assignment to generate a BIA that has been downscaled
        using max pool of kernel size by factor
        """
        #Initialize result to the correct size
        result = [
            [0 for i in range(len(self.image[0]) // factor)]
            for j in range(len(self.image) // factor)]

        #For each pixel in the result
        for i, row in enumerate(result):
            for j, pixel in enumerate(result):

                #For each pixel in kernel of original BIA
                for k in range(factor):
                    for l in range(factor):

                        #If there is an active pixel in the kernel,
                        #activate result pixel
                        if self.image[factor * i + k][factor * j + l]:
                            result[i][j] = 1
        self.image = result
        return

