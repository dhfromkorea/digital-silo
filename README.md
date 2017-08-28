# SiloBreaker
GSoC 2017 project for [Red Hen Labs](http://www.redhenlab.org/). Details about the project can be found [here](https://github.com/dhfromkorea/digital-silo/blob/master/docs/project_overview.pdf) 

## The problem
The project has a large archive of TV news videos recorded since 70's. Each video is roughly 8-hour-long. We want to split each video by their natural boundaries where a program changes to another (typically with a commercial in between).

## Getting started
### Dependencies
We use Python 3.X. The easiest way to get the dependencies is to use Anaconda. 

```bash
conda env create -f environment.yml
```

If you prefer using virtualenv or other forms, you may want to install the following.
* dejavu [link](https://github.com/worldveil/dejavu/blob/master/INSTALLATION.md)
* python=3.5
* numpy=1.13.0
* pandas=0.20.2
* scikit-learn=0.18.1
* scipy=0.19.0
* pytest=3.1.2

### The Data
Check the data folder for examples. There are four types of data to be used:

* video: mp4
* audio: mp3 (extracted from video using ```extract_audio.sh```)
* text: txt3/4 (subtitle files)
* cutfiles: program boundary annotations (hand-labelled) 

For full acccess to the data, you will need to make a request for access to the Red Hen Labs team. Assuming you have read access to the archive, you can use ```get_data.sh``` to fetch and sync the data to your local machine. Tip: you can choose to download only the videos that have corresponding cutfiles.


### How to use
Your playground for loading different models and evaluate them against test data is src/main.py. Run main.py at src/.

The available models (to be added) are:
* text: KeywordSearch
* audio: AudioFingerprint
* video: VisualStock

```python
keywords = ['caption', 'story', 'commercial']
model = ks.KeywordSearch(keywords)
f1_score= model.test('test_data/')
print(f1_score)
```

### Testing

```bash
cd src/
pytest
```
or to test a specific module

```bash
cd src/
pytest path_to_the_test_module
```

### Todos
* data collection
* feature extraction

### Issues
cleanup

