Welcome to adisp's documentation!
=================================


Adisp is a library that allows structuring code with asynchronous calls and
callbacks without defining callbacks as separate functions.

The code then becomes sequential and easy to read. The library is not a framework by itself
and can be used in other environments that provides asynchronous working model
(see an example with Tornado server in examples/proxy_example.py).

INSTALLATION
------------

To install adisp you can use `easy_install`::

  easy_install adisp

or via `pip`::

  pip adisp


USAGE
-----

Organizing calling code
^^^^^^^^^^^^^^^^^^^^^^^

All the magic is done with Python 2.5 decorators that allow for control flow to
leave a function, do sometihing else for some time and then return into the
calling function with a result. So the function that makes asynchronous calls
should look like this::

    @process
    def my_handler():
        response = yield some_async_func()
        data = parse_response(response)
        result = yield some_other_async_func(data)
        store_result(result)

Each ``yield`` is where the function returns and lets the framework around it to
do its job. And the code after ``yield`` is what usually goes in a callback.

The ``@process`` decorator is needed around such a function. It makes it callable
as an ordinary function and takes care of dispatching callback calls back into
it.

Writing asynchronous function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the example above functions ``some_async_func`` and ``some_other_async_func``
are those that actually run an asynchronous process. They should follow two
conditions:

- accept a ``callback`` parameter with a callback function that they should call
  after an asynchronous process is finished
- a callback should be called with one parameter -- the result
- be wrapped in the ``@async`` decorator

The @async decorator makes a function call lazy allowing the @process that
calls it to provide a callback to call.

Using async with @-syntax is most convenient when you write your own
asynchronous function (and can make your callback parameter to be named
"callback"). But when you want to call some library function you can wrap it in
async in place.::

    # call http.fetch(url, callback=callback)
    result = yield async(http.fetch)

    # call http.fetch(url, cb=safewrap(callback))
    result = yield async(http.fetch, cbname='cb', cbwrapper=safewrap)(url)

Here you can use two optional parameters for async:

- `cbname`: a name of a parameter in which the function expects callbacks
- `cbwrapper`: a wrapper for the callback iself that will be applied before
  calling it

Chain calls
^^^^^^^^^^^

``@async`` function can also be ``@process'es`` allowing to effectively chain
asynchronous calls as it can be done with normal functions. In this case the
``@async`` decorator shuold be the outer one::

    @async
    @process
    def async_calling_other_asyncs(arg, callback):
        # ....

Multiple asynchronous calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The library also allows to call multiple asynchronous functions in parallel and
get all their result for processing at once::

    @async
    def async_http_get(url, callback):
        # get url asynchronously
        # call callback(response) at the end

    @process
    def get_stat():
        urls = ['http://.../', 'http://.../', ... ]
        responses = yield map(async_http_get, urls)

After *all* the asynchronous calls will complete ``responses`` will be a list of
responses corresponding to given urls.


CONTRIBUTE
----------

Fork https://github.com/Lispython/adisp/ , create commit and pull request.


SEE ALSO
--------

Originally `adisp`_  developed by Ivan Sagalaev, but no longer supported them.

- `PEP 342 - Coroutines via Enhanced Generators <http://www.python.org/dev/peps/pep-0342/>`_
- `A Curious Course on Coroutines and Concurrency <http://dabeaz.com/coroutines/>`_

.. _`adisp`: http://softwaremaniacs.org/blog/2009/12/11/adisp/
