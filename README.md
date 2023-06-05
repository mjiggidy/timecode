# timecode

This is a refactor and retooling of the `timecode` library in my `posttools` package.  **Currently under heavy development.**

The goal is to support custom frame counting modes, handle frame rate conversions, and support iterable timecode ranges.

## Basic Usage

### Timecode

The `Timecode` class defaults to 24fps, Non-Drop Frame timecode.  A frame number or a timecode string can be given:

```python
from timecode import Timecode
tc = Timecode("01:00:00:00")
print("Repr:",repr(tc))
print("String:",tc)
print("Frames:",tc.frame_number)
```

Output:

     Repr: <Timecode 01:00:00:00 @ 24 NDF>
     String: 01:00:00:00
     Frames: 86400
     
Frame rate and counting modes can be specified explicitly:

```python
from timecode import Timecode, modes
tc = Timecode("01:00:00:00", rate=24, mode=modes.NonDropFrame())
print("Repr:",repr(tc))
print("String:",tc)
print("Frames:",tc.frame_number)
```

Output will be the same as before:

     Repr: <Timecode 01:00:00:00 @ 24 NDF>
     String: 01:00:00:00
     Frames: 86400

### Counting Modes

Counting modes are provided in the `modes` submodule.  `NonDropFrame` and `DropFrame` are provided, as well as a `TimecodeMode` abstract class which can be subclassed to create your own weird little counting modes.

Each counting mode defaults to an ideal frame rate if not specified.  `NonDropFrame` creats a `Timecode` object with `rate=24` by default.  `DropFrame` creates a `Timecode` object with `rate=30` by default.  Of course, specifying a `Timecode` with `rate=` will force that frame rate.

```python
from timecode import Timecode, modes
tc = Timecode(86400, mode=modes.DropFrame())
print("Repr:",repr(tc))
print("String:",tc)
print("Frames:",tc.frame_number)
```

Output:

     Repr: <Timecode 00;48;02;28 @ 30 DF>
     String: 00;48;02;28
     Frames: 86400
     
## TimecodeRange

A `TimecodeRange` object defines a continuous range of frames.  Creating a `TimecodeRange` object involves specifying two of `start`, `duration`, and `end`.

```python
from timecode import Timecode, TimecodeRange

tc_start    = Timecode("01:00:00:00")
tc_duration = Timecode("01:00")

tc_range = TimecodeRange(start=tc_start, duration=tc_duration)

print("Repr:",repr(tc_range))
print("Len:",len(tc_range))
print("Start:",tc_range.start)
print("End:",tc_range.end)

print("Loop:")
for tc in tc_range:
     print(tc)
```

Outputs:

     Repr: <TimecodeRange 01:00:00:00 - 01:00:01:00 (1:00) @ 24 NDF>
     Len: 24
     Start: 01:00:00:00
     End: 01:00:01:00
     Loop:
     01:00:00:00
     01:00:00:01
     01:00:00:02
     01:00:00:03
     01:00:00:04
     01:00:00:05
     01:00:00:06
     01:00:00:07
     01:00:00:08
     01:00:00:09
     01:00:00:10
     01:00:00:11
     01:00:00:12
     01:00:00:13
     01:00:00:14
     01:00:00:15
     01:00:00:16
     01:00:00:17
     01:00:00:18
     01:00:00:19
     01:00:00:20
     01:00:00:21
     01:00:00:22
     01:00:00:23
