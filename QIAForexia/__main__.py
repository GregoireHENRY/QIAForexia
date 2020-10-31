"""
QIAForexia library's main.
"""

import yaml

from QIAForexia.QIAForexia import start

if __name__ == "__main__":
    with open(r"config.yaml") as file:
        config = yaml.full_load(file)
    start(config)
