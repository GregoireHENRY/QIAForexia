# QIAForexia

inputs:

+ date de départ
+ date d'arrivée
+ timeframe des bougies
+ pair de devise

outputs:
+ par bougie:
    + hight
    + low
    + open
    + close
    + date

## Setup

```sh
# Install dependencies
pipenv install --dev

# Setup pre-commit and pre-push hooks
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```
