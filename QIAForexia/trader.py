"""
Trader class to help using XTBApi
"""

import datetime
import logging
import sys
import time
from typing import Dict, Optional

import numpy
from XTBApi.api import Client


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

    def setup(
        self,
        config: Dict,
    ):
        """
        Import configuration
        """
        self.config.update(config)

    def candle_time(self, candles: Dict, index: int = 0) -> str:
        """Get time of candle by index from now to past."""
        if "TIME_FORMAT" not in self.config.keys():
            sys.exit("Error: Trader.time_format is not setup.")
        return time.strftime(
            "TIME_FORMAT", time.localtime(candles[index]["timestamp"])
        )

    def get_candles_last(
        self,
        currency_peer: str = None,
        time_frame: int = None,
        number: int = None,
    ):
        """Get number's latest candles with possible setup configuration."""
        if not currency_peer:
            currency_peer = self.config["CURRENCY_PEER"]
        if not time_frame:
            time_frame = self.config["TIME_FRAME"]
        if not number:
            number = self.config["NUMBER"]
        candles = self.client.get_lastn_candle_history(
            currency_peer, time_frame, number
        )
        _size_candles = len(candles)
        _pool_time = self.candle_time(candles, 0)
        # print("%d candles extracted from %s" % (size_candles, pool_time))
        return candles

    def get_candles(
        self,
        currency_peer: str = None,
        time_frame: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Get candles from start to end dates with possible setup configuration.
        It extract candles as a Nx5 NDArray matrix with N the number of
        requested candles. The 5 columns are:
            timestamp, open, close, high, low

        One weakness of using XTApi is that it can only extract the n-th latest
        candles. Here, we are removing the overage candles.
        """
        if not currency_peer:
            currency_peer = self.config["CURRENCY_PEER"]
        if not time_frame:
            time_frame = self.config["TIME_FRAME"]
        if not start_date:
            start_date = self.config["START_DATE"]
        if not end_date:
            end_date = self.config["END_DATE"]
        if "TIME_FORMAT" not in self.config.keys():
            sys.exit("Error: Trader.time_format is not setup.")
        if "TIME_FRAME" not in self.config.keys():
            sys.exit("Error: Trader.time_frame is not setup.")
        if "START_DATE" not in self.config.keys():
            sys.exit("Error: Trader.start_date is not setup.")
        if "END_DATE" not in self.config.keys():
            sys.exit("Error: Trader.end_date is not setup.")
        start_timestamp = time.mktime(
            datetime.datetime.strptime(
                start_date, self.config["TIME_FORMAT"]
            ).timetuple()
        )
        end_timestamp = time.mktime(
            datetime.datetime.strptime(
                end_date, self.config["TIME_FORMAT"]
            ).timetuple()
        )
        last_candle = self.get_candles_last(number=1)
        last_timestamp = last_candle[0]["timestamp"]
        number_from_last = (
            int((last_timestamp - start_timestamp) / time_frame) + 1
        )
        number_actual = int((end_timestamp - start_timestamp) / time_frame) + 1
        candles = self.get_candles_last(number=number_from_last)
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
