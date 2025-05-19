"""The Transaction class definition."""
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
from .Block import Block

class Transaction:
    # TODO: docstring
    def __init__(self, dict_, client):
        self._client = client

        self.block = Block(dict_['block'])
        self.signature = dict_['signature']
        self.work = dict_['work']

    def __repr__(self):
        return f'<Transaction {self.block.public_key[0:6]}... {self.block.height}>'

    def __str__(self):
        return str(self.block)
