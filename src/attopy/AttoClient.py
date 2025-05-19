"""The AttoClient class definition."""
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
from .Account import Account
from .Transaction import Transaction
from .Receivable import Receivable
from .Entry import Entry
from .convert import address_to_key
from .boilerplate import _repr
import httpx
import datetime
import dataclasses
import json

__all__ = ['AttoClient']

def _account_to_key(account):
    if type(account) == Account:
        return account.public_key

    if len(account) == 64:
        return account

    if account.startswith('atto://'):
        account = account.removeprefix('atto://')

    return address_to_key(account)

_DEFAULT_BASE_URL = 'https://h.tail006b6.ts.net/api'
class AttoClient:
    """A synchronous connection to an Atto Node.

    The class methods directly correspond to API endpoints.

    Because they are synchronous, all methods, including the generators, block
    the thread that they're called in.

    Typical usage example::

        with AttoClient() as atto_client:
            account = atto_client.get_account(PUBLIC_KEY)

            # print first 100 transactions
            print('Hash\\tAmount')
            for entry in atto_client.entries_stream(account,
                                                    from_=1,
                                                    to=100,
                                                    timeout=None):
                print(f'{entry.hash_[0:3]}...\\t{entry.amount}')

    Attributes:
        base_url: the node API's base URL
    """
    def __init__(self, base_url=_DEFAULT_BASE_URL, **kwargs):
        """Create a synchronous client with a connection to a node.

        Args:
            base_url: the node API's base URL
            **kwargs: arguments to pass to httpx.Client()
        """
        self.base_url = base_url
        self._client = httpx.Client(base_url=base_url, **kwargs)

    def instants(self, instant=None):
        """Return time information about the client and the server.

        Args:
            instant: A datetime object. Defaults to datetime.now().

        Returns:
            A dataclass containing the date and time of the client
            (client_instant), the date and time of the server (server_instant)
            and the time delta between the client and the server (difference).
        """
        if not instant:
            instant = datetime.datetime.now()
        instant = instant.astimezone(datetime.UTC).isoformat()

        @dataclasses.dataclass
        class Instants:
            client_instant: any
            server_instant: any
            difference: any

            def __repr__(self):
                return f'<Instants {server_instant.isoformat()}>'

            def __str__(self):
                return f'{self.difference.microseconds/1000000:6>,.3f} seconds {"ahead " if self.difference.total_seconds() < 0 else "behind"}'

        instants = self._get_json(f'instants/{instant}')
        client_instant = datetime.datetime.fromisoformat(instants['clientInstant'])
        server_instant = datetime.datetime.fromisoformat(instants['serverInstant'])
        difference = datetime.timedelta(
                milliseconds=instants['differenceMillis'])
        return Instants(client_instant=client_instant,
                        server_instant=server_instant,
                        difference=difference)
    
    def account(self, account, *args, stream=False, **kwargs):
        """Return an up-to-date Account object

        Args:
            account: an Account object, an address (with or without the
            atto:// protocol prefix) or a bytestring derived from the account
            name, with the version and checksum omitted (using
            address_to_key())
        """
        public_key = _account_to_key(account)

        if not stream:
            return Account(self._get_json(f'/accounts/{public_key}'), self)

        return self._stream(f'accounts/{public_key}/stream',
                            Account,
                            *args,
                            **kwargs)

    # stream=False because "entry" is singular, and singular methods aren't
    # streamed by default
    def entry(self, hash_, *args, stream=False, **kwargs):
        # TODO: docstring
        if not stream:
            raise ValueError(f'{stream=}')

        return self._stream(f'accounts/entries/{hash_}/stream',
                            Entry,
                            *args,
                            **kwargs)

    # stream=False because "transaction" is singular, and singular methods aren't
    # streamed by default
    def transaction(self, hash_, *args, stream=False, **kwargs):
        # TODO: docstring
        if not stream:
            raise ValueError(f'{stream=}')

        return self._stream(f'transactions/{hash_}/stream',
                            Transaction,
                            *args,
                            **kwargs)

#    TODO: not supported by gatekeeper node; can't test
#    def get_transaction(self, hash_):
#        return Transaction(self._get_json(f'/transactions/{hash_}'), self)

#    TODO: not supported by gatekeeper node; can't test
#    def latest_accounts_stream(self, public_key, *args, **kwargs):
#        public_key = _account_to_key(public_key)
#        with self._client.stream('get',
#                                 f'accounts/stream',
#                                 *args,
#                                 **kwargs) as stream:
#            for line in stream.iter_lines():
#                yield Account(json.loads(line), self)

    def receivables(self, account, *args, min_amount=1, stream=True, **kwargs):
        # TODO: docstring
        if not stream:
            raise ValueError(f'{stream=}')

        public_key = _account_to_key(account)
        return self._stream(f'accounts/{public_key}/receivables/stream',
                            Receivable, *args, **kwargs)

    def entries(self, account=None, *args, from_=None, to=4294967295, stream=True,
                **kwargs):
        # TODO: docstring
        if not stream:
            raise ValueError(f'{stream=}')

        if account is None:
            endpoint = 'accounts/entries/stream'
            params = {}
            if from_ is not None:
                raise ValueError(f'{account=}, {from_=}')
            if to is not None:
                raise ValueError(f'{account=}, {to=}')
        else:
            endpoint = f'accounts/{_account_to_key(account)}/entries/stream'
            params = {'fromHeight': from_, 'toHeight': to}

        return self._stream(endpoint, Entry, params=params, *args, **kwargs)

    def transactions(self, account=None, *args, from_=None, to=None,
                     stream=True, **kwargs):
        # TODO: docstring
        if not stream:
            raise ValueError(f'{stream=}')
        
        if account is None:
            endpoint = 'transactions/stream'
            params = {}
        else:
            public_key = _account_to_key(account)
            endpoint = f'accounts/{public_key}/transactions/stream'
            params = {'fromHeight': from_, 'toHeight': to}

        return self._stream(endpoint, Transaction, params=params, *args,
                            **kwargs)

    def close(self):
        """Close the client connection.

        When used as a context generator, this is called automatically upon
        exiting the context.
        """
        self._client.close()

    def __repr__(self):
        return _repr(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get_json(self, *args, **kwargs):
        response = self._client.get(*args, **kwargs)
        response.raise_for_status()
        return response.json()

    def _stream(self, url, type_, *args, **kwargs):
        """Yield a type_ constructed from the next line at url"""
        with self._client.stream('get', url, *args, **kwargs) as stream:
            for line in stream.iter_lines():
                yield type_(json.loads(line), self)
