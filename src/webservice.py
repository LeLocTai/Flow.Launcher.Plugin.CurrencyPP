import urllib
import urllib.request as request
import json


class PrivateDomain():

    url = 'https://arthurvedana.com/currency/latest.json'

    def __init__(self, plugin):
        self.plugin = plugin

    def build_request(self):
        return self.url

    def load_from_url(self):
        self.plugin.logger.info("loading from cache server...")
        opener = request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]

        requestURL = self.build_request()

        with opener.open(requestURL) as conn:
            response = conn.read()

        data = json.loads(response)
        rates = data['rates']

        currencies = {}
        for rate in rates:
            private_rate = {
                'name': rate,
                'price': rates[rate]
            }
            currencies[rate] = private_rate

        return currencies, data['timestamp']


class OpenExchangeRates():

    url = 'https://openexchangerates.org/api/latest.json'

    def __init__(self, plugin, app_id):
        self.plugin = plugin
        self.app_id = app_id

    def build_request(self, parameters):
        return self.url + '?' + urllib.parse.urlencode(parameters)

    def load_from_url(self):
        self.plugin.logger.info("loading from API...")
        opener = request.build_opener()

        params = {'app_id': self.app_id,
                  'show_alternative': True}

        requestURL = self.build_request(params)

        with opener.open(requestURL) as conn:
            response = conn.read()

        data = json.loads(response)
        rates = data['rates']

        currencies = {}
        for rate in rates:
            private_rate = {
                'name': rate,
                'price': rates[rate]
            }
            currencies[rate] = private_rate

        return currencies, data['timestamp']
