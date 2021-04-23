# chiner

chiner (verb) : to hunt for rare or obscure objects

chiner is a simply python based playlist generator that use embedings to create (hopefully) meaningful playlist automagically

## Training 

First we need to create a small dataset: copy some of your albums into "data/": about 200 files should do
Then run the `makeDs.py` script to create a training dataset
Finally, run the `main.py` script to train the model

## Analyzing

To create playlist we need to compute the embeding of all songs. To do that, just run `infer.py`, which will create a json file containing the embedding of all files contained in `data`, along with some other features

## Creating a playlist

Finally, we can create a playlist using `makePlaylist.py`
