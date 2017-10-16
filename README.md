# SiloBreaker
GSoC 2017 project for [Red Hen Labs](http://www.redhenlab.org/). The latest status report can be found [here](https://medium.com/@dhfromkorea/gsoc-phase-3-update-14e710ee3aa1)

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
Each model/module has a corresponding test module where you can look and get a sense of how the module is supposed to be used. Your playground for loading different models and evaluate them against test data is src/main.py. Run main.py at ```src/```. 

The available models (to be added) are:
* text: KeywordSearch
* audio: AudioFingerprint
* video: VisualStock
* datautils: utilities to preprocessing video, audio, text, cut files


### Performance
The problem can be approached either in supervised or unsupervised learning. Currently the problem is structured as a binary classification problem on a series of time segments (default to 10 seconds). Since we have labelled samples (cutfiles), if incomplete, we can train on and cross-validate against them. Just note that the cutfiles are not so useful (noisy) and many in existence. 

```python
keywords = ['caption', 'type=story', 'type=commercial'] 
model = ks.KeywordSearch(keywords)
f1_score= model.test('test_data/')
print(f1_score)
```

As of now, the f1 score does not give you an accurate picture of how well your model is performing, because labelled data (cutfiles) are incomplete and inconsistent.  The hypothesis to test is that program boundaries are a subset of the story boundaries. I tested this hypothesis with the keytwords 'type=story/commercial' and achieved 93% recall with a 3 minute padding (see predict() method for KeywordSearch). The remaining 7% is I believe due to the incompleteness of caption files (see the issues page).

### Testing
```bash
cd src/
pytest
```

### Todos & issues
[link](https://github.com/dhfromkorea/digital-silo/issues)
