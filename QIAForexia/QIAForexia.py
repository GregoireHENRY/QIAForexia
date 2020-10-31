"""
QIAForexia library
"""

# pylint: disable=invalid-name

from typing import Dict

from QIAForexia.trader import Trader

# from pudb import set_trace as bp


def start(config: Dict):
    """Start a trading session from a config file."""
    trader = Trader(
        config["ACCOUNT"],
        config["PASSWORD"],
    )
    trader.setup(config)

    if "GET" in config.keys():
        _candles = trader.get_candles()
