User's Guide
============

.. _installation:

Installation
------------

To use :py:mod:`timecode`, first install it using pip:

.. code-block:: console

   (.venv) $ pip install timecode


.. _use_timecode:

Timecode
--------

.. autoclass:: timecode.Timecode
   :noindex:

.. _use_mode:

Specifying the Counting Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:py:class:`~timecode.Timecode` will default to :py:class:`~timecode.modes.NonDropFrame` mode, unless otherwise specified.

:py:class:`~timecode.modes.NonDropFrame` and :py:class:`~timecode.modes.DropFrame` counting modes are available in the :py:mod:`timecode.modes` subpackage.

A :py:class:`~timecode.modes.CountingMode` can be set during the creation of a :py:class:`~timecode.Timecode` object by setting the ``mode`` parameter.

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame
..
>>> Timecode(86400, mode=DropFrame())
<Timecode 00;48;02;28 @ 30 DF>

The default counting mode can be set program-wide by assigning a :py:class:`~timecode.modes.CountingMode` class to :py:const:`timecode.Timecode.DEFAULT_MODE` 

.. note::
   Also included in the :py:mod:`timecode.modes` subpackage is an abstract class :py:class:`~timecode.modes.CountingMode`, which can be subclassed to make your 
   own weird little counting modes.  Give it a shot!

.. _use_rate:

Specifying the rate
~~~~~~~~~~~~~~~~~~~

:py:class:`~timecode.Timecode` will default to the :py:const:`~timecode.modes.CountingMode.DEFAULT_RATE` set by the :py:class:`~timecode.modes.CountingMode`.  Or, it 
may be explicitly set with the ``rate`` parameter.

>>> from timecode import Timecode
..
>>> Timecode("01:00:00:00", rate=30)
<Timecode 01:00:00:00 @ 30 NDF>

.. warning::
   The  :py:class:`~timecode.modes.CountingMode` will validate the specified rate and may throw an exception if the rate is inappropriate.  For example, 
   :py:class:`~timecode.modes.DropFrame` only accepts frame rates which are multiples of 30.


Math
~~~~

So you got all these timecodes goin', but what do you do with them?  Well I guess you can add them together:

>>> # Two Timecodes
>>> Timecode("01:00:01:00") + Timecode("02:03")
<Timecode 01:00:03:03 @ 24 NDF>
..
>>> # A Timecode and some frames
>>> Timecode("59:59:00") + 24
<Timecode 01:00:00:00 @ 24 NDF>

Oh!  You can :py:meth:`~timecode.Timecode.resample` from one kind to another:

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame, NonDropFrame
..
>>> Timecode("00:48:20:12", mode=NonDropFrame()).resample(rate=30)
<Timecode 00:48:20:15 @ 30 NDF>
..
>>> Timecode("00:48:20:15", rate=30, mode=NonDropFrame()).resample(mode=DropFrame())
<Timecode 00;48;23;13 (88) @ 30 DF>

More Info
~~~~~~~~~

See :py:class:`timecode.Timecode` in the :doc:`api`.

.. _use_timecoderange:

TimecodeRange
-------------

.. autoclass:: timecode.TimecodeRange
   :noindex:

Yes

More Info
~~~~~~~~~

See :py:class:`timecode.TimecodeRange` in the :doc:`api`.

Counting Modes
--------------
Also yes

More Info
~~~~~~~~~

See :py:class:`timecode.modes.CountingMode` in the :doc:`api`.

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