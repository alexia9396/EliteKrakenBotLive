import time
import hashlib
import hmac
import base64
import requests
import urllib.parse
import logging
from bot.utils.helpers import load_config

class KrakenProAPI:
    def __init__(self):
        self.config = load_config()
        self.api_key = self.config["kraken"]["api_key"]
        self.api_secret = self.config["kraken"]["api_secret"]
        self.base_url = "https://api.kraken.com"

    def _sign(self, urlpath, data, nonce):
        post_data = urllib.parse.urlencode(data)
        encoded = (str(nonce) + post_data).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        signature = hmac.new(base64.b64decode(self.api_secret), message, hashlib.sha512)
        sig_digest = base64.b64encode(signature.digest())
        return sig_digest.decode()

    def _request(self, method, endpoint, data=None, private=False):
        urlpath = f"/0/{endpoint}"
        url = self.base_url + urlpath
        headers = {}
        data = data or {}

        if private:
            nonce = str(int(time.time() * 1000))
            data["nonce"] = nonce
            headers["API-Key"] = self.api_key
            headers["API-Sign"] = self._sign(urlpath, data, nonce)

        try:
            response = requests.post(url, headers=headers, data=data) if private else requests.get(url, params=data)
            response.raise_for_status()
            result = response.json()
            if result.get("error"):
                logging.warning(f"Kraken API error: {result['error']}")
            return result.get("result")
        except Exception as e:
            logging.error(f"Exception calling Kraken API: {e}")
            return None

    def get_balance(self):
        return self._request("private", "Balance", private=True)

    def get_ticker(self, pair):
        return self._request("public", "Ticker", data={"pair": pair})

    def get_tradable_pairs(self):
        return self._request("public", "AssetPairs")

    def place_order(self, pair, type_, ordertype, volume, price=None):
        data = {
            "pair": pair,
            "type": type_,
            "ordertype": ordertype,
            "volume": str(volume),
        }
        if price:
            data["price"] = str(price)
        return self._request("private", "AddOrder", data=data, private=True)

    def cancel_order(self, txid):
        return self._request("private", "CancelOrder", data={"txid": txid}, private=True)

    def get_open_orders(self):
        return self._request("private", "OpenOrders", private=True)

    def get_closed_orders(self):
        return self._request("private", "ClosedOrders", private=True)
