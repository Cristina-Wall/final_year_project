from random import randint
import copy
import datetime
import mido
from mido import MidiFile, MidiTrack
import random
import os
import ast
import math

####################
# Before the run these are all the parameters that can be set
save_to_file = "output/16_03_04.mid" # the name and location of the file the song will be saved to
velocity = 100  # the strength of each note (dynamics)
curr_note = 36  # starting note (middle C)
length = 500  # length of song in notes
chosen_key = "c" # key the song will be in
chosen_tonality = "major" # tonality of the song
num_past_notes = 1 # number of past notes to base the probabilities on
    # ^ if changing this also have to change what function is called for select_next_note
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
    # if(prev_note == 127):
    #     prev_note = 60 # do something about this!!! this is here because when prev_note is 127, the index is too high and it doesnt actually exist
    while True:
        # probability_distribution = copy.copy(input_notes[(prev_note * num_notes) + prev_note + curr_note])
        probability_distribution = copy.copy(input_notes[(prev_note * num_notes) + curr_note])
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
        probability_distribution = copy.copy(input_notes[((prev_prev_note * num_notes)^2) + (prev_note * num_notes) + curr_note])
        cumulative_probabilities = [sum(probability_distribution[:idx+1]) for idx in range(len(probability_distribution))]
        random_value = random.uniform(0, 1)

        # Find the index where the random_value falls in the cumulative probabilities
        for index, cumulative_prob in enumerate(cumulative_probabilities):
            if random_value <= cumulative_prob:
                if index in notes_allowed:
                    # Return the note found
                    return index

# Function that imports a midi file and removes any duplicate tracks
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

# Function that goes through all the files in the directory and gets the note values from each file
# Each note gets added to a list in the order that they occur so that the probabilities can be calculated later
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

        if i['type'] == 'note_on' and i['note'] >= 24 and i['note'] < 108:
            mem2.append(i['note'])
            output.append(mem2)
            total_notes += 1

    output = [item for sublist in output for item in sublist]
    return output, total_notes

# Function that gets all the file names from the input directory
def get_file_names(directory):
    file_names = []
    for dir in directory:
        for filename in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, filename)):
                file_names.append(dir + "/" + filename)
    return file_names

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
    for x in range(84):
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
    for x in range(84):
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
        if scale[i - removed] > 84:
            scale.remove(scale[i - removed])
            removed += 1
    return scale

# Function that creates the initial empty arrays
def start_probs(num_notes, num_past_notes):
    probabilities_array = [[0] * num_notes for _ in range(pow(num_notes, num_past_notes))]
    normalised_probabilities = [[0] * num_notes for _ in range(pow(num_notes, num_past_notes))]
    probabilities_note_count = [[0]*num_notes for _ in range(pow(num_notes, num_past_notes))]
    states = list(range(pow(num_notes, num_past_notes)))
    return probabilities_array, normalised_probabilities, probabilities_note_count, states

# Function that counts the occurrences of each note in the tunes
def count_notes_for_probs(states, num_notes, probabilities_array, all_tunes, probabilities_note_count, num_past_notes):
    for i in range(len(states)):
        for j in range(num_notes):
            probabilities_array[i][j] = 100 / len(states) / 100 / num_notes

    if num_past_notes == 1:
        for tune in all_tunes:
            for i in range(len(tune)):
                current_note = tune[i]

                if i < len(tune) - 1:
                    next_note = tune[i + 1]
                    next_note -= 24
                    current_note -= 24
                    probabilities_note_count[current_note][next_note] += 1
                else:
                    return probabilities_array, probabilities_note_count
    elif num_past_notes == 2:
        for tune in all_tunes:
            for i in range(len(tune)):
                current_note = tune[i]

                if i < len(tune) - 2:
                    next_note = tune[i + 1]
                    next_next_note = tune[i + 2]
                    current_note -= 24
                    next_note -= 24
                    next_next_note -= 24
                    probabilities_note_count[(current_note * num_notes) + next_note][next_next_note] += 1
                else:
                    return probabilities_array, probabilities_note_count
    elif num_past_notes == 3:
        for tune in all_tunes:
            for i in range(len(tune)):
                current_note = tune[i]

                if i < len(tune) - 3:
                    next_note = tune[i + 1]
                    next_next_note = tune[i + 2]
                    next_next_next_note = tune[i + 3]
                    current_note -= 24
                    next_note -= 24
                    next_next_note -= 24
                    next_next_next_note -= 24
                    probabilities_note_count[((current_note * num_notes)^2) + (next_note * num_notes) + next_next_note][next_next_next_note] += 1
                else:
                    return probabilities_array, probabilities_note_count
    return probabilities_array, probabilities_note_count

def calculate_norm_probs(probabilities_note_count, probabilities_array, normalised_probabilities, num_notes, num_past_notes, states):
    for i in range(len(probabilities_note_count)):
        for j in range(len(probabilities_note_count[i])):
            normalised_probabilities[i][j] = (1 + (probabilities_note_count[i][j]) *100) / (len(probabilities_note_count[i]) + (sum(probabilities_note_count[i])) *100)
    # probabilities_note_count.delete()
    return normalised_probabilities

def choose_timing(prev_duration):
    if random.random() < 0.5:
        duration = randint(prev_duration - 20, prev_duration + 20)
    elif random.random() < 0.75:
        duration = randint(randint(prev_duration - 50, prev_duration - 20), randint(prev_duration + 20, prev_duration + 50))
    elif random.random() < 0.1:
        duration = randint(randint(prev_duration - 90, prev_duration - 50), randint(prev_duration + 50, prev_duration + 90))
    else:
        duration = randint(randint(prev_duration - 150, prev_duration - 90), randint(prev_duration + 90, prev_duration + 150))

    if duration < 0 or duration > 200:
        duration = choose_timing(prev_duration)
    return duration

def find_chord(note):
    if note < 12:
        note1 = None
        note2 = None
        note3 = None
    else:
        note1 = note - 12
        note2 = note - 8
        note3 = note - 5
    return note1, note2, note3

time1 = datetime.datetime.now()
print("time taken before anything started: ", time1 - start_time)
# directory_path = ["midiFiles/maestro-v3.0.0/2004", "midiFiles/maestro-v3.0.0/2006", "midiFiles/maestro-v3.0.0/2008", "midiFiles/maestro-v3.0.0/2009", "midiFiles/maestro-v3.0.0/2011", "midiFiles/maestro-v3.0.0/2013", "midiFiles/maestro-v3.0.0/2014", "midiFiles/maestro-v3.0.0/2015", "midiFiles/maestro-v3.0.0/2017", "midiFiles/maestro-v3.0.0/2018"]
directory_path = ["midiFiles/one_note_melodies"]
file_names = get_file_names(directory_path)

time2 = datetime.datetime.now()
print("time taken to import files: ", time2 - time1)

all_tunes = []

# get all the notes from each of the files
for i in range(len(file_names)):
    tune, total_notes = get_notes_from_file(file_names[i])
    all_tunes.append(copy.copy(tune))
    total_notes_in_tunes += total_notes

time3 = datetime.datetime.now()
print("time taken to read notes from files: ", time3 - time2)

# num_notes are all the possible notes on the piano
num_notes = 84

# create a dictionary to store the probabilities
probabilities = {}
probabilities_array, normalised_probabilities, probabilities_note_count, states = start_probs(num_notes, num_past_notes)

time4 = datetime.datetime.now()
print("time taken to create empty probability lists: ", time4 - time3)

probabilities_array, probabilities_note_count = count_notes_for_probs(states, num_notes, probabilities_array, all_tunes, probabilities_note_count, num_past_notes)

time5 = datetime.datetime.now()
print("time taken to count note occurrences: ", time5 - time4)

normalised_probabilities = calculate_norm_probs(probabilities_note_count, probabilities_array, normalised_probabilities, num_notes, num_past_notes, states)

time6 = datetime.datetime.now()
print("time taken to calculate normalised probabilities: ", time6 - time5)

total_prob = 0
for i in range(len(states)):
    for j in range(num_notes):
        total_prob += probabilities_array[i][j]
print("total probabilities: ", total_prob)

# Write to file
# file1 = open('15_03_08.txt', 'w')
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
prev_note = 36
prev_prev_note = 36
channel = 0
pitch = 0
prev_duration = 50
duration = randint(50, 150)
chord_pos = 0

notes_allowed = get_allowed_notes(chosen_key, chosen_tonality)

time7 = datetime.datetime.now()
print("time taken to get key and create scale: ", time7 - time6)

track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))

# bpm = mido.tempo2bpm(tempo)
# print("bpm: ", math.floor(bpm))
# print("curr time: ", math.floor((datetime.datetime.now().microsecond) / 100000))
# song_start_time = math.floor((datetime.datetime.now().microsecond) / 100000)
# print("song start time: ", song_start_time)

for i in range(length):
    if chord_pos%4 == 0:
        note1, note2, note3 = find_chord(curr_note)
        if note1 == None:
            track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
            track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))
        else:
            track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
            track.append(mido.Message('note_on', note=note1, velocity=velocity, time=time))
            track.append(mido.Message('note_on', note=note2, velocity=velocity, time=time))
            track.append(mido.Message('note_on', note=note3, velocity=velocity, time=time))

            track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))
            track.append(mido.Message('note_off', note=note1, velocity=velocity, time=time+duration))
            track.append(mido.Message('note_off', note=note2, velocity=velocity, time=time+duration))
            track.append(mido.Message('note_off', note=note3, velocity=velocity, time=time+duration))
    else:
        track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
        track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))

    # track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
    # track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))

    chord_pos += 1
    prev_duration = duration
    duration = choose_timing(prev_duration)
    time += duration
    time = math.floor(math.sqrt(time))

    # Generate the next note based on the probabilities
    next_note_temp = select_next_note(normalised_probabilities, curr_note, notes_allowed)
    # next_note_temp = select_next_note_from_two(normalised_probabilities, curr_note, prev_note, notes_allowed, num_notes)
    # next_note_temp = select_next_note_from_three(normalised_probabilities, curr_note, prev_note, prev_prev_note, notes_allowed, num_notes)

    prev_prev_note = prev_note
    prev_note = curr_note
    curr_note = next_note_temp

# Save the MIDI file
midi_file.save(save_to_file)
# print(midi_file)

time8 = datetime.datetime.now()
print("time taken to write the song: ", time8 - time7)

# get end time
end_time = datetime.datetime.now()
# print the time taken to run the program
print(end_time - start_time)
