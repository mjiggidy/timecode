"""Contains the `TimecodeRange` class, which represents a continuous range of frames"""

import typing
from . import Timecode
from .modes import CountingMode

class TimecodeRange:
	"""An unbroken sequence of timecodes between a specified range"""

	ALLOW_NEGATIVE_RANGES = False
	"""Allow a start timecode which is later than the end timecode"""

	__slots__ = ("_start_tc", "_duration")
	
	def __init__(self, *, start:typing.Union[Timecode,str,int,None]=None, duration:typing.Union[Timecode,str,int,None]=None, end:typing.Union[Timecode,str,int,None]=None):

		rate, mode = self._get_common_mode(start, duration, end)

		self._start_tc = Timecode(start, rate=rate, mode=mode()) if start is not None else None
		self._duration = Timecode(duration, rate=rate, mode=mode()) if duration is not None else None
		end = Timecode(end, rate=rate, mode=mode()) if end is not None else None

		
		if end:
			if duration and not start:
				self._start_tc = end - self.duration	
			elif start and not duration:
				self._duration = end - self.start
			elif start and duration:
				# Just do a sanity check
				if self.start + self.duration != end:
					raise ValueError("`end` does not match `start` + `duration`")
		
		if not self._start_tc and self._duration:
			raise ValueError(f"Two of `start`,`duration`, and `end` are required")
	
	@classmethod
	def _get_common_mode(cls, *args:typing.Iterable[typing.Union[Timecode,str,int,None]]) -> typing.Tuple[int, CountingMode]:
		"""Returns the common counting mode and rate from the provided arguments"""
		
		known_mode = None
		known_rate = None
		
		for tc in (t for t in args if isinstance(t, Timecode)):

			if known_mode is not None and type(tc.mode) is not known_mode:
				print("For",tc,":", type(tc.mode), known_mode)
				raise ValueError(f"All given Timecode objects must have matching counting modes (found: {known_mode.__name__} vs {type(tc.mode).__name__})")
			elif known_rate is not None and known_rate != tc.rate:
				raise ValueError(f"All given Timecode ojbects must have matching rates (found: {known_rate} vs {tc.rate})")
		
			known_mode = type(tc.mode)
			known_rate = tc.rate
		
		# Set defaults if none were given
		# NOTE: If one is None, the other should be too.  I don't know what to do with this information but it seems like I should mention it or something.
		known_mode = known_mode or Timecode.DEFAULT_MODE
		known_rate = known_rate or known_mode.DEFAULT_RATE

		return (known_rate, known_mode)

	@property
	def start(self) -> Timecode:
		"""The start timecode in this range"""
		return self._start_tc
	
	@property
	def end(self) -> Timecode:
		"""The end timecode in this range (exclusive)"""
		return self._start_tc + self._duration
	
	@property
	def duration(self) -> Timecode:
		"""The duration of this timecode range"""
		return self._duration
	
	@property
	def rate(self) -> int:
		return self.start.rate
	
	@property
	def mode(self) -> CountingMode:
		return self.start.mode
	
	def __len__(self) -> int:
		return abs(int(self.duration))
	
	def __iter__(self) -> typing.Iterator["Timecode"]:
		return (self.start.__class__(x, mode=self.mode, rate=self.rate) for x in range(self.start.frame_number, self.end.frame_number))
	
	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} {self.start} - {self.end} ({str(self.duration.frame_number).lstrip('00:')}) @ {self.rate} {self.mode}>"