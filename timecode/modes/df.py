import typing
from . import CountingMode

class DropFrame(CountingMode):
	"""Drop-frame timecode mode"""

	"""
	In 30fps DF, two frames are dropped at the beginning of the minute,
	except for every ten minutes.
	
	Examples:  01:01:59;29 -> 01:02:00;02
	           01:18:59;29 -> 01:19:00;02
	           01:19:59;29 -> 01:20:00;00
	
	Multiples of 30 fps will drop a proportional amount.
	60 fps drops 4 frames, 120 drops 8 frames, etc.
	"""

	DEFAULT_RATE = 30
	"""DF timecodes are intended for multiples of 30"""

	SEPARATOR = ";"
	"""The character expected and used for separation of elements"""

	@classmethod
	def validate_rate(cls, rate:typing.Optional[int]=None) -> int:
		"""Validate and clean the user-provided rate"""
		
		# Do the usual checks
		rate = super().validate_rate(rate)

		if rate % 30:
			raise ValueError("Drop Frame mode requires the rate to be a multiple of 30.")
		
		return rate
	
	@classmethod
	def _frame_number_from_string(cls, timecode: str, rate: int) -> int:
		
		# First get the base frame number without drops
		frame_number = super()._frame_number_from_string(timecode, rate)

		# TODO: return
		return frame_number

	@classmethod
	def get_dropped_frames(cls, framenumber:int, rate:int) -> int:
		"""Calculate the number of frames to drop"""

		# NDF:
		# 00:00:59:23 = 1799
		# 00:01:00:00 = 1800

		# DF:
		# 00;00;59;23 = 1799
		# 00;01;00;02 = 1802 (1800 + 2)

		# For every full segment, add 9 * 2 * (rate/30)
		# For every start segment (rate*61), add 2
		# For every partial sgment, add 2
		
		multiplier = -1 if framenumber <  0 else 1
		framenumber_normalized = abs(framenumber)
		
		# Drop-frame adds two frames every minute, except every ten minutes
		# First: Let's get some things straight
		drop_offset = (2 * rate // 30)			# Frames to drop -- 2 per 30fps
		
		full_minute = rate * 60							# Length of a full non-drop minute (in frames) (60 seconds)
		drop_minute = full_minute - drop_offset			# Length of a drop-minute (in frames)
		drop_segment = full_minute + (drop_minute * 9)	# Length of a drop-segment (in frames) (One full minute + Nine drop minutes = 10 Minutes)
		
		# So how many full 10-minute drop-segments have elapsed
		drop_segments_elapsed = framenumber_normalized // drop_segment

		# And as for the remaining frames at the end...
		remaining_frames = framenumber_normalized % drop_segment
		remaining_drop_frames = max(remaining_frames - full_minute + 1, 0)	# I don't understand why +1 yet, but that was a problem for like three days. max() will be bad for negative values
		
		# Number of complete drop-minutes
		drop_minutes_elapsed = remaining_drop_frames // drop_minute

		# And then any other frames will need a 2-frame boost! Oooh!
		remainder = drop_offset if (remaining_drop_frames % drop_minute) else 0


		return ((drop_segments_elapsed * (9 * drop_offset)) + (drop_minutes_elapsed * drop_offset) + remainder) * multiplier

	@classmethod
	def hours(cls, framenumber:int, rate:int) -> int:
		"""Hours element"""
		dropped_frames = cls.get_dropped_frames(framenumber, rate)
		return super().hours(framenumber+dropped_frames, rate)
	
	@classmethod
	def minutes(cls, framenumber:int, rate:int) -> int:
		"""Minutes element"""
		dropped_frames = cls.get_dropped_frames(framenumber, rate)
		return super().minutes(framenumber+dropped_frames, rate)
	
	@classmethod
	def seconds(cls, framenumber:int, rate: int) -> int:
		"""Seconds element"""
		dropped_frames = cls.get_dropped_frames(framenumber, rate)
		return super().seconds(framenumber+dropped_frames, rate)
	
	@classmethod
	def frames(cls, framenumber:int, rate:int) -> int:
		"""Frames element"""
		dropped_frames = cls.get_dropped_frames(framenumber, rate)
		return super().frames(framenumber+dropped_frames, rate)
	
	@classmethod
	def _string_from_frame_number(cls, framenumber: int, rate: int) -> str:
		return super()._string_from_frame_number(framenumber, rate)  + f" ({cls.get_dropped_frames(framenumber, rate)})"

	@classmethod
	def __str__(cls):
		return "DF"