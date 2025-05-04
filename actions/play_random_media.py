import argparse
import mbpy.mbtools


def play_random_media(pdir="/home/mb/link/seesil"):
	gurl = mbpy.mbtools.mbtools.get_random_path(pdir)
	print(gurl)
	mbpy.mbtools.mbtools.mpv_play(gurl, -1, -1, "--config=yes", "--load-scripts=yes", "--keep-open=always", "--force-window=yes", bg_process=True) #, "-no-video", "--fullscreen=yes")
	mbpy.mbtools.mbtools.touch_file(gurl)




if __name__ == '__main__':

	argprs = argparse.ArgumentParser()        
	argprs.add_argument('--path', default="/home/mb/link/seesil", required=False, type=str, help="dir")

	# args = argprs.parse_args() #don't allow undefined parameters
	args, _ = argprs.parse_known_args() #ignore unknown arguments.

	play_random_media(args.path)




