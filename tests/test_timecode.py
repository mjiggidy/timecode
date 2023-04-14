from timecode import Timecode, TimecodeRange


tc1 = Timecode("01:00:00:00", rate=24)
tc2 = Timecode("0:02:30:00", rate=24)

range = TimecodeRange(start=tc1, duration=tc2)
print(range.duration, range.end)
print(range)
print(Timecode("01:02:00:00") in range)

for f in range:
    print(f)