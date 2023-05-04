from timecode import Timecode, TimecodeRange, Modes

tc1 = Timecode("-01:00:00:00", rate=24)
tc2 = Timecode("-0:02:30:15", rate=30)

print("Timecode 1 is", repr(tc1))
print("Timecode 2 is", repr(tc2))

tc3 = tc1.convert(rate=24)
tc4 = tc2.convert(rate=24)

print("Timecode 1 resampled is", repr(tc3))
print("Timecode 2 resampled is", repr(tc4))

print("---")

#print(Timecode(30*60, rate=30))
#exit()

print("30 DF range:")
prev_tc:Timecode = None
for tc in TimecodeRange(start=Timecode(0, mode=Modes.DropFrame()), duration=Timecode(5000000, mode=Modes.DropFrame())):
	if prev_tc is not None and prev_tc.frames != (tc.frames-1)%tc.rate:
		print(prev_tc, f"({prev_tc.frame_number})")
		print(tc, f"({tc.frame_number})")
		print("\n")
	prev_tc = tc