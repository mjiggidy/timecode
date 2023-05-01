"""Contains the `TimecodeRange` class, which represents a continuous range of frames"""

import typing
from . import Timecode, Modes

class TimecodeRange:
	"""A timecode range"""
	
	def __init__(self, start:typing.Union[Timecode,str,int], duration:typing.Union[Timecode,int,None]=None, end=typing.Union[Timecode,int,None]):
		
		self._start_tc = start if isinstance(start, Timecode) else Timecode(start)
		
		# TODO: Fancier handling of different timecode modes/rates
		# TODO: Deal with start > end and zero-duration ranges
		if duration is not None:
			self._duration = int(duration)
		elif end is not None:
			self._duration = int(end if isinstance(end, Timecode) else Timecode(end) - self._start_tc)
		else:
			raise ValueError(f"One of `duration` or `end` must be provided")

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
		return self.start.__class__(int(self._duration), mode=self.start.mode, rate=self.start.rate)
	
	@property
	def rate(self) -> int:
		return self.start.rate
	
	@property
	def mode(self) -> Modes.TimecodeMode:
		return self.start.mode
	
	def __len__(self) -> int:
		return abs(int(self.duration))
	
	def __iter__(self) -> typing.Iterator["Timecode"]:
		return (self.start.__class__(x, mode=self.mode, rate=self.rate) for x in range(self.start.frame_number, self.end.frame_number))
	
	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} {self.start} - {self.end} ({str(self.duration).lstrip('00:')}) @ {self.rate} {self.mode}>"