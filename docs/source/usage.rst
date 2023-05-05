Usage
=====

.. _installation:

Installation
------------

To use `timecode`, first install it using pip:

.. code-block:: console

   (.venv) $ pip install timecode

`Timecode` assumes Non Drop Frame mode by default.  Non Drop Frame assumes 24fps by default.
But let me tell you something: you can set those to whatever you need.

Specifying the rate:

>>> from timecode import Timecode
>>> Timecode("01:00:00:00", rate=30)
<Timecode 01:00:00:00 @ 30 NDF>

`NonDropFrame` and `DropFrame` counting modes are available in the `modes` subpackage.
Just like `NonDropFrame` assumes 24fps by default, `DropFrame` assumes 30fps by default.

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame
>>> Timecode(86400, mode=DropFrame())
<Timecode 00;48;02;28 @ 30 DF>

So you got all these timecodes goin', but what do you do with them?  Well I guess you can add them together:

>>> # Two Timecodes
>>> Timecode("01:00:01:00") + Timecode("02:03")
<Timecode 01:00:12:03 @ 24 NDF>
..
>>> # A Timecode and some frames
>>> Timecode("59:59:00") + 24
<Timecode 01:00:00:00 @ 24 NDF>

Oh!  You can convert from one kind to another:

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame, NonDropFrame
>>> Timecode("00:48:20:12", mode=NonDropFrame()).convert(rate=30)
<Timecode 00:48:20:15 @ 30 NDF>
>>> Timecode("00:48:20:15", rate=30, mode=NonDropFrame()).convert(mode=DropFrame())
<Timecode 00;48;23;13 (88) @ 30 DF>

Or resample:

.. Creating recipes
.. ----------------
.. 
.. To retrieve a list of random ingredients,
.. you can use the ``lumache.get_random_ingredients()`` function:
.. 
.. .. autofunction:: lumache.get_random_ingredients
.. 
.. The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
.. or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
.. will raise an exception.
.. 
.. .. autoexception:: lumache.InvalidKindError
.. 
.. For example:
.. 
.. >>> import lumache
.. >>> lumache.get_random_ingredients()
.. ['shells', 'gorgonzola', 'parsley']
.. 