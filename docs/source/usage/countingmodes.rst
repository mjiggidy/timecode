Counting Modes
==============

A :py:class:`~timecode.modes.CountingMode` defines the frame counting behavior of a :py:class:`~timecode.Timecode` or 
:py:class:`~timecode.TimecodeRange` object.  It also handles string formatting, as different modes may be represented 
differently (e.g. :py:class:`~timecode.modes.DropFrame` timecode traditionally uses a ``;`` separator).

.. autoclass:: timecode.modes.CountingMode
   :noindex:

Two of the most common modes are provided: :py:class:`~timecode.modes.NonDropFrame` and :py:class:`~timecode.modes.DropFrame`.  
Additional modes may be created by subclassing the :py:class:`~timecode.modes.CountingMode` class.

.. note::
	The :py:class:`~timecode.modes.CountingMode` classes are provided in the :py:mod:`timecode.modes` subpackage.


Using a Counting Mode
---------------------

A :py:class:`~timecode.modes.CountingMode` is typically provided by setting the ``mode`` parameter to an instance of a 
:py:class:`~timecode.modes.CountingMode` during the creation of a :py:class:`~timecode.Timecode` object:

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame, NonDropFrame
>>> Timecode("01:00:00:00", mode=DropFrame())
<Timecode 01;00;00;00 @ 30 DF>

See also: :ref:`use_mode`

Defaults
--------

A :py:class:`~timecode.modes.CountingMode` defines a default ``rate`` to use if the ``rate`` is not explicitly set during 
the creation of a :py:class:`~timecode.Timecode` object.  It may also define additional rules to validate the ``rate``.  
Below are the defaults and rules for the out-of-the-box :py:class:`~timecode.modes.CountingMode` classes:

.. list-table::
	:header-rows: 1

	* - Mode
	  - Default Rate
	  - Additional Rules
	
	* - :py:class:`~timecode.modes.NonDropFrame`
	  - 24
	  - Rate must be a positive integer
	
	* - :py:class:`~timecode.modes.DropFrame`
	  - 30
	  - Rate must be a positive integer, and a multiple of 30

Here we illustrate the default rates and rate validation:

>>> from timecode import Timecode
>>> from timecode.modes import DropFrame, NonDropFrame
..
>>> # NonDropFrame defaults to 24 fps
>>> Timecode("01:00:00:00", mode=NonDropFrame())
<Timecode 01:00:00:00 @ 24 NDF>
..
>>> # DropFrame defaults to 30 fps
>>> Timecode("01:00:00:00", mode=DropFrame())
<Timecode 01;00;00;00 @ 30 DF>
..
>>> # DropFrame throws a `ValueError` for rates
>>> # that are not multiples of 30
>>> Timecode("01:00:00:00", mode=DropFrame(), rate=24)
ValueError: Drop Frame mode requires the rate to be a multiple of 30.


See also: :ref:`use_rate`

More Info
---------

See :py:class:`timecode.modes.CountingMode` in the API Documentation.