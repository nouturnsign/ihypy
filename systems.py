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

class TwelveToneEqualTemperament(TuningSystem):
    """A 12 tone equal temperament tuning system, standard for pianos."""

    def __init__(self):
        self.__r = 2 ** (1 / 12)
        pass

    def __str__(self):
        return "EqualTemperament"

    def get_frequency_ratio(self, delta_half_step: int) -> float:
        """Get the frequency ratio based on the number of half_steps between two notes. This is the ratio between the after and before pitch.

        Parameters
        ----------
        delta_half_step : int
            The integer number of half_steps going from a pitch to another. A negative value indicates going down to the note.

        Returns
        -------
        float
            The ratio of frequencies.
        """
        return self.__r ** delta_half_step

class FiveLimitTuning(TuningSystem):
    """Just intonation, with 5-limit tuning."""

    def __init__(self):
        self.__interval_ratio = [1, 25/24, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
        self.__octave_ratio = 2
        pass

    def __str__(self):
        return "FiveLimitTuning"

    def get_frequency_ratio(self, delta_half_step: int) -> float:
        """Get the frequency ratio based on the number of half_steps between two notes. This is the ratio between the after and before pitch.

        Parameters
        ----------
        delta_half_step : int
            The integer number of half_steps going from a pitch to another. A negative value indicates going down to the note.

        Returns
        -------
        float
            The ratio of frequencies.
        """
        ascending = 1 if delta_half_step >= 0 else -1
        octave, interval = divmod(abs(delta_half_step), 12)
        return (self.__octave_ratio ** octave * self.__interval_ratio[interval]) ** ascending

class NotationSystem(abc.ABC):
    """Abstract class for notation systems.

    Attributes
    ----------
    valid_notation_pattern : re.Pattern
        The regular expression to fully match a musical object's notation.

    Methods
    -------
    validate_notation(notation: str) -> bool
        Check whether a certain notation is valid, based on the valid_notation_pattern.
    """

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass

    @property
    def valid_notation_pattern(self) -> re.Pattern:
        return self._valid_notation_pattern

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
        return re.fullmatch(self.valid_notation_pattern, notation) is not None

class NoteNotationSystem(NotationSystem):
    """Abstract class for notation systems of musical notes.

    Methods
    -------
    get_interval_between(self, from_notation: str, to_notation: str) -> Interval
        Get the interval between two notes based on their notations.
    """

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
        return "International Pitch Notation"

    def __get_absolute_half_step(self, notation):
        # get the absolute number of half_steps, with 0 half_steps defined as C0.

        _, start_accidental_index = re.search(self.__pitch, notation).span()
        end_accidental_index, _ = re.search(self.__octave, notation).span()
        
        pitch = notation[ : start_accidental_index]
        accidental = notation[start_accidental_index : end_accidental_index]
        octave = notation[end_accidental_index : ]

        return int(octave) * 12 + self.__pitch_conversion[pitch] + self.__accidental_conversion[accidental]

    def get_interval_between(self, from_notation: str, to_notation: str) -> SemitoneInterval:
        """Get the interval, in half_steps, between two pitches based on their notations.

        Parameters
        ----------
        from_notation : str
            The notation used to represent the starting note.
        to_notation : str
            The notation used to represent the ending note.

        Returns
        -------
        SemitoneInterval
            An interval with the number of half_steps. A negative number indicates going down.

        Raises
        ------
        NotationError
            If either of the notations are invalid.
        """
        if not self.validate_notation(from_notation):
            raise NotationError(from_notation, self)
        if not self.validate_notation(to_notation):
            raise NotationError(to_notation, self)
        return SemitoneInterval(self.__get_absolute_half_step(to_notation) - self.__get_absolute_half_step(from_notation))

class IntervalNotationSystem(NotationSystem):
    """Abstract class for notation systems of musical intervals.

    Methods
    -------
    get_interval : Interval
        Get the interval from an interval's notation.
    """
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_interval(self, notation: str) -> Interval:
        pass

class QualityNumberSystem(IntervalNotationSystem):
    """Interval notation using quality and number for the chromatic scale."""

    def __init__(self):

        # define interval notation
        self.__quality_conversion_perfect = {"diminished": -1, "perfect": 0, "augmented": 1}
        self.__quality_conversion_perfect_abbrev = {"d": -1, "P": 0, "A": 1}
        self.__quality_conversion_imperfect = {"diminished": -1.5, "minor": -0.5, "major": 0.5, "augmented": 1.5}
        self.__quality_conversion_imperfect_abbrev = {"d": -1.5, "m": -0.5, "M": 0.5, "A": 1.5}

        self.__number_conversion_perfect = {"unison": 0, "fourth": 5, "fifth": 7, "octave": 12}
        self.__number_conversion_perfect_abbrev = {"1": 0, "4": 5, "5": 7, "8": 12}
        self.__number_conversion_imperfect = {"second": 1.5, "third": 3.5, "sixth": 8.5, "seventh": 10.5}
        self.__number_conversion_imperfect_abbrev = {"2": 1.5, "3": 3.5, "6": 8.5, "7": 10.5}
        
        self.__alternative  = {"semitone": 1, "half tone": 1, "half step": 1,
                               "tone": 1, "whole tone": 1, "whole step": 1,
                               "trisemitone": 3,
                               "tritone": 6}

        self.__quality_number_conversion = {}

        # full
        for quality_perfect, semitone_modification in self.__quality_conversion_perfect.items():
            for number_perfect, semitone_guess in self.__number_conversion_perfect.items():
                quality = quality_perfect + " " + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number
                self.__quality_number_conversion[quality.title()] = number
        for quality_perfect, semitone_modification in self.__quality_conversion_imperfect.items():
            for number_perfect, semitone_guess in self.__number_conversion_imperfect.items():
                quality = quality_perfect + " " + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number
                self.__quality_number_conversion[quality.title()] = number

        # abbreviated
        for quality_perfect, semitone_modification in self.__quality_conversion_perfect_abbrev.items():
            for number_perfect, semitone_guess in self.__number_conversion_perfect_abbrev.items():
                quality = quality_perfect + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number
        for quality_perfect, semitone_modification in self.__quality_conversion_imperfect_abbrev.items():
            for number_perfect, semitone_guess in self.__number_conversion_imperfect_abbrev.items():
                quality = quality_perfect + number_perfect
                number = semitone_guess + semitone_modification
                self.__quality_number_conversion[quality] = number

        # other
        for quality, number in self.__alternative.items():
            self.__quality_number_conversion[quality] = number
            self.__quality_number_conversion[quality.title()] = number

        self._valid_notation_pattern = re.compile("(" + "|".join(self.__quality_number_conversion.keys()) + ")")

    def __str__(self):
        return "Quality Number Notation"

    def get_interval(self, notation: str) -> SemitoneInterval:
        """Get the interval described by quality number notation in semitones.
        
        Parameters
        ----------
        notation: str
            The interval's notation. Abbreviations and common names acceptable.
        
        Returns
        -------
        SemitoneInterval
            The interval.

        Raises
        ------
        NotationError
            If the interval notation is invalid.
        """
        if not self.validate_notation(notation):
            raise NotationError(notation, self)
        return SemitoneInterval(self.__quality_number_conversion[notation])

class MusicalSystem(abc.ABC):
    """Abstract class for musical systems, containing a notation system, tuning system, and pitch standard.

    Attributes
    ----------
    note_notation_system : NoteNotationSystem
        The notation system to use for notes.
    interval_notation_system : IntervalNotationSystem
        The interval notation system to use for intervals.
    tuning_system : TuningSystem
        The tuning system to use.
    pitch_standard : tuple[str, int | float]
        The pitch tuned to an absolute frequency.
    valid_chord_pattern : re.Pattern
        The regular expression to fully match a chord's notation.
    
    Methods
    -------
    create_note(notation: str) -> Note
        Create a note with the given notation based on the musical system's notation_system and tuning_system.
    create_scale(scale: Scale, notation: str) -> list[Note]
        Create a list of notes starting from the given notation based on the scale increments and musical system's notation_system and tuning_system.
    create_interval(interval: SemitoneInterval | str, note: Note | str = None) -> list[list[Note]] | SemitoneInterval
        Create a specific interval or generic SemitoneInterval.
    create_chord(chord: SemitoneChord | str, note: Note | str = None) -> list[list[Note]] | SemitoneChord
        Create a specific chord or generic SemitoneChord. The original root of the chord will be ignored if note is None. If the root of the chord and note do not match, the chord will be transposed to note.
    """
    
    @abc.abstractmethod
    def __init__(self):
        pass

    @property
    def note_notation_system(self) -> NoteNotationSystem:
        return self._note_notation_system

    @property
    def interval_notation_system(self) -> IntervalNotationSystem:
        return self._interval_notation_system

    @property
    def tuning_system(self) -> TuningSystem:
        return self._tuning_system

    @property
    def pitch_standard(self) -> tuple[str, int | float]:
        return (self._pitch_standard_notation, self._pitch_standard_frequency)

    @property
    def valid_chord_pattern(self) -> re.Pattern:
        return self._valid_chord_pattern

    @abc.abstractmethod
    def get_frequency(self, notation):
        # not truly abstract
        if not self.note_notation_system.validate_notation(notation):
            raise NotationError(self.note_notation_system, self.tuning_system)

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
        return Note(self.get_frequency(notation))

    def create_scale(self, scale: Scale, note: Note | str) -> list[Note]:
        """Create a scale based on a starting note's notation and the scale structure.

        Parameters
        ----------
        scale : Scale
            The structure of the scale.
        note : Note | str
            The notation as a string, or the note itself.
    
        Returns
        -------
        list[Note]
            A list of notes.
        """
        if isinstance(note, str):
            note = self.create_note(note)
        scale_instance = [note]
        for delta_unit in scale.increment:
            frequency_ratio = self.tuning_system.get_frequency_ratio(delta_unit)
            prev_note = scale_instance[-1]
            scale_instance.append(Note(prev_note.frequency * frequency_ratio))
        return scale_instance

    def create_interval(self, interval: SemitoneInterval | str, note: Note | str = None) -> list[list[Note]] | SemitoneInterval:
        """Create an interval based on a tonic note's notation and the interval structure.

        Parameters
        ----------
        interval : SemitoneInterval | str
            The structure of the scale. Either a string or SemitoneInterval.
        note : Note | str = None
            The tonic note's notation as a Note or string. If not specified, a generic interval will be returned.
    
        Returns
        -------
        list[list[Note]] | SemitoneInterval
            A list of singletons containing one note, or a SemitoneInterval.
        """
        if isinstance(interval, str):
            interval = self.interval_notation_system.get_interval(interval)
        if note is None:
            return interval

        if isinstance(note, str):
            tonic = self.create_note(note)
        else:
            tonic = note
        
        interval_instance = [[tonic], [Note(tonic.frequency * self.tuning_system.get_frequency_ratio(interval.relation))]]
        return interval_instance

    def create_chord(self, chord: SemitoneChord | str, note: Note | str = None) -> list[list[Note]] | SemitoneChord:
        """Create a chord based on a tonic note's notation and the chord structure.

        Parameters
        ----------
        chord : SemitoneChord | str
            The structure of the chord. Either a string or SemitoneInterval.
        note : Note | str = None
            The tonic note's notation as a Note or string. If not specified, a generic interval will be returned.
    
        Returns
        -------
        list[list[Note]] | SemitoneChord
            A list of singletons containing one note, or a SemitoneChord.
        """
        
        if isinstance(chord, str):
            # TODO: regular expression stuff here
            pass
        if note is None:
            # chord should be an actual SemitoneChord by now
            return chord

        if isinstance(note, str):
            tonic = self.create_note(note)
        else:
            tonic = note

        chord_instance = [[tonic]]
        for interval in chord.intervals:
            chord_instance.append([Note(tonic.frequency * self.tuning_system.get_frequency_ratio(interval.relation))])
        return chord_instance

class WesternClassicalSystem(MusicalSystem):
    """A standard Western classical system, using IPN and 12-TET.
    
    Methods
    -------
    get_frequency(notation: str) -> float
        Get the frequency, tuned by 12-TET, associated with the notation expressed in IPN.
    """

    def __init__(self):
        self._note_notation_system = InternationalPitchNotation()
        self._interval_notation_system = QualityNumberSystem()
        self._tuning_system = TwelveToneEqualTemperament()
        self._pitch_standard_notation = "A4"
        self._pitch_standard_frequency = 440
        # TODO: fix this
        self._valid_chord_pattern = ""

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
        super().get_frequency(notation)
        pitch_standard_notation, pitch_standard_frequency = self.pitch_standard
        delta_half_step = self.note_notation_system.get_interval_between(pitch_standard_notation, notation).relation
        return pitch_standard_frequency * self.tuning_system.get_frequency_ratio(delta_half_step)

class PtolemaicSystem(MusicalSystem):
    """A Ptolemaic sequence, or justly tuned major scale, using IPN and 5-limit tuning.
    
    Methods
    -------
    get_frequency(notation: str) -> float
        Get the frequency, tuned by Ptolemy's intense diatonic scale, associated with the notation expressed in IPN.
    """

    def __init__(self):
        self._note_notation_system = InternationalPitchNotation()
        self._interval_notation_system = QualityNumberSystem()
        self._tuning_system = FiveLimitTuning()
        self._pitch_standard_notation = "A4"
        self._pitch_standard_frequency = 440
        # TODO: fix this
        self._valid_chord_pattern = ""

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
        super().get_frequency(notation)
        pitch_standard_notation, pitch_standard_frequency = self.pitch_standard
        delta_half_step = self.note_notation_system.get_interval_between(pitch_standard_notation, notation).relation
        return pitch_standard_frequency * self.tuning_system.get_frequency_ratio(delta_half_step)

if __name__ == "__main__":
    WCS = WesternClassicalSystem()
    PS = PtolemaicSystem()

    print(WCS.create_note("Csharp4"))
    print(PS.create_note("Csharp4"))
    print(WCS.create_note("Csharp5"))
    print(PS.create_note("Csharp5"))

    print(WCS.create_interval("A4", "P5"))
    print(PS.create_interval("A4", "P5"))