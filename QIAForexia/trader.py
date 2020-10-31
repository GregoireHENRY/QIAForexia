"""
Trader class to help using XTBApi
"""

import datetime
import logging
import sys
import time
from typing import Dict

import numpy
from XTBApi.api import Client

import QIAForexia.kit as kit


class Trader(Client):
    """Trader class to help using XTBApi"""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        account: int,
        password: str,
        account_type: str = "real",
        logger: bool = False,
    ):
        self.account: int = account
        self.account_type: str = account_type
        self.config: Dict = {}

        if not logger:
            logging.disable(sys.maxsize)

        # Init client
        super().__init__()
        self.client = Client()
        self.client.login(account, password, account_type)
        print(f"{kit.Colors.GREEN}✓{kit.Colors.NC}")

    def setup(
        self,
        config: Dict,
    ):
        """
        Import configuration
        """
        self.config.update(config)

    def test_if_configured(self, *keys: str):
        """Test if variables are correctly configured in config."""
        for key in keys:
            if key not in self.config.keys():
                sys.exit(f"Error: {key} does not exist in Trader.config.")
            if self.config[key] is None:
                sys.exit(f"Error: {key} is None.")

    def candle_time(self, candles: Dict, index: int = 0) -> str:
        """Get time of candle by index from now to past."""
        if "TIME_FORMAT" not in self.config.keys():
            sys.exit("Error: Trader.time_format is not setup.")
        return time.strftime(
            "TIME_FORMAT", time.localtime(candles[index]["timestamp"])
        )

    def get_candles_last(self, number_candles: int = 1):
        """Get number's latest candles."""
        candles = self.client.get_lastn_candle_history(
            self.config["CURRENCY_PEER"],
            self.config["TIME_FRAME"],
            number_candles,
        )
        _size_candles = len(candles)
        _pool_time = self.candle_time(candles, 0)
        # print("%d candles extracted from %s" % (size_candles, pool_time))
        return candles

    def get_candles(
        self,
    ):
        """
        Get candles from start to end date.
        It extract candles as a Nx5 NDArray matrix with N the number of
        requested candles. The 5 columns are:
            timestamp, open, close, high, low

        One weakness of using XTApi is that it can only extract the n-th latest
        candles. Here, we are removing the overage candles.
        """
        self.test_if_configured(
            "TIME_FORMAT", "TIME_FRAME", "START_DATE", "END_DATE"
        )
        start_timestamp = time.mktime(
            datetime.datetime.strptime(
                self.config["START_DATE"], self.config["TIME_FORMAT"]
            ).timetuple()
        )
        end_timestamp = time.mktime(
            datetime.datetime.strptime(
                self.config["END_DATE"], self.config["TIME_FORMAT"]
            ).timetuple()
        )
        last_candle = self.get_candles_last()
        last_timestamp = last_candle[0]["timestamp"]
        number_from_last = (
            int((last_timestamp - start_timestamp) / self.config["TIME_FRAME"])
            + 1
        )
        number_actual = (
            int((end_timestamp - start_timestamp) / self.config["TIME_FRAME"])
            + 1
        )
        candles = self.get_candles_last(number_candles=number_from_last)
        candles = candles[:number_actual]
        candles_array = numpy.zeros((number_actual, 5))
        for _index, candle in enumerate(candles):
            candles_array[:] = numpy.array(
                [
                    int(candle["timestamp"]),
                    candle["open"],
                    candle["close"],
                    candle["high"],
                    candle["low"],
                ]
            )
        return candles_array

    def logout(self):
        self.client.logout()
