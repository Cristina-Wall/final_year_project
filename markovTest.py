import numpy as np
import random
import mido
from mido import MidiFile, MidiTrack

states = []
transitions = []
probabilityMatrix = []
curr_note = 0
note_probability = 0

# put all possible note values into states array
for x in range(128):
    states.append(x)

# put all possible combinations into transitions array
for y in states:
    transitions.append(states)
    #probabilityMatrix.append([])

for z in states:
    if z-curr_note == 0:
        note_probability = 0.7
    else:
        note_probability = 1/(z-curr_note)/10*8
    probabilityMatrix.append(note_probability)

# probability = 1/num /10*8

print(probabilityMatrix)

major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
notes = []


def create_scale(start_note):
    for i in range(len(major_scale)):
        note = start_note + major_scale[i]
        notes.append(note)


def create_song(key, tonality, length):
    mid = MidiFile()
    track = MidiTrack()
    note_time = 0
    key = key
    start_note = key

    for x in range(length):
        note = random.choice(major_scale)
        track.append(mido.Message('note_on', note=note + start_note, velocity=64, time=note_time + 64))
        track.append(mido.Message('note_off', note=note + start_note, velocity=64, time=note_time + 128))
        mid.tracks.append(track)

    mid.save('output_random_test8.mid')


create_song(60, "major", 20)

