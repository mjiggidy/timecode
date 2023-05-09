Getting Started
===============

Let's get ya started real quick here.

Timecode
--------

>>> # Import it
>>> from timecode import Timecode

You can create a :py:class:`~timecode.Timecode` from a frame number, or a timecode :py:class:`str`.

>>> # Timecode from a frame number
>>> Timecode(86400)
<Timecode 01:00:00:00 @ 24 NDF>

>>> # Timecode from a string
>>> Timecode("01:00:00:00")
<Timecode 01:00:00:00 @ 24 NDF>
..
>>> # Protip: You don't need leading zeroes
>>> Timecode("30:00")
<Timecode 00:00:30:00 @ 24 NDF>

----

Specify a rate (see:  :ref:`use_rate`)

>>> # Specify a rate
>>> Timecode("59:40", rate=30)
<Timecode 00:00:59:40 @ 30 NDF>

----

Specify a counting mode (see:  :ref:`use_mode`)

>>> # Specify a different counting mode
>>> from timecode.modes import DropFrame
>>> Timecode("32:19;28", mode=DropFrame())
<Timecode 00;32;19;28 @ 30 DF>

----

For more information, check out the :ref:`use_timecode` section of the :doc:`usage`.

TimecodeRange
-------------

Define a range of frames by start, end, and/or duration!

>>> from timecode import Timecode, TimecodeRange
>>> tc_start = Timecode("00:59:59:00")
>>> tc_dur = Timecode("00:00:00:10")
>>> tc_range = TimecodeRange(start=tc_start, duration=tc_dur)
>>> repr(tc_range)
<TimecodeRange 00:59:59:00 - 00:59:59:10 (10) @ 24 NDF>
..
>>> Loop over it amd admore the frames for what they are
>>> for tc in tc_range:
...     print(tc)
...
00:59:59:00
00:59:59:01
00:59:59:02
00:59:59:03
00:59:59:04
00:59:59:05
00:59:59:06
00:59:59:07
00:59:59:08
00:59:59:09

----

For more information, check out the :ref:`use_timecoderange` section of the :doc:`usage`.

.. note::

   This project is under active development.

Contents
--------

.. toctree::
   :maxdepth: 2
   
   usage
   api