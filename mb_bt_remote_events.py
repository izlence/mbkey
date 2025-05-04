import os
import subprocess
import re
from datetime import datetime
from xml.etree.ElementInclude import include

from mbpy import mbtools

import action



class events_remote():

	def __init__(self):
		self.ts_last_action = 0
		self.is_center_down = False
		self.is_extra_down = False
	

	def center_button_down(self):
		self.is_center_down = True
		self.ts_center_down = datetime.now().timestamp()
		print("Center button down")
		# mbtools.mbwin.send_key("XF86AudioPlay")
		# mbtools.mbwin.send_key("XF86AudioPause")
		# mbtools.mbwin.send_key("XF86AudioNext")
		# mbtools.mbwin.send_key("XF86AudioPrev")
		# mbtools.mbwin.send_key("XF86AudioStop")
		# mbtools.mbwin.send_key("XF86AudioMute")
		# mbtools.mbwin.send_key("XF86AudioMicMute")
		# mbtools.mbwin.send_key("XF86AudioRaiseVolume")
		# mbtools.mbwin.send_key("XF86AudioLowerVolume")
		
		

	def center_button_up(self):
		self.is_center_down = False
		ts_diff = datetime.now().timestamp() - self.ts_center_down
		print("Center button press duration: ", ts_diff)

		if ts_diff > 4:
			self.center_button_preesed_too_long()
			return
		elif ts_diff >= 1:
			self.center_button_preesed_long()
			return
		else: #short press
			self.center_button_preesed()

		print("Center button up")

	def center_button_preesed(self):
		self.ts_last_action = datetime.now().timestamp()
		action.mb_actions.mpv_toggle_play()

	def center_button_preesed_long(self):
		self.ts_last_action = datetime.now().timestamp()
		action.mb_actions.mpv_save_range_tsv()
		print("Center button long pressed")


	def center_button_preesed_too_long(self):
		self.ts_last_action = datetime.now().timestamp()
		print("Center button too long pressed")


	def extra_button_down(self):
		self.is_extra_down = True
		self.ts_extra_down = datetime.now().timestamp()
		print("Extra button down")


	def extra_button_up(self):
		self.is_extra_down = False
		ts_diff = datetime.now().timestamp() - self.ts_extra_down
		print("Extra button press duration: ", ts_diff)

		if ts_diff > 4:
			self.extra_button_too_long()
			return

		elif ts_diff >= 1:
			self.extra_button_long()
			return

		else: #short press
			self.extra_button_preesed()
		
		#print("Extra button up")


	def extra_button_preesed(self):
		self.ts_last_action = datetime.now().timestamp()
		action.mb_actions.mpv_jump(True)
		print("Extra button pressed")


	def extra_button_long(self):
		self.ts_last_action = datetime.now().timestamp()
		action.mb_actions.mpv_change_filter()
		print("Extra button long pressed")


	def extra_button_too_long(self):
		self.ts_last_action = datetime.now().timestamp()
		cmd = "mb.yt.cli --play_latest --audio_only &"
		os.system(cmd)
		print("Extra button too long pressed")


	def left_button_pressed(self):
		self.ts_last_action = datetime.now().timestamp()

		if self.is_center_down:
			action.mb_actions.mpv_jump_abloop_a()
			# print("ab-a")

		else:
			action.mb_actions.mpv_set_loob_a()

		# print("Left button pressed")
	
	
	def right_button_pressed(self):
		self.ts_last_action = datetime.now().timestamp()

		if self.is_center_down:
			action.mb_actions.mpv_jump_abloop_b()

		else:
			action.mb_actions.mpv_set_loob_b()

		print("Right button pressed")


	def up_button_pressed(self):
		self.ts_last_action = datetime.now().timestamp()
		if self.is_center_down:
			action.mb_actions.vol_up()

		elif self.is_extra_down:
			print("Next mpv")
			action.mb_actions.play_next_mpv()
			mbtools.mbwin.speak("Next mpv", pwait=False)

		else:
			action.mb_actions.mpv_change_speed()
		print("Up button pressed")


	def down_button_pressed(self):
		self.ts_last_action = datetime.now().timestamp()
		if self.is_center_down:
			action.mb_actions.vol_down()
			

		else:
			action.mb_actions.mpv_jump_small(True)

		# print("Down button pressed")	
		# mbtools.mbwin.send_key("XF86AudioMute")




	



myevents = events_remote()

def monitor_ble_buttons():
	print("Starting BLE monitoring... Press buttons on your device")
	print("Press Ctrl+C to stop\n")
	
	try:
		# Start hcidump process
		process = subprocess.Popen(
			['sudo', 'hcidump', '--raw', '-i', 'hci0'],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			universal_newlines=True
		)
		
		while True:
			line = process.stdout.readline()
			if not line:
				continue
			
			# Print raw line for debugging
			# print(line.strip())
			# > 02 00 22 0E 00 0A 00 42 00 A1 02 00 04 16 0D 70 04 00 00 
			# > 02 00 21 0E 00 0A 00 41 00 A1 02 00 05 BC 02 70 04 00 00

			# Check if line contains your device's MAC (reversed byte order)
			# if '> 79 C8 43 33 22 11' in line or '< 79 C8 43 33 22 11' in line:
			# if '> 02 00 21 0E 00 0A' in line or '< 02 00 21 0E 00 0A' in line:
			# if '0E 00 0A 00 42 00 A1' in line or '< 02 00 22 0E 00 0A' in line:
			if  '> 02 00 21 0E 00 0A 00 41 00 A1' in line or '> 02 00 21 0E 00 0A 00 42 00 A1' in line or '> 02 00 22 0E 00 0A 00 42 00 A1' in line or '> 02 00 22 0E 00 0A 00 41 00 A1' in line: # or '< 02 00 21 0E 00 0A' in line:
				timestamp = datetime.now().strftime("%H:%M:%S.%f")
				# print(f"[{timestamp}] ", line.strip())

				data = line.strip().replace('>', '').replace('<', '') #.replace(' ', '')

				
				if data.endswith('A1 02 07 07 70 07 70 07 01 00'):
					myevents.center_button_down()
				elif data.endswith('A1 02 00 07 70 07 70 07 00 00'):
					myevents.center_button_up()
				elif data.endswith('A1 02 07 04 00 02 70 04 01 00'):
					myevents.left_button_pressed()
					#press finished: A1 02 00 04 16 0D 70 04 00 00
				elif data.endswith('A1 02 07 05 00 0D 70 04 01 00'):
					myevents.right_button_pressed()
					#right button released: A1 02 00 05 BC 02 70 04 00 00
				elif data.endswith('A1 02 07 06 70 07 F4 03 01 00'):
					myevents.up_button_pressed()
					#up button released: 1 02 00 06 70 07 AC 0D 00 00
				elif data.endswith('A1 02 00 06 70 07 C8 00 00 00'):
					myevents.down_button_pressed()
					#down button down: ('A1 02 07 06 70 07 80 0C 01 00'):
					#down button released: A1 02 00 06 70 07 C8 00 00 00

				elif data.find("A1 02 07 08") >= 0: # data.endswith('A1 02 07 08 00 08 60 0D 01 00') or data.endswith('A1 02 07 08 00 08 E0 04 01 00') or data.endswith('A1 02 07 08 00 08 60 02 01 00'):
					print("Extra button down")
					myevents.extra_button_down()
				elif data.find("A1 02 00 08") >= 0: # data.endswith('A1 02 00 08 00 08 60 0D 00 00') or data.endswith('A1 02 00 08 00 08 E0 04 00 00') or data.endswith('A1 02 07 08 00 08 60 02 00 00'):
					print("Extra button up")
					myevents.extra_button_up()
				else:
					# print(f"Unknown data pattern: [{timestamp}] :: {line}")
					pass


				
				# Extract hex data
				hex_data = re.findall(r'([0-9A-F]{2}\s?){4,}', line)
				if hex_data:
					# print(f"[{timestamp}] Packet: {hex_data[0].strip()}")
					
					# Special handling for a1 02 pattern (from your btmon output)
					if 'a1 02' in hex_data[0]:
						data_bytes = bytes.fromhex(hex_data[0].replace(' ', ''))
						if len(data_bytes) > 2:
							print(f"Possible button data: {data_bytes[2:].hex()}")


							
	except KeyboardInterrupt:
		print("\nStopping monitoring...")
		process.terminate()
	except Exception as e:
		print(f"Error: {e}")
		if 'process' in locals():
			process.terminate()



if __name__ == "__main__":
	monitor_ble_buttons()