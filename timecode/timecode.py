"""Contains the `Timecode` class, which represents a single frame in the context of a given frame rate"""

import typing
from .modes import CountingMode, NonDropFrame

class Timecode:
	"""Timecode representing a given frame number and rate"""

	DEFAULT_MODE = NonDropFrame
	"""The default frame counting mode class to use if not provided"""

	__slots__ = ("_mode", "_rate", "_frame_number")

	def __init__(self, timecode:typing.Union[str,int, "Timecode"], mode:typing.Optional[CountingMode]=None, rate:typing.Optional[int]=None):

		# If a timecode object is provided, make a copy of it
		if isinstance(timecode, self.__class__):
			if mode is not None and timecode.mode is type(mode):
				raise ValueError(f"The mode provided ({mode}) does not match the mode of the timecode object passed ({timecode.mode}).  Use Timecode.convert() to change the mode of an existing Timecode object.")
			elif rate is not None and timecode.rate != rate:
				raise ValueError(f"The rate provided ({rate}) does not match the rate of the timecode object passed ({timecode.rate}).  Use Timecode.convert() to change the rate of an existing Timecode object.")
			mode = timecode.mode
			rate = timecode.rate
			timecode = timecode.frame_number

		# Create a new timecode object from raw parameters
		self._mode = self._normalize_mode(mode)
		self._rate = self._mode.validate_rate(rate)
		self._frame_number = self._mode._frame_number_from_string(str(timecode), self._rate)
	
	@classmethod
	def _normalize_mode(cls, mode:CountingMode) -> CountingMode:
		"""Validate and clean the user-provided timecode mode"""

		if mode is None:
			return cls.DEFAULT_MODE()

		if isinstance(mode, CountingMode):
			return mode

		raise ValueError(f"Mode must be an instance of the `CountingMode` class")
	
	def convert(self, *, mode:typing.Optional[CountingMode]=None, rate:typing.Optional[int]=None):
		"""Create a new timecode object resampled to a new rate or frame counting mode"""

		# NOTE: These fellas'll be further validated in the constructor
		new_rate = rate or self.rate
		new_mode = mode or self.mode
		new_frame_number = round(self.frame_number * (new_rate/self.rate))

		return self.__class__(
			timecode = new_frame_number,
			mode = new_mode,
			rate = new_rate
		)

	@property
	def frame_number(self) -> int:
		"""The timecode as a frame number"""
		return self._frame_number
	
	@property
	def rate(self) -> int:
		"""The rate (per second) of this timecode"""
		return self._rate
	
	@property
	def mode(self) -> CountingMode:
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
			return self.mode.__class__ == other.mode.__class__ and self.rate == other.rate
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