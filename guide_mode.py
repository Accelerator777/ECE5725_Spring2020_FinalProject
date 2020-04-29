import pygame
from pygame.locals import*
import time
import os
import random
import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis

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

NOTE_C5 = 0
NOTE_D5 = 1
NOTE_E5 = 2
NOTE_F5 = 3
NOTE_G5 = 4
NOTE_A5 = 5
NOTE_B5 = 6
NOTE_C6 = 7
NOTE_D6 = 8
NOTE_E6 = 9

melody_lemon = [NOTE_C6, NOTE_D6, NOTE_E6, NOTE_C6, NOTE_A5, NOTE_D6,
    NOTE_B5, NOTE_G5, NOTE_E5, NOTE_B5, NOTE_A5, NOTE_G5,
    NOTE_C5, NOTE_G5, NOTE_E5,

    NOTE_D5, NOTE_E5, NOTE_F5,
    NOTE_C6, NOTE_B5, NOTE_C6, NOTE_G5, NOTE_F5, NOTE_E5,
    NOTE_F5, NOTE_F5, NOTE_F5, NOTE_C6, NOTE_B5, NOTE_A5, NOTE_G5,

    NOTE_C6, NOTE_D6, NOTE_E6, NOTE_C6, NOTE_A5,
    NOTE_D6, NOTE_B5, NOTE_G5, NOTE_E5, NOTE_B5, NOTE_A5, NOTE_G5,
    NOTE_C5, NOTE_G5, NOTE_E5,

    NOTE_D5, NOTE_E5, NOTE_F5,
    NOTE_G5, NOTE_F5, NOTE_G5, NOTE_E5, NOTE_G5, NOTE_C6,
    NOTE_E6, NOTE_D6, NOTE_D6, NOTE_D6, NOTE_C6, NOTE_C6]

audio_file = None

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

def play_file(audio_filename):
	pygame.mixer.music.load(path+audio_filename)
	pygame.mixer.music.play()

# this will be called when button events are received
def blink(event):
	# turn the LED on when a rising edge is detected
	if event.edge == NeoTrellis.EDGE_RISING:  # Trellis button pushed
		trellis.pixels[event.number] = WHITE
		if shuffled_names[event.number] != "":
			play_file(shuffled_names[event.number])
			print("START MUSIC")
	# turn the LED off when a rising edge is detected
	if event.edge == NeoTrellis.EDGE_FALLING:
		print("STOP MUSIC")
		pygame.mixer.music.stop()	
		trellis.pixels[event.number] = shuffled_colors[event.number]

path = "/home/pi/Final/piano/"
wavefiles = [file for file in os.listdir(path) if (file.endswith(".ogg") and not file.startswith("._"))]
if len(wavefiles) < 1:
	print("No wav files found in sounds directory")
else:
	print("Audio files found: ", wavefiles)

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
	# set all keys to trigger the blink callback
	trellis.callbacks[i] = blink

	# cycle the LEDs on startup
	trellis.pixels[i] = WHITE
	time.sleep(0.05)
 
for i in range(16):
	trellis.pixels[i] = shuffled_colors[i]
	time.sleep(0.05)

while True:
	# call the sync function call any triggered callbacks
	trellis.sync()
	


	# the trellis can only be read every 17 milliseconds or so
	time.sleep(0.001)