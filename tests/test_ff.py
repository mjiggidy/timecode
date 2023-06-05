from timecode import Footage, Timecode

for frames in range(-3200,3200):
	footage = Footage(frames)
	timecode = Timecode(frames)
	as_int = int(frames)
	print(f"{frames=}\t{as_int=}\t{footage=}\t{timecode=}")