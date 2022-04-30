from theory import *
from systems import *
from instruments import *

WCS = WesternClassicalSystem()
a_major_scale_1_octave = WCS.create_scale("A3", MajorScale(octaves = 1))
piano = Piano()

piano.play_scale(a_major_scale_1_octave, 6000)