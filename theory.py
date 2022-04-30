import abc

class Note:
    """A musical note, described by its frequency.

    Attributes
    ----------
    frequency : int | float
        The frequency, expressed in Hz.
    """

    def __init__(self, frequency: int | float):
        self.frequency = frequency

    def __str__(self):
        return "Note{" + str(self.frequency) + " Hz}"

# abstract class Piece
# class Scale(Piece)
# class MajorScale(Scale)

class Piece(abc.ABC):
    """Abstract class for collections of notes."""
    
    @abc.abstractmethod
    def __init__(self):
        pass

class Scale(Piece):
    """Base class for scales, sequences of singular notes.
    
    Attributes
    ----------
    increment : list[float]
        The list of increments to get to the period of the scale.
    """

    def __init__(self):
        pass

    @property
    def increment(self):
        return self._increment

class MajorScale(Scale):
    """A standard Western major scale."""

    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [2, 2, 1, 2, 2, 2, 1] * octaves # halfsteps between each note

# class Chord:

#     def __init__(self, note_list):
#         self.note_list = note_list