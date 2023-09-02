from enum import Enum
import time
import os
import subprocess
import re
import mbpy.mbtools

from dev_base import mbdev_base

mbKEY = mbdev_base.mbKEY


class mb_actions():

    def play_next_mpv():
        wins = mbpy.mbtools.mbwin.get_win_ids_by_name(".*mpv", 11)
        print(wins)
        for w in wins:
            mbpy.mbtools.mbwin.send_key_to_win(w, "ctrl+q")

        if len(wins)>0: 
            mbpy.mbtools.mbwin.run_cmd("xdotool windowraise " + str(wins[0]))
            mbpy.mbtools.mbwin.send_key_to_win(wins[0], "k", "f")


class mbMODE(Enum):
    NORMAL = 1
    RANDOM_RANGE = 2
    MPV = 4
    AUDACIOUS = 8
    # INPUT = 16

# class mbKEY(Enum):
#     UNSET = 0
#     MENU = 208
#     UP_DBL = 171
#     UP_LONG = 216
#     DOWN_DBL = 173
#     DOWN_LONG = 176

#     def get_mbKEY(pkey=0):
#         if gkey == 209: gkey = 208
#         return mbKEY(gkey)



class mbTASK(Enum):
    UNSET = 0
    RATE_LAST_RANGE = 1



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



class mb_xinput_process():

        
    #devid=$(xinput list | grep -ioP "touchpad.*id=\K\d+");
    #devid=$(xinput list | grep -ioP "Mouse.*id=\K\d+");
    # devid=$(xinput list | grep -m 3 -ioP "Philips TAH4205.*id=\K\d+" | tail -n 1);

    def __init__(self) -> None:
        global mbKEY
        self.mode = mbMODE.NORMAL
        # self.mode_quick = mbMODE.NORMAL
        self.last_mode_change = 0
        self.dtlastkey = int(time.time()) - 55
        self.keys_value = 0

        self.mb_input = mb_input_value(mbTASK.UNSET, is_input_active=False)

        self.keys = []
        # self.keys = [mbKEY.MENU, mbKEY.MENU, mbKEY.MENU, mbKEY.MENU]
        # self.keys[0] = mbKEY.MENU
        # self.keys[1] = mbKEY.MENU
        # self.keys[2] = mbKEY.MENU

        devname = "Philips TAH4205"
        devname = "VSON#WP9622"

        cmd = f'''xinput list | grep -m 3 -ioP "{devname}.*id=\K\d+" | tail -n 1'''
        # cmd = '''xinput list | grep -m 3 -ioP "Philips TAH4205.*id=\K\d+" | tail -n 1'''
        self.devid = mbpy.mbtools.mbwin.run_bash_cmd(cmd)
        print("device id:", self.devid)
        if self.devid == None or self.devid == '':
            exit()

        # self.mbKEY = mbKEY
        # self.mbKEY = mbdevice.mbKEY
        if devname.find("Philips")>-1:
            from dev_headphone import mbdevice
            mbKEY = mbdevice.mbKEY
        else:
            from dev_tablet import mbdevice
            mbKEY = mbdevice.mbKEY
            

        self.main_loop()

    def change_mode(self):

        if (self.last_mode_change > time.time() - 5): return
        self.last_mode_change = time.time()

        #self.mode = self.mode.next_item
        # for enm in mbMODE:
        #     if enm.value == self.mode.value:

        members = list(mbMODE)
        idx = members.index(self.mode) + 1
        if idx >= len(members): idx = 0
        self.mode = members[idx]

        print("Mode: ", self.mode.name, self.mode.value, idx)
        mbpy.mbtools.mbwin.speak("Mode: " + self.mode.name)


    def process_key(self, pkey):
        # if gkey == 209: gkey = 208
        # gkey = mbKEY(gkey)
        # gkey = mbdevice.get_mbKEY(pkey)
        gkey = mbKEY.get_mbKEY(pkey)
        if gkey == mbKEY.IGNORE: return
        
        if self.mb_input.is_input_active:
            self.mb_input.process_input(pkey=gkey)
            return
        
        if int(time.time()) - self.dtlastkey > 15:
            self.keys.clear()
            self.keys_value = 0
        self.dtlastkey = int(time.time())

        self.keys.insert(0, gkey)
        print(self.keys)
        
        if len(self.keys) > 1 and self.keys[1] == mbKEY.MENU and self.keys[0] == mbKEY.MENU: #M3-vol up long : change mode
            print("change mode")
            self.change_mode()
            return
        
        if gkey != mbKEY.MENU: #confirm...
            self.keys_value += mbKEY.get_key_number(gkey)
            self.menu_options(speak=True, execute=False)
            
        else: 
            self.menu_options(speak=False, execute=True)



    def menu_options(self, speak=True, execute=False):

        wintitle = mbpy.mbtools.mbwin.get_active_win_title() 
        print(self.keys_value, "title: ", wintitle)
        #winclass=$(xprop -id $hwnd WM_CLASS);


        if self.mode == mbMODE.RANDOM_RANGE:
            if self.keys_value == 1:
                if speak: mbpy.mbtools.mbwin.speak("1. range play rate 4")
                cmd = "mb.player.random_range --audio_only --play --rate 4 &"
                if execute: os.system(cmd)
                return
            elif self.keys_value == 2:
                if speak: mbpy.mbtools.mbwin.speak("2. next with voice changer")
                cmd = "mb.player.random_range --next --voice_changer &" #play next range with voice changer
                if execute: os.system(cmd)
                return
            elif self.keys_value == 3:
                if speak: mbpy.mbtools.mbwin.speak("3. next range")
                cmd = "mb.player.random_range --next 1" # &" #play next range from the last file
                if execute: 
                    ret = os.system(cmd)
                    if ret == 0:
                        self.mb_input = mb_input_value(mbTASK.RATE_LAST_RANGE, is_input_active = True)
                        mbpy.mbtools.mbwin.speak("menu key to rate")
                return
            elif self.keys_value == 4:
                if speak: mbpy.mbtools.mbwin.speak("4. next range from previous")
                cmd = "mb.player.random_range --next 2 &" #play next range from 2 before files
                if execute: os.system(cmd)
                return
            elif self.keys_value == 5:
                if speak: mbpy.mbtools.mbwin.speak("5. play range non-rated")
                cmd = "mb.player.random_range --audio_only --play -rate 0" # &" #play next range from 2 before files
                if execute: 
                    ret = os.system(cmd)
                    if ret == 0:
                        self.mb_input = mb_input_value(mbTASK.RATE_LAST_RANGE, is_input_active = True)
                        mbpy.mbtools.mbwin.speak("menu key to rate")
                return
        elif self.mode == mbMODE.NORMAL:
            if self.keys_value == 1:
                if speak: mbpy.mbtools.mbwin.speak("1. play back burner")
                cmd = "mb.yt.cli  --back_burner 411 &"
                if execute: os.system(cmd)
                # mbpy.mbtools.mbwin.run_bash_cmd(cmd)
            # elif self.key_2 == mbKEY.MENU and self.key_1 == mbKEY.MENU and self.key_0 == mbKEY.UP_DBL: #M-M- vol dbl up 
            #     pass
                return
            elif self.keys_value == 2:
                if speak: mbpy.mbtools.mbwin.speak("2. play next")
                if execute: mb_actions.play_next_mpv()
                return

        elif self.mode == mbMODE.MPV:
            if self.keys_value == 1:
                if speak: mbpy.mbtools.mbwin.speak("1. play next")
                if execute: mb_actions.play_next_mpv()
                return
            elif self.keys_value == 2:
                if speak: mbpy.mbtools.mbwin.speak("2. mark mpv pos")
                cmd = "mb.xdgopen mbpy:mpv_mark_pos &" 
                if execute: os.system(cmd)
                return

        elif self.mode == mbMODE.AUDACIOUS:

            if self.keys_value == 1:
                if speak: mbpy.mbtools.mbwin.speak("1. play next")
                cmd = "audtool playlist-advance" 
                if execute: 
                    mbpy.mbtools.mbwin.send_key("XF86AudioNext")
                    mbpy.mbtools.mbwin.run_bash_cmd(cmd)
                return
            elif self.keys_value == 2:
                if speak: mbpy.mbtools.mbwin.speak("2. play previous")
                cmd = "audtool playlist-reverse" 
                if execute: 
                    mbpy.mbtools.mbwin.send_key("XF86AudioPrev")
                    mbpy.mbtools.mbwin.run_bash_cmd(cmd)
                return
            elif self.keys_value == 3:
                if speak: mbpy.mbtools.mbwin.speak("3. audacious flag current media in mbplayer")
                cmd = "mb.player.cli -audacious -flag -1 &" 
                if execute: os.system(cmd)
                return
            elif self.keys_value == 4:
                if speak: mbpy.mbtools.mbwin.speak("4. current song has been removed from audacious playlist")
                cmd = "pos=$(audtool playlist-position); audtool playlist-delete $pos; audtool playlist-jump $pos;" 
                if execute: mbpy.mbtools.mbwin.run_bash_cmd(cmd)
                return                
            elif self.keys_value == 5:
                if speak: mbpy.mbtools.mbwin.speak("5. toggle play")
                cmd = "audtool playback-playpause" 
                if execute: 
                    mbpy.mbtools.mbwin.send_key("XF86AudioPlay")
                    mbpy.mbtools.mbwin.run_bash_cmd(cmd)
                return
        
        mbpy.mbtools.mbwin.speak(f"value not set: {self.keys_value}")


    # if [[ $wintitle =~ " - CutList" ]]; then
	# 		wid=$(xdotool search --name " - CutList"); 
	# 		xdotool windowactivate --sync $wid key m; 
	# 		echo "CutList: add mark";
	# fi





    def main_loop(self):
        # subprocess.call(["mpv", gurl]) #waits for the app to end
            #(output, err) = p.communicate()
            #exit_code = p.wait()        
        cmd = ["xinput", "test", self.devid]
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        while True:
            # time.sleep(.2)
            retcode = ps.poll()
            if retcode is not None: # Process finished.
                if retcode == 0: print(ps.stdout)
                else: print("""Error handling.""")
                break
        
            # No process is done, wait a bit and check again.
            line = ps.stdout.readline()
            if not line: break

            line=line.strip().decode('utf-8')
            print(line)

            
            p = ".*key press\s+(\d+)"
            match = re.search(p, line, re.RegexFlag.IGNORECASE)
            if match == None: continue
            gkey = match.group(1)
            gkey = int(gkey)
            
            self.process_key(gkey)




mb_xinput_process()
print("main loop ended")


# # devs = sh.xinput("list")
#     # print(devs)
# for line in sh.xinput("test", devid, _iter=True):
#     print(line)
#     line = str(line)

#     if line.find("key press") > -1:
#         key_2 = key_1
#         key_1 = key_0
        
#         p = ".*key press\s+(\d+)"
#         result = re.search(p, line, re.RegexFlag.IGNORECASE)
#         key_0 = result.group(1)
#         key_0 = int(key_0)

#         if key_0 == 209: key_0 = 208

#         wintitle = mbpy.mbtools.mbwin.get_active_win_title() 
#         #winclass=$(xprop -id $hwnd WM_CLASS);
#         print(key_0 , key_1 , key_2, "title: ", wintitle)

#     else:
#         continue


#     #M, vol up dbl: play next. next mpv window
#     if key_1 == mbKEY.MENU and key_0 == mbKEY.UP_DBL:
# 		#xdotool key XF86AudioNext; 
#         #audtool playlist-advance; 
#         mbpy.mbtools.mbwin.speak("play next")
#         mb_actions.play_next_mpv()

#     elif key_2 == mbKEY.MENU and key_1 == mbKEY.MENU and key_0 == mbKEY.DOWN_DBL: #M-M- vol dbl down
#         mbpy.mbtools.mbwin.speak("play back burner")
#         cmd = "mb.yt.cli  -back_burner"
#         mbpy.mbtools.mbwin.run_bash_cmd(cmd)