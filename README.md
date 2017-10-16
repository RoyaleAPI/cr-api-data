# cr-api-data

The Python scripts inside `/src` combines columns inside several csv files to generate a collection of JSON files to be used for Clash Royale application development.

## Submodules

You will need to clone the repo with the submodules downloaded.

```git clone --recursive https://github.com/cr-api/cr-api-data```

## Install requirements

### 1. Create a virtualenv to run this repo

```virtualenv --python=$(which python3) cr-api-data```

### 2. Install requirements

```pip install -r requirements.txt```

## Generate JSON from source

Change folder to /src

```cd src```

Runnable scripts:

`./cards.py`
`./rarities.py`

These will output to /dst


