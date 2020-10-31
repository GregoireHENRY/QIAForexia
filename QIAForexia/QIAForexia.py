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
    trader.setup(
        time_format=config["TIME_FORMAT"],
        currency_peer=config["CURRENCY_PEER"],
        number=config["NUMBER"],
        time_frame=config["TIME_FRAME"],
        start_date=config["START_DATE"],
        end_date=config["END_DATE"],
    )
    _candles = trader.get_candles()
