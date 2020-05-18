import pygame
from pygame.locals import*
import time
import os, re
import random
import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from music_data import*
from pydub.pydub import AudioSegment
from pydub.pydub.playback import play
from multiprocess import*
from copy import deepcopy

#color
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (127, 127, 127)

#create i2c object
i2c_bus = busio.I2C(SCL, SDA)
#create trellis
trellis = NeoTrellis(i2c_bus)
print("NeoTrellis created")

path = ""

COLORS = ["RED", "YELLOW", "GREEN", "CYAN", "BLUE", "PURPLE", "WHITE"]
COLOR_TUPLES = [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE]

buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
button_colors = [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF]
shuffled_colors = list(button_colors)
Shuffled = False

wavnames = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
shuffled_names = list(wavnames)  # Duplicate list, wavnames is our reference

record_data = []
period_data = []
period_start = 0
period_end = 0

audio_file = None

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

def play_file(audio_filename):
	pygame.mixer.music.load(path+audio_filename)
	pygame.mixer.music.play()

# this will be called when button events are received
def blink(event):
	global period_start, period_end
	# turn the LED on when a rising edge is detected
	if event.edge == NeoTrellis.EDGE_RISING:  # Trellis button pushed
		if shuffled_names[event.number] != "":
			play_file(shuffled_names[event.number])
			record_data.append(event.number)
			print(record_data)
			period_start = time.time()
	# turn the LED off when a rising edge is detected
	if event.edge == NeoTrellis.EDGE_FALLING:
		pygame.mixer.music.stop()
		period_end = time.time() - period_start
		period_data.append(period_end)
		print(period_data)
		
def run(instrument,melody):
	global path,wavnames,shuffled_names,buttons,button_colors,shuffled_colors,Shuffled,record_data,period_data,period_start,period_end
	path = "/home/pi/Final/"+instrument+"/"
	buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	button_colors = [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF]
	shuffled_colors = list(button_colors)
	Shuffled = False

	wavnames = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
	shuffled_names = list(wavnames)  # Duplicate list, wavnames is our reference
	wavefiles = [file for file in os.listdir(path) if (file.endswith(".ogg") and not file.startswith("._"))]

	if len(wavefiles) < 1:
		print("No wav files found in sounds directory")
	else:
		print("Audio files found: ", wavefiles)

	dir = "/home/pi/Final/"
	for f in os.listdir(dir):
		if re.search(".wav", f):
			os.remove(os.path.join(dir, f))
		if re.search(".mp3", f):
			os.remove(os.path.join(dir, f))

	shuffled = False

	for soundfile in wavefiles:
		print("Processing "+soundfile)
		pos = int(soundfile[0:2])
		if pos >= 0 and pos < 16:      # Valid filenames start with 00 to 15
			wavnames[pos] = soundfile  # Store soundfile in proper index
			shuffled_names[pos] = soundfile
			skip = soundfile[3:].find('-') + 3
			user_color = soundfile[3:skip].upper()  # Detect file color
			print("For file "+soundfile+", color is "+user_color+".")
			file_color = COLOR_TUPLES[COLORS.index(user_color)]
			button_colors[pos] = file_color
			shuffled_colors[pos] = file_color
		else:
			print("Filenames must start with a number from 00 to 15 - "+soundfile)

	for i in range(16):
		# activate rising edge events on all keys
		trellis.activate_key(i, NeoTrellis.EDGE_RISING)
		# activate falling edge events on all keys
		trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
		# set all keys to trigger the blinkblink callback
		trellis.callbacks[i] = blink

		# cycle the LEDs on startup
		trellis.pixels[i] = WHITE
		time.sleep(0.05)
 
	for i in range(16):
		trellis.pixels[i] = OFF
		time.sleep(0.05)

	# play begins
	for i in range(len(melody_lemon)):
		trellis.pixels[melody_lemon[i]] = COLOR_TUPLES[i%len(COLOR_TUPLES)]

		time_start = time.time()
		while (time.time() - time_start < 0.25*noteDurations_lemon[i]):
			# call the sync function call any triggered callbacks
			trellis.sync()

			# the trellis can only be read every 1 milliseconds or so
			time.sleep(0.001)
		
		trellis.pixels[melody_lemon[i]] = OFF


	wav_piano_list = ("piano/00-red-do.wav", "piano/01-purple-re.wav", "piano/02-blue-mi.wav", "piano/03-green-fa.wav", "piano/04-yellow-sol.wav", "piano/05-cyan-la.wav", "piano/06-white-si.wav", "piano/07-red-do.wav", "piano/08-red-re.wav", "piano/09-purple-mi.wav", "piano/10-blue-do.wav", "piano/11-green-re.wav", "piano/12-cyan-mi.wav", "piano/13-yellow-fa.wav", "piano/14-white-sol.wav", "piano/15-red-la.wav")
	wav_guitar_list = ("guitar/00-red-c3.wav", "guitar/01-purple-d3.wav", "guitar/02-blue-e3.wav", "guitar/03-green-f3.wav", "guitar/04-yellow-g3.wav", "guitar/05-cyan-a3.wav", "guitar/06-white-b3.wav", "guitar/07-red-c4.wav", "guitar/08-red-d4.wav", "guitar/09-purple-e4.wav", "guitar/10-blue-f4.wav", "guitar/11-green-g4.wav", "guitar/12-cyan-a4.wav", "guitar/13-yellow-b4.wav", "guitar/14-white-c5.wav","guitar/15-red-d5.wav")

	if(instrument=="piano"):
		temp_list = deepcopy(wav_piano_list)
	elif(instrument=="guitar"):
		temp_list = deepcopy(wav_guitar_list)

	output = AudioSegment.from_file(temp_list[record_data[0]], format="wav")
	first_output = period_data[0] * 1000
	slice_output = output[:first_output]
	record_data = record_data[1:]
	period_data = period_data[1:]

	for i in range(len(record_data)):
			song = AudioSegment.from_file(temp_list[record_data[i]], format="wav")
			first_seconds = period_data[i] * 1000
			slice_song = song[:first_seconds]
			slice_output = slice_output + slice_song
			slice_output.export("out.wav", format="wav")
			four_core = AudioSegment.from_file("out.wav", format="wav")

	count = four_core.duration_seconds
	print(count)
	count_four = count/4
	print(count_four)
	core0 = four_core[:count_four*1000]
	core1 = four_core[count_four*1000:count_four*2000]
	core2 = four_core[count_four*2000:count_four*3000]
	core3 = four_core[count_four*3000:]

	core0.export("out0.wav", format="wav")
	core1.export("out1.wav", format="wav")
	core2.export("out2.wav", format="wav")
	core3.export("out3.wav", format="wav")

	parallel_convertor()

	core0_read = AudioSegment.from_file("temp0.mp3", format="mp3")
	core1_read = AudioSegment.from_file("temp1.mp3", format="mp3")
	core2_read = AudioSegment.from_file("temp2.mp3", format="mp3")
	core3_read = AudioSegment.from_file("temp3.mp3", format="mp3")

	four_core_output = core0_read + core1_read + core2_read + core3_read
	four_core_output.export("output_four.mp3", format="mp3")
	
	while True:
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP):
				pos=pygame.mouse.get_pos()
				x,y=pos
				if y>200:
					if x>180 and x<220:
						return 1
					elif x>240:
						for i in range(16):
							trellis.pixels[i] = OFF
						return 0
