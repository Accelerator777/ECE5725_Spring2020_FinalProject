import os
import random
import board
from board import SCL, SDA
import digitalio
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from music_data import*
from pydub.pydub import AudioSegment
from pydub.pydub.playback import play

# #output = AudioSegment.from_file("./piano/15-red-la.wav", format="wav")
# record_data = [0, 1, 2, 3, 4, 5, 6]
# period_data = [7, 7, 8]
# wav_piano_list = ("piano/00-red-do.wav", "piano/01-purple-re.wav", "piano/02-blue-mi.wav", "piano/03-green-fa.wav", "piano/04-yellow-sol.wav", "piano/05-cyan-la.wav", "piano/06-white-si.wav", "piano/07-red-do.wav", "piano/08-red-do.wav", "piano/09-purple-re.wav", "piano/10-blue-mi.wav", "piano/11-green-fa.wav", "piano/12-cyan-la.wav", "piano/13-yellow-sol.wav", "piano/14-white-si.wav", "piano/15-red-do.wav")


# output = AudioSegment.from_file(wav_piano_list[record_data[5]], format="wav")

# first_output = period_data[0] * 1000
# print(period_data[0])
# slice_output = output[:first_output]


# song = AudioSegment.from_file(wav_piano_list[record_data[2]], format = "wav")

# first_seconds = 5 * 1000
# slice_song = song[:first_seconds]
# slice_output = slice_output + slice_song
# slice_output.export("out.wav", format="wav")

four_core = AudioSegment.from_file("out.wav", format="wav")
count = four_core.duration_seconds
print(count)
count_four = count/4
print(count_four)
core0 = four_core[:count_four*1000]
core1 = four_core[count_four:count_four*2000]
core2 = four_core[count_four*2000:count_four*3000]
core3 = four_core[count_four*3000:]

core0.export("out0.wav", format="wav")
core1.export("out1.wav", format="wav")
core2.export("out2.wav", format="wav")
core3.export("out3.wav", format="wav")

core0_read = AudioSegment.from_file("out0.wav", format="wav")
core1_read = AudioSegment.from_file("out1.wav", format="wav")
core2_read = AudioSegment.from_file("out2.wav", format="wav")
core3_read = AudioSegment.from_file("out3.wav", format="wav")

four_core_output = core0_read + core1_read + core2_read + core3_read
four_core_output.export("output.mp3", format="mp3")
