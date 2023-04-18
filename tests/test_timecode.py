from timecode import Timecode, TimecodeRange, NonDropFrame, DropFrame

tc1 = Timecode("-01:00:00:00", rate=24)
tc2 = Timecode("-0:02:30:15", rate=30)

print("Timecode 1 is", repr(tc1))
print("Timecode 2 is", repr(tc2))

tc3 = tc1.convert(rate=24)
tc4 = tc2.convert(rate=24)

print("Timecode 1 resampled is", repr(tc3))
print("Timecode 2 resampled is", repr(tc4))

print("---")

tc3 = Timecode("01:00:00:00", mode=DropFrame())

print("Timecode 3 is", repr(tc3))
print("+1 is ", tc3+1)