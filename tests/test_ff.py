from timecode import Footage, Timecode

for frames in range(-3200,3200):
	footage = Footage(frames)
	timecode = Timecode(frames)
	print(f"{frames=}\t{footage=}\t{timecode=}")