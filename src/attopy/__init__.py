"""A Python interface for the Atto node API.

This module includes the synchronous client AttoClient (for interacting with
the API) as well as utility functions that may be needed during this
interaction.

Typical usage example::

    ADDRESS = 'ad7z3jdoeqwayzpaiafizb5su6zc2fyvbeg2wq5t3yfj3q5iuprx23z437juk'

    with AttoClient() as atto_client:
        account = atto_client.get_account(address_to_key(ADDRESS))

        # print first 100 transactions
        print('Hash\\tAmount')
        for entry in atto_client.entries_stream(account,
                                                from_height=1,
                                                to_height=100,
                                                timeout=None):
            print(f'{entry.hash_[0:3]}...\\t{entry.amount}')

Although this documentation should be sufficient, an API reference can be found
at https://atto.cash/api/node.
"""
"""This file is part of Atto.py.

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
import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    dist_name = "atto.py"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

from .AttoClient import *
import base64

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
