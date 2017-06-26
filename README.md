# SiloBreaker

[![Master Build Status](https://travis-ci.org/dhfromkorea/digital-silo.svg?branch=master)](https://travis-ci.org/dhfromkorea/digital-silo)

[![Dev Build Status](https://travis-ci.org/dhfromkorea/digital-silo.svg?branch=dev)](https://travis-ci.org/dhfromkorea/digital-silo)

## Todos
* write the following todos in the github issues

* write a test module for keyword based search
* update keyword search module to take two arguments (program length, timewindow)
* write a module to visualize the predictions(for each keyword used) /program cuts
* fix readme

* commercial detection?
* script module imports now relative 
* write a bash script that downloads only the videos/subtitles that have cutfiles.
* write a python/bash script to strip away rows that have SEG markers (for training)
* try coveralls:https://coveralls.io/sign-up
* opencv orb for logo detection

## Getting started

### Dependencies
The easiest way to get the dependencies is to use Anaconda.

```
conda env create -f environment.yml
```
If you prefer using virtualenv or other forms, you may want to install the following.
* python=3.6.1
* numpy=1.13.0
* pandas=0.20.2
* scikit-learn=0.18.1
* scipy=0.19.0
* pytest=3.1.2
```

### Run models
```
cd src/
python main.py
```

The available models (to be added) are:

* text: KeywordSearch
* audio:
* video: 


## Testing
```
cd src/
pytest
```