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

class Entry:
    # TODO: docstring
    def __init__(self, dict_):
        self.hash_ = dict_['hash']
        self.algorithm = dict_['algorithm']
        self.public_key = dict_['publicKey']
        self.height = dict_['height']
        self.block_type = dict_['blockType']  # TODO: enum (all classes)
        self.subject_algorithm = dict_['subjectAlgorithm']
        self.subjectPublicKey = dict_['subjectPublicKey']

        self.previous_balance = dict_['previousBalance']
        self.balance = dict_['balance']
        self.amount = self.balance - self.previous_balance
        # TODO: not a POSIX timestamp?
        #self.timestamp = datetime.datetime.fromtimestamp(dict_['timestamp'])
