Usage
=====

.. _installation:

Installation
------------

To use `timecode`, first install it using pip:

.. code-block:: console

   (.venv) $ pip install timecode

Creating a timecode
-------------------

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. autoclass:: timecode.Timecode

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`timecode.Timecode.__init__()`
will raise an exception.

.. .. autoexception:: timecode.InvalidKindError

For example:

>>> from timecode import Timecode
>>> Timecode(86400)
<Timecode 01:00:00:00 @ 24 NDF>
