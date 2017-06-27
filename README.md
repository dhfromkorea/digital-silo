# SiloBreaker

[![Master Build Status](https://travis-ci.org/dhfromkorea/digital-silo.svg?branch=master)](https://travis-ci.org/dhfromkorea/digital-silo)
[![Dev Build Status](https://travis-ci.org/dhfromkorea/digital-silo.svg?branch=dev)](https://travis-ci.org/dhfromkorea/digital-silo)

## Getting started
### Dependencies
The easiest way to get the dependencies is to use Anaconda.

```bash
conda env create -f environment.yml
```

If you prefer using virtualenv or other forms, you may want to install the following.
* python=3.6.1
* numpy=1.13.0
* pandas=0.20.2
* scikit-learn=0.18.1
* scipy=0.19.0
* pytest=3.1.2


### Run models
Your playground for loading different models and evaluate them against test data is src/main.py.

```python
caption_data, _, _ = load_caption_data('test_data/test_caption_0.txt3')
y = load_program_cut_data('test_data/test_program_cuts_0.cuts')


model = ks.KeywordSearch()

pred = model.predict(caption_data, keywords=['caption'], merge_time_window=20)

evaluate_model(y, pred)
```

The available models (to be added) are:
* text: KeywordSearch
* audio:
* video: 


### Testing
A new module will be preceded by a test module (TDD). Travis handles continuous integration whose build status is showing at the top section of this document.

```bash
cd src/
pytest
```