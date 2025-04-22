"""The Block class definition."""
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
from .convert import (_str_to_algorithm, _timestamp_to_datetime,
                      _str_to_network, _raw_to_atto, _str_to_block_type)

class Block:
    # TODO: docstring
    def __init__(self, dict_):
        self.public_key = dict_['publicKey']
        self.version = dict_['version']
        self.algorithm = _str_to_algorithm(dict_['algorithm'])
        self.timestamp = _timestamp_to_datetime(dict_['timestamp'])
        self.network = _str_to_network(dict_['network'])
        self.balance = _raw_to_atto(dict_['balance'])
        self.type = _str_to_block_type(dict_['type'])
        self.height = dict_.get('height')
        self.previous = dict_.get('previous')
        # TODO: not present (tested /transactions/{hash}/stream
        #self.representative_algorithm = dict_['representativeAlgorithm']
        #self.representative_public_key = dict_['representativePublicKey']
