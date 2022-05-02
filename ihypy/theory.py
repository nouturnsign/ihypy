import abc as _abc

class IntervalLengthError(Exception):
    """Exception raised for errors in lengths of intervals.

    Attributes
    ----------
    value : int | float
        The faulty number associated with the interval.
    interval : str
        The interval, expressed as a string.
    """

    def __init__(self, value: int | float, interval: str):
        self.value = value
        self.interval = interval

    def __str__(self):
        return f"{self.value} is not a valid value for {self.interval} intervals."

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

# TODO: Create musical units

class Piece(_abc.ABC):
    """Abstract class for collections of relationships of notes."""
    
    @_abc.abstractmethod
    def __init__(self):
        pass

class Scale(Piece):
    """Base class for scales, relationships defining sequences of notes.
    
    Attributes
    ----------
    increment : list[float]
        The list of increments to get to the period of the scale.
    units : str
        The unit for the increment.
    """

    @property
    def increment(self) -> list[float]:
        return self._increment

    @property
    def units(self) -> str:
        return self._units

class SemitoneScale(Scale):
    """Base class for semitone-based scales."""

    def __init__(self, increment: list[float], octaves: int):
        if not isinstance(octaves, int) or octaves < 1:
            raise IntervalLengthError(octaves, "octave")
        self._increment = increment * octaves
        self._unit = "semitones"

class IonianScale(SemitoneScale):
    """One of the seven modern modes, commonly referred to as the major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([2, 2, 1, 2, 2, 2, 1], octaves)

class DorianScale(SemitoneScale):
    """One of the seven modern modes, formed by starting and ending on the second degree of a major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([2, 1, 2, 2, 2, 1, 2], octaves)

class PhrygianScale(SemitoneScale):
    """One of the seven modern modes, formed by starting and ending on the third degree of a major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([1, 2, 2, 2, 1, 2, 2], octaves)

class LydianScale(SemitoneScale):
    """One of the seven modern modes, formed by starting and ending on the fourth degree of a major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([2, 2, 2, 1, 2, 2, 1], octaves)

class MixolydianScale(SemitoneScale):
    """One of the seven modern modes, formed by starting and ending on the fifth degree of a major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([2, 2, 1, 2, 2, 1, 2], octaves)

class AeolianScale(SemitoneScale):
    """One of the modern modes, commonly referred to as the natural minor scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([2, 1, 2, 2, 1, 2, 2], octaves)

class LocrianScale(SemitoneScale):
    """One of the seven modern modes, formed by starting and ending on the seventh degree of a major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([1, 2, 2, 1, 2, 2, 2], octaves)

class MajorScale(IonianScale):
    """A standard Western major scale."""
    def __init__(self, octaves : int = 1):
        super().__init__(octaves)

class NaturalMinorScale(AeolianScale):
    """A standard Western natural minor scale."""
    def __init__(self, octaves : int = 1):
        super().__init__(octaves)

class Interval(_abc.ABC):
    """An abstract class for intervals.
    
    Attributes
    ----------
    relation : int | float
        How the two notes are related. This can be expressed in absolute (e.g. semitones) or relative (e.g. frequency ratio) units.
    unit : str
        The unit for the relation.
    """

    @_abc.abstractmethod
    def __init__(self):
        pass

    @property
    def relation(self) -> int | float:
        return self._relation

    @property
    def unit(self) -> str:
        return self._unit

    def __str__(self):
        return "Interval{" + str(self.relation) + " " + self.unit + "}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self == other:
            return True
        if not issubclass(type(other), Interval):
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

class Chord(_abc.ABC):
    """An abstract class describing a chord.
    
    Attributes
    ----------
    intervals: list[Interval]
        The list of intervals from the tonic. The intervals should be sorted in order of lowest interval to highest interval. Do not include the unison.
    """

    @_abc.abstractmethod
    def __init__(self):
        pass

    @property
    def intervals(self) -> list[Interval]:
        return self._intervals

    def __str__(self):
        return str(self.intervals)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self == other:
            return True
        if not issubclass(type(other), Chord):
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