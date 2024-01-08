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
		self.cur_key_val = 0

		self.repeat_mode = mbMODE.NORMAL
		self.repeat_keyval = 0
		

	def mark_media_position():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".*mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+alt+b")

		else: #TODO: chrome f4t script..
			wins = mbpy.mbtools.mbwin.get_win_ids_by_name("Free4Talk - .*", 1)
			if len(wins)>0: 
				mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
				mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+alt+b")


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
			gkey = "Up"
			if pback: gkey = "Down"
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], gkey)
				

	
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
			if speak: mbpy.mbtools.mbwin.speak(f"change mode: {pkeyval}", False)
			if execute:
				self.mode = self.next_mode(self.mode)
				# if (self.last_mode_change < time.time() - 2):
				# 	self.last_mode_change = time.time()
			return
		elif pkeyval == -2:
			if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. vol up", False)
			cmd = "amixer -D pulse sset Master 5%+" 
			if execute: os.system(cmd)
			return
		elif pkeyval == -3:
			if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. vol down", False)
			cmd = "amixer -D pulse sset Master 5%-" 
			if execute: os.system(cmd)
			return


		if pmode == mbMODE.NORMAL:
			if pkeyval == 0:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle play", False)
				if execute: mb_actions.mpv_toggle_play()
				return
			elif pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play next", False)
				if execute: mb_actions.play_next_mpv()
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. jump back", False)
				if execute: mb_actions.mpv_jump(pback=True)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. change mpv speed", False)
				if execute: mb_actions.mpv_change_speed()
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play back burner", False)
				cmd = "mb.yt.cli  --back_burner 411 &"
				if execute: os.system(cmd)
				# mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. mark mpv pos", False)
				if execute: mb_actions.mark_media_position()
				return
			
			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play latest", False)
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					cmd = "mb.yt.cli --play_latest &"
					os.system(cmd)
					self.cur_key_val = 0
					# self.set_repeat_action(pmode, pkeyval)
					# self.repeat_keyval = 0
				return

			elif pkeyval == 7:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. disconnect Philips headphone", False)
				cmd = "bluetoothctl disconnect 98:D3:31:05:DD:A8" 
				if execute: os.system(cmd)
				return

			# elif pkeyval == 6:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. re-connect Piranha speaker")
			# 	cmd = "bluetoothctl disconnect 84:91:BB:A2:C4:FF ; sleep 1; bluetoothctl connect 84:91:BB:A2:C4:FF" 
			# 	if execute: os.system(cmd)
					
		elif pmode == mbMODE.AUDACIOUS:

			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play next", False)
				cmd = "audtool playlist-advance" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioNext")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play previous", False)
				cmd = "audtool playlist-reverse" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPrev")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. flag current", False)
				cmd = "mb.player.cli -audacious -flag -1 &" 
				if execute: 
					self.set_repeat_action(pmode, pkeyval)
					os.system(cmd)
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. remove current song from playlist", False)
				cmd = "pos=$(audtool playlist-position); audtool playlist-delete $pos; audtool playlist-jump $pos;" 
				if execute: mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle play", False)
				cmd = "audtool playback-playpause" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPlay")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			
		elif pmode == mbMODE.RANDOM_RANGE:
			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. range play rate 4", False)
				cmd = "mb.player.random_range --audio_only --play --rate 4 &"
				if execute: os.system(cmd)
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next with voice changer", False)
				cmd = "mb.player.random_range --next --voice_changer &" #play next range with voice changer
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next range", False)
				cmd = "mb.player.random_range --next 1" # &" #play next range from the last file
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next range from previous", False)
				cmd = "mb.player.random_range --next 2 &" #play next range from 2 before files
				if execute: os.system(cmd)
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play range non-rated", False)
				cmd = "mb.player.random_range --audio_only --play --rate -1" # &" #play next range from 2 before files
				if execute: 
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
						# mbpy.mbtools.mbwin.speak("menu key to rate")
				return
			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. random latest", False)
				cmd = "mb.player.random_range --audio_only --random_latest" # &" 
				if execute: os.system(cmd)
				return

			elif pkeyval == 7:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. random bunch", False)
				cmd = "mb.player.random_range --audio_only --random_bunch 15 &" 
				if execute: os.system(cmd)
				return
			
		elif pmode == mbMODE.RATING:
			if pkeyval > 0 and pkeyval < 5:
				if speak: mbpy.mbtools.mbwin.speak(f"Rate: {pkeyval}", False)
				if execute: 
					cmd = f"mb.player.random_range --set_rate {pkeyval}"
					os.system(cmd)
			else:
				mbpy.mbtools.mbwin.speak(f"{pkeyval}. Rate should be less than 5.", False)

			if execute: self.switch_mode(self.mode_pre)
			return
			
		elif pmode == mbMODE.DYNAMIC:
			if pkeyval == 101:  #repeat last action
				# if speak: 
				mbpy.mbtools.mbwin.speak(f"Repeat last action", False)
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
		mbpy.mbtools.mbwin.speak(f"{pkeyval}", False)


