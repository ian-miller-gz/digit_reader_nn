from abc import ABC, abstractmethod
import random

class Sampler(ABC):
    #Keep track of which file is next to be retrieved and populate attributes likewise.
    def __init__(self, fileNames, targets):
        self.fileNames = fileNames
        self.targets = targets
        self.__init__itemIterator()
        self.numInputs = len(self.inputs)
        self.numSources = len(self.fileNames)
        return

    @abstractmethod
    def _readFile(self):
        #Iterate over specified files and use specific method to yield values in an ordered tuple.
        for fileName, target in zip(self.fileNames, self.targets):
            inputs = fileName #.read() - where read is the child's process
            pass #yield (inputs, target, fileName)

    def getNextItem(self):
        self.item = next(self._itemIterator)
        self.inputs = self.item[0]
        self.target = self.item[1]
        self.source = self.item[2]
        return

    def assignSet(self, fileNames, targets):
        self.fileNames = fileNames
        self.targets = targets
        self.__init__itemIterator()
        self.numSources = len(self.fileNames)

    def setSlice(self, begin, end=-1, interval=1):
        if end == -1:
            end = len(self.targets)
        self.fileNames = self.fileNames[begin:end:interval]
        self.targets = self.targets[begin:end:interval]
        self.numSources = (end - begin) // interval
        self.__init__itemIterator()
        return

    def delSlice(self, begin, end=-1, interval=1):
        if end == -1:
            end = len(self.targets)
        self.fileNames = (
            self.fileNames[:begin:] + self.fileNames[end::] )
        self.targets = self.targets[:begin:] + self.targets[end::]
        self.numSources -= (end - begin) // interval
        self.__init__itemIterator()
        return

    def shuffle(self):
        shuffledData = [x for x in zip(self.fileNames, self.targets)]
        random.shuffle(shuffledData)
        self.fileNames = [
            fileName for fileName, target in shuffledData]
        self.targets = [target for fileName, target in shuffledData]
        self.__init__itemIterator()
        return

    def _getItem(self):
        while True:
            result = self._readFile()
            while True:
                try:
                    yield next(result)
                except StopIteration:
                    break

    def __init__itemIterator(self):
        #Bootstrap first iteration
        self._itemIterator = self._getItem()
        self.getNextItem()        
        return
