"""A Python interface for the Atto node API.

This module includes the synchronous client AttoClient (for interacting with
the API) as well as utility classes and functions that may be needed during
this interaction.

Typical usage example::

    ADDRESS = 'atto://ad7z3jdoeqwayzpaiafizb5su6zc2fyvbeg2wq5t3yfj3q5iuprx23z437juk'

    with AttoClient() as atto_client:
        account = atto_client.get_account(ADDRESS)

        # print first 100 transactions
        print('Hash\\tAmount')
        for entry in atto_client.entries_stream(account,
                                                from_height=1,
                                                to_height=100,
                                                timeout=None):
            print(f'{entry.hash_[0:3]}...\\t{entry.amount}')

Although this documentation should be sufficient, an `API reference
<https://atto.cash/api/node>`_ exists.
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
from .convert import *
