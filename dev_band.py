from enum import Enum


class mbdevice():

	#super().mbKEY.IGNORE

	class mbKEY(Enum):
		# super.__init__()
		IGNORE = 0
		PLAY = 101
		PAUSE = 102
		BACKWARD = 103
		FORWARD = 104
		VOL_DOWN = 105
		VOL_UP = 106
		MUSIC_OPEN = 121
		MUSIC_CLOSE = 122
		FIND_DEVICE_START = 123
		FIND_DEVICE_END = 124
		WATCHFACE_CHANGED = 125

		# BASE_TEST = 1111

		def get_mbKEY(pkey=0):
			if pkey == mbdevice.mbKEY.PAUSE.value:
				return mbdevice.mbKEY.PLAY
				# return mbdevice.mbKEY.IGNORE
			return mbdevice.mbKEY(pkey)
		
		
		def get_key_number(pkey):
			if pkey == mbdevice.mbKEY.PLAY: return 100
			if pkey == mbdevice.mbKEY.FORWARD: return 3
			if pkey == mbdevice.mbKEY.BACKWARD: return 2
			if pkey == mbdevice.mbKEY.VOL_UP: return 1
			if pkey == mbdevice.mbKEY.VOL_DOWN: return -1
			return 0