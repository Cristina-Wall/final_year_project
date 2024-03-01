from random import randint
import copy
import mido
from mido import MidiFile, MidiTrack
import random

# this file prints a midi file either to console or to a file

# file_name = "midiFiles/maestro-v3.0.0/2004/MIDI-Unprocessed_SMF_02_R1_2004_01-05_ORIG_MID--AUDIO_02_R1_2004_05_Track05_wav.midi"
file_name = "midiFiles/one_note_melodies/gravity_falls.mid"
mid = MidiFile(file_name, clip=True)
message_numbers = []
duplicates = []

for track in mid.tracks:
    if len(track) in message_numbers:
        duplicates.append(track)
    else:
        message_numbers.append(len(track))

for track in duplicates:
    mid.tracks.remove(track)

# print to console
# print(mid)

# print to text file
output_file = "output2.txt"
with open(output_file, "w") as file:
    file.write(str(mid))
