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

    Methods
    -------
    transpose(frequency_ratio: int | float) -> Note
        Transpose the note by a certain frequency ratio.
    invert(about: Note) -> Note
        Invert the note about another note.

    Notes
    -----
    Treat Notes as immutable.
    """

    def __init__(self, frequency: int | float):
        self.frequency = frequency

    def __str__(self):
        return "Note{" + str(self.frequency) + " Hz}"

    def __repr__(self):
        return str(self)

    def transpose(self, frequency_ratio: int | float) -> "Note":
        """Tranpose the note by a certain frequency ratio.
        
        Parameters
        ----------
        frequency_ratio: int | float
            The ratio by which to multiply the current note's frequency. This is the frequency ratio between the desired frequency and current frequency.

        Returns
        -------
        Note
            A new note with the transposed frequency.
        """
        return Note(self.frequency * frequency_ratio)

    def invert(self, about: "Note") -> "Note":
        """Invert about a certain note.
        
        Parameters
        ----------
        about: Note
            The note to invert about. 

        Returns
        -------
        Note
            A new note with the inverted frequency.
        """
        # frequency ratio of from about to self
        frequency_ratio = self.frequency / about.frequency
        # 1 / frequency ratio to go in opposite direction from about
        return about.transpose(1 / frequency_ratio)

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
    """Base class for semitone-based scales.
    
    Attributes
    ----------
    octaves: int
        How many octaves the scale spans.
    
    Methods
    -------
    arpeggiate(degrees: list[int] = [1, 3, 5]) -> SemitoneChord
        Return a SemitoneChord that represents the arpeggio.
    """

    def __init__(self, increment: list[float], octaves: int):
        if not isinstance(octaves, int) or octaves < 1:
            raise IntervalLengthError(octaves, "octave")
        # if not sum(increment) == 12:
        #     raise IntervalLengthError(sum(increment), "halfsteps in octave")
        self.octaves = octaves
        self._increment = increment * octaves
        self._unit = "semitones"

    def arpeggiate(self, degrees: list[int] = [1, 3, 5]) -> "SemitoneChord":
        """Convert a semitone scale into an arpeggio.
        
        Parameters
        ----------
        degrees: list[int] = [1, 3, 5]
            Which degrees of the scale to be used in the scale, starting from the first degree of the scale. By default, the 1st, 3rd, and 5th are used.

        Returns
        -------
        SemitoneChord
            A semitone chord consisting of the intervals based on the degrees of the scale.
        """
        intervals = []
        for octave in range(self.octaves):
            for degree in degrees:
                index = degree - 1
                intervals.append(SemitoneInterval(12 * octave + sum(self.increment[:index]))) # could be faster with prefix sum if necessary
        if SemitoneInterval(0) in intervals:
            intervals.remove(SemitoneInterval(0))
            intervals.append(SemitoneInterval(12 * self.octaves))
        return SemitoneChord(intervals)

class IonianScale(SemitoneScale):
    """One of the seven modern modes, commonly referred to as the major scale."""
    def __init__(self, octaves: int = 1):
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

class HarmonicMinorScale(SemitoneScale):
    """A standard Western harmonic minor scale."""
    def __init__(self, octaves : int = 1):
        super().__init__([2, 1, 2, 2, 1, 3, 1], octaves)

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
        if not issubclass(type(other), Interval):
            return False
        return self.relation == other.relation and self.unit == other.unit

class SemitoneInterval(Interval):
    """An interval, in terms of absolute semitones."""

    def __init__(self, semitones: int):
        self._relation = semitones
        self._unit = "semitones"

    def __add__(self, other):
        if not issubclass(other, self.__class__):
            raise TypeError(f"{self} and {other} do not have the same units. Do not add intervals with different units.")
        return SemitoneInterval(self.relation + other.relation)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise IntervalLengthError(other, "semitones")
        return SemitoneInterval(self.relation * other)

    def __rmul__(self, other):
        return self.__mul__(other)

# Minor, major, or perfect intervals
# tritone, and diminished twelfth are defined to complete two octaves

class MinorSecond(SemitoneInterval):
    """A Western minor second."""
    def __init__(self):
        super().__init__(1)

class MajorSecond(SemitoneInterval):
    """A Western major second."""
    def __init__(self):
        super().__init__(2)

class MinorThird(SemitoneInterval):
    """A Western minor third."""
    def __init__(self):
        super().__init__(3)

class MajorThird(SemitoneInterval):
    """A Western major third."""
    def __init__(self):
        super().__init__(4)

class PerfectFourth(SemitoneInterval):
    """A Western perfect fourth."""
    def __init__(self):
        super().__init__(5)

class Tritone(SemitoneInterval):
    """A Western tritone."""
    def __init__(self):
        super().__init__(6)

class PerfectFifth(SemitoneInterval):
    """A Western perfect fifth."""
    def __init__(self):
        super().__init__(7)

class MinorSixth(SemitoneInterval):
    """A Western minor sixth."""
    def __init__(self):
        super().__init__(8)

class MajorSixth(SemitoneInterval):
    """A Western major sixth."""
    def __init__(self):
        super().__init__(9)

class MinorSeventh(SemitoneInterval):
    """A Western minor seventh."""
    def __init__(self):
        super().__init__(10)

class MajorSeventh(SemitoneInterval):
    """A Western major seventh."""
    def __init__(self):
        super().__init__(11)

class PerfectOctave(SemitoneInterval):
    """A Western perfect octave."""
    def __init__(self):
        super().__init__(12)

class MinorNinth(SemitoneInterval):
    """A Western minor ninth."""
    def __init__(self):
        super().__init__(13)

class MajorNinth(SemitoneInterval):
    """A Western major ninth."""
    def __init__(self):
        super().__init__(14)

class MinorTenth(SemitoneInterval):
    """A Western minor tenth."""
    def __init__(self):
        super().__init__(15)

class MajorTenth(SemitoneInterval):
    """A Western major tenth."""
    def __init__(self):
        super().__init__(16)

class PerfectEleventh(SemitoneInterval):
    """A Western perfect eleventh."""
    def __init__(self):
        super().__init__(17)

class DiminishedTwelfth(SemitoneInterval):
    """A Western diminished twelfth, or augmented eleventh."""
    def __init__(self):
        super().__init__(18)

class PerfectTwelfth(SemitoneInterval):
    """A Western perfect twelfth."""
    def __init__(self):
        super().__init__(19)

class MinorThirteenth(SemitoneInterval):
    """A Western minor thirteenth."""
    def __init__(self):
        super().__init__(20)

class MajorThirteenth(SemitoneInterval):
    """A Western major tenth."""
    def __init__(self):
        super().__init__(21)

class MinorFourteenth(SemitoneInterval):
    """A Western minor fourteenth."""
    def __init__(self):
        super().__init__(22)

class MajorFourteenth(SemitoneInterval):
    """A Western major fourteenth."""
    def __init__(self):
        super().__init__(23)

class PerfectFifteenth(SemitoneInterval):
    """A Western perfect fifteenth."""
    def __init__(self):
        super().__init__(24)

# Augmented or diminished intervals and alternative names

AugmentedUnison = Semitone = HalfTone = HalfStep = MinorSecond
DiminishedThird = Tone = WholeTone = WholeStep = MajorSecond
AugmentedSecond = Trisemitone = MinorThird
DiminishedFourth = MajorThird
AugmentedThird = PerfectFourth
DiminishedFifth = AugmentedFourth = Tritone
DiminishedSixth = PerfectFifth
AugmentedFifth = MinorSixth
DiminishedSeventh = MajorSixth
AugmentedSixth = MinorSeventh
DiminishedOctave = MajorSeventh
AugmentedSeventh = DiminishedNinth = PerfectOctave

AugmentedOctave = MinorNinth
DiminishedTenth = MajorNinth
AugmentedNinth =  MinorTenth
DiminishedFourth = MajorTenth
AugmentedThird = PerfectEleventh
AugmentedEleventh = DiminishedTwelfth
DiminishedThirteenth = Tritave = PerfectTwelfth
AugmentedTwelfth = MinorThirteenth
DiminishedFourteenth = MajorThirteenth
AugmentedThirteenth = MinorFourteenth
DiminishedFifteenth = MajorFourteenth
AugmentedFourteenth = DoubleOctave = PerfectFifteenth

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
        if not issubclass(type(other), Chord):
            return False
        return self.intervals == other.intervals

class SemitoneChord(Chord):
    """A chord, in terms of absolute semitones."""

    def __init__(self, intervals):
        self._intervals = intervals

class MinorTriad(SemitoneChord):
    """A minor triad."""

    def __init__(self):
        super().__init__([MinorThird(), PerfectFifth()])

class MajorTriad(SemitoneChord):
    """A major triad."""

    def __init__(self):
        super().__init__([MajorThird(), PerfectFifth()])