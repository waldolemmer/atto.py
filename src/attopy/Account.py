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
class Account:
    # TODO: docstring
    def __init__(self, dict_):
        self.public_key = dict_['publicKey']
        self.network = dict_['network']
        self.version = dict_['version']
        self.algorithm = dict_['algorithm']
        self.height = dict_['height']
        self.balance = dict_['balance']
        self.last_transaction_hash = dict_['lastTransactionHash']
        self.last_transaction_timestamp = dict_['lastTransactionTimestamp']
        self.representative_algorithm = dict_['representativeAlgorithm']
        self.representative_public_key = dict_['representativePublicKey']
