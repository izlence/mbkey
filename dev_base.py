from enum import Enum

class mbdev_base():

    class mbKEY(Enum):
        IGNORE = 0
        UNSET = 0
        MENU = 208
        UP_DBL = 171
        UP_LONG = 216
        DOWN_DBL = 173
        DOWN_LONG = 176
        BASE_TEST = 111

        def get_mbKEY(pkey=0):
            if pkey == 209: pkey = 208
            return mbdev_base.mbKEY(pkey)
        
        def get_key_number(pkey):
            if pkey == mbdev_base.mbKEY.MENU: return 100
            if pkey == mbdev_base.mbKEY.UP_DBL: return 3
            if pkey == mbdev_base.mbKEY.UP_LONG: return 2
            if pkey == mbdev_base.mbKEY.DOWN_LONG: return 1
            if pkey == mbdev_base.mbKEY.DOWN_DBL: return -1

        