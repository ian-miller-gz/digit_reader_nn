# Digit Reader 
###### Version 0.1, Summer 2018
Something I wrote as an exercise in ML.

A crude script designed to exhibit a custom built neural network
written entirely in python. The Neural network is slow but extensible.
It was meant for tinkering, but not for practical application.

Character Reader learns to read "boolean images" representations of digits 0-9.

The mean-squared-error (MSE) is printed out at each training epoch.
After training, each validation sample's correct classification will be printed
besides it file name and path, and each of the network's incorrect
classifications will be marked.

## Organization
#### Boolean Image
Boolean images are essentially 2D arrays that map true values onto a drawing of a digit.


Manipulator has downscaling and related methods for modifyin boolean images. I may add detail
on how the downscaling algo works when I have more time, or if If there is any demand, but I expect none.


#### Sample Reader
Instead of keeping every sample used for training in memory, sample reader used a generator
to retrieve the next sample to be used for training. This is terribly inefficient, but the idea is
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

ianm@bgsu.edu
