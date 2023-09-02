import pandas as pd

from scrapping.rest_api_scrapper import RestApiScrapper
from parsing.json_parser import JsonParser
from strategies.rsi.compute_rsi import ComputeRsi
from core.action import Action


def rsi_strategy(symbol) -> pd.DataFrame:
    """Workflow of RSI strategy"""

    # Step 1
    scrapper = RestApiScrapper(symbol=symbol)
    response = scrapper.get_candles()
    
    # Step 2
    parser = JsonParser()
    candles = parser.transform_to_df(response)

    # Step 3
    computer = ComputeRsi(candles)
    candles = computer.compute_rsi()

    # Step 4
    trader = Action(symbol=symbol, candles=candles)
    trader.buy_sell_crypto()

    return candles


if __name__ == "__main__":
    candles_ = rsi_strategy(symbol="vet")
