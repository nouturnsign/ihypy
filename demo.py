from ihypy import *

WCS = system.WesternClassicalSystem()
c_minor_scale_1_octave = WCS.create_scale(theory.NaturalMinorScale(octaves = 1), "C3")
piano = instrument.Piano()

piano.play_scale(c_minor_scale_1_octave, 6000)