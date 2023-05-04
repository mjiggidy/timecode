from timecode import Timecode, TimecodeRange, Modes

print("NonDrop Frame")
tc_start = Timecode("01:00:00:00")
tc_end   = Timecode("01:02:03:00")
tc_range = TimecodeRange(start=tc_start, end=tc_end)
print(f"{tc_start=}\n{tc_end=}\n{tc_range=}")

print("---")

tc_start = Timecode("01:00:00:00")
tc_duration   = Timecode("2:03:00")
tc_range = TimecodeRange(start=tc_start, duration=tc_duration)
print(f"{tc_start=}\n{tc_duration=}\n{tc_range=}")

print("---")

frame_start = 86400
frame_duration = 2400
tc_range = TimecodeRange(start=frame_start, duration=frame_duration)
print(f"{frame_start=}\n{frame_duration=}\n{tc_range=}")