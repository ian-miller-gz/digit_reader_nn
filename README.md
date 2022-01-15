# Digit Reader 
###### Version 0.1, Summer 2018
Something I wrote as an exercise in ML.

A toy neural network with virtually zero application. A project that I undertook to help me understand
neural networks in the abstract. Stochastic gradient descent.

Character Reader learns to read black-white bitmap representations of digits 0-9.

The mean-squared-error (MSE) is printed out at each training epoch.
After training, each validation sample's correct classification will be printed
besides it file name and path, and each of the network's incorrect
classifications will be marked.

## Organization
#### Boolean Image
Boolean images are basically black-white bitmaps.


Manipulator has downscaling and related methods for modifying boolean images. I do not explain those
methods here for lack of interest.


#### Sample Reader
Instead of keeping every sample used for training in memory, sample reader used a generator
to retrieve the next sample to be used for training. The idea is that in realistic scenarios
sample sizes could be much too large to hold in memory; I just wanted play around with ideas for 
managing large amounts of data.

#### Neural Net
Sigmoid activiation MLP. Network is designed to be extensible, but still needs a lot of work.
Currently, it can only be used to implement simple NNs - 3 layers, sigmoid activiation.

## Installation and Use
Clone the repository.
Preserve the directory structure.
Call 'digit_reader.py' with python3. Parameters will be listed if not called correctly.

#### Prerequisites
Python 3

imageio

#### Parameters
Arguments are passed in order, not by name.

    -Number of files to read
    -Number of tests
    -Epochs

## Author
Ian Miller
