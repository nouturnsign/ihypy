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

class IonianScale(Scale):
    """One of the seven modern modes, commonly referred to as the major scale."""

    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [2, 2, 1, 2, 2, 2, 1] * octaves # halfsteps between each note

class DorianScale(Scale):
    """One of the seven modern modes."""
    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [2, 1, 2, 2, 2, 1, 2] * octaves # halfsteps between each note

class PhrygianScale(Scale):
    """One of the seven modern modes."""
    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [1, 2, 2, 2, 1, 2, 2] * octaves # halfsteps between each note

class LydianScale(Scale):
    """One of the seven modern modes."""
    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [2, 2, 2, 1, 2, 2, 1] * octaves # halfsteps between each note

class MixolydianScale(Scale):
    """One of the seven modern modes."""
    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [2, 2, 1, 2, 2, 1, 2] * octaves # halfsteps between each note

class AeolianScale(Scale):
    """One of the modern modes, commonly referred to as the natural minor scale."""
    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [2, 1, 2, 2, 1, 2, 2] * octaves # halfsteps between each note

class LocianScale(Scale):
    """One of the seven modern modes."""
    def __init__(self, octaves : int = 1):
        # TODO: assert that there is a valid number of octaves
        self._increment = [1, 2, 2, 1, 2, 2, 2] * octaves # halfsteps between each note

class MajorScale(IonianScale):
    """A standard Western major scale."""

    def __init__(self, octaves : int = 1):
        super().__init__(octaves)

class NaturalMinorScale(AeolianScale):
    """A standard Western natural minor scale."""

    def __init__(self, octaves : int = 1):
        super().__init__(octaves)

class Chord(abc.ABC):
    """An abstract class describing a chord.
    
    Attributes
    ----------
    frequency_ratio: list[float]
        The list of frequency ratios from the tonic.
    """

    def __init__(self):
        pass

    @property
    def frequency_ratio(self):
        return self._frequency_ratio