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
    MPVCUTS = 7
    AI_CHAT = 8
    
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
		

	class ai_chat():
		# cmd = "xdotool search --class mpv click --window %@ 9;"
			# xdotool click --repeat 33 --delay 11000 1
		def replay():
			mbpy.mbtools.mbwin.run_cmd("xdotool key  alt+Left")
			# mbpy.mbtools.mbwin.run_cmd("xdotool click 6")

		def repost_latest():
			mbpy.mbtools.mbwin.run_cmd("xdotool key  alt+Right")
			# mbpy.mbtools.mbwin.run_cmd("xdotool click 7")

		def delete_latest():
			mbpy.mbtools.mbwin.run_cmd("xdotool click 2")

		def start_record():
			mbpy.mbtools.mbwin.run_cmd("xdotool click 9")

		def stop_record():
			mbpy.mbtools.mbwin.run_cmd("xdotool click 8")

		def go_next():
			mbpy.mbtools.mbwin.run_cmd("xdotool key  ctrl+Down")

		def go_prev():
			mbpy.mbtools.mbwin.run_cmd("xdotool key  ctrl+Up")

		def auto_suggest():
			mbpy.mbtools.mbwin.run_cmd("xdotool key  ctrl+a")


	def vol_up():
		cmd = "amixer -D pulse sset Master 7%+" 
		os.system(cmd)


	def vol_down():
		cmd = "amixer -D pulse sset Master 7%-" 
		os.system(cmd)


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

	

	def mpv_set_loob_a():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		# print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "A")
			# mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "k", "a")
			# time.sleep(0.2)
			# mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "k")

	def mpv_set_loob_b():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		# print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "B")
			# mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "k", "b")
			# time.sleep(0.5)
			# mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "k")

	def mpv_save_range_tsv():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+alt+e")
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+b") #jump to B position
			# time.sleep(0.2)
			# mbpy.mbtools.mbwin.run_cmd("xdotool click --repeat 2 3") #left button click 2 times. when mpv is not full screen the cursor may click another window



	def mpv_change_filter():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			# mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+v")
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+s")


	def mpv_play_next_item_in_playlist():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "Return") #next item 


	def play_next_mpv():
		# mbpy.mbtools.mbwin.run_cmd("xdotool search --class mpv key --window %@  ctrl+q")

		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 22)
		print(wins)
		for w in wins:
			mbpy.mbtools.mbwin.send_key_to_win(w, "ctrl+q")

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[0]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[0], "space", "f")


	def mpv_toggle_play():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "space", "f")
			

	def mpv_change_speed():
		cmd = "xdotool search --class mpv click --window %@ 9;"
		os.system(cmd)


	def mpv_jump(pback=True):
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			gkey = "Up"
			if pback: gkey = "Down"
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], gkey)
				
	def mpv_jump_small(pback=True):
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)
		print(wins)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			gkey = "Right"
			if pback: gkey = "Left"
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], gkey)


	def mpv_jump_abloop_a():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+a") #jump to A position

	def mpv_jump_abloop_b():
		wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".* - mpv", 11)

		if len(wins)>0: 
			mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[-1]))
			mbpy.mbtools.mbwin.send_key_to_win(wins[-1], "ctrl+b") #jump to B position



	
	def next_mode(self) -> mbMODE:
		members = list(mbMODE)
		idx = members.index(self.mode) + 1
		if idx >= len(members): idx = 0
		new_mode = members[idx]

		if new_mode.value < 0: #modes not available for manual selections
			idx = 0
			new_mode = members[idx]

		print("Mode: ", new_mode.name, new_mode.value, idx)
		mbpy.mbtools.mbwin.speak("Mode: " + new_mode.name, False)
		self.mode = new_mode
		return new_mode
	

	def switch_mode(self, pmode:mbMODE, pspeak=True) -> mbMODE:
		if pmode == self.mode: return self.mode

		self.mode_pre = self.mode
		self.mode = pmode

		print("Switch mode to: ", self.mode.name, self.mode.value)
		if pspeak: mbpy.mbtools.mbwin.speak("Mode: " + self.mode.name, False)

		return self.mode


	def set_repeat_action(self, pmode:mbMODE, pkeyval=0):
		self.repeat_mode = pmode
		self.repeat_keyval = pkeyval
		self.dt_last_execute = time.time()


	def menu_options(self, pkeyval=0, pmode=mbMODE.NORMAL, speak=True, execute=False):

		wintitle = mbpy.mbtools.mbwin.get_active_win_title() 
		print(pkeyval, "title: ", wintitle)
		#winclass=$(xprop -id $hwnd WM_CLASS);

		if pkeyval == -4: #change mode
			if speak: mbpy.mbtools.mbwin.speak(f"change mode: {pkeyval}", False)
			if execute:
				self.next_mode()
				# if (self.last_mode_change < time.time() - 2):
				# 	self.last_mode_change = time.time()
			return

		elif pkeyval == -2:
			if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. vol up", False)
			if execute: mb_actions.vol_up()
			return

		elif pkeyval == -3:
			if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. vol down", False)
			if execute: mb_actions.vol_down()
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
				cmd = "mb.yt.cli  --back_burner 3600 &"
				if execute: 
					os.system(cmd)
					self.cur_key_val = 0
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play saved range", False)
				cmd = "mb.yt.cli  --play_marked_range --next_range 300 &"
				if execute: 
					os.system(cmd)
					self.cur_key_val = 0
				return
			
			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play latest", False)
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					cmd = "mb.yt.cli --play_latest --audio_only &"
					os.system(cmd)
					self.cur_key_val = 0
					# self.set_repeat_action(pmode, pkeyval)
					# self.repeat_keyval = 0
				return
		
			elif pkeyval == 7:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. mark mpv pos", False)
				if execute: mb_actions.mark_media_position()
				return
			
			elif pkeyval == 8:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next item in mpv playlist", False)
				if execute:
					mb_actions.mpv_play_next_item_in_playlist()
				return
			
			elif pkeyval == 9:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. charge warning in 90 min", False)
				cmd = "sleep 5500 && zenity --info --title 'charger' --text 'charge warning' &" 
				if execute: os.system(cmd)
				return
			
			elif pkeyval == 10:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. increse monitor brightness", False)
				cmd = "xdotool key XF86MonBrightnessUp" 
				if execute: os.system(cmd)
				return

			elif pkeyval == 11:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. reconnect bluetooth speakers", False)
				cmd = "mb.ops --op bt_disconnect_speakers ; sleep 60; mb.ops --op bt_connect_speakers ;" 
				if execute: 
					mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
					os.system(cmd)
					self.cur_key_val = 0
				return

			elif pkeyval == 12:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle bluetooth audio sink profile")
				if execute: 
					cmd = "bash /home/mb/dev/script/bash/mb/tools/bt_change_profile.sh"
					mbpy.mbtools.mbwin.run_cmd(cmd)
				return

			elif pkeyval == 13:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play random seesil media")
				if execute: 
					from actions import play_random_media				
					play_random_media.play_random_media("/home/mb/link/seesil")
					self.cur_key_val = 0
				return
					
		elif pmode == mbMODE.AUDACIOUS:
			if pkeyval == 0:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle play", False)
				cmd = "audtool playback-playpause" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPlay")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next", False)
				cmd = "audtool playlist-advance" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioNext")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. previous", False)
				cmd = "audtool playlist-reverse" 
				if execute: 
					mbpy.mbtools.mbwin.send_key("XF86AudioPrev")
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. flag current", False)
				if execute: 
					cmd = "mb.player.cli -audacious -flag -1 &" 
					self.set_repeat_action(pmode, pkeyval)
					os.system(cmd)
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. remove current song from playlist", False)
				if execute: 
					cmd = "pos=$(audtool playlist-position); audtool playlist-delete $pos; audtool playlist-jump $pos;" 
					mbpy.mbtools.mbwin.run_bash_cmd(cmd)
					self.cur_key_val = 0
				return
			
		elif pmode == mbMODE.RANDOM_RANGE:
			if pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. range play rate 4", False)
				cmd = "mb.player.random_range --audio_only --play --rate 4 &"
				if execute: os.system(cmd)
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next range", False)
				cmd = "mb.player.random_range --next 1 --rate -1" # &" #play next range from the last file
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next non-rated range", False)
				# cmd = "mb.player.random_range --next 1 --rate 0" # &" #play next rate=0 range from the last file
				cmd = "mb.player.random_range --next 1 --rate 0 &" #2025-03
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					# if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
					if ret == 0: #2025-03
						self.switch_mode(mbMODE.RATING, pspeak=False)
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next range from previous", False)
				cmd = "mb.player.random_range --next 2 &" #play next range from 2 before files
				if execute: 
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play range non-rated", False)
				cmd = "mb.player.random_range --audio_only --play --rate 0" # &" #play next range from 2 before files
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
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
				return
			elif pkeyval == 7:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next with voice changer", False)
				cmd = "mb.player.random_range --next --voice_changer &" #play next range with voice changer
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
				return

			elif pkeyval == 8:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. random bunch", False)
				cmd = "mb.player.random_range --audio_only --random_bunch 9 &" 
				if execute: os.system(cmd)
				return
			
			elif pkeyval == 9:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. play marked range", False)
				cmd = "mb.yt.cli  --db 2 --play_marked_range --next_range 120 &"
				if execute: os.system(cmd)
				return
			
			elif pkeyval == 10:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. flag last played file", False)
				cmd = "mb.player.random_range --toggle_file_flag 4" #TEMP_MARK = 4
				if execute: os.system(cmd)
				return
			elif pkeyval == 11:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next non-rated range from flagged", False)
				cmd = "mb.player.random_range --audio_only --next 1 --choose_flagged 4 --rate 0" # &" #play next range from the last file
				if execute:
					self.set_repeat_action(pmode, pkeyval)
					ret = os.system(cmd)
					if ret == 0 and (time.time() - self.dt_last_execute) > 33: #if not eof
						self.switch_mode(mbMODE.RATING)
				return
			
		elif pmode == mbMODE.RATING:
			if pkeyval > 0 and pkeyval <= 5:
				if speak: mbpy.mbtools.mbwin.speak(f"Rate: {pkeyval}", False)
				if execute: 
					cmd = f"mb.player.random_range --set_rate {pkeyval}"
					os.system(cmd)
			else:
				mbpy.mbtools.mbwin.speak(f"{pkeyval}. Rate should be less than 5.", False)

			if execute: self.switch_mode(self.mode_pre)
			return
		
		elif pmode == mbMODE.MPVCUTS:
			if pkeyval == -1:
				if speak: mb_actions.mpv_set_loob_a()
				# if execute: os.system(cmd)
				self.cur_key_val = 0
				return
			elif pkeyval == 1:
				if speak: mb_actions.mpv_set_loob_b()
				# if execute:
				# 	self.set_repeat_action(pmode, pkeyval)
					# ret = os.system(cmd)
				self.cur_key_val = 0
				return
			elif pkeyval == 0:
				mb_actions.mpv_jump_small(pback=True)
				# if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. jump back", False)
				# if execute: 
				# 	self.cur_key_val = 0
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. -4. change mode", False)
				if execute:
					self.cur_key_val = -4
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. save range", False)
				if execute:
					mb_actions.mpv_save_range_tsv()
					self.cur_key_val = 0
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next player", False)
				if execute: mb_actions.play_next_mpv()
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. toggle play", False)
				if execute: mb_actions.mpv_toggle_play()
				return

			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. pick for cutlist", False)
				if execute: 
					cmd = "mb.player.random_range --pick_for_cutlist &" #start a media not marked for cutlist
					os.system(cmd)
				return
			
			elif pkeyval == 7:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next item in mpv playlist", False)
				if execute:
					mb_actions.mpv_play_next_item_in_playlist()
				return
			
		elif pmode == mbMODE.AI_CHAT:
			if pkeyval == 0:
				pass
			elif pkeyval == 1:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. replay", False)
				if execute: 
					mb_actions.ai_chat.replay()
				return
			elif pkeyval == 2:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. auto suggest", False)
				if execute: 
					self.set_repeat_action(pmode, pkeyval)
					mb_actions.ai_chat.auto_suggest()
				return
			elif pkeyval == 3:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. repost latest", False)
				if execute: 
					mb_actions.ai_chat.repost_latest()
				return
			elif pkeyval == 4:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. delete latest", False)
				if execute: 
					mb_actions.ai_chat.delete_latest()
				return
			elif pkeyval == 5:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. start record", False)
				if execute: 
					mb_actions.ai_chat.start_record()
				return
			elif pkeyval == 6:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. stop record", False)
				if execute: 
					mb_actions.ai_chat.stop_record()
				return
			elif pkeyval == 7:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. previous", False)
				if execute: 
					mb_actions.ai_chat.go_prev()
				return
			elif pkeyval == 8:
				if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. next", False)
				if execute: 
					mb_actions.ai_chat.go_next()
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


