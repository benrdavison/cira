import pandas as pd
import warnings


# Alpaca
import alpaca
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, OrderType, AssetStatus
from alpaca.data.models import Bar
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import LimitOrderRequest, StopLimitOrderRequest
from alpaca.trading.client import TradingClient


# stock
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.live import StockDataStream


# cira
from cira.asset import asset
from cira import auth, config


class Stock(asset.Asset):
    def __init__(self, symbol: str) -> None:
        """Exchange for trading stocks"""
        APCA_ID, APCA_SECRET = auth.get_api_keys()
        self.symbol = symbol
        self.live_client = StockDataStream(APCA_ID, APCA_SECRET)
        self.history = StockHistoricalDataClient(APCA_ID, APCA_SECRET)
        self.trade = TradingClient(APCA_ID, APCA_SECRET, paper=config.PAPER_TRADING)
        self.latest_quote_request = StockLatestQuoteRequest
        self.bars_request = StockBarsRequest

    def price(self) -> float:
        """gets the asking price of the symbol"""
        perms = self.latest_quote_request(symbol_or_symbols=self.symbol)
        return float(self.history.get_stock_latest_quote(perms)[self.symbol].ask_price)

    @classmethod
    def get_all_assets(self):
        APCA_ID, APCA_SECRET = auth.get_api_keys()
        trade = TradingClient(APCA_ID, APCA_SECRET, paper=config.PAPER_TRADING)
        search_params = GetAssetsRequest(
            asset_class=AssetClass.US_EQUITY, status=AssetStatus.ACTIVE
        )
        return [a.symbol for a in trade.get_all_assets(search_params)]

    def short(self, qty: float) -> None:
        if not self.is_sortable():
            warnings.warn(
                f"tryied to short {self.symbol}, but alpaca markets dose not allow for short position in {self.symbol}"
            )
            return
        if self.position() != None:
            warnings.warn(
                f"tryied to short {self.symbol}, but a long position is being held there for short just result in a sale of the same qty {qty}"
            )
        self.sell(qty)

    def short_exit(self, qty: float) -> None:
        if not self.is_sortable():
            warnings.warn(
                f"tryied to exit short {self.symbol}, but alpaca markets dose not allow for short position in {self.symbol}"
            )
            return
        self.buy(qty)
