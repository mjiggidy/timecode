import typing, copy
from . import TimecodeMode, NonDropFrame

class Timecode:
	"""Timecode representing a given frame number and rate"""

	def __init__(self, timecode:typing.Union[str,int], mode:typing.Optional[TimecodeMode]=None, rate:typing.Optional[int]=None):

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