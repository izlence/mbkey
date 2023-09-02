from enum import Enum

class mbdevice():

	class mbKEY(Enum):
		IGNORE = 0
		UNSET = 0
		MENU = 208
		UP_DBL = 171
		UP_LONG = 216
		DOWN_DBL = 173
		DOWN_LONG = 176
		TEST_HEADPHONE = 2222

		def get_mbKEY(pkey=0):
			if gkey == 209: gkey = 208
			return mbdevice.mbKEY(gkey)
		
		def get_key_number(pkey):
			if pkey == mbdevice.mbKEY.MENU: return 100
			if pkey == mbdevice.mbKEY.UP_DBL: return 3
			if pkey == mbdevice.mbKEY.UP_LONG: return 2
			if pkey == mbdevice.mbKEY.DOWN_LONG: return 1
			if pkey == mbdevice.mbKEY.DOWN_DBL: return -1