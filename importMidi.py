
from mido import MidiFile

mid = MidiFile("midiFiles/midi1.midi", clip=True)
## print(mid)

message_numbers = []
duplicates = []

for track in mid.tracks:
    if len(track) in message_numbers:
        duplicates.append(track)
    else:
        message_numbers.append(len(track))

for track in duplicates:
    mid.tracks.remove(track)

mid.save("output/test2.mid")

print(mid)
