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
import httpx
import datetime
import dataclasses
import json

__all__ = ['AttoClient']

def _try_account_to_key(public_key):
    if type(public_key) == Account:
        public_key = public_key.public_key
    return public_key

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
                                                    from_height=1,
                                                    to_height=100,
                                                    timeout=None):
                print(f'{entry.hash_[0:3]}...\\t{entry.amount}')

    Attributes:
        base_url: the node API's base URL
    """
    def __init__(self, base_url='https://h.tail006b6.ts.net/api', **kwargs):
        """Create a synchronous client with a connection to a node.

        Args:
            base_url: the node API's base URL
            **kwargs: arguments to pass to httpx.Client()
        """
        self.base_url = base_url
        self._client = httpx.Client(base_url=base_url, **kwargs)
    
    def get_account(self, public_key):
        """Return an up-to-date Account object

        Args:
            public_key: an Account object, or a bytestring derived from the
                account name, with the version and checksum omitted
        """
        public_key = _try_account_to_key(public_key)

        return Account(self._get_json(f'/accounts/{public_key}'))

#    TODO: not supported by gatekeeper node; can't test
#    def get_transaction(self, hash_):
#        return Transaction(self._get_json(f'/transactions/{hash_}'))

    def get_instants(self, instant=datetime.datetime.now()):
        """Return time information about the client and the server.

        Args:
            instant: A datetime object

        Returns:
            A dataclass containing the date and time of the client
            (client_instant), the date and time of the server (server_instant)
            and the time delta between the client and the server (difference).
        """
        instant = instant.astimezone(datetime.UTC).isoformat()

        @dataclasses.dataclass
        class Instants:
            client_instant: any
            server_instant: any
            difference: any

        instants = self._get_json(f'instants/{instant}')
        client_instant = datetime.datetime.fromisoformat(instants['clientInstant'])
        server_instant = datetime.datetime.fromisoformat(instants['serverInstant'])
        difference = datetime.timedelta(
                milliseconds=instants['differenceMillis'])
        return Instants(client_instant=client_instant,
                        server_instant=server_instant,
                        difference=difference)

    def account_stream(self, public_key, *args, **kwargs):
        # TODO: docstring
        public_key = _try_account_to_key(public_key)
        yield from self._stream(f'accounts/{public_key}/stream',
                                Account,
                                *args,
                                **kwargs)

#    TODO: not supported by gatekeeper node; can't test
#    def latest_accounts_stream(self, public_key, *args, **kwargs):
        public_key = _try_account_to_key(public_key)
#        with self._client.stream('get',
#                                 f'accounts/stream',
#                                 *args,
#                                 **kwargs) as stream:
#            for line in stream.iter_lines():
#                yield Account(json.loads(line))
    
    def receivables_stream(self, public_key, min_amount=1, *args, **kwargs):
        # TODO: docstring
        public_key = _try_account_to_key(public_key)
        yield from self._stream(f'accounts/{public_key}/receivables/stream',
                                Receivable,
                                *args,
                                **kwargs)

    def entry_stream(self, hash_, *args, **kwargs):
        # TODO: docstring
        yield from self._stream(f'accounts/entries/{hash_}/stream',
                                Entry,
                                *args,
                                **kwargs)

    def entries_stream(self,
                       public_key,
                       from_height,
                       to_height,
                       *args,
                       **kwargs):
        # TODO: docstring
        public_key = _try_account_to_key(public_key)
        yield from self._stream(f'accounts/{public_key}/entries/stream',
                                Entry,
                                params={'fromHeight': from_height,
                                        'toHeight': to_height},
                                *args,
                                **kwargs)

    def latest_entries_stream(self, *args, **kwargs):
        # TODO: docstring
        yield from self._stream(f'accounts/entries/stream',
                                Entry,
                                *args,
                                **kwargs)

    def transaction_stream(self, hash_, *args, **kwargs):
        # TODO: docstring
        yield from self._stream(f'transactions/{hash_}/stream',
                                Transaction,
                                *args,
                                **kwargs)

    def transactions_stream(self,
                            public_key,
                            from_height,
                            to_height,
                            *args,
                            **kwargs):
        # TODO: docstring
        public_key = _try_account_to_key(public_key)
        yield from self._stream(f'accounts/{public_key}/transactions/stream',
                                Transaction,
                                params={'fromHeight': from_height,
                                        'toHeight': to_height},
                                *args,
                                **kwargs)

    def latest_transactions_stream(self, *args, **kwargs):
        # TODO: docstring
        yield from self._stream(f'transactions/stream',
                                Transaction,
                                *args,
                                **kwargs)

    def close(self):
        """Close the client connection.

        When used as a context generator, this is called automatically upon
        exiting the context.
        """
        self._client.close()

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
                yield type_(json.loads(line))
