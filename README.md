# Digit Reader 
###### Version 0.1, Summer 2018
A from-scratch neural network that learns to recognize digits. It is terrible but it works!

Nothing here has any real world application. A project that I undertook to help me understand neural networks in the abstract.

Samples are low resolution hand drawn characters in only black and white.

## Organization

#### Samples - The samples; hand drawn digit characters.
#### Sample Reader - File reader.
#### bwi - Fits samples.
#### nn - Neural network.

#### Samples are not kept in memory
Instead of keeping every sample used for training in memory, sample reader used a generator to retrieve the next sample to be used for training. The idea is that it might not be possible to hold training samples in memory I guess?

## Use
Preserve the directory structure.
Call 'digit_reader.py' with python3. Parameters are
    -Number of files to read (44)
    -Number of tests	(44)
    -Epochs

The hyper parameters are hard coded right now.

#### Requirements
imageio

## Author
Ian Miller
