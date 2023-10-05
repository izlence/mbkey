from enum import Enum
import sys
import time
import os
import subprocess
import re
import mbpy.mbtools

from action import mb_actions, mbMODE, mbTASK

from dev_band import mbdevice
mbKEY = mbdevice



class mb_xinput_process():

        
    #devid=$(xinput list | grep -ioP "touchpad.*id=\K\d+");
    #devid=$(xinput list | grep -ioP "Mouse.*id=\K\d+");
    # devid=$(xinput list | grep -m 3 -ioP "Philips TAH4205.*id=\K\d+" | tail -n 1);

    def __init__(self) -> None:
        global mbKEY
        self.actions = mb_actions()
        # self.mode = mbMODE.NORMAL
        # self.mode_quick = mbMODE.NORMAL
        # self.last_mode_change = 0
        self.dtlastkey = int(time.time()) - 55
        self.keys_value = 0
        self.KEY_GROUP_DURATION = 11 #seconds after the last key to reset the keys value

        # self.mb_input = mb_input_value(mbTASK.UNSET, is_input_active=False)

        self.keys = []
        # self.keys = [mbKEY.MENU, mbKEY.MENU, mbKEY.MENU, mbKEY.MENU]
        # self.keys[0] = mbKEY.MENU
        # self.keys[1] = mbKEY.MENU
        # self.keys[2] = mbKEY.MENU

        # devname = "Philips TAH4205"
        # devname = "VSON#WP9622"

        # cmd = f'''xinput list | grep -m 3 -ioP "{devname}.*id=\K\d+" | tail -n 1'''
        # # cmd = '''xinput list | grep -m 3 -ioP "Philips TAH4205.*id=\K\d+" | tail -n 1'''
        # self.devid = mbpy.mbtools.mbwin.run_bash_cmd(cmd)
        # print("device id:", self.devid)
        # if self.devid == None or self.devid == '':
        #     exit()

        mbKEY = mbdevice.mbKEY
        
        while True:
            self.main_loop()
            time.sleep(11)



    def process_key(self, pkey):
        # if gkey == 209: gkey = 208
        # gkey = mbKEY(gkey)
        # gkey = mbdevice.get_mbKEY(pkey)
        gkey = mbKEY.get_mbKEY(pkey)
        if gkey == mbKEY.IGNORE: return
        
        # if self.mb_input.is_input_active:
        #     self.mb_input.process_input(pkey=gkey)
        #     return
        
        if int(time.time()) - self.dtlastkey > self.KEY_GROUP_DURATION:
            self.keys.clear()
            self.keys_value = 0
        self.dtlastkey = int(time.time())

        self.keys.insert(0, gkey)
        # print(self.keys)
        
        # if len(self.keys) > 1 and self.keys[1] == mbKEY.PLAY and self.keys[0] == mbKEY.PLAY: #M3-vol up long : change mode
        if self.keys[0] == mbKEY.WATCHFACE_CHANGED:
            mb_actions.mark_media_position()
            # mb_actions.mpv_toggle_play()
            # mbpy.mbtools.mbwin.send_key("XF86AudioPlay")
            # if (self.last_mode_change < time.time() - 3):
            #     self.last_mode_change = time.time()
            #     self.actions.mode = self.actions.next_mode(self.actions.mode)
            return
        
        elif len(self.keys) > 2 and self.keys[2] == mbKEY.MUSIC_CLOSE and self.keys[1] == mbKEY.MUSIC_OPEN and self.keys[0] == mbKEY.MUSIC_CLOSE:
            if (self.actions.dt_last_execute > time.time() - 600):
                self.actions.menu_options(101, mbMODE.DYNAMIC, speak=False, execute=True)
            
            return

        keynum = mbKEY.get_key_number(gkey)
        if keynum == 0: return

        if gkey != mbKEY.PLAY: #confirm...
            self.keys_value += keynum
            self.actions.menu_options(self.keys_value, self.actions.mode, speak=True, execute=False)
            
        else: 
            self.actions.menu_options(self.keys_value, self.actions.mode, speak=False, execute=True)





    def main_loop(self):
        # subprocess.call(["mpv", gurl]) #waits for the app to end
            #(output, err) = p.communicate()
            #exit_code = p.wait()        
        # cmd = ["xinput", "test", self.devid]
        cmd = ["python3.10", "/home/mb/dev/python/mblib/individual/amazfitband5/mb_band_cli.py"]
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=False)

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
