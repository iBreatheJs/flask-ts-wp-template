from distutils.dep_util import newer
import json
from os import error
from numpy.lib.function_base import select
from pygments.token import Error
from app import app
from flask import jsonify, request
from general.tax import get_taxes_min
from exchange.kraken.Trade import Trade
from exchange.kraken.rest import KrakenRest

from exchange.kraken.tablesCoinsTraded import TablesCoinsTraded
from exchange.kraken.Trades import Trades
from cw.MarketData import getMarketHistory
from exchange.exchange import Exchange
from exchange.bittrex.userData.ledger import get_ledger
from openSea.openSea import get_collection, get_items_without_reserve_price
# from .exchange.exchange import Exchange
from utils import writeInFile
import traceback

class APIResponse:
    def __init__(self):
        self._error = []
        self._data = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, newError: BaseException):
        return self._error.append({str(type(newError)): newError.args[0]})

    def toObj(self):
        return {'error': self.error, 'data': self._data}


# KRAKEN:
@app.route("/_get-all-transactions")
def _getAllTransactions():
    resp = APIResponse()
    try:
        # get trades obj:
        trades = Trades()
        # sorted = trades.sort_trades(sortBy='cost')
        trades.sort_trades('time')

        if not trades.trades:
            raise ValueError('No Trades.')
        resp.data['kraken'] = {}
        resp.data['kraken'] = trades.json
        bittrexLedger = get_ledger()
        # print(bittrexLedger)
        resp.data['bittrex'] = bittrexLedger
    except Exception as e:
        print(e.__traceback__())
        resp.error = e
    respObj = resp.toObj()
    return jsonify(respObj)


@app.route("/_getTradesByPairs")
def _getTradesByPairs():
    resp = APIResponse()
    try:
        print("get Trades sorted by Pairs")
        trades = Trades().get_trades_by_pairs()
        resp.data = trades
    except Exception as e:
        print(e)
        resp.error = e
    respObj = resp.toObj()
    return jsonify(respObj)


@app.route("/all-tables-and-trades")
def all_table_and_trades():
    resp = APIResponse()
    try:
        print("get Trades sorted by Pairs")

        # get trades obj:
        trades = Trades()
        # sorted = trades.sort_trades(sortBy='cost')
        trades.sort_trades('time')

        # generate pair dict:
        trades.get_trades_by_pairs()

        # tax = get_taxes_min(trades)
        # return jsonify('respObj')

        resp.data = {}
        # convert trades to json:
        # resp.data['trades'] =taxes.pairs_to_json()
        # resp.data['trades'] = get_taxes_min(trades).pairs_to_json()
        print(trades.byPairs)
        writeInFile(trades.pairs_to_json())
        resp.data['trades'] = trades.pairs_to_json()

        # TODO: combine _getTablesCoinsTraded and _getTradesByPairs or dynamiclaly fetch, its needed for table anyways. Would probably have been easier to just do everything on frontend
        print("get table basic stats")
        tables = TablesCoinsTraded()
        # table = getTablesCoinsTraded()
        resp.data['tables'] = tables.getTablesCoinsTraded()
    except Exception as e:
        print(e.with_traceback())
        resp.error = e
    respObj = resp.toObj()
    return jsonify(respObj)


@app.route("/_getAllTablesAndTrades")
def _getAllTablesAndTrades():
    resp = APIResponse()
    try:
        print("get Trades sorted by Pairs")

        # ex = Exchange()
        # ex.kraken.update.trades()

        
        # get trades obj:
        trades = Trades()
        # sorted = trades.sort_trades(sortBy='cost')
        trades.sort_trades('time')

        # generate pair dict:
        trades.get_trades_by_pairs()

        # tax = get_taxes_min(trades)
        # return jsonify('respObj')

        resp.data = {}
        # convert trades to json:
        # resp.data['trades'] =taxes.pairs_to_json()
        # resp.data['trades'] = get_taxes_min(trades).pairs_to_json()
        print(trades.byPairs)
        # writeInFile(trades.pairs_to_json())
        resp.data['tradesByPair'] = trades.pairs_to_json()

        # TODO: combine _getTablesCoinsTraded and _getTradesByPairs or dynamiclaly fetch, its needed for table anyways. Would probably have been easier to just do everything on frontend
        print("get table basic stats")
        tables = TablesCoinsTraded()
        # table = getTablesCoinsTraded()
        resp.data['tables'] = tables.getTablesCoinsTraded()
    except Exception as e:
        print(e)
        resp.error = e
    respObj = resp.toObj()
    return jsonify(respObj)

# CRYPTOWATCH:
@app.route("/_getMarketHistory")
def _getMarketHistory():
    exchange = request.args['exchange']
    pair = request.args['pair']

    paramsOpt = {
        'periods': request.args.get('periods'),
        'before': request.args.get('before'),
        'after': request.args.get('after')
    }

    print(paramsOpt['periods'])
    print(type(paramsOpt['periods']))
    resp = APIResponse()
    try:
        history = getMarketHistory(
            exchange, pair, paramsOpt)
        resp.data = history
    except Exception as e:
        print(e.with_traceback())
        resp.error = e
    respObj = resp.toObj()
    return jsonify(respObj)


@app.route("/_get_collection_opensea")
def _get_collection_opensea():
    get_collection()
    return "asdf"