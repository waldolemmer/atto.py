=========
Changelog
=========

Version 0.9.0
=============

* feat: Throw ValueError immediately when a method is incorrectly called with
  stream=False, rather than waiting for the generator to be iterated once.
  Affected methods:
  * AttoClient.entry()
  * AttoClient.transaction()
  * AttoClient.receivables()
  * AttoClient.entries()
  * AttoClient.transactions()

Version 0.8.2
=============

* fix: Accept httpx arguments such as timeout in AttoClient.account()

Version 0.8.1
=============

* fix: Fix undefined 'client' variable in Account.stream()

Version 0.8.0
=============

* feat: The following functions now have custom .__repr__() methods:
  * AttoClient
  * Account
  * Block
  * Entry
  * Instants
  * Receivable
  * Transaction
* feat: The following functions now convert nicely to strings and are displayed
  in table format when printed with print():
  * Account
  * Block
  * Entry
  * Instants
  * Receivable
  * Transaction

Version 0.7.0
=============

* feat: add Account.entries(), Account.receivables() and
  Account.transactions(), which are equivalent to AttoClient.entries(account),
  AttoClient.receivables(account) and AttoClient.transactions(account),
  respectively.

Version 0.6.1
=============

* fix: AttoClient.account() now returns an Account object instead of a
  generator when stream=False

Version 0.6.0
=============

* feat: add Account.{get,stream}()
* feat: add Entry.stream()

Version 0.5.0
=============

* feat: rename get_instants to instants
* feat: rename latext_x_stream to x with unused account param
* feat: rename get_account to account
* feat: move account_stream to account(stream=True)
* feat: rename entry_stream to entry
* feat: move transaction_stream to transaction
* feat: move entries_stream to entries
* feat: rename receivables_stream to receivables
* feat: move transactions_stream to transactions

Version 0.4.0
=============

* feat: accept addresses

Version 0.3.0
=============

* feat: rename {from,to}_height to {from\_,to}

Version 0.2.0
=============

* feat: use Decimal for amounts

  Using Decimal avoids floating-point errors.

Version 0.1.3
=============

feat: convert fields
--------------------

* refactor: move address_to_key to convert.py
* refactor: add field conversion functions
* feat: return some fields as enums

  The following fields are now returned as enums:
  
  * network
  * algorithm
  * type/block_type
* refactor: fix typo
* feat: add representative fields to Block
* feat: return timestamps as datetime objects

Version 0.1.2
=============

fix: get_instants() default argument
------------------------------------

The default argument of AttoClient.get_instants() was ``datetime.now()``.
However, Python only evaluates default arguments once, so it did not reflect
the current time.

Now, the default argument is None, which is equivalent to
datetime.now().

Version 0.1.1
=============

fix: change base url to Waldo's node
------------------------------------

The gatekeeper base URL doesn't support the full API. This commit
updates the URL to point to Waldo's node.

Waldo's node doesn't guarantee high uptime, so users should have a
fallback node.


Version 0.1.0
=============

A synchronous client (AttoClient) with most of the GET methods implemented.

* Minimal documentation
* No testing framework
* No POST methods
* No GET methods that don't work with https://gatekeeper.live.application.atto.cash/
