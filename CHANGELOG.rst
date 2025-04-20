=========
Changelog
=========

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
