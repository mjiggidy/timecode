from . import CountingMode

class NonDropFrame(CountingMode):
	"""Non-drop-frame timecode mode"""

	DEFAULT_RATE = 24
	SEPARATOR = ":"
	
	@classmethod
	def __str__(cls):
		return "NDF"