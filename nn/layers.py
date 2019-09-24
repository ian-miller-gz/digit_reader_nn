import random
import copy
import math
from abc import ABC, abstractmethod


class BaseLayer(ABC):
    """
    Base layer

    Any layer of any type of perceptron. Abstract.
    Stores length value as count (as in neuron count)
    Capable of calling built-in activation functions
    """
    def __init__(self, count):
        self.count = count
        self.values = [0 for x in range(count)]

    @staticmethod
    def sigmoidActivation(weightedNodeInputsSummed):
        """f(x) = 1 ÷ (1 + e(-x))"""
        return 1 / (1 + math.exp(-weightedNodeInputsSummed))

    @staticmethod
    def dersigmoidActivation(activatedNodeValue):
        """f(x)` = f(x)(1 - f(x))"""
        return activatedNodeValue * (1 - activatedNodeValue)

    @staticmethod
    def heavinsideActivation(weightedNodeInputsSummed):
        """Step function, f(x) y < 0, = 0; y >= 0, = 1"""
        return 1 if weightedNodeInputsSummed >= 0 else 0


class InputLayer(BaseLayer):
    """
    Input layer of any Perceptron algorithm.

    Hold no lead, weights, or connection of
    any kind. The number of neurons depend on data
    upstream, so initialize accordingly.
    """
    def __init__(self, values):
        self.values = copy.deepcopy(values)
        self.count = len(self.values)

    def populate(self, values):
        """Populate from passed values"""
        self.values = copy.deepcopy(values)


class MultiLayer(BaseLayer, ABC):
    """
    Layer of a Neural Network with one or more hidden layers.

    Each Layer after the input layer must be equipped for back
    propagation. The connections between an instance of these layers,
    and the preceding, "lead", layer belong to that instance.
    """
    def __init__(self, count, lead):
        BaseLayer.__init__(self, count)
        self.lead = lead
        self.weights = [
            [random.uniform(-0.5, 0.5) for x in self.lead.values]
            for y in self.values]
        self.deltas = [0 for x in range(self.count)]
        self.previousWeights = copy.deepcopy(self.weights)

    def propagate(self):
        """
        Populate layer with activated weighted values from the
        previous layer

        σ(θⁱᵢ(Iᵥ))
        """
        self.values = [self.sigmoidActivation(sum(
                [i * w for i, w in zip(
                    self.lead.values, self.weights[x])
                ] ) )
            for x in range(self.count)]

    def updateWeights(self, momentum, learnRate):
        """
        Update weights for each connection in layer based on deltas
        and inputs

        θʰᵢ = α(θʰᵢ-θʰ⁻¹ᵢ) + ηδ(Hᵢ)Hⱼ⁻¹
        """
        #Set aside previous weights
        tempWeights = copy.deepcopy(self.weights)
        for i, _ in enumerate(self.values):
            for j, _ in enumerate(self.lead.values):
                self.weights[i][j] += (momentum * 
                    (self.weights[i][j] - self.previousWeights[i][j]))
                self.weights[i][j] += (learnRate * self.deltas[i] *
                    self.lead.values[j])
        self.previousWeights = copy.deepcopy(tempWeights)

    @abstractmethod
    def updateDeltas(self):
        """The method for updating deltas will depend on the layer"""
        pass


class HiddenLayer(MultiLayer):
    """Hidden Layer of a neural network """
    def __init__(self, count, lead):
        MultiLayer.__init__(self, count, lead)
        return

    def updateDeltas(self, outputLayer): #Hidden
        """
        For each output layer delta, the corresponding output layer
        value was product each hidden layer neuron, and a set of
        weights to each. To find the hidden deltas, first find the sum
        of the product of each output layer delta and and the set of
        weights to each output. Then find the product of the sum and
        the derivative of the sigmoid activation function of the
        corresponding hidden layer neuron's value.

        Note: Again there is a a set of weights for each neurond going
        both ways, the relationship is transformed propagating
        backwards as opposed to forwards. ie:
        hidden[a] -> output[z] = weights[a][z]
        output[z] -> hidden[a] = weights[z][a]

        δHᵢ = δOᵥ Θᴼᵢ σ(Hᵢ)'
        """
        for i, _ in enumerate(self.values):
            self.deltas[i] = 0
            for j, _ in enumerate(outputLayer.values):
                self.deltas[i] += (
                    outputLayer.deltas[j] * outputLayer.weights[j][i])
            self.deltas[i] *= self.dersigmoidActivation(
                self.values[i])


class OutputLayer(MultiLayer):
    """The last layer of a neural network"""
    def __init__(self, count, lead):
        MultiLayer.__init__(self, count, lead)
        self.error = 0
        return

    def updateDeltas(self, target): #Output
        """
        Modify deltas attribute.

        The derivative of the sigmoid activation function used in
        propagation is found for the value of each output neuron. The
        new delta value is this value multiplied by the value of the
        corresponding output neuron.

        The would-be correct output neuron compensates twoards 0, and
        the rest away from 0.

        δOᵢ = -Oᵢσ(Oᵢ)'
        """
        self.error = 0
        for i, neuron in enumerate(self.values):
            if i != target:
                self.deltas[i] = ((0 - self.values[i]) *
                    self.dersigmoidActivation(self.values[i]) )
                self.error += ( (0 - self.values[i]) *
                    (0 - self.values[i]) )
            else:
                self.deltas[i] = ( (1 - self.values[i]) *
                    self.dersigmoidActivation(self.values[i]) )
                self.error +=((1 - self.values[i]) *
                    (1 - self.values[i]) )

    def getBestFitNeuron(self):
        """
        Return the neuron with the highest value after propagation
        """
        #Sigmoid activation function has a lower limit of -1
        limit = -1
        result = 0
        for index, neuron in enumerate(self.values):
            if neuron > limit:
                limit = neuron
                result = index
        return result
