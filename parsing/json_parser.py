from datetime import datetime
import pandas as pd

from utils.tools import DataFrame


class JsonParser:
    """
    This class parses the input provides by Binance into a dataframe which contains the last candles on the market.
    Binance Rest Api can be load in a dictionary (json) object.
    """

    def __init__(self):
        self.df = DataFrame()
        self.df.candles = pd.DataFrame(
            {
                "closetime": [],
                "close": [],
                "opentime": [],
                "open": [],
                "high": [],
                "low": [],
                "volume": []
            }
        )
        self.datetime_format = "%Y-%m-%d %H:%M:%S"
        self.response = {}

    def transform_to_df(self, response) -> pd.DataFrame:
        """Entry point of the parser object"""
        self._transform_binance_response(response)
        self._change_datetime_format()
        self._create_candles_df()
        return self.df.candles

    def _transform_binance_response(self, response) -> None:
        """This method check if Binance response is readable. If yes, this method transforms the reponse into a list."""
        try:
            self.response = response.json()
        except:
            raise TypeError

    def _change_datetime_format(self) -> None:
        """This method converts Millisecond Unix Timestamp into pandas datetime format"""
        format = self.datetime_format
        for candle in self.response:
            # candle[i] is a MillisecondsUnixTimestamp string
            # 1st -> Convert the string candle[i] to int
            # 2nd -> Convert MillisecondsUnixTimestamp to UnixTimeStamp
            # 3rd -> Convert UnixTimestamp to string well formatted
            str_opentime_formatted = datetime.fromtimestamp(int(candle[0])/1000).strftime(format)
            str_closetime_formatted = datetime.strftime(datetime.fromtimestamp(int(candle[6]) / 1000), format)

            # Convert string to datetime64 format
            candle[0] = datetime.strptime(str_opentime_formatted, format)
            candle[6] = datetime.strptime(str_closetime_formatted, format)

    def _create_candles_df(self) -> None:
        """This method creates a df which contains all the candles retrieved from Binance API"""
        candles = self.df.candles

        for candle in self.response:
            candles = candles.append(
                pd.Series(
                    {
                        "closetime": candle[6],
                        "close": candle[4],
                        "opentime": candle[0],
                        "open": candle[1],
                        "high": candle[2],
                        "low": candle[3],
                        "volume": candle[5]
                    }
                ),
                ignore_index=True
                )
            
        self.df.candles = candles


# 1 candle is:
# openTime - 0
# open - 1
# high - 2
# low - 3
# close - 4
# volume - 5
# closeTime - 6
# quoteAssetVolume - 7
# numberOfTrades - 8
# takerBuyBaseAssetVolume - 9
# takerBuyQuoteAssetVolume - 10
# ignore - 11
#
# UnixTimeStamp: 1636722000
