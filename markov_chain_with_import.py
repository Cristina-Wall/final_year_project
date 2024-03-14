from random import randint
import copy
import datetime
import mido
from mido import MidiFile, MidiTrack
import random
import ast
import math

####################
# Before the run these are all the parameters that can be set
save_to_file = "output/12_03_14.mid" # the name and location of the file the song will be saved to
duration = 50  # in beats - the length of each note
velocity = 100  # the strength of each note (dynamics)
curr_note = 59  # starting note (middle C)
length = 500  # length of song in notes
chosen_key = "c" # key the song will be in
chosen_tonality = "major" # tonality of the song
num_past_notes = 1 # number of past notes to base the probabilities on
tempo = 500000 # tempo of the song
# length of song in seconds????
# instrument????
####################


total_notes_in_tunes = 0
# get start time
start_time = datetime.datetime.now()
print("start time: ", start_time)

# Function that will get the next note based on the probabilities, if the program is running based on a single note
def select_next_note(input_notes, curr_note, notes_allowed):
    while True:
        probability_distribution = copy.copy(input_notes[curr_note])
        cumulative_probabilities = [sum(probability_distribution[:idx + 1]) for idx in range(len(probability_distribution))]
        random_value = random.uniform(0, 1)

        # Find the index where the random_value falls in the cumulative probabilities
        for index, cumulative_prob in enumerate(cumulative_probabilities):
            if random_value <= cumulative_prob and index in notes_allowed:
                return index

# Similar to function above but this uses the probabilities based on the two previous notes
def select_next_note_from_two(input_notes, curr_note, prev_note, notes_allowed, num_notes):
    if(prev_note == 127):
        prev_note = 60 # do something about this!!! this is here because when prev_note is 127, the index is too high and it doesnt actually exist
    while True:
        probability_distribution = copy.copy(input_notes[(prev_note * num_notes) + prev_note + curr_note])
        cumulative_probabilities = [sum(probability_distribution[:idx+1]) for idx in range(len(probability_distribution))]
        random_value = random.uniform(0, 1)

        # Find the index where the random_value falls in the cumulative probabilities
        for index, cumulative_prob in enumerate(cumulative_probabilities):
            if random_value <= cumulative_prob:
                if index in notes_allowed:
                    # Return the note found
                    return index

# Similar to function above but this uses the probabilities based on the three previous notes
def select_next_note_from_three(input_notes, curr_note, prev_note, prev_prev_note, notes_allowed, num_notes):
    while True:
        probability_distribution = copy.copy(input_notes[(prev_note * num_notes) + (prev_prev_note * num_notes) + prev_note + prev_prev_note + curr_note])
        cumulative_probabilities = [sum(probability_distribution[:idx+1]) for idx in range(len(probability_distribution))]
        random_value = random.uniform(0, 1)

        # Find the index where the random_value falls in the cumulative probabilities
        for index, cumulative_prob in enumerate(cumulative_probabilities):
            if random_value <= cumulative_prob:
                if index in notes_allowed:
                    # Return the note found
                    return index

# Function that gets the allowed notes based on the key and tonality
# The program will later then only be allowed to select notes from this list
def get_allowed_notes(key, tonality):
    scale_of_major_c = make_scale_of_major_c()
    scale_of_minor_c = make_scale_of_minor_c()

    if key == "c" and tonality == "major":
        return scale_of_major_c
    elif key == "c" and tonality == "minor":
        return scale_of_minor_c
    elif tonality == "major":
        scale = make_scale(key, scale_of_major_c)
        return scale
    elif tonality == "minor":
        scale = make_scale(key, scale_of_minor_c)
        return scale
    else:
        return 0

# Function that makes a scale of C major, spanning across 0 to 128 notes (the range in a midi file)
# All major scales are based on the C scale, adding the number of semitones to each note in the scale
def make_scale_of_major_c():
    scale = []
    # The scale of C is made up of notes number 0, 2, 4, 5, 7, 9, 11 in every octave
    for x in range(128):
        if x % 12 == 0:
            scale.append(x)
        elif x % 12 == 2:
            scale.append(x)
        elif x % 12 == 4:
            scale.append(x)
        elif x % 12 == 5:
            scale.append(x)
        elif x % 12 == 7:
            scale.append(x)
        elif x % 12 == 9:
            scale.append(x)
        elif x % 12 == 11:
            scale.append(x)
    return scale

# Function that makes a scale of C minor, spanning across 0 to 128 notes (the range in a midi file)
# All minor scales are based on the C scale, adding the number of semitones to each note in the scale
def make_scale_of_minor_c():
    scale = []
    # The scale of C is made up of notes number 0, 2, 3, 5, 7, 8, 11 in every octave
    for x in range(128):
        if x % 12 == 0:
            scale.append(x)
        elif x % 12 == 2:
            scale.append(x)
        elif x % 12 == 3:
            scale.append(x)
        elif x % 12 == 5:
            scale.append(x)
        elif x % 12 == 7:
            scale.append(x)
        elif x % 12 == 8:
            scale.append(x)
        elif x % 12 == 11:
            scale.append(x)
    return scale

# Function that makes a scale based on the key and the scale of C, adding the number of semitones to each note in the scale
def make_scale(key, scale_of_c):
    scale = len(scale_of_c)*[0]
    if key == "d":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 2
    elif key == "e":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 4
    elif key == "f":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 5
    elif key == "g":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 7
    elif key == "a":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 9
    elif key == "b":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 11
    elif key == "d_flat" or key == "c_sharp":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 1
    elif key == "e_flat" or key == "d_sharp":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 3
    elif key == "g_flat" or key == "f_sharp":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 6
    elif key == "a_flat" or key == "g_sharp":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 8
    elif key == "b_flat" or key == "a_sharp":
        for i in range(len(scale_of_c)):
            scale[i] = scale_of_c[i] + 10
    else:
        return "invalid key"
    
    removed = 0
    
    # Remove any notes that are above 128
    for i in range(len(scale) - removed):
        if scale[i - removed] > 128:
            scale.remove(scale[i - removed])
            removed += 1
    return scale

# Function that creates the initial empty arrays
def start_probs(num_notes, num_past_notes):
    normalised_probabilities = [[0] * num_notes for _ in range(pow(num_notes, num_past_notes))]
    states = list(range(pow(num_notes, num_past_notes)))
    return normalised_probabilities, states

def choose_timing():
    return randint(60, 240)

def import_probabilities():
    with open('output_norm_probs_one_small_01.txt', 'r') as file1:
        lines = file1.readlines()
    reconstructed_list = []
    for line in lines:
        value = ast.literal_eval(line.strip())
        reconstructed_list.append(value)
    return reconstructed_list

num_notes = 128
normalised_probabilities, states = start_probs(num_notes, num_past_notes)
normalised_probabilities = import_probabilities()

time2 = datetime.datetime.now()
print("time taken to set up lists: ", time2 - start_time)

# file1 = open('output_norm_probs_12_03_23.txt', 'w')
# for i in range(len(normalised_probabilities)):
#     file1.write(str(normalised_probabilities[i]) + "\n")
# file1.close()

# Create a MIDI file
midi_file = MidiFile()

# Set the tempo and other MIDI parameters
track = MidiTrack()
midi_file.tracks.append(track)

# Before the run these are all the parameters that can be set
time = 0  # current time in tune
next_note_temp = 0
prev_note = 59
prev_prev_note = 59
channel = 0
pitch = 0

notes_allowed = get_allowed_notes(chosen_key, chosen_tonality)

time3 = datetime.datetime.now()
print("time taken to create midi and get allowed notes and scales: ", time3 - time2)

# time7 = datetime.datetime.now()
# print("time taken to get key and create scale: ", time7 - time6)

track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

for i in range(length):
    # Add the note to the MIDI file
    track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
    track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))

    time += duration
    time = math.floor(math.sqrt(time))

    # duration = choose_timing()
    # Generate the next note based on the probabilities
    # next_note_temp = select_next_note(normalised_probabilities, curr_note, notes_allowed)
    next_note_temp = select_next_note_from_two(normalised_probabilities, curr_note, prev_note, notes_allowed, num_notes)
    # next_note_temp = select_next_note_from_three(normalised_probabilities, curr_note, prev_note, prev_prev_note, notes_allowed, num_notes)

    # prev_prev_note = prev_note
    prev_note = curr_note
    curr_note = next_note_temp

time4 = datetime.datetime.now()
print("time taken to make song: ", time4 - time3)

# Save the MIDI file
midi_file.save(save_to_file)
# print(midi_file)

time5 = datetime.datetime.now()
print("time taken to save song as midi file: ", time5 - time4)

# get end time
end_time = datetime.datetime.now()
# print the time taken to run the program
print("total time: ", end_time - start_time)
