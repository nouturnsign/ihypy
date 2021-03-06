from ihypy.system import *
from ihypy.theory import *
from ihypy.instrument import *

# ihypy
WCS = WesternClassicalSystem()
piano = Piano()
c_minor_scale_2_octave = WCS.create_scale(NaturalMinorScale(octaves = 2), "C3")
g_dominant_altered_chord = WCS.create_chord("G7f139sus2/D", "G2")
piano.play_scale(c_minor_scale_2_octave, 6000, DESCENDING > ASCENDING)
piano.play_arpeggio(g_dominant_altered_chord, 2000)
piano.play_chord(g_dominant_altered_chord)

# ihypy.system
WCS = WesternClassicalSystem()
PS = PtolemaicSystem()

print(WCS.create_note("Csharp4"))
print(PS.create_note("Csharp4"))
print(WCS.create_note("Csharp5"))
print(PS.create_note("Csharp5"))

print(WCS.create_interval("P5"))
print(WCS.create_interval("P5", "A4"))
print(PS.create_interval(PerfectFifth(), "A4"))

# ihypy.theory
major_triad = MajorTriad()
print(major_triad)

# ihypy.instrument
piano = Piano()
piano.play_frequency(440)

trumpet = Trumpet()
trumpet.play_frequency(440)

violin = Violin()
violin.play_frequency(440)

flute = Flute()
flute.play_frequency(440)