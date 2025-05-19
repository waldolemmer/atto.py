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


    A Python API wrapper for the `Atto`_ node API.

Atto.py provides a Pythonic interface for communicating with Atto nodes,
allowing developers to interact with the account-chain ledgers without dealing
with low-level API details.

An instance of `AttoClient()` represents a connection to an Atto node.
Communication with the node happens through `AttoClient()`'s members.

The methods wrap the information from `API responses
<https://atto.cash/api/node>`_ in the form of Python builtins and classes in
this module, such as:

* Account
* Entry
* Receivable
* Transaction
* Block

Typical usage example:

.. code-block:: python

    from attopy import AttoClient
    
    ADDRESS = '<your_address>'
    
    with AttoClient('http://h:8080') as node:
        print('Account:')
        account = node.account(ADDRESS)
        print(account)
        print()
    
        COUNT = 10
        print(f'First {COUNT} entries:')
        for entry in account.entries(to=COUNT):
            print(entry)

Example output:

.. code-block:: text

    Account:
    FF9DA..E37D:     2,665,633.1703     #93
    
    First 10 entries:
    03E9.. O           10.0000 ECC0E..99EA FF9DA..E37D      #1 @ 20250415 18:03
    2B82.. +           10.0000 ECC0E..99EA FF9DA..E37D      #2 @ 20250415 18:03
    04D3.. +           10.0000 ECC0E..99EA FF9DA..E37D      #3 @ 20250415 18:05
    5DF6.. +           10.0000 ECC0E..99EA FF9DA..E37D      #4 @ 20250415 18:06
    7AB1.. +           10.0000 ECC0E..99EA FF9DA..E37D      #5 @ 20250415 18:07
    1D46.. +           10.0000 ECC0E..99EA FF9DA..E37D      #6 @ 20250415 18:39
    A710.. +           10.0000 ECC0E..99EA FF9DA..E37D      #7 @ 20250415 18:47
    EE78.. +           10.0000 ECC0E..99EA FF9DA..E37D      #8 @ 20250415 18:49
    E911.. +           10.0000 ECC0E..99EA FF9DA..E37D      #9 @ 20250415 18:50
    C435.. +           10.0000 ECC0E..99EA FF9DA..E37D     #10 @ 20250415 18:52

.. _Atto: https://atto.cash/

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

Need help?
----------

I'm always available in the `Atto Discord server`_. Feel free to get in touch.

For some insight into what inspired me to write this library, see `this blog
post <https://atto.cash/blog/writing-python-api-wrapper>`_.

.. _Atto Discord server: https://discord.gg/TfQGzEdzKp
