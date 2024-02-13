import numpy as np
import random
import mido
from mido import MidiFile, MidiTrack

major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
minor_scale = [0, 2, 3, 5, 7, 8, 10, 12]
chromatic_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
notes = []  # notes that are allowed to use in the song


def create_scale(start_note, tonality):
    if tonality == "major":
        for i in range(len(major_scale)):
            note = start_note + major_scale[i]
            notes.append(note)
    elif tonality == "minor":
        for i in range(len(minor_scale)):
            note = start_note + minor_scale[i]
            notes.append(note)
    elif tonality == "chromatic":
        for i in range(len(chromatic_scale)):
            note = start_note + chromatic_scale[i]
            notes.append(note)

#create_scale(1, "minor")
#print(notes)


def probability(note):
    probabilities = []
    difference = 0

    for x in range(len(notes)):
        difference = abs(notes[x] - note)
        if difference < 10:
            probabilities[x] = 10 - difference
        else:
            probabilities[x] = 0.5


def create_song(start_note, tonality, length):
    mid = MidiFile()
    track = MidiTrack()
    note_time = 0
    note = start_note

    create_scale(start_note, tonality)

    for x in range(length):
        weightedNotes = []
        probabilities = []

        for i in range(len(notes)):
            probabilities[i] = probability(note)
            weightedNotes[i] = probabilities[i] * notes[i]

        prob = probability(note)  ####
        note = random.choice(notes) * prob
        track.append(mido.Message('note_on', note=note, velocity=64, time=note_time + 64))
        track.append(mido.Message('note_off', note=note, velocity=64, time=note_time + 128))
        mid.tracks.append(track)

    mid.save('output_random_song6.mid')


create_song(60, "major", 20)
print(notes)
