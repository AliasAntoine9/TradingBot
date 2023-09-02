from dataclasses import dataclass
import pandas as pd
from requests import get
from pathlib import Path

from utils.config import database_url


@dataclass
class DataFrame:
    candles = pd.DataFrame()
    candles_tail = pd.DataFrame()


@dataclass
class Candle:
    opentime: str = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None
    closetime: str = None


def create_candle(series) -> Candle:
    df = series.to_frame().T
    return Candle(
        opentime=str({df["opentime"]}),
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        volume=df["volume"],
        closetime=str({df["closetime"]})
    )


@dataclass
class Position:
    symbol: str = None
    opentime_trigger_candle: str = None
    opentime_buying_candle: str = None
    buying_timestamp: str = None
    sales_timestamp: str = None
    buying_price: float = None
    profit_target_in_percentage: float = None
    sales_price: float = None
    bet: float = None
    crypto_quantity: float = None
    currency_couple: str = None


class PreviousPositions:
    """Get previous positions for 1 symbol (crypto)"""

    @dataclass
    class Dataframe:
        opened_positions = pd.DataFrame()
        closed_positions = pd.DataFrame()

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.df = self.Dataframe()
        self.get_positions(symbol)

    def get_positions(self, symbol: str) -> None:
        """This method allows to get the opened position for 1 symbol"""

        for status in ("opened", "closed"):

            endpoint = f"create_{status}_position"
            url = Path(database_url) / endpoint

            positions = get(url)

            setattr(self.df, f"{status}_positions", positions)
