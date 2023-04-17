from timecode import Timecode, TimecodeRange


tc1 = Timecode("01:00:00:00", rate=24)
tc2 = Timecode("0:02:30:15", rate=30)

print("Timecode 1 is", repr(tc1))
print("Timecode 2 is", repr(tc2))

tc3 = tc1.convert(rate=1)
tc4 = tc2.convert(rate=1)

print("Timecode 1 resampled is", repr(tc3))
print("Timecode 2 resampled is", repr(tc4))