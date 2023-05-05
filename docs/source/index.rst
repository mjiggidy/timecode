How to timecode
===============

Timecode
--------

Let's get ya started real quick here:

>>> from timecode import Timecode
..
>>> # Timecode from a frame number
>>> Timecode(86400)
<Timecode 01:00:00:00 @ 24 NDF>
..
>>> # Timecode from a string
>>> Timecode("01:00:00:00")
<Timecode 01:00:00:00 @ 24 NDF>
..
>>> # Specifying a rate
>>> Timecode("59:40", rate=30)
<Timecode 00:00:59:40 @ 30 NDF>
..
>>> # Specifying a different counting mode
>>> from timecode.modes import DropFrame
>>> Timecode("32:19;28", mode=DropFrame())
<Timecode 00;32;19;28 @ 30 DF>

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







Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

.. note::

   This project is under active development.

Contents
--------

.. toctree::

   usage
   api