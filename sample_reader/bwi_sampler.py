from sample_reader.sampler import Sampler
from bwi.manipulator import Manipulator
import imageio
from itertools import chain


class BWISampler(Sampler):
    def __init__(self, fileNames, targetsFileName, scale=2, factor=2):
        self.scale = scale
        self.factor = factor
        Sampler.__init__(self, fileNames, targetsFileName)
        return

    def _readFile(self):
        for fileName, target in zip(self.fileNames, self.targets):
            inputs = imageio.imread(fileName)
            x, y = inputs.shape

            #This line should be factored out at some point
            inputs = list(chain.from_iterable(inputs))
            result = Manipulator(inputs, x, y)

            #The arguments for downscaling should be factored out
            result.recursivePadDownscale(y / self.scale, self.factor)
            result.center()
            yield (result.flatImage, target, fileName)


