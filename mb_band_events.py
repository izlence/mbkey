from enum import Enum
import time
import os
import subprocess
import re
import mbpy.mbtools

from dev_base import mbdev_base
from action import mb_actions, mbMODE, mbTASK, mb_input_value

mbKEY = mbdev_base.mbKEY





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

        # devname = "Philips TAH4205"
        # devname = "VSON#WP9622"

        # cmd = f'''xinput list | grep -m 3 -ioP "{devname}.*id=\K\d+" | tail -n 1'''
        # # cmd = '''xinput list | grep -m 3 -ioP "Philips TAH4205.*id=\K\d+" | tail -n 1'''
        # self.devid = mbpy.mbtools.mbwin.run_bash_cmd(cmd)
        # print("device id:", self.devid)
        # if self.devid == None or self.devid == '':
        #     exit()

        # # self.mbKEY = mbKEY
        # # self.mbKEY = mbdevice.mbKEY
        # if devname.find("Philips")>-1:
        #     from dev_headphone import mbdevice
        #     mbKEY = mbdevice.mbKEY
        # else:
        from dev_tablet import mbdevice
        mbKEY = mbdevice.mbKEY
        

        self.main_loop()



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
            self.mode = mb_actions.change_mode(self.mode)
            return
        
        if gkey != mbKEY.MENU: #confirm...
            self.keys_value += mbKEY.get_key_number(gkey)
            mb_actions.menu_options(self.keys_value, self.mode, speak=True, execute=False)
            
        else: 
            mb_actions.menu_options(self.keys_value, self.mode, speak=False, execute=True)





    def main_loop(self):
        # subprocess.call(["mpv", gurl]) #waits for the app to end
            #(output, err) = p.communicate()
            #exit_code = p.wait()        
        # cmd = ["xinput", "test", self.devid]
        cmd = ["python3.10", "/media/m1/data/KURULUM/phone/smart-band_test/smart-band/git/miband4/mb_band_cli.py"]
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
