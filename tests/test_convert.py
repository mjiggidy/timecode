from timecode import Timecode, modes

#tc_orig = Timecode("01:00:00:23")
#tc_new = tc_orig.convert(rate=30)

tc_orig = Timecode("00:00:59:30", rate=30)
tc_new = tc_orig.convert(mode=modes.DropFrame())

print(repr(tc_orig))
print(repr(tc_new))