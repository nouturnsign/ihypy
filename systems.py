# sticking with classical Western notation for now

import abc
import re

from theory import *

class NotationError(Exception):
    """Exception raised for errors in string representations of musical notation.

    Attributes
    ----------
    notation : str
        The faulty musical notation, expressed as a string.
    notation_system : str
        The notation system, expressed as a string.
    """

    def __init__(self, notation: str, notation_system: str):
        self.notation = notation
        self.notation_system = notation_system

    def __str__(self):
        return f"{self.notation} is not a valid musical notation in the {self.notation_system} notation system."

class TuningSystem(abc.ABC):
    """Abstract class for tuning systems."""

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def get_frequency_ratio(self, delta_unit: int | float) -> int | float:
        pass

# TODO: abstract an EqualTemperament class
class TwelveToneEqualTemperament(TuningSystem):
    """A 12 tone equal temperament tuning system, standard for pianos."""

    def __init__(self):
        self.__r = 2 ** (1 / 12)
        pass

    def __str__(self):
        return "EqualTemperament"

    def get_frequency_ratio(self, delta_halfstep: int) -> float:
        """Get the frequency ratio based on the number of halfsteps between two notes. This is the ratio between the after and before pitch.

        Parameters
        ----------
        delta_halfstep : int
            The integer number of halfsteps going from a pitch to another. A negative value indicates going down to the note.

        Returns
        -------
        float
            The ratio of frequencies.
        """
        return self.__r ** delta_halfstep

class FiveLimitTuning(TuningSystem):
    """Just intonation, with 5-limit tuning."""

    def __init__(self):
        self.__interval_ratio = [1, 25/24, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
        self.__octave_ratio = 2
        pass

    def __str__(self):
        return "FiveLimitTuning"

    def get_frequency_ratio(self, delta_halfstep: int) -> float:
        """Get the frequency ratio based on the number of halfsteps between two notes. This is the ratio between the after and before pitch.

        Parameters
        ----------
        delta_halfstep : int
            The integer number of halfsteps going from a pitch to another. A negative value indicates going down to the note.

        Returns
        -------
        float
            The ratio of frequencies.
        """
        ascending = 1 if delta_halfstep >= 0 else -1
        octave, interval = divmod(abs(delta_halfstep), 12)
        return (self.__octave_ratio ** octave * self.__interval_ratio[interval]) ** ascending

class NotationSystem(abc.ABC):
    """Abstract class for notation systems.

    Attributes
    ----------
    valid_notation_pattern : re.Pattern
        The regular expression to fully match a musical object's notation.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @property
    def valid_notation_pattern(self):
        return self._valid_notation_pattern

    @abc.abstractmethod
    def validate_notation(self, notation: str) -> bool:
        pass

class NoteNotationSystem(NotationSystem):
    """Abstract class for notation systems of musical notes.

    Attributes
    ----------
    valid_notation_pattern : re.Pattern
        The regular expression to fully match a note's notation.
    """
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_interval_between(self, from_notation: str, to_notation: str) -> Interval:
        pass

class InternationalPitchNotation(NoteNotationSystem):
    """The international pitch notation, described by pitch name, accidental, and octave number."""
    
    def __init__(self):
        self.__pitch_conversion = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        self.__accidental_conversion = {"𝄫": -2, "bb": -2, "double_flat": -2, "df": -2,
                                 "♭": -1, "b": -1, "flat": -1, "f": -1,
                                 "♮": 0, "": 0, "natural": 0, "n": 0,
                                 "♯": 1, "#": 1, "sharp": 1, "s": 1,
                                 "𝄪": 2, "x": 2, "double_sharp": 2, "ds": 2}
        self.__pitch = "[A-G]"
        self.__accidental = "(" + "|".join(self.__accidental_conversion.keys()) + ")"
        # self.__accidental = "(𝄫|bb|double_flat|df|♭|b|flat|f|♮||natural|n|♯|#|sharp|s|𝄪|x|double_sharp|ds)"
        self.__octave = "[+-]?\d+"
        self._valid_notation_pattern = re.compile(self.__pitch + self.__accidental + self.__octave)

    def __str__(self):
        return "IPN"

    def validate_notation(self, notation: str) -> bool:
        """Check whether the string notation is valid.

        Parameters
        ----------
        notation : str
            The notation used to represent the note.

        Returns
        -------
        bool
            Whether the notation was valid.
        """
        if len(notation) < 2:
            return False
        return re.fullmatch(self._valid_notation_pattern, notation) is not None

    def __get_absolute_halfstep(self, notation):
        # get the absolute number of halfsteps, with 0 halfsteps defined as C0.

        _, start_accidental_index = re.search(self.__pitch, notation).span()
        end_accidental_index, _ = re.search(self.__octave, notation).span()
        
        pitch = notation[ : start_accidental_index]
        accidental = notation[start_accidental_index : end_accidental_index]
        octave = notation[end_accidental_index : ]

        return int(octave) * 12 + self.__pitch_conversion[pitch] + self.__accidental_conversion[accidental]

    def get_interval_between(self, from_notation: str, to_notation: str) -> SemitoneInterval:
        """Get the interval, in halfsteps, between two pitches based on their notations.

        Parameters
        ----------
        from_notation : str
            The notation used to represent the starting note.
        to_notation : str
            The notation used to represent the ending note.

        Returns
        -------
        SemitoneInterval
            An interval with the number of halfsteps. A negative number indicates going down.
        """
        return SemitoneInterval(self.__get_absolute_halfstep(to_notation) - self.__get_absolute_halfstep(from_notation))

class IntervalNotationSystem(NotationSystem):
    """Abstract class for notation systems of musical intervals.

    Attributes
    ----------
    valid_notation_pattern : re.Pattern
        The regular expression to fully match an interval's notation.
    """
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_interval(self, notation: str) -> Interval:
        pass

class NumberQualitySystem(IntervalNotationSystem):
    """Interval notation using number and quality for the chromatic scale."""

    def __init__(self):
        # TODO: set self._valid_notation_pattern
        pass

    # TODO: define how to parse notation for an interval

class MusicalSystem(abc.ABC):
    """Abstract class for musical systems, containing a notation system, tuning system, and pitch standard.

    Attributes
    ----------
    notation_system : NotationSystem
        The notation system to use.
    tuning_system : TuningSystem
        The tuning system to use.
    pitch_standard : tuple[str, int | float]
        The pitch tuned to an absolute frequency.
    
    Methods
    -------
    create_note(notation: str) -> Note
        Create a note with the given notation based on the musical system's notation_system and tuning_system.

    create_scale(notation: str, scale: Scale) -> list[Note]
        Create a list of notes starting from the given notation based on the scale increments and musical system's notation_system and tuning_system.
    """
    
    @abc.abstractmethod
    def __init__(self):
        pass

    @property
    def notation_system(self):
        return self._notation_system

    @property
    def tuning_system(self):
        return self._tuning_system

    @property
    def pitch_standard(self):
        return (self._pitch_standard_notation, self._pitch_standard_frequency)

    @abc.abstractmethod
    def get_frequency(self, notation):
        pass

    def create_note(self, notation: str) -> Note:
        """Create a note based on its notation.

        Parameters
        ----------
        notation : str
            The notation as a string.
    
        Returns
        -------
        Note
            The note, with the associated frequency.
        """
        if not self.notation_system.validate_notation(notation):
            raise NotationError(notation, self.notation_system)
        return Note(self.get_frequency(notation))

    def create_scale(self, notation: str, scale: Scale) -> list[Note]:
        """Create a scale based on a starting note's notation and the scale structure.

        Parameters
        ----------
        notation : str
            The notation as a string.
        scale : Scale
            The structure of the scale.
    
        Returns
        -------
        list[Note]
            A list of notes.
        """
        if not self.notation_system.validate_notation(notation):
            raise NotationError(notation, self.notation_system)
        scale_instance = [self.create_note(notation)]
        for delta_unit in scale.increment:
            frequency_ratio = self.tuning_system.get_frequency_ratio(delta_unit)
            prev_note = scale_instance[-1]
            scale_instance.append(Note(prev_note.frequency * frequency_ratio))
        return scale_instance

class WesternClassicalSystem(MusicalSystem):
    """A standard Western classical system, using IPN and 12-TET.
    
    Methods
    -------
    get_frequency(notation: str) -> float
        Get the frequency, tuned by 12-TET, associated with the notation expressed in IPN.
    """

    def __init__(self):
        self._notation_system = InternationalPitchNotation()
        self._tuning_system = TwelveToneEqualTemperament()
        self._pitch_standard_notation = "A4"
        self._pitch_standard_frequency = 440

    def get_frequency(self, notation: str) -> float:
        """Get the 12-TET frequency of the IPN notation.

        Parameters
        ----------
        notation : str
            The IPN notation as a string.
    
        Returns
        -------
        float
            The frequency, in Hz.
        """
        if not self.notation_system.validate_notation(notation):
            raise NotationError(self.notation_system, self.tuning_system)
        pitch_standard_notation, pitch_standard_frequency = self.pitch_standard
        delta_halfstep = self.notation_system.get_interval_between(pitch_standard_notation, notation).relation
        return pitch_standard_frequency * self.tuning_system.get_frequency_ratio(delta_halfstep)

class PtolemaicSystem(MusicalSystem):
    """A Ptolemaic sequence, or justly tuned major scale, using IPN and 5-limit tuning.
    
    Methods
    -------
    get_frequency(notation: str) -> float
        Get the frequency, tuned by Ptolemy's intense diatonic scale, associated with the notation expressed in IPN.
    """

    def __init__(self):
        self._notation_system = InternationalPitchNotation()
        self._tuning_system = FiveLimitTuning()
        self._pitch_standard_notation = "A4"
        self._pitch_standard_frequency = 440

    def get_frequency(self, notation: str) -> float:
        """Get the 5-limit tuning frequency of the IPN notation.

        Parameters
        ----------
        notation : str
            The IPN notation as a string.
    
        Returns
        -------
        float
            The frequency, in Hz.
        """
        if not self.notation_system.validate_notation(notation):
            raise NotationError(self.notation_system, self.tuning_system)
        pitch_standard_notation, pitch_standard_frequency = self.pitch_standard
        delta_halfstep = self.notation_system.get_interval_between(pitch_standard_notation, notation).relation
        return pitch_standard_frequency * self.tuning_system.get_frequency_ratio(delta_halfstep)

if __name__ == "__main__":
    WCS = WesternClassicalSystem()
    PS = PtolemaicSystem()

    print(WCS.create_note("Csharp4"))
    print(PS.create_note("Csharp4"))
    print(WCS.create_note("Csharp5"))
    print(PS.create_note("Csharp5"))