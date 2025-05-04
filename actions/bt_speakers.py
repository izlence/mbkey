import argparse
import os
import mbpy.mbtools


MACS = [
	"D1:2B:AA:AB:77:48", #Heifer, X6, Kemik iletimli
	"78:15:2D:1C:C3:4F", #Anker Soundcore headphone
	"98:D3:31:05:DD:A8", #Philips headphone
	"9E:4D:DC:EC:2E:25", #K30 lenovo speaker
	"C9:BB:BF:16:34:5A", #K3 pro lenovo speaker
	"41:42:F9:80:F5:00", #prozone speaker
	"AA:9E:A6:D5:A4:7C", #bluetooth speaker
	"11:22:33:43:C8:79", #bt remote control
]

def connect():
	mbpy.mbtools.mbwin.speak(f"connecting bt", False)
	for mac in MACS:
		cmd = f"bluetoothctl connect {mac}"
		os.system(cmd)
		# mbpy.mbtools.mbwin.run_cmd(cmd)

def disconnect():
	mbpy.mbtools.mbwin.speak(f"disconnecting bt", False)
	for mac in MACS:
		cmd = f"bluetoothctl disconnect {mac}"
		os.system(cmd)


def toggle_bluetooth_audio_profile():
	cmd = "bash /home/mb/dev/script/bash/mb/tools/bt_change_profile.sh"
	mbpy.mbtools.mbwin.run_cmd(cmd)
	mbpy.mbtools.mbwin.speak(f"toggle bluetooth audio sink profile")



		# elif pkeyval == 11:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. Anker Soundcore headphone", False)
			# 	cmd = "bluetoothctl disconnect 78:15:2D:1C:C3:4F; sleep 60; bluetoothctl connect 78:15:2D:1C:C3:4F;" 
			# 	if execute: 
			# 		mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
			# 		os.system(cmd)
			# 		self.cur_key_val = 0
			# 	return

			# elif pkeyval == 12:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. Philips headphone", False)
			# 	cmd = "bluetoothctl disconnect 98:D3:31:05:DD:A8; sleep 60; bluetoothctl connect 98:D3:31:05:DD:A8;" 
			# 	if execute: 
			# 		mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
			# 		os.system(cmd)
			# 		self.cur_key_val = 0
			# 	return
			
			# elif pkeyval == 13:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. K30 lenovo speaker")
			# 	cmd = "bluetoothctl disconnect 9E:4D:DC:EC:2E:25; sleep 60; bluetoothctl connect 9E:4D:DC:EC:2E:25" 
			# 	if execute: 
			# 		mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
			# 		os.system(cmd)
			# 		self.cur_key_val = 0
			# 	return
			
			# elif pkeyval == 14:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. K3 pro lenovo speaker")
			# 	cmd = "bluetoothctl disconnect C9:BB:BF:16:34:5A; sleep 60; bluetoothctl connect C9:BB:BF:16:34:5A" 
			# 	if execute: 
			# 		mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
			# 		os.system(cmd)
			# 		self.cur_key_val = 0
			# 	return

			# elif pkeyval == 15:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. prozone speaker")
			# 	cmd = "bluetoothctl disconnect 41:42:F9:80:F5:00; sleep 60; bluetoothctl connect 41:42:F9:80:F5:00" 
			# 	if execute: 
			# 		mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
			# 		os.system(cmd)
			# 		self.cur_key_val = 0
			# 	return		

			# elif pkeyval == 16:
			# 	if speak: mbpy.mbtools.mbwin.speak(f"{pkeyval}. bluetoooth speaker")
			# 	cmd = "bluetoothctl disconnect AA:9E:A6:D5:A4:7C ; sleep 60; bluetoothctl connect AA:9E:A6:D5:A4:7C" 
			# 	if execute: 
			# 		mbpy.mbtools.mbwin.speak("re-connect will happen in 1 minute:", False)
			# 		os.system(cmd)
			# 		self.cur_key_val = 0
			# 	return



if __name__ == '__main__':
	argprs = argparse.ArgumentParser()
	
	argprs.add_argument('--connect', action='store_true', help="connect pre-defined and available bt speakers")
	argprs.add_argument('--disconnect', action='store_true', help="disconnect pre-defined and connected bt speakers")
	argprs.add_argument('--toggle_audio_profile', action='store_true', help="toggle bluetooth audio sink profile for the active speaker")

	# args = argprs.parse_args() #don't allow undefined parameters
	args, _ = argprs.parse_known_args() #ignore unknown arguments.


	if args.connect:
		connect()
	elif args.disconnect:
		disconnect()
	elif args.toggle_audio_profile:
		toggle_bluetooth_audio_profile()

