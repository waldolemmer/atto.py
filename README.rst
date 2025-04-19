.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/attopy.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/attopy
    .. image:: https://img.shields.io/coveralls/github/<USER>/attopy/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/attopy
    .. image:: https://img.shields.io/pypi/v/attopy.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/attopy/
    .. image:: https://img.shields.io/conda/vn/conda-forge/attopy.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/attopy
    .. image:: https://pepy.tech/badge/attopy/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/attopy
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/attopy

.. image:: https://readthedocs.org/projects/attopy/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://attopy.readthedocs.io/en/stable/
.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=======
atto.py
=======


    A Python API wrapper for the Atto node API.


An instance of `AttoClient()` represents a connection to an Atto node.
Communication with the node happens through `AttoClient()`'s members.

The methods wrap the information from API responses in the form of
Python builtins and classes in this module, such as:

* Account
* Entry
* Receivable
* Transaction
* Block

Typical usage example:

.. code-block:: python

    from attopy import AttoClient, address_to_key
    
    ADDRESS = '<your_address>'.removeprefix('atto://')
    
    with AttoClient() as node:
        public_key = address_to_key(ADDRESS)
        account = node.get_account(public_key)
        print(f'balance: {account.balance}')
    
        # print first 100 transactions
        print('Hash\\tAmount')
        for entry in node.entries_stream(account, from_height=1, to_height=10, timeout=None):
            print(f'{entry.hash_[0:4]}...\\t{entry.amount}')

Example output:

.. code-block:: text

    balance: 1349500000
    hash        Amount
    A5DF...     10000000
    BEEF...     49000000000
    DEAD...     2500000000
    ... 97 more lines ...

Installation
------------

Simply run ``pip install atto.py``.

What's missing?
---------------

`AttoClient()` is a synchronous client, meaning that all calls are blocking.
Generators that access endpoints that stream indefinitely (such as the endpoint
to scan for new entries) therefore should not be iterated over using `for`
without a timeout, as they will never end and cannot be interrupted without
user intervention.

An asynchronous client, `AttoClientAsync()`, is in the works. This client would
facilitate near-instant updating of UI elements representing balances and lists
of new entries, and would be able to wait for transactions to be confirmed,
all without blocking the main thread.

Currently, `AttoClient()` supports some of the GET methods provided by the node
API, and none of the POST methods. This means that `AttoClient()` can only
query nodes, and can't post transactions. This will change once a testing
framework has been set up.

All classes and members should be fully documented soon.
