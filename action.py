from enum import Enum
import time
import os
import subprocess
import re
import mbpy.mbtools

from dev_base import mbdev_base

mbKEY = mbdev_base.mbKEY


class mbMODE(Enum):
    NORMAL = 1
    RANDOM_RANGE = 2
    MPV = 4
    AUDACIOUS = 8
    # INPUT = 16


class mbTASK(Enum):
    UNSET = 0
    RATE_LAST_RANGE = 1
    

class mb_actions():

	dt_last_mode_change = 0

	def play_next_mpv():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".*mpv", 11)
		print(wins)
		for w in wins:
			mbpy.mbtools.mbwin.send_key_to_win(w, "ctrl+q")

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[0]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[0], "k", "f")


            
	def change_mode(pmode:mbMODE) -> mbMODE:
		if (mb_actions.dt_last_mode_change > time.time() - 5): return
		mb_actions.dt_last_mode_change = time.time()
		#self.mode = self.mode.next_item
		# for enm in mbMODE:
		#     if enm.value == self.mode.value:

		members = list(mbMODE)
		idx = members.index(pmode) + 1
		if idx >= len(members): idx = 0
		new_mode = members[idx]

		print("Mode: ", new_mode.name, new_mode.value, idx)
		mbpy.mbtools.mbwin.speak("Mode: " + new_mode.name, False)
		return new_mode



	def menu_options(pkeyval=0, pmode=mbMODE.NORMAL, speak=True, execute=False):

		wintitle = mbpy.mbtools.mbwin.get_active_win_title() 
		print(pkeyval, "title: ", wintitle)
		#winclass=$(xprop -id $hwnd WM_CLASS);


		if self.mode == mbMODE.RANDOM_RANGE:
			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak("1. range play rate 4")
				cmd = "mb.player.random_range --audio_only --play --rate 4 &"
				if execute: os.system(cmd)
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak("2. next with voice changer")
				cmd = "mb.player.random_range --next --voice_changer &" #play next range with voice changer
				if execute: os.system(cmd)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak("3. next range")
				cmd = "mb.player.random_range --next 1" # &" #play next range from the last file
				if execute: 
					ret = os.system(cmd)
					if ret == 0:
						mb_input = mb_input_value(mbTASK.RATE_LAST_RANGE, is_input_active = True)
						mbpy.mbtools.mbwin.speak("menu key to rate")
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak("4. next range from previous")
				cmd = "mb.player.random_range --next 2 &" #play next range from 2 before files
				if execute: os.system(cmd)
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak("5. play range non-rated")
				cmd = "mb.player.random_range --audio_only --play -rate 0" # &" #play next range from 2 before files
				if execute: 
					ret = os.system(cmd)
					if ret == 0:
						mb_input = mb_input_value(mbTASK.RATE_LAST_RANGE, is_input_active = True)
						mbpy.mbtools.mbwin.speak("menu key to rate")
				return
		elif self.mode == mbMODE.NORMAL:
			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak("1. play back burner")
				cmd = "mb.yt.cli  --back_burner 411 &"
				if execute: os.system(cmd)
				# mbpy.mbtools.mbwin.run_bash_cmd(cmd)
			# elif self.key_2 == mbKEY.MENU and self.key_1 == mbKEY.MENU and self.key_0 == mbKEY.UP_DBL: #M-M- vol dbl up 
			#     pass
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak("2. play next")
				if execute: mb_actions.play_next_mpv()
				return

		elif self.mode == mbMODE.MPV:
			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak("1. play next")
				if execute: mb_actions.play_next_mpv()
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak("2. mark mpv pos")
				cmd = "mb.xdgopen mbpy:mpv_mark_pos &" 
				if execute: os.system(cmd)
				return

		elif self.mode == mbMODE.AUDACIOUS:

			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak("1. play next")
				cmd = "audtool playlist-advance" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioNext")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak("2. play previous")
				cmd = "audtool playlist-reverse" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPrev")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak("3. audacious flag current media in mbplayer")
				cmd = "mb.player.cli -audacious -flag -1 &" 
				if execute: os.system(cmd)
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak("4. current song has been removed from audacious playlist")
				cmd = "pos=$(audtool playlist-position); audtool playlist-delete $pos; audtool playlist-jump $pos;" 
				if execute: mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return                
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak("5. toggle play")
				cmd = "audtool playback-playpause" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPlay")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
		
		mbpy.mbtools.mbwin.speak(f"value not set: {pkeyval}")


	# if [[ $wintitle =~ " - CutList" ]]; then
	# 		wid=$(xdotool search --name " - CutList"); 
	# 		xdotool windowactivate --sync $wid key m; 
	# 		echo "CutList: add mark";
	# fi






class mb_input_value():

    def __init__(self, ptask:mbTASK, is_input_active = True) -> None:
        self.task = ptask
        # self.is_started = False
        # self.is_completed = False
        # self.is_value_used = False
        self.current_value = 3
        self.is_input_active = is_input_active
        self.is_waiting_start_key = True
        
    
    def add_value(self, pval:int):
        self.current_value += pval
        mbpy.mbtools.mbwin.speak(f"value: {self.current_value}")

    def complete_task (self):
        if self.task == mbTASK.RATE_LAST_RANGE:
            if self.current_value>=0 and self.current_value<=5:
                cmd = f"mb.player.random_range --set_rate {self.current_value}"
                os.system(cmd)
        
        self.is_input_active = False
        mbpy.mbtools.mbwin.speak(f"input completed: {self.current_value}")
        

    def process_input(self, pkey:mbKEY):
        if self.is_waiting_start_key == True:
            if pkey == mbKEY.MENU:
                self.is_waiting_start_key = False
                mbpy.mbtools.mbwin.speak(f"double up and down to change value.")
            else:
                self.is_input_active = False
                mbpy.mbtools.mbwin.speak(f"input interrupted. menu key was expected.")
            return
    

        if pkey == mbKEY.UP_DBL:
            self.add_value(1)
        elif pkey == mbKEY.DOWN_DBL:
            self.add_value(-1)
        elif pkey == mbKEY.MENU:
            self.complete_task()

