from random import randint
import copy
import mido
from mido import MidiFile, MidiTrack
import random
import os

total_notes_in_tunes = 0


def select_next_note(input_notes, curr_note):
    probability_distribution = copy.copy(input_notes[curr_note])
    cumulative_probabilities = [sum(probability_distribution[:idx+1]) for idx in range(len(probability_distribution))]
    random_value = random.uniform(0, 1)

    # Find the index where the random_value falls in the cumulative probabilities
    for idx, cumulative_prob in enumerate(cumulative_probabilities):
        if random_value <= cumulative_prob:
            return idx


def import_file(file_name):
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

    return mid


def get_notes_from_file(file_name):
    mid = MidiFile(file_name, clip=True)
    mididict = []
    output = []
    total_notes = 0

    for i in mid:
        if i.type == 'note_on':
            mididict.append(i.dict())

    for i in mididict:

        if i['type'] == 'note_on' and i['velocity'] == 0:
            i['type'] = 'note_off'

        mem2=[]

        if i['type'] == 'note_on':
            mem2.append(i['note'])
            output.append(mem2)
            total_notes += 1

    output = [item for sublist in output for item in sublist]
    return output, total_notes

def get_file_names(directory):
    file_names = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_names.append(directory + "/" + filename)
    return file_names

# directory_path = "midiFiles/maestro-v3.0.0/2004"
directory_path = "midiFiles/one_note_melodies"
file_names = get_file_names(directory_path)

all_tunes = []

# import all the midi files
# mid1 = import_file("midiFiles/one_note_melodies/gravity_falls.mid")

# get all the notes from each of the files
for i in range(len(file_names)):
    tune, total_notes = get_notes_from_file(file_names[i])
    all_tunes.append(copy.copy(tune))
    total_notes_in_tunes += total_notes

# states are all the possible notes on the piano
states = list(range(0, 128))
num_notes = 128

# create a dictionary to store the probabilities
probabilities = {}
probabilities_array = [[0] * num_notes for _ in range(num_notes)]
normalised_probabilities = [[0] * num_notes for _ in range(num_notes)]

for i in range(len(states)):
    for j in range(len(states)):
        probabilities_array[i][j] = 100 / len(states) / 100

probabilities_note_count = [[0]*num_notes for _ in range(num_notes)]

# iterate over each note in all tunes
for tune in all_tunes:
    for i in range(len(tune)):
        current_note = tune[i]

        if i < len(tune) - 1:
            next_note = tune[i + 1]
            probabilities_note_count[current_note - 1][next_note - 1] += 1
        else:
            break

# calculate the probabilities by dividing the counts by the total occurrences of each note
for i in range(len(probabilities_note_count)):
    for j in range(len(probabilities_note_count[i])):
        normalised_probabilities[i][j] = (1 + (probabilities_note_count[i][j] * 3)) / (len(probabilities_note_count[i]) + (sum(probabilities_note_count[i]) * 3))

# Create a MIDI file
midi_file = MidiFile()

# Set the tempo and other MIDI parameters
track = MidiTrack()
midi_file.tracks.append(track)
# track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))

# Set the duration and velocity for each note
duration = 100  # in beats
velocity = 100  # 0-127
time = 0  # current time in tune
curr_note = 59  # starting note
length = 500  # length of song in notes
next_note_temp = 0

channel = 0
pitch = 0

track.append(mido.MetaMessage('set_tempo', tempo=120, time=0))

for i in range(500):
    # Add the note to the MIDI file
    track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
    track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))
    time += duration
    
    # midi_file.addNote(channel, i, pitch+i, duration, 100)

    # Generate the next note based on the probabilities
    next_note_temp = select_next_note(normalised_probabilities, curr_note)
    curr_note = next_note_temp

# Save the MIDI file
# midi_file.save("output/output_markov28.mid")
# print(midi_file)
