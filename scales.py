import random

import mido
from mido import MidiFile, MidiTrack

# notes:
#     c = 60,    c# = 61,   d = 62,    d# = 63,    e = 64
#     f = 65,    f# = 66,   g = 67,    g# = 68,    a = 69
#     a# = 70,   b = 71,    c = 72,    c# = 73,    d = 74
#     d# = 75,   e = 76

major_scale = [0, 2, 4, 5, 7, 9, 11, 12]
minor_scale = [0, 2, 3, 5, 7, 8, 10, 12]
chromatic_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def create_scale(note, tonality):
    mid = MidiFile()
    track = MidiTrack()
    time = 0
    start_note = note

    if tonality == "major":
        for x in major_scale:
            track.append(mido.Message('note_on', note=start_note + x, velocity=64, time=time + 32))
            track.append(mido.Message('note_off', note=start_note + x, velocity=64, time=time + 64))
            mid.tracks.append(track)
            time += 32
    elif tonality == "minor":
        for x in minor_scale:
            track.append(mido.Message('note_on', note=start_note + x, velocity=64, time=time + 32))
            track.append(mido.Message('note_off', note=start_note + x, velocity=64, time=time + 64))
            mid.tracks.append(track)
            time += 32
    elif tonality == "chromatic":
        for x in chromatic_scale:
            track.append(mido.Message('note_on', note=start_note + x, velocity=64, time=time + 32))
            track.append(mido.Message('note_off', note=start_note + x, velocity=64, time=time + 64))
            mid.tracks.append(track)
            time += 32
    else:
        print("bad input")

    mid.save('output_error_test.mid')

def create_song(key, tonality, length):
    mid = MidiFile()
    track = MidiTrack()
    note_time = 0
    key = key
    start_note = key

    if tonality == "major":
        for x in range(length):
            note = random.choice(major_scale)
            track.append(mido.Message('note_on', note=note + start_note, velocity=64, time=note_time + 64))
            track.append(mido.Message('note_off', note=note + start_note, velocity=64, time=note_time + 128))
            mid.tracks.append(track)
    elif tonality == "minor":
        for x in range(length):
            note = random.choice(minor_scale)
            track.append(mido.Message('note_on', note=note + start_note, velocity=64, time=note_time + 64))
            track.append(mido.Message('note_off', note=note + start_note, velocity=64, time=note_time + 128))
            mid.tracks.append(track)
    elif tonality == "chromatic":
        for x in range(length):
            note = random.choice(chromatic_scale)
            track.append(mido.Message('note_on', note=note + start_note, velocity=64, time=note_time + 64))
            track.append(mido.Message('note_off', note=note + start_note, velocity=64, time=note_time + 128))
            mid.tracks.append(track)
    else:
        print("bad input")

    mid.save('output_random_test8.mid')


# create_scale(60, "minor")

create_song(60, "major", 20)
