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

    def __repr__(self):
        return str(self)

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

class LocrianScale(Scale):
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

class Interval(abc.ABC):
    """An abstract class for intervals.
    
    Attributes
    ----------
    relation : int | float
        How the two notes are related. This can be expressed in absolute (e.g. semitones) or relative (e.g. frequency ratio) units.
    unit : str
        The unit for the relation.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @property
    def relation(self):
        return self._relation

    @property
    def unit(self):
        return self._unit

    def __str__(self):
        return "Interval{" + str(self.relation) + " " + self.unit + "}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self == other:
            return True
        if not issubclass(other, Interval):
            return False
        return self.relation == other.relation and self.unit == other.unit

class SemitoneInterval(Interval):
    """An interval, in terms of absolute semitones."""

    def __init__(self, semitones: int):
        self._relation = semitones
        self._unit = "semitones"

    def __add__(self, other):
        # e.g. SemitoneInterval(2) + SemitoneInterval(3) = SemitoneInterval(5)
        # TODO: assert a valid sum
        return SemitoneInterval(self.relation + other.relation)

    def __mul__(self, semitones):
        # e.g. SemitoneInterval(2) * 3 = SemitoneInterval(6)
        # TODO: assert a valid product
        return SemitoneInterval(self.relation * semitones)

    def __rmul__(self, semitones):
        return self.__mul__(semitones)

class Semitone(SemitoneInterval):
    """A Western semitone."""

    def __init__(self):
        super().__init__(1)

class MajorThird(SemitoneInterval):
    """A Western major third."""

    def __init__(self):
        super().__init__(4)

class PerfectFifth(SemitoneInterval):
    """A Western perfect fifth."""

    def __init__(self):
        super().__init__(7)

# TODO: define the intervals under https://en.wikipedia.org/wiki/Interval_(music)#Main_intervals
# TODO: have an instrument be able to play a chord

class Chord(abc.ABC):
    """An abstract class describing a chord.
    
    Attributes
    ----------
    intervals: list[Interval]
        The list of intervals from the tonic. The intervals should be sorted in order of lowest interval to highest interval. Do not include the unison.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @property
    def intervals(self):
        return self._intervals

    def __str__(self):
        return str(self.intervals)

    def __eq__(self, other):
        if self == other:
            return True
        if not issubclass(other, Interval):
            return False
        return self.intervals == other.intervals

class SemitoneChord(Chord):
    """A chord, in terms of absolute semitones."""

    def __init__(self, intervals):
        self._intervals = intervals

class MajorTriad(SemitoneChord):
    """A major triad."""

    def __init__(self):
        super().__init__([MajorThird(), PerfectFifth()])

# TODO: define arpeggios to be consistent with chords
# TODO: define chord dictionary for consistency and interpretation

if __name__ == "__main__":

    major_triad = MajorTriad()
    print(major_triad)