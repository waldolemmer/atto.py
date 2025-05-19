"""The Entry class definition."""
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
from .convert import (_str_to_algorithm, _str_to_block_type, _raw_to_atto,
                      _timestamp_to_datetime)
from . import _format

class Entry:
    # TODO: docstring
    def __init__(self, dict_, client):
        self._client = client

        self.hash_ = dict_['hash']
        self.algorithm = _str_to_algorithm(dict_['algorithm'])
        self.public_key = dict_['publicKey']
        self.height = dict_['height']
        self.block_type = _str_to_block_type(dict_['blockType'])
        self.subject_algorithm = _str_to_algorithm(dict_['subjectAlgorithm'])
        self.subjectPublicKey = dict_['subjectPublicKey']
        self.previous_balance = _raw_to_atto(dict_['previousBalance'])
        self.balance = _raw_to_atto(dict_['balance'])
        self.amount = self.balance - self.previous_balance
        self.timestamp = _timestamp_to_datetime(dict_['timestamp'])

    def stream(self, *args, **kwargs):
        yield from client.entry(self.hash_, *args, stream=True, **kwargs)

    def __repr__(self):
        return f'<Entry {self.hash_[0:6]}...>'

    def __str__(self):
        return (f'{_format.hash(self.hash_)} '
                f'{_format.block_type(self.block_type)}'
                f'{_format.amount(self.amount)} '
                f'{_format.pub_key(self.subjectPublicKey if self.amount > 0 else self.public_key)} '
                f'{_format.pub_key(self.public_key if self.amount > 0 else self.subjectPublicKey)} '
                f'{_format.height(self.height)} @ '
                f'{_format.timestamp(self.timestamp)}')
