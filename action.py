from enum import Enum
import time
import os
import mbpy.mbtools

# from dev_base import mbdev_base
# mbKEY = mbdev_base.mbKEY


class mbMODE(Enum):
    NORMAL = 1
    RANDOM_RANGE = 2
    # MPV = 3
    AUDACIOUS = 4
    RATING = 5
    CUSTOM = 6
    
    # < 0: modes not available for manual selections
    DYNAMIC = -11


class mbTASK(Enum):
    UNSET = 0
    RATE_LAST_RANGE = 1
    

class mb_actions():

	def __init__(self) -> None:
		# dt_last_mode_change = 0
		self.dt_last_execute = 0
		self.mode_pre = mbMODE.NORMAL
		self.mode = mbMODE.NORMAL

		self.repeat_mode = mbMODE.NORMAL
		self.repeat_keyval = 0


	def play_next_mpv():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".*mpv", 11)
		print(wins)
		for w in wins:
			mbpy.mbtools.mbwin.send_key_to_win(w, "ctrl+q")

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[0]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[0], "k", "f")


	def mpv_toggle_play():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".*mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "k", "f")
			

	def mpv_change_speed():
		cmd = "xdotool search --class mpv click --window %@ 9;"
		os.system(cmd)


	def mpv_jump(pback=True):
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".*mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			if pback:
				mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "Down")
			else:
				mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "Up")
				

	
	def next_mode(self, pmode_cur:mbMODE) -> mbMODE:
		members = list(mbMODE)
		idx = members.index(pmode_cur) + 1
		if idx >= len(members): idx = 0
		new_mode = members[idx]

		if new_mode.value < 0: #modes not available for manual selections
			idx = 0
			new_mode = members[idx]

		print("Mode: ", new_mode.name, new_mode.value, idx)
		mbpy.mbtools.mbwin.speak("Mode: " + new_mode.name, False)
		return new_mode
	

	def switch_mode(self, pmode:mbMODE) -> mbMODE:
		if pmode == self.mode: return self.mode

		self.mode_pre = self.mode
		self.mode = pmode

		print("Switch mode to: ", self.mode.name, self.mode.value)
		mbpy.mbtools.mbwin.speak("Mode: " + self.mode.name, False)
		return self.mode


	def set_repeat_action(self, pmode:mbMODE, pkeyval=0):
		self.repeat_mode = pmode
		self.repeat_keyval = pkeyval
		self.dt_last_execute = time.time()


	def menu_options(self, pkeyval=0, pmode=mbMODE.NORMAL, speak=True, execute=False):

		wintitle = mbpy.mbtools.mbwin.get_active_win_title() 
		print(pkeyval, "title: ", wintitle)
		#winclass=$(xprop -id $hwnd WM_CLASS);


		if pkeyval == -1: #change mode
			if speak: mbpy.mbtools.mbwin.speak(f"change mode: {pkeyval}")
			if execute:
				self.mode = self.next_mode(self.mode)
				# if (self.last_mode_change < time.time() - 2):
				# 	self.last_mode_change = time.time()
			return


		if pmode == mbMODE.NORMAL:
			if pkeyval == 0:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle play")
				if execute: mb_actions.mpv_toggle_play()
			
			elif pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play next")
				if execute: mb_actions.play_next_mpv()
			
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. jump back")
				if execute: mb_actions.mpv_jump(pback=True)
			
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. change mpv speed")
				if execute: mb_actions.mpv_change_speed()

			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play back burner")
				cmd = "mb.yt.cli  --back_burner 411 &"
				if execute: os.system(cmd)
				# mbpy.mbtools.mbwin.run_bash_cmd(cmd)
			
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. mark mpv pos")
				cmd = "mb.xdgopen mbpy:mpv_mark_pos &" 
				if execute: os.system(cmd)
			
			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. disconnect Philips headphone")
				cmd = "bluetoothctl disconnect 98:D3:31:05:DD:A8" 
				if execute: os.system(cmd)
			
			# elif pkeyval == 6:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. re-connect Piranha speaker")
			# 	cmd = "bluetoothctl disconnect 84:91:BB:A2:C4:FF ; sleep 1; bluetoothctl connect 84:91:BB:A2:C4:FF" 
			# 	if execute: os.system(cmd)
			
			return
			
		elif pmode == mbMODE.AUDACIOUS:

			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play next")
				cmd = "audtool playlist-advance" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioNext")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play previous")
				cmd = "audtool playlist-reverse" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPrev")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. audacious flag current media in mbplayer")
				cmd = "mb.player.cli -audacious -flag -1 &" 
				if execute: os.system(cmd)
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. remove current song from audacious playlist")
				cmd = "pos=$(audtool playlist-position); audtool playlist-delete $pos; audtool playlist-jump $pos;" 
				if execute: mbpy.mbtools.mbwin.run_bash_cmd(cmd)
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle play")
				cmd = "audtool playback-playpause" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPlay")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
			
			return
		elif pmode == mbMODE.RANDOM_RANGE:
			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. range play rate 4")
				cmd = "mb.player.random_range --audio_only --play --rate 4 &"
				if execute: os.system(cmd)
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next with voice changer")
				cmd = "mb.player.random_range --next --voice_changer &" #play next range with voice changer
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next range")
				cmd = "mb.player.random_range --next 1" # &" #play next range from the last file
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next range from previous")
				cmd = "mb.player.random_range --next 2 &" #play next range from 2 before files
				if execute: os.system(cmd)
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play range non-rated")
				cmd = "mb.player.random_range --audio_only --play -rate 0" # &" #play next range from 2 before files
				if execute: 
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
						# mbpy.mbtools.mbwin.speak("menu key to rate")
			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. random latest")
				cmd = "mb.player.random_range --random_latest" # &" 
				if execute: os.system(cmd)
			
			return
		elif pmode == mbMODE.RATING:
			if pkeyval > 0 and pkeyval < 5:
				if speak: mbpy.mbtools.mbwin.speak(f"Rate: {pkeyval}" )
				if execute: 
					cmd = f"mb.player.random_range --set_rate {pkeyval}"
					os.system(cmd)
			else:
				mbpy.mbtools.mbwin.speak(f"{pkeyval}. Rate should be less than 5.")

			if execute: self.switch_mode(self.mode_pre)
			return
			
		elif pmode == mbMODE.DYNAMIC:
			if pkeyval == 101:  #repeat last action
				# if speak: 
				mbpy.mbtools.mbwin.speak(f"Repeat last action" )
				if execute: 
					self.menu_options(self.repeat_keyval, self.repeat_mode, speak=False, execute=True)
			return
		
		elif pmode == mbMODE.CUSTOM:
			if pkeyval >= 0 and pkeyval <= 9:
				if speak:
					cmd = f"mb.cli --speak --action {pkeyval}"
					os.system(cmd)
				if execute: 
					cmd = f"mb.cli --execute --action {pkeyval}"
					os.system(cmd)
			return
		
		print(f"not set: {pmode} :: {pkeyval}")
		mbpy.mbtools.mbwin.speak(f"not set: {pkeyval}")


