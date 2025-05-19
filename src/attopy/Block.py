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
from . import _format

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
        self.representative_algorithm = dict_.get('representativeAlgorithm', None)
        if self.representative_algorithm is not None:
            self.representative_algorithm = _str_to_algorithm(
                    self.representative_algorithm)
        self.representative_public_key = dict_.get('representativePublicKey', None)

    def __repr__(self):
        return f'<Block {self.public_key[0:6]}... {self.height}>'

    def __str__(self):
        return (f'{_format.block_type(self.type)} '
                f'{_format.balance(self.balance)} '
                f'{_format.pub_key(self.public_key)}'
                f'{_format.height(self.height)} @ '
                f'{_format.timestamp(self.timestamp)}')
