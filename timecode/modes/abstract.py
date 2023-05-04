import abc, typing

class CountingMode(abc.ABC):
	"""An abstract class to facilitate timecode frame counting modes"""

	SEPARATOR = ":"
	"""The character expected and used for separation of elements"""

	ALLOW_NEGATIVE_TIMECODE = True
	"""Allow negative timecodes with this mode"""

	DEFAULT_RATE = 24
	"""The default frame rate to use if not provided"""

	__slots__ = ()

	@classmethod
	def validate_rate(cls, rate:typing.Optional[int]=None) -> int:
		"""Validate and clean the user-provided rate"""
		
		if rate is None:
			return cls.DEFAULT_RATE
		
		elif isinstance(rate, int) and rate > 0:
			return int(rate)
		
		raise ValueError("Timecode rate must be a positive integer")

	@classmethod
	def _santize_string(cls, timecode:str) -> str:
		"""Remove any weirdness"""

		timecode = timecode.replace(cls.SEPARATOR, ":")
		timecode = timecode.lstrip("-+:")
		return timecode
	
	@classmethod
	def _frame_number_from_string(cls, timecode:str, rate:int) -> int:
		"""Validate and convert a timecode string to the NDF frame number it represents"""

		sign = -1 if timecode.startswith("-") else 1

		if not cls.ALLOW_NEGATIVE_TIMECODE and sign == -1:
			raise ValueError("Negative timecodes are not allowed by this frame counting mode")
		
		# Sanitize that string
		timecode = cls._santize_string(timecode)

		# Split into elements
		tc_elements = timecode.split(":")
		multipliers = [1, rate, rate*60, rate*60*60]
		
		if len(tc_elements) > len(multipliers):
			raise ValueError("Timecode is not in the expected format of hh:mm:ss:ff")
		
		frame_count = 0
		
		try:
			for idx, tc_element in enumerate(tc_elements[::-1]):
				frame_count += int(tc_element) * multipliers[idx]
		except Exception:
			raise ValueError("Timecode is not in the expected format of hh:mm:ss:ff")
		
		return frame_count * sign
	
	@classmethod
	def _string_from_frame_number(cls, framenumber:int, rate:int) -> str:
		"""Format the given frame number to as a timecode string"""

		sign = '-' if framenumber < 0 else ''
		frame_fill = len(str(rate))

		framenumber = abs(framenumber)
		
		tc_string = cls.SEPARATOR.join([
			str(cls.hours(framenumber, rate)).zfill(2),
			str(cls.minutes(framenumber, rate)).zfill(2),
			str(cls.seconds(framenumber, rate)).zfill(2),
			str(cls.frames(framenumber, rate)).zfill(frame_fill)
		])

		return sign + tc_string

	@classmethod
	def hours(cls, framenumber:int, rate:int) -> int:
		"""Hours element"""
		return framenumber // (rate * 60 * 60)
	
	@classmethod
	def minutes(cls, framenumber:int, rate:int) -> int:
		"""Minutes element"""
		return framenumber // (rate * 60) % 60
	
	@classmethod
	def seconds(cls, framenumber:int, rate: int) -> int:
		"""Seconds element"""
		return framenumber // rate % 60
	
	@classmethod
	def frames(cls, framenumber:int, rate:int) -> int:
		"""Frames element"""
		return framenumber % rate