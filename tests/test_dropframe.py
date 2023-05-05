from timecode import Timecode, TimecodeRange
from timecode.modes import DropFrame

def debug_range(tc_range: TimecodeRange):
	tc_old = Timecode(0, mode=DropFrame())
	for tc_current in tc_range:
		
		if str(tc_current).split()[1] != str(tc_old).split()[1]:
			print(tc_old)
			print(tc_current)
			print("")

		elif tc_current.frames == 0 and tc_current.seconds == 0:
			print(tc_old, " -- Non-Drop Minute")
			print(tc_current, " -- Non-Drop Minute")
			print("")
		
		tc_old = tc_current
	
tc_start = Timecode(0, mode=DropFrame())
duration = Timecode(180000, mode=DropFrame())

tc_range = TimecodeRange(tc_start, duration=duration)

debug_range(tc_range)