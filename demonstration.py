from theory import *
from systems import *
from instruments import *

WCS = WesternClassicalSystem()
c_minor_scale_1_octave = WCS.create_scale("C3", NaturalMinorScale(octaves = 1))
piano = Piano()

piano.play_scale(c_minor_scale_1_octave, 6000)