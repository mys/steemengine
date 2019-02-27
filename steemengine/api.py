from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta, date
import time
import io
import json
import requests
from timeit import default_timer as timer
import logging
from .rpc import RPC


class Api(object):
    """ Access the steem-engine API
    """
    def __init__(self, user=None, password=None, **kwargs):
        self.url = 'https://api.steem-engine.com/'
        self.rpc = RPC()

    def get_history(self, account, symbol, limit=1000, offset=0, histtype="user"):
        """"Get the transaction history for an account and a token"""
        response = ""
        cnt2 = 0
        while str(response) != '<Response [200]>' and cnt2 < 10:
            response = requests.get(self.url + "accounts/history?account=%s&limit=%d&offset=%d&type=%s&symbol=%s" % (account, limit, offset, histtype, symbol))
            cnt2 += 1
        return response.json()

    def getLatestBlockInfo(self):
        """get the latest block of the sidechain"""
        ret = self.rpc.getLatestBlockInfo(endpoint="blockchain")
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret

    def getBlockInfo(self, blocknumber):
        """get the block with the specified block number of the sidechain"""
        ret = self.rpc.getBlockInfo({"blockNumber": blocknumber}, endpoint="blockchain")
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret

    def getTransactionInfo(self, txid):
        """Retrieve the specified transaction info of the sidechain"""
        ret = self.rpc.getTransactionInfo({"txid": txid}, endpoint="blockchain")
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret

    def getContract(self, contract_name):
        """ Get the contract specified from the database"""
        ret = self.rpc.getContract({"name": contract_name}, endpoint="contracts")
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret

    def findOne(self, contract_name, table_name, query = {}):
        """Get the object that matches the query from the table of the specified contract"""
        ret = self.rpc.findOne({"contract": contract_name, "table": table_name, "query": query}, endpoint="contracts")
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret


    def find(self, contract_name, table_name, query = {}, limit=1000, offset=0, indexes=[]):
        """Get an array of objects that match the query from the table of the specified contract"""
        ret = self.rpc.find({"contract": contract_name, "table": table_name, "query": query,
                             "limit": limit, "offset": offset, "indexes": indexes}, endpoint="contracts")
        if isinstance(ret, list) and len(ret) == 1:
            return ret[0]
        else:
            return ret