from random import randint
import copy
import mido
from mido import MidiFile, MidiTrack
import random
        

def select_next_note(input_notes, curr_note):
    rand_val = random.random()
    total = 0
    for next_note, probs in input_notes[curr_note][1].items():
        total += probs
        if rand_val <= total:
            return next_note


tune1 = []
tune2 = []
tune3 = []
tune4 = []
tune5 = []
all_tunes = []

# go through all midi files and add notes to the tune lists (for now they are random notes)
for i in range(500):
    tune1.append(randint(1, 88))
    tune2.append(randint(30, 60))
    tune3.append(randint(50, 55))
    tune4.append(randint(10, 70))
    tune5.append(randint(15, 65))

# add all the tunes to the one list of lists
all_tunes.append(copy.copy(tune1))
all_tunes.append(copy.copy(tune2))
all_tunes.append(copy.copy(tune3))
all_tunes.append(copy.copy(tune4))
all_tunes.append(copy.copy(tune5))

# states are all the possible notes on the piano
states = list(range(1, 88))

# create a dictionary to store the probabilities
probabilities = {}

# iterate over each note in all tunes
for tune in all_tunes:
    for i in range(len(tune)-1):
        current_note = tune[i]
        next_note = tune[i+1]
        
        # check if the current note is already in the dictionary
        if current_note in probabilities:
            # check if the next note is already in the nested dictionary
            if next_note in probabilities[current_note]:
                # increment the count of the next note
                probabilities[current_note][next_note] += 1
            else:
                # add the next note to the nested dictionary with count 1
                probabilities[current_note][next_note] = 1
        else:
            # add the current note to the dictionary with the next note and count 1
            probabilities[current_note] = {next_note: 1}

# calculate the probabilities by dividing the counts by the total occurrences of each note
for current_note in probabilities:
    total_occurrences = sum(probabilities[current_note].values())
    for next_note in probabilities[current_note]:
        probabilities[current_note][next_note] /= total_occurrences

# order the probabilities by the current_note
sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[0])

# iterate over each note in the range of 1 to 88
for note in states:
    # check if the note is not in the probabilities dictionary
    if note not in probabilities:
        # add the note to the probabilities dictionary with a nested dictionary containing only 0
        probabilities[note] = {0: 0}

# Order the nested dictionaries within each note in probabilities by the next_note and add in zeros for the missing probabilities
for note, probability in sorted_probabilities:
    next_notes = {k: probability.get(k, 0) for k in states}
    # print(f"Note {note}: {next_notes} \n\n")

# Create a MIDI file
midi_file = MidiFile()

# Set the tempo and other MIDI parameters
track = MidiTrack()
midi_file.tracks.append(track)
track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))

# Set the duration and velocity for each note
duration = 1  # in beats
velocity = 100  # 0-127
time = 0  # current time in tune
curr_note = 59  # starting note
length = 500  # length of song in notes
next_note_temp = 0

for i in range(10000):
    # Add the note to the MIDI file
    track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
    track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=(duration + time)))
    time += duration

    # Generate the next note based on the probabilities
    next_note_temp = select_next_note(sorted_probabilities, curr_note % len(sorted_probabilities))
    curr_note = next_note_temp

# Save the MIDI file
# midi_file.save("output/output_markov2.mid")
# print(midi_file)
