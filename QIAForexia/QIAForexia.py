"""
QIAForexia library
"""

# pylint: disable=invalid-name

import numpy
import yaml

from QIAForexia.trader import Trader

# from pudb import set_trace as bp


def start(account, password):
    """Start a trading session from a config file."""
    # Load config
    with open(r"config.yaml") as file:
        config = yaml.full_load(file)

    # Start Trader
    trader = Trader(
        account,
        password,
    )
    trader.setup(config)

    if "GET" in config.keys():
        candles = trader.get_candles()
        with open(
            f"stocks/{config['CURRENCY_PEER']}_{config['TIME_FRAME']}_"
            f"{config['START_DATE']}_{config['END_DATE']}.npy",
            "wb",
        ) as file:
            numpy.save(file, candles)
