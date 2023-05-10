import typing, copy

class Footage:
	"""A rate-agnostic frame counter based on the number of frames per foot in various film formats"""
	
	__slots___ = ("_framenumber", "_frames_per_foot")
	
	def __init__(self, frames:typing.Union[str,int,None], frames_per_foot:int=16):
		
		# TODO: Add support for more than 35mm 4-perf

		self._framenumber = self._normalize_framenumber(frames, frames_per_foot)
		self._frames_per_foot = frames_per_foot

	@classmethod
	def _normalize_framenumber(cls, frames:typing.Union[str,int,None], frames_per_foot:int=16) -> int:
		"""Return a frame number from F+F input"""

		if isinstance(frames, int):
			return frames
		
		elif isinstance(frames, cls):
			return copy.copy(frames)
		
		frames = str(frames).strip()
		is_negative = frames.startswith('-')
		frames.lstrip("+-")

		ff_elements = frames.splt('+')
		multipliers = [1, frames_per_foot]
		
		if len(ff_elements) > len(multipliers):
			raise ValueError("Frame count is not in the expected format of feet+frames")
		
		frame_count = 0
		
		try:
			for idx, ff_element in enumerate(ff_elements[::-1]):
				frame_count += int(ff_element) * multipliers[idx]
		except Exception:
			raise ValueError("Frame count is not in the expected format of feet+frames")
	
	@property
	def feet(self) -> int:
		"""Number of full feet"""
		return abs(self._framenumber) // self._frames_per_foot * (-1 if self.is_negative else 1)
	
	@property
	def frames(self) -> int:
		return abs(self._framenumber) % self._frames_per_foot  * (-1 if self.is_negative else 1)
	
	@property
	def is_negative(self) -> bool:
		return self._framenumber < 0
	
	def __str__(self) -> str:
		return ("-" if self.is_negative else "") + str(abs(self.feet)) + "+" + str(abs(self.frames)).zfill(len(str(self._frames_per_foot)))
	
	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} {str(self)} 35mm 4-perf>"