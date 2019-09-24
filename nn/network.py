from nn.layers import InputLayer, HiddenLayer, OutputLayer


def _getIntegerMean(*args):
    #Apparently this is a terrible way to get the mean
    return round(sum(args) / len(args))


class NeuralNetwork(object):
    """
    Multi-layer Perceptron Neural Network
    """
    defaultKwargs = {'epochs':100,
                     'learnRate':0.1,
                     'momentum':0.1,
                     'verbose':False}
    def __init__(self, numOutput, trainData, **kwargs):
        self.trainData = trainData
        self.mse = 0
        self.__init__layers(numOutput)
        self.__init__kwargs(kwargs)
        return

    def train(self, verbose=None):
        """
        Train network

        Handle calling verbose or silent traing method
        """
        if verbose == None:
            verbose = self.verbose
        if verbose:
            self._trainVerbose()
        else:
            self._train()
        return

    def predict(self, predictData):
        """
        Generate list of predictions indexed to each item in
        prediciton input data
        """
        result = []
        for i in range(predictData.numSources):
            self.inputLayer.populate(predictData.inputs)
            self.propagate()
            prediction = self.outputLayer.getBestFitNeuron()
            result.append(prediction)
            predictData.getNextItem()
        return result

    def propagate(self):
        """
        Update each Layer's values forward from the input to the
        output layer

        Should call before finding the next epoch's deltas
        """
        self.hiddenLayer.propagate()
        self.outputLayer.propagate()
        return

    def updateDeltas(self, target):
        """
        Update each layer's deltas backwards from output to input
        layer

        Should call after propagation
        """
        self.outputLayer.updateDeltas(target)
        self.hiddenLayer.updateDeltas(self.outputLayer)
        return

    def updateWeights(self):
        """
        Forward update the weights connecting each layer feed forward

        Should call after updating deltas
        """
        self.hiddenLayer.updateWeights(self.momentum, self.learnRate)
        self.outputLayer.updateWeights(self.momentum, self.learnRate)
        return

    def _train(self):
        """
        Train the network with no print calls to terminal
        """
        for i in range(self.epochs):
            self.trainData.shuffle()
            for i in range(self.trainData.numSources):
                self.inputLayer.populate(self.trainData.inputs)
                self.propagate()
                self.updateDeltas(self.trainData.target)
                self.updateWeights()
                self.trainData.getNextItem()
        return

    def _trainVerbose(self):
        """
        Train the network and print to terminal each epoch
        """
        for i in range(self.epochs):
            self.trainData.shuffle()
            self.mse = 0.0
            for i in range(self.trainData.numSources):
                self.inputLayer.populate(self.trainData.inputs)
                self.propagate()
                self.updateDeltas(self.trainData.target)
                self.updateWeights()
                self.mse += self.outputLayer.error
                self.trainData.getNextItem()
            self.mse /= (self.outputLayer.count + 1)
            print("MSE:", self.mse)
        return

    def __init__layers(self, numOutput):
        """
        Initialize each Layer of the neural network
        """
        self.inputLayer = InputLayer(self.trainData.inputs)
        numHidden = _getIntegerMean(numOutput, self.inputLayer.count)
        self.hiddenLayer = HiddenLayer(numHidden, self.inputLayer)
        self.outputLayer = OutputLayer(numOutput, self.hiddenLayer)
        return

    def __init__kwargs(self, kwargs):
        """
        Initialize each keyword.

        If they have not been explicitly passed, assignt to class 
        attribute defaultKwargs
        """
        self.epochs    = self.__init__keyword(kwargs, 'epochs')
        self.learnRate = self.__init__keyword(kwargs, 'learnRate')
        self.momentum  = self.__init__keyword(kwargs, 'momentum')
        self.verbose   = self.__init__keyword(kwargs, 'verbose')
        return

    @classmethod
    def __init__keyword(cls, kwargs, key):
        """
        Exception handle to return kwarg value.
        """
        try:
            return kwargs[key]
        except KeyError:
            return cls.defaultKwargs[key]

