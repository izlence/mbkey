from enum import Enum


class mbdevice():

	#super().mbKEY.IGNORE

	class mbKEY(Enum):
		# super.__init__()
		IGNORE = 0
		UNSET = 0
		MENU = 117
		UP_DBL = 112
		UP_LONG = 46
		DOWN_LONG = 33
		DOWN_DBL = 26

		# BASE_TEST = 1111

		def get_mbKEY(pkey=0):
			if pkey == 37:
				return mbdevice.mbKEY.IGNORE
			return mbdevice.mbKEY(pkey)
		
		
		def get_key_number(pkey):
			if pkey == mbdevice.mbKEY.MENU: return 100
			if pkey == mbdevice.mbKEY.UP_DBL: return 3
			if pkey == mbdevice.mbKEY.UP_LONG: return 2
			if pkey == mbdevice.mbKEY.DOWN_LONG: return 1
			if pkey == mbdevice.mbKEY.DOWN_DBL: return -1