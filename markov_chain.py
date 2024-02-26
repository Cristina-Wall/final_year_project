from random import randint
import copy
import mido
from mido import MidiFile, MidiTrack
import random

total_notes_in_tunes = 0


def select_next_note(input_notes, curr_note):
    rand_val = random.random()
    total = 0
    for next_note, probs in input_notes[curr_note][1].items():
        total += probs
        if rand_val <= total:
            return next_note


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


all_tunes = []

# import all the midi files
mid1 = import_file("midiFiles/one_note_melodies/gravity_falls.mid")

# add all the tunes to the one list of lists
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/gravity_falls.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/howls_moving_castle.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/beauty_and_the_beast.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/cant_help_falling_in_love.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/happy_birthday.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/hedwigs_theme.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/la_vie_en_rose.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/pink_panther.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/tetris.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/twinkle_twinkle.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/you_are_my_sunshine.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/youve_got_a_friend_in_me.mid")
all_tunes.append(copy.copy(tune))
total_notes_in_tunes += total_notes
tune, total_notes = get_notes_from_file("midiFiles/one_note_melodies/you_belong_with_me.mid")
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
        normalised_probabilities[i][j] = (1 + probabilities_note_count[i][j]) / (num_notes + total_notes_in_tunes)
        
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
# track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))

# Set the duration and velocity for each note
duration = 5  # in beats
velocity = 100  # 0-127
time = 0  # current time in tune
curr_note = 72  # starting note
length = 500  # length of song in notes
next_note_temp = 0

channel = 0
pitch = 0

# for i in range(1000):
#     # Add the note to the MIDI file
#     track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
#     track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))
#     time += duration
    
#     # midi_file.addNote(channel, i, pitch+i, duration, 100)

#     # Generate the next note based on the probabilities
#     next_note_temp = select_next_note(sorted_probabilities, curr_note % len(sorted_probabilities))
#     curr_note = next_note_temp

# Save the MIDI file
# midi_file.save("output/output_markov20.mid")
# print(midi_file)
