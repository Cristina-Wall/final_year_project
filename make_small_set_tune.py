from random import randint
import copy
import datetime
import mido
from mido import MidiFile, MidiTrack
import random
import os
import ast
import math

from mido import MidiFile, MidiTrack, bpm2tempo
from mido import Message, MetaMessage
from mido.midifiles.units import tick2second, second2tick
from mido import bpm2tempo

####################
# Before the run these are all the parameters that can be set
save_to_file = "output/14_03_07_set_notes.mid" # the name and location of the file the song will be saved to
duration = 50  # in beats - the length of each note
velocity = 100  # the strength of each note (dynamics)
curr_note = 40  # starting note (middle C)
length = 500  # length of song in notes
tempo = 500000 # tempo of the song
# length of song in seconds????
# instrument????
####################

# Create a MIDI file
midi_file = MidiFile(ticks_per_beat=480)

# Set the tempo and other MIDI parameters
track = MidiTrack()
midi_file.tracks.append(track)

# Before the run these are all the parameters that can be set
time = 0  # current time in tune
next_note = 0
channel = 0
pitch = 0

def choose_timing():
    return random.randint(1, 4)

track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
# track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
# track.append(mido.MetaMessage('smpte_offset', frame_rate=25, hours=1, minutes=0, seconds=0, frames=0, sub_frames=0, time=0))

for i in range(length):
    if curr_note > 100:
        break

    track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
    track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))

    time += duration
    time = math.floor(math.sqrt(time))
    curr_note = curr_note + 1


# Save the MIDI file
midi_file.save("output/14_03_26_set_notes.mid")
print(midi_file)
