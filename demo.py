from ihypy import *

# ihypy
WCS = system.WesternClassicalSystem()
piano = instrument.Piano()

print(WCS.create_chord("C"))

c_minor_scale_1_octave = WCS.create_scale(theory.NaturalMinorScale(octaves = 1), "C3")
g_dominant_altered_chord = WCS.create_chord("G7f139/D", "G2")
piano.play_scale(c_minor_scale_1_octave, 6000)
piano.play_arpeggio(g_dominant_altered_chord, 2000)
piano.play_chord(g_dominant_altered_chord)

# ihypy.system
WCS = WesternClassicalSystem()
PS = PtolemaicSystem()

print(WCS.create_note("Csharp4"))
print(PS.create_note("Csharp4"))
print(WCS.create_note("Csharp5"))
print(PS.create_note("Csharp5"))

print(WCS.create_interval("P5", "A4"))
print(PS.create_interval("P5", "A4"))

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