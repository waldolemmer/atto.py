"""Conversion functions between the API's types and our types"""
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
import base64
import datetime
import decimal
from .field_types import *

decimal.setcontext(decimal.BasicContext) # enable most traps
_context = decimal.getcontext()
for signal in (decimal.Inexact, decimal.Rounded, decimal.Subnormal):
    _context.traps[signal] = True # enable the remaining traps
_context.prec = 20 # 99,999,999,999.999999999

__all__ = ['address_to_key']

def address_to_key(address_without_protocol):
    """Convert an address into a public key.

    Addresses are base32-encoded strings that start with atto://. Public keys
    are the decoded form, with the version and checksum removed.

    Client API functions accept public keys, not addresses. Similarly, accounts
    returned from API functions contain public keys, not addresses.

    Args:
        address: An address (which typically starts with atto://), with atto://
            removed. The protocol (atto://) can be removed from an address using
            ``address.removeprefix('atto://')``.
    Return:
        A public key in the form of a binary string that can be passed to the
        Atto.py client API functions.
    """
    decoded = base64.b32decode(address_without_protocol.upper() + '===')

    # The first byte is the version. The last five bytes are the checksum.
    key_bytes_hex = (format(byte, '02X') for byte in decoded[1:-5])

    return ''.join(key_bytes_hex)

def _timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000)

def _raw_to_atto(amount) -> decimal.Decimal:
    return amount / decimal.Decimal(1_000_000_000)

def _str_to_network(str_):
    try:
        return Network(str_)
    except ValueError:
        raise NotImplementedError(f'{str_} is not a known network')

def _str_to_algorithm(str_):
    try:
        return Algorithm(str_)
    except ValueError:
        raise NotImplementedError(f'{str_} is not a known algorithm')

def _str_to_block_type(str_):
    try:
        return BlockType(str_)
    except ValueError:
        raise NotImplementedError(f'{str_} is not a known block type')
