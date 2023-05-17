from timecode import Timecode, TimecodeRange, modes

def test_creation():

	print("NonDrop Frame")

	print("Start and end TC")
	tc_start = Timecode("01:00:00:00")
	tc_end   = Timecode("01:02:03:00")
	tc_range = TimecodeRange(start=tc_start, end=tc_end)
	print(f"{tc_start=}\n{tc_end=}\n{tc_range=}")

	print("---")

	print("Start and duration TC")
	tc_start = Timecode("01:00:00:00")
	tc_duration   = Timecode("2:03:00")
	tc_range = TimecodeRange(start=tc_start, duration=tc_duration)
	print(f"{tc_start=}\n{tc_duration=}\n{tc_range=}")

	print("---")

	print("Start and duration frames")
	frame_start = 86400
	frame_duration = 2952
	tc_range = TimecodeRange(start=frame_start, duration=frame_duration)
	print(f"{frame_start=}\n{frame_duration=}\n{tc_range=}")

	print("---")

	print("Duration and end TC")
	tc_end = 5
	duration = Timecode("02:30:00", rate=30, mode=modes.DropFrame())
	tc_range = TimecodeRange(duration=duration, end=tc_end)
	print(f"{tc_end=}\n{duration=}\n{tc_range=}")

def test_contains():

	tc_range = TimecodeRange(
		start = Timecode("01:00:00:00"),
		end   = Timecode("01:30:00:00")
	)

	tc_test = "01:29:59:23"
	print(f"{tc_test} in {tc_range}?\t{tc_test in tc_range}")

	tc_sub = TimecodeRange(
		start = Timecode("01:00:00:00"),
		end   = Timecode("01:30:00:00")
	)

	print(f"{tc_sub} in {tc_range}?\t{tc_sub in tc_range}")

if __name__ == "__main__":

	test_contains()