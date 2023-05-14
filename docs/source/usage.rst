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

A :py:class:`~timecode.modes.CountingMode` can be set during the creation of a :py:class:`~timecode.Timecode` object by setting the ``mode`` parameter.

:py:class:`~timecode.modes.NonDropFrame` and :py:class:`~timecode.modes.DropFrame` counting modes are available in the :py:mod:`timecode.modes` subpackage.

:py:class:`~timecode.Timecode` will default to :py:class:`~timecode.modes.NonDropFrame` mode, unless otherwise specified.

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

Specifying A Range
~~~~~~~~~~~~~~~~~~

:py:class:`~timecode.TimecodeRange` requires at least two of the following parameters: ``start``, ``duration``, ``end``.  The third parameter will be calculated from the other 
two if it is not given.

>>> from timecode import Timecode, TimecodeRange
>>> from timecode.modes import DropFrame, NonDropFrame
..
>>> # Create a `TimecodeRange` from a start and duration
>>> tc_start    = Timecode("00:59:59:00")
>>> tc_duration = Timecode("01:02:00")
>>> TimecodeRange(start=tc_start, duration=tc_duration)
<TimecodeRange 00:59:59:00 - 01:01:01:00 (1488) @ 24 NDF>

>>> # Create a `TimecodeRange` from a start and an end
>>> tc_start  = Timecode("00:59:59:00")
>>> tc_end    = Timecode("01:01:01:00")
>>> TimecodeRange(start=tc_start, end=tc_end)
<TimecodeRange 00:59:59:00 - 01:01:01:00 (1488) @ 24 NDF>

``start``, ``duration``, and ``end`` can be provided as :py:class:`~timecode.Timecode` objects, or as any of the standard types supported by the :py:class:`~timecode.Timecode` 
constructor (:py:class:`str` or :py:class:`int`).  The types can be mixed and matched for each input parameter.  

>>> # Create a `TimecodeRange` that is 48 frames long
>>> tc_start     = Timecode("01:00:00:00")
>>> frm_duration = 48
>>> TimecodeRange(start=tc_start, duration=frm_duration)
<TimecodeRange 01:00:00:00 - 01:00:02:00 (48) @ 24 NDF>

CountingModes and Rates
~~~~~~~~~~~~~~~~~~~~~~~

The :py:class:`~timecode.modes.CountingMode` and rate of the :py:class:`~timecode.TimecodeRange` object is determined by the ``mode`` and ``rate`` of the input :py:class:`~timecode.Timecode` objects; 
or by the :py:class:`~timecode.Timecode`  defaults if none are provided.  Thus, to set the ``mode`` and/or ``rate`` for  a :py:class:`~timecode.TimecodeRange`, at least one of the inputs should be a 
:py:class:`~timecode.Timecode` object with the desired settings.

>>> # Create a `TimecodeRange` that is 60 FPS drop frame (oh my)
>>> tc_start = Timecode("01:00:00;00", rate=60, mode=DropFrame())
>>> duration = 120
>>> TimecodeRange(start=tc_start, duration=duration)
<TimecodeRange 01;00;00;00 - 01;00;02;00 (120) @ 60 DF>

.. warning::
   If more than one of the input parameters are :py:class:`~timecode.Timecode` objects, they must all have matching :py:class:`~timecode.modes.CountingMode`\s and ``rate``\s.  Otherwise, :py:class:`~timecode.TimecodeRange` 
   will raise an exception.

Using TimecodeRange
~~~~~~~~~~~~~~~~~~~

>>> from timecode import Timecode, TimecodeRange
...
>>> tc_start = Timecode("01:00:00:00")
>>> tc_duration = Timecode("00:10")
>>> tc_range = TimecodeRange(start=tc_start, duration=tc_duration)
>>> tc_range
<TimecodeRange 01:00:00:00 - 01:00:00:10 (10) @ 24 NDF>

Accessing Properties
********************

``start``\, ``duration``\, and ``end``\, properties return :py:class:`~timecode.Timecode` objects.

>>> tc_range.start
<Timecode 01:00:00:00 @ 24 NDF>
..
>>> tc_range.start.frame_number
86400
..
>>> tc_range.duration
<Timecode 00:00:00:10 @ 24 NDF>
..
>>> tc_range.end
<Timecode 01:00:00:10 @ 24 NDF>
..
>>> tc_range.end.frame_number
86410

Iterating over a :py:class:`~timecode.TimecodeRange`
****************************************************

>>> len(tc_range)
10
..
>>> for tc in tc_range:
...     repr(tc)
...
'<Timecode 01:00:00:00 @ 24 NDF>'
'<Timecode 01:00:00:01 @ 24 NDF>'
'<Timecode 01:00:00:02 @ 24 NDF>'
'<Timecode 01:00:00:03 @ 24 NDF>'
'<Timecode 01:00:00:04 @ 24 NDF>'
'<Timecode 01:00:00:05 @ 24 NDF>'
'<Timecode 01:00:00:06 @ 24 NDF>'
'<Timecode 01:00:00:07 @ 24 NDF>'
'<Timecode 01:00:00:08 @ 24 NDF>'
'<Timecode 01:00:00:09 @ 24 NDF>'


Checking For Membership
***********************

>>> # Based on Timecode string
>>> "01:00:00:05" in tc_range
True
..
>>> # Based on frame number
>>> 86405 in tc_range
True
..
>>> # Based on a `Timecode` object
>>> Timecode("01:00:00:05") in tc_range
True

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