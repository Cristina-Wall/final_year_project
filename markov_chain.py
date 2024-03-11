from random import randint
import copy
import datetime
import mido
from mido import MidiFile, MidiTrack
import random
import os
# from flask import Flask, render_template, request , jsonify

# app = Flask(__name__,template_folder="templates") 

# @app.route("/") 
# def hello(): 
# 	return render_template('index.html') 

# @app.route('/process', methods=['POST']) 
# def process(): 
# 	data = request.get_json() # retrieve the data sent from JavaScript 
# 	# process the data using Python code 
# 	result = data['value'] * 2
# 	return jsonify(result=result) # return the result to JavaScript 

# if __name__ == '__main__': 
# 	app.run(debug=True) 


total_notes_in_tunes = 0
# get start time
start_time = datetime.datetime.now()

def select_next_note(input_notes, curr_note, notes_allowed):
    probability_distribution = copy.copy(input_notes[curr_note])
    cumulative_probabilities = [sum(probability_distribution[:idx+1]) for idx in range(len(probability_distribution))]
    random_value = random.uniform(0, 1)

    # Find the index where the random_value falls in the cumulative probabilities
    for idx, cumulative_prob in enumerate(cumulative_probabilities):
        if random_value <= cumulative_prob:
            if idx in notes_allowed:
                return idx
            else:
                select_next_note(input_notes, curr_note, notes_allowed)


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
    for directory in directory:
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                file_names.append(directory + "/" + filename)
    return file_names

def make_scale_of_c():
    scale = []
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

def make_scale_of_major_c():
    scale = []
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

def make_scale_of_minor_c():
    scale = []
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

    for i in range(len(scale) - removed):
        if scale[i - removed] > 128:
            scale.remove(scale[i - removed])
            removed += 1
    return scale

directory_path = ["midiFiles/maestro-v3.0.0/2004", "midiFiles/maestro-v3.0.0/2006", "midiFiles/maestro-v3.0.0/2008", "midiFiles/maestro-v3.0.0/2009", "midiFiles/maestro-v3.0.0/2011", "midiFiles/maestro-v3.0.0/2013", "midiFiles/maestro-v3.0.0/2014", "midiFiles/maestro-v3.0.0/2015", "midiFiles/maestro-v3.0.0/2017", "midiFiles/maestro-v3.0.0/2018"]
# directory_path = "midiFiles/one_note_melodies"
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
chosen_key = "c"
chosen_tonality = "major"

channel = 0
pitch = 0

notes_allowed = get_allowed_notes(chosen_key, chosen_tonality)

track.append(mido.MetaMessage('set_tempo', tempo=120, time=0))

for i in range(500):
    # Add the note to the MIDI file
    track.append(mido.Message('note_on', note=curr_note, velocity=velocity, time=time))
    track.append(mido.Message('note_off', note=curr_note, velocity=velocity, time=time+duration))
    time += duration
    # Generate the next note based on the probabilities
    next_note_temp = select_next_note(normalised_probabilities, curr_note, notes_allowed)
    curr_note = next_note_temp

# print(normalised_probabilities)
# Save the MIDI file
midi_file.save("output/output_markov_dataset_01.mid")
# print(midi_file)

# writing to file
# file1 = open('output_09_03_dataset04_probs.txt', 'w')
# for i in range(len(normalised_probabilities)):
#     file1.write(str(normalised_probabilities[i]) + "\n")
# file1.close()

# get end time
end_time = datetime.datetime.now()
# print the time taken to run the program
print(end_time - start_time)
