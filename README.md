# cr-api-data

The Python scripts inside `/cr` combines columns inside several csv files to generate a collection of JSON files to be used for Clash Royale application development.

We try to update these files every time a client / balance update is released. The JSON files should be current.

**However**, you should note that `/json/cards_stats.json` is not complete as it would require some additional logic to flush it out. You are welcome to look into the source `/cr` folder and see if you can complete the logic and send us a pull request. 

## Submodules

You will need to clone the repo with the submodules downloaded.

```git clone --recursive https://github.com/cr-api/cr-api-data```

## Install requirements

### 1. Create a virtualenv to run this repo

```virtualenv --python=$(which python3) cr-api-data```

### 2. Install requirements

```pip install -r requirements.txt```

## Generate JSON from source

Run `./run.py`

## Loading data files from the web

https://royaleapi.github.io/cr-api-data/json/cards.json




