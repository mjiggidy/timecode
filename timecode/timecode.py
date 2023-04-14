import typing, abc, copy

class TimecodeMode(abc.ABC):
	"""An abstract class to facilitate timecode counting modes"""

	@abc.abstractclassmethod
	def _frame_number_from_string(cls, timecode:str, rate:int) -> int:
		"""Validate and convert a timecode string to the frame number it represents"""

	@abc.abstractclassmethod
	def _string_from_frame_number(cls, framenumber:int, rate:int) -> str:
		"""Format a timecode string from a given frme number"""

	@abc.abstractclassmethod
	def hours(cls, framenumber:int, rate:int) -> int:
		"""Hours element"""

	@abc.abstractclassmethod
	def minutes(cls, framenumber:int, rate:int) -> int:
		"""Minutes element"""

	@abc.abstractclassmethod
	def seconds(cls, framenumber:int, rate:int) -> int:
		"""Seconds element"""

	@abc.abstractclassmethod
	def frames(cls, framenumber:int, rate:int) -> int:
		"""Frames element"""

class NonDropFrame(TimecodeMode):
	"""Non-drop-frame timecode mode"""

	SEPARATOR = ":"
	"""The character expected and used for separation of elements"""
	
	@classmethod
	def _frame_number_from_string(cls, timecode:str, rate:int) -> int:
		"""Validate and convert a timecode string to the NDF frame number it represents"""

		sign = -1 if timecode.startswith("-") else 1
		
		# Sanitize that string
		timecode = cls._santize_string(timecode)

		# Split into elements
		tc_elements = timecode.split(cls.SEPARATOR)
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
			str(framenumber % rate).zfill(frame_fill)
		])

		return sign + tc_string
	
	@classmethod
	def _santize_string(cls, timecode:str) -> str:
		"""Remove any weirdness"""
		timecode = timecode.replace(";", cls.SEPARATOR)
		timecode = timecode.lstrip("-+:")
		return timecode
	
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
	
	@classmethod
	def __str__(cls):
		return "NDF"

class Timecode:
	"""Timecode representing a given frame number and rate"""

	def __init__(self, timecode:typing.Union[str,int,"Timecode"], mode:typing.Optional[TimecodeMode]=None, rate:typing.Optional[int]=None):


		if isinstance(timecode, self.__class__):
			if mode is not None and timecode.mode != mode:
				raise ValueError("The input timecode's mode does not match the requested mode")
			elif rate is not None and timecode.rate != rate:
				raise ValueError("The input timecode's framerate does not match the requested rate")
			
			return copy.copy(timecode)

		mode = mode or NonDropFrame()
		
		if rate is not None:
			if not isinstance(rate, int) or not rate > 0:
				raise ValueError(f"Invalid timecode rate: Must be a positive integer")
		else:
			rate = 24

		self._mode = mode or NonDropFrame()
		self._rate = rate
		self._frame_number = self._parse_frame_number(timecode)
	
	@property
	def frame_number(self) -> int:
		"""The timecode as a frame number"""
		return self._frame_number
	
	@property
	def rate(self) -> int:
		"""The rate (per second) of this timecode"""
		return self._rate
	
	@property
	def mode(self) -> TimecodeMode:
		"""The counting mode used with this timecode"""
		return self._mode
	
	@property
	def hours(self) -> int:
		"""The hours elapsed"""
		return self.mode.hours(self.frame_number, self.rate)
	
	@property
	def minutes(self) -> int:
		"""The minutes per hour elapsed"""
		return self.mode.minutes(self.frame_number, self.rate)
	
	@property
	def seconds(self) -> int:
		"""The seconds per minute elapsed"""
		return self.mode.seconds(self.frame_number, self.rate)
	
	@property
	def frames(self) -> int:
		"""The frames per second elapsed"""
		return self.mode.frames(self.frame_number, self.rate)
	
	@property
	def is_negative(self) -> bool:
		"""Is the timecode negative"""
		return self._frame_number < 0
	
	@property
	def is_positive(self) -> bool:
		"""Is the timecode positive"""
		return not self.is_negative
	
	def _parse_frame_number(self, timecode:typing.Union[str,int]) -> int:
		"""Call the frame number parser"""
		return self._mode._frame_number_from_string(str(timecode), self._rate)
	
	def __str__(self) -> str:
		return self._mode._string_from_frame_number(self._frame_number, self._rate)
	
	def __int__(self) -> int:
		return self.frame_number
	
	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} {str(self)} @ {self.rate} {self.mode}>"
	
	def __hash__(self) -> int:
		"""Create a unique hash for this timecode"""
		return hash(
			(self.frame_number, self.rate, self.mode)
		)
	
	# Comparisons
	# TODO: Only comparing like types for now

	def _is_compatible(self, other:typing.Any) -> bool:
		"""Determine if an object can be compared properly to Timecode"""
		# TODO: Only comparing like types for now
		if isinstance(other, self.__class__):
			return self.mode == other.mode and self.rate == other.rate
		elif isinstance(other, int):
			return True
		else:
			raise TypeError(f"Cannot compare {self.__class__.__name__} to {other.__class__.__name__}")
	
	def __eq__(self, other) -> bool:
		return self._is_compatible(other) and int(self) == int(other)
	
	def __ne__(self, other) -> bool:
		return not self == other
	
	def __lt__(self, other) -> bool:
		return self._is_compatible(other) and int(self) < int(other)
	
	def __le__(self, other) -> bool:
		return self < other or self == other
	
	def __gt__(self, other) -> bool:
		return self._is_compatible(other) and int(self) > int(other)
	
	def __ge__(self, other) -> bool:
		return self > other or self == other
	
	# Math operations
	
	def __add__(self, other) -> "Timecode":
		if not self._is_compatible(other):
			raise TypeError(f"Cannot compare {self.__class__.__name__} to {other.__class__.__name__}")
		return self.__class__(int(self) + int(other), mode=self.mode, rate=self.rate)
	
	def __sub__(self, other) -> "Timecode":
		if not self._is_compatible(other):
			raise TypeError(f"Cannot compare {self.__class__.__name__} to {other.__class__.__name__}")
		return self.__class__(int(self) - int(other), mode=self.mode, rate=self.rate)
	
	# TODO: More?