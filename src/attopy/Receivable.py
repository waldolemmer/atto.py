"""The Receivable class definition."""
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
import datetime

class Receivable:
    # TODO: docstring
    def __init__(self, dict_):
        self.hash_ = dict_['hash']
        self.version = dict_['version']
        self.algorithm = dict_['algorithm']
        self.public_key = dict_['publicKey']
        # TODO: not a POSIX timestamp?
        #self.timestamp = datetime.datetime.fromtimestamp(dict_['timestamp'])
        self.receiver_algorithm = dict_['receiverAlgorithm']
        self.receiver_public_key = dict_['receiverPublicKey']
        self.amount = dict_['amount']
