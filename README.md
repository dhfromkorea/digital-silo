# SiloBreaker

## Getting started
### Dependencies
The easiest way to get the dependencies is to use Anaconda.

```bash
conda env create -f environment.yml
```

If you prefer using virtualenv or other forms, you may want to install the following.
* dejavu
* python=3.6.1
* numpy=1.13.0
* pandas=0.20.2
* scikit-learn=0.18.1
* scipy=0.19.0
* pytest=3.1.2


### Run models
Your playground for loading different models and evaluate them against test data is src/main.py. Run main.py at src/.

```python
keywords = ['caption', 'story', 'commercial']
model = ks.KeywordSearch(keywords)
# validate to tune hyperparams here

# test here
f1_score= model.test('test_data/')
print(f1_score)
```

The available models (to be added) are:
* text: KeywordSearch
* audio:
* video: 


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
