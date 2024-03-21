
from mido import MidiFile


def get_notes_from_file(file_name):
    mid = MidiFile(file_name, clip=True)
    mididict = []
    output = []

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

    output = [item for sublist in output for item in sublist]
    return output


mid1 = get_notes_from_file("midiFiles/one_note_melodies/gravity_falls.mid")
# print(mid1.tracks)


# states = list(range(1, 88))

# probabilities = {}

# for i in range(len(mid1)-1):
#     current_note = mid1[i]
#     next_note = mid1[i+1]
    
#     # check if the current note is already in the dictionary
#     if current_note in probabilities:
#         # check if the next note is already in the nested dictionary
#         if next_note in probabilities[current_note]:
#             # increment the count of the next note
#             probabilities[current_note][next_note] += 1
#         else:
#             # add the next note to the nested dictionary with count 1
#             probabilities[current_note][next_note] = 1
#     else:
#         # add the current note to the dictionary with the next note and count 1
#         probabilities[current_note] = {next_note: 1}

# # calculate the probabilities by dividing the counts by the total occurrences of each note
# for current_note in probabilities:
#     total_occurrences = sum(probabilities[current_note].values())
#     for next_note in probabilities[current_note]:
#         probabilities[current_note][next_note] /= total_occurrences

# # order the probabilities by the current_note
# sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[0])

# # iterate over each note in the range of 1 to 88
# for note in states:
#     # check if the note is not in the probabilities dictionary
#     if note not in probabilities:
#         # add the note to the probabilities dictionary with a nested dictionary containing only 0
#         probabilities[note] = {0: 0}

# # Order the nested dictionaries within each note in probabilities by the next_note and add in zeros for the missing probabilities
# for note, probability in sorted_probabilities:
#     next_notes = {k: probability.get(k, 0) for k in states}
#     # print(f"Note {note}: {next_notes} \n\n")

