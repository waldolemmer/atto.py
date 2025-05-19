"""The Account class definition."""
"""
This file is part of Atto.py.

Atto.py is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>. 
"""
from .convert import (_str_to_network, _str_to_algorithm, _raw_to_atto,
                      _timestamp_to_datetime)
from . import _format

class Account:
    # TODO: docstring
    def __init__(self, dict_, client):
        self._client = client

        self.public_key = dict_['publicKey']
        self.network = _str_to_network(dict_['network'])
        self.version = dict_['version']
        self.algorithm = _str_to_algorithm(dict_['algorithm'])
        self.height = dict_['height']
        self.balance = _raw_to_atto(dict_['balance'])
        self.last_transaction_hash = dict_['lastTransactionHash']
        self.last_transaction_timestamp = _timestamp_to_datetime(
                dict_['lastTransactionTimestamp'])
        self.representative_algorithm = _str_to_algorithm(
                dict_['representativeAlgorithm'])
        self.representative_public_key = dict_['representativePublicKey']

    def get(self, *args, **kwargs):
        return client.account(account=self.public_key, *args, stream=False,
                              **kwargs)

    def stream(self, *args, **kwargs):
        yield from self._client.account(account=self.public_key, *args,
                                        stream=True, **kwargs)

    def entries(self, *args, **kwargs):
        return self._client.entries(account=self, *args, **kwargs)

    def receivables(self, *args, **kwargs):
        return self._client.receivables(account=self, *args, **kwargs)

    def transactions(self, *args, **kwargs):
        return self._client.transactions(account=self, *args, **kwargs)

    def __repr__(self):
        return f'<Account {self.public_key[0:6]}... {self.height}>'

    def __str__(self):
        return (f'{_format.pub_key(self.public_key)}: '
                f'{_format.balance(self.balance)} '
                f'{_format.height(self.height)}')
