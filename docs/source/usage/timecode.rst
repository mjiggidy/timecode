Timecode
========

:py:class:`~timecode.Timecode` is good.

.. autoclass:: timecode.Timecode
   :noindex:

.. _use_mode:

Specifying The Counting Mode
----------------------------

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

See also: :doc:`./countingmodes`

.. _use_rate:

Specifying The Rate
-------------------

:py:class:`~timecode.Timecode` will default to the :py:const:`~timecode.modes.CountingMode.DEFAULT_RATE` set by the :py:class:`~timecode.modes.CountingMode`.  Or, it 
may be explicitly set with the ``rate`` parameter.

>>> from timecode import Timecode
..
>>> Timecode("01:00:00:00", rate=30)
<Timecode 01:00:00:00 @ 30 NDF>

.. warning::
   The  :py:class:`~timecode.modes.CountingMode` will validate the specified rate and may throw an exception if the rate is inappropriate.  For example, 
   :py:class:`~timecode.modes.DropFrame` only accepts frame rates which are multiples of 30.


Doin' Math
----------

Arithmetic
~~~~~~~~~~

:py:class:`timecode.Timecode` supports typical arithmetic operations (addition, subtraction, multiplication, and division) against 
other :py:class:`timecode.Timecode` objects, as well as other :py:class:`int`\-type numbers.  If the operand is an :py:class:`int`\, 
it will be assumed to be a frame number.

>>> # Add two `Timecode`s
>>> Timecode("01:00:01:00") + Timecode("02:03")
<Timecode 01:00:03:03 @ 24 NDF>
..
>>> # Add a `Timecode`` and some frames
>>> Timecode("59:59:00") + 24
<Timecode 01:00:00:00 @ 24 NDF>

Resampling
~~~~~~~~~~

Oh!  You can :py:meth:`~timecode.Timecode.resample` a :py:class:`timecode.Timecode` object from one rate and/or mode to another.

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame, NonDropFrame
..
>>> Timecode("00:48:20:12", mode=NonDropFrame()).resample(rate=30)
<Timecode 00:48:20:15 @ 30 NDF>
..
>>> Timecode("00:48:20:15", rate=30, mode=NonDropFrame()).resample(mode=DropFrame())
<Timecode 00;48;23;13 (88) @ 30 DF>


More Info
---------

See :py:class:`timecode.Timecode` in the API Documentation.