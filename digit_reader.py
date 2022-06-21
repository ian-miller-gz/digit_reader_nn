#!/usr/bin/python

from nn.network import NeuralNetwork
from sample_reader.bwi_sampler import BWISampler
from bwi.manipulator import Manipulator
import sys
"""
Digit Reader Script

Summary:
    -A neural network to learn that learns to read digit characters

Arguments:
    -Number of files to read
        -i.e. '44'
        -Samples should each have their own file
        -Samples should be named <x>.bmp in 0 inclusive
        -Samples should be stored in the raw directory
    -Number of tests
        -i.e. '44'
        -Extra samples to validate with, these will not be used for
         training
        -Samples named img<number of files>.<extension> up through
         <number of tests>
    -Epochs
        -i.e. '7'
        -The number of training epochs
"""

NUM_ALL_FILES = 44

def printResults(validateSamples, network):
    """
    Have the network read each character in the validation sample set 
    and print those predictions to measure accuracy
    """
    #Run the prediction algorithm and store results as 'predictions'
    predictions = network.predict(validateSamples)
    
    #Print a header for tabular print
    print('\t\t', 'Actual', '\t', 'Predicted', '\t', 'Missed?')
    
    #Print out each prediction with corresponding fileName and target 
    #reading of image
    for target, prediction, fileName in zip(
    validateSamples.targets, predictions, validateSamples.fileNames):
        missed = "X" if target != prediction else ""
        print(fileName, '\t', target, '\t\t', prediction,'\t\t', missed)


def populateTargets(targetsFileName):
    """
    Read in a list of targets from a file
    """
    with open(targetsFileName) as f:
        data = f.read()
        stringTargets = data.split('\n')
        result = []
        for x in stringTargets:
            try:
                result.append(int(x) )
            except ValueError:
                #ignore eof
                pass
    return result


if __name__ == '__main__':
    #Constants
    OUTPUT_NEURONS = 10
    TARGETS   = "samples/targets.txt"
    SCALE  = 2
    FACTOR = 2

    #Parameters
    try:
        NUM_FILES = int(sys.argv[1])
        NUM_TESTS = int(sys.argv[2])
        EPOCHS    = int(sys.argv[3])

    except IndexError:
        print("Arguments: 'number of files'\t'number of tests'" +
              "'\t'number of epochs")
        exit()

    #Populate list of fileNames, targets - names use "img0.bmp" format
    files = ["samples/" + str(i) + ".bwi" for i in range(NUM_FILES)]
    allFiles = ["samples/" + str(i) + ".bwi" for i in range(NUM_ALL_FILES)]
    goals = populateTargets(TARGETS)
    
    #Generate Sample Sets
    validateSamples = BWISampler(allFiles, goals, SCALE, FACTOR)
    trainingSamples = BWISampler(files, goals, SCALE, FACTOR)

    #Slice opposite of each other
    validateSamples.setSlice(1)
    trainingSamples.setSlice(0, NUM_TESTS)
    
    #Randomize order samples
    validateSamples.shuffle()
    trainingSamples.shuffle()

    #Generate network and train
    numberReader = NeuralNetwork(
        OUTPUT_NEURONS, trainingSamples, epochs=EPOCHS)
    numberReader.train(True)

    #Have the network read each character in the validation sample set
    #and print those predictions to measure accuracy
    printResults(validateSamples, numberReader)
