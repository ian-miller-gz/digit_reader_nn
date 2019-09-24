from abc import ABC, abstractmethod
import random

class Sampler(ABC):
    """
    File loader for neural network training data.

    Read a file, use methods supplied by child classes to populate
    self.attributes. Keep track of which file is next to be retrieved,
    and populate attributes likewise.

    TrainingData objects will only contain one data point at a time
    represented by:

    self.inputs = the values, as array, to be plugged into the input
    neurons, or featured scaled and treated unsupervised in more
    complex models.

    self.target = the correct prediciton for supervised training.

    self.source = the fileName for reference.
    """
    def __init__(self, fileNames, targets):
        self.fileNames = fileNames
        self.targets = targets
        self.__init__itemIterator()
        self.numInputs = len(self.inputs)
        self.numSources = len(self.fileNames)
        #Note: four attributes, item, inputs, target and source are
        #initialized in getNextItem, which is called in 
        #__init__itemIterator()
        return

    @abstractmethod
    def _readFile(self):
        """
        Iterate over specified files and use specific method to yield
        values in an ordered tuple.

        The specific method must be supplied by the inheriting class,
        but that method must also be a generator; the general function
        is modeled below
        """
        for fileName, target in zip(self.fileNames, self.targets):
            inputs = fileName #.read() - where read is the child's process
            pass #yield (inputs, target, fileName)

    def getNextItem(self):
        """
        Advance trackers to next file, assign attributes to results
        yielded by  self._itemIterator, which is an instance of
        self._getItem().
        """
        self.item = next(self._itemIterator)
        self.inputs = self.item[0]
        self.target = self.item[1]
        self.source = self.item[2]
        return

    def assignSet(self, fileNames, targets):
        """
        Assign items to read from list of tuples
        """
        self.fileNames = fileNames
        self.targets = targets
        self.__init__itemIterator()
        self.numSources = len(self.fileNames)

    def setSlice(self, begin, end=-1, interval=1):
        """
        Assign items to read from index 'begin' to index 'end'.
        """
        if end == -1:
            end = len(self.targets)
        self.fileNames = self.fileNames[begin:end:interval]
        self.targets = self.targets[begin:end:interval]
        self.numSources = (end - begin) // interval
        self.__init__itemIterator()
        return

    def delSlice(self, begin, end=-1, interval=1):
        """
        Delete items to be read from index 'begin' to index 'end'.
        """
        if end == -1:
            end = len(self.targets)
        self.fileNames = (
            self.fileNames[:begin:] + self.fileNames[end::] )
        self.targets = self.targets[:begin:] + self.targets[end::]
        self.numSources -= (end - begin) // interval
        self.__init__itemIterator()
        return

    def shuffle(self):
        """
        Shuffle set of files and their corresponding targets to read
        """
        shuffledData = [x for x in zip(self.fileNames, self.targets)]
        random.shuffle(shuffledData)
        self.fileNames = [
            fileName for fileName, target in shuffledData]
        self.targets = [target for fileName, target in shuffledData]
        self.__init__itemIterator()
        return

    def _getItem(self):
        """
        Generator which intialize instancs of _readFile iterators and
        yield those results until exhausted, then _getItem will loop.
        """
        while True:
            result = self._readFile()
            while True:
                try:
                    yield next(result)
                except StopIteration:
                    break

    def __init__itemIterator(self):
        """
        Initialize iterable self._itemIterator.

        Bootstrap first iteration to ensure properly poulated
        attributes at all times
        """
        self._itemIterator = self._getItem()
        self.getNextItem()        
        return
