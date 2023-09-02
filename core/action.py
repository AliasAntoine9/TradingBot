import pandas as pd
from sqlalchemy import create_engine
import logging

from strategies.rsi.decision_rules import search_candle_to_buy
from utils.tools import Candle, Position, PreviousPositions

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %H:%M:%S")


class Action:
    """
    This class is used to check if there is a buy or sell action to make. If there is, the CryptoBot will buy
    and/or sell crypto on Binance.
    """
    def __init__(self, symbol, candles):
        self.symbol = symbol
        self.candles = candles
        self.candle_to_buy = Candle()
        self.candle_trigger = Candle()
        self.candles_tail = pd.DataFrame()
        self.previous_positions = PreviousPositions(self.symbol)

    def buy_sell_crypto(self):
        self._search_buying_signal()
        self._search_selling_signal()

    def _candle_to_buy_is_the_last_candle(self):
        if self.candle_to_buy.closetime == self.candle_trigger.opentime:
            return True
        else:
            return False

    def _search_buying_signal(self, is_selling_order=False) -> None:
        """A buying order is passed when the multiple if condition is respected"""
        self.candle_to_buy, self.candle_trigger, self.candles_tail = search_candle_to_buy(self.candles)
        opened_positions = self.previous_positions.df.opened_positions

        if self.candle_to_buy is not None \
                and self.candle_to_buy.opentime not in opened_positions["opentime_buying_candle"] \
                and self._candle_to_buy_is_the_last_candle():
            self._buy()
            self._send_telegram_notification()
            self._record_order(is_selling_order)
        else:
            logging.info(f"\n{self.symbol} | Nothing bought.\n")

    def _buy(self):
        """This method is appying the buying on Binance"""
        # Make the buy order on Binance
        return

    def _send_telegram_notification(self):
        """Use Telegram API to get the notification that a buying order were passed"""
        return

    def _record_order(self, is_selling_record=False) -> None:
        """This method records either buying or selling order into the DB"""
        api = None
        new_position = self._create_new_position(is_selling_record)

        # Insert position in Sql database through the API of the project
        api.post(new_position, is_selling_record)


    def _create_new_position(self, is_selling_record=False) -> pd.DataFrame:
        """This method is either creating an opened or closed position"""
        new_position = pd.DataFrame(
                {
                    "opentime_trigger_candle": [self.opentime_trigger_candle],
                    "opentime_buying_candle": [self.opentime_buying_candle],
                    "buying_timestamp": [self.buying_timestamp],
                    "buying_price": [self.buying_price],
                    "target_sales_price": [self.buying_price * 1.02],
                    "bet": [self.bet],
                    "crypto_quantity": [self.crypto_quantity],
                }
            )
        
        if is_selling_record:
            new_position["sales_timestamp"] = self.sales_timestamp
            new_position["sales_price"] = self.sales_price

        return new_position

    def _search_selling_signal(self, is_selling_order=True):
        """A selling order is passed when the multiple if condition is respected"""
        if ...:
            self._sell()
            self._send_telegram_notification()
            self._record_order(is_selling_order)
        else:
            logging.info(f"\n{self.symbol} | Nothing sold.\n")

    def _sell(self):
        pass

