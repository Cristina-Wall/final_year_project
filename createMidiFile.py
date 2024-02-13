import mido
from mido import MidiFile, MidiTrack

mid = MidiFile()
track = MidiTrack()
track.append(mido.Message('note_on', note=60, velocity=64, time=32))
track.append(mido.Message('note_off', note=60, velocity=64, time=1500))
mid.tracks.append(track)
mid.save('output.mid')

print("mid: ")
print(mid)
print("track: ")
print(track)
