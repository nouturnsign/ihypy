import abc as _abc
from pydub import AudioSegment as _AudioSegment, playback as _playback

from . import theory as _theory

class Instrument(_abc.ABC):
    """Abstract class for instruments.

    Attributes
    ----------
    base_sound: AudioSegment
        The original audio clip of a single note.
    base_frequency: float
        The likely original intended frequency of the note being played in the original audio clip.
    
    Methods
    -------
    play_frequency(frequency: int | float, duration: int = 1000) -> None
        Play a frequency on the instrument for duration number of milliseconds.
    play_note(note: Note, duration: int = 1000) -> None
        Play a note on the instrument for duration number of milliseconds.
    play_scale(scale: list[Note], duration: int = 10000) -> None
        Play a list of notes as a scale for roughly duration number of milliseconds.
    """

    @_abc.abstractmethod
    def __init__(self):
        pass

    @property
    def base_sound(self) -> _AudioSegment:
        return self._base_sound

    @property
    def base_frequency(self) -> float:
        return self._base_frequency

    @_abc.abstractmethod
    def __str__(self):
        pass

    def __get_audio(self, frequency: int | float, duration: int = 1000) -> _AudioSegment:
        new_sample_rate = int(self._base_sound.frame_rate * frequency / self.base_frequency)
        new_sound = self._base_sound._spawn(self._base_sound.raw_data, overrides={'frame_rate': new_sample_rate})
        new_sound = new_sound.set_frame_rate(44100)
        new_sound = new_sound[:duration]
        return new_sound

    def play_frequency(self, frequency: int | float, duration: int = 1000) -> None:
        """Play the given frequency, generated using the timbre of the instrument.
        
        Parameters
        ----------
        frequency: int | float
            The frequency to be played.
        duration: int = 1000
            The whole number of milliseconds to be played.

        Returns
        -------
        None
        """
        new_sound = self.__get_audio(frequency, duration)
        _playback.play(new_sound)

    def play_note(self, note: _theory.Note, duration: int = 1000) -> None:
        """Play the given note, generated using the timbre of the instrument.
        
        Parameters
        ----------
        note: Note
            The note to be played.
        duration: int
            The number of milliseconds over which the note should be played.

        Returns
        -------
        None
        """
        self.play_frequency(note.frequency, duration)

    def play_scale(self, scale: list[_theory.Note], duration: int = 10000) -> None:
        """Play the given instance of a scale of notes, generated using the timbre of the instrument.
        
        Parameters
        ----------
        scale: list[Note]
            The list of notes to be played.
        duration: int
            The number of milliseconds over which the scale should be played.

        Returns
        -------
        None
        """
        note_duration = duration // len(scale)
        new_sound = sum(self.__get_audio(note.frequency, note_duration) for note in scale)
        _playback.play(new_sound)

class Piano(Instrument):
    """A generated piano from an actual middle C.
    
    Notes
    -----
    Audio of middle C taken from https://www.ee.columbia.edu/~dpwe/sounds/instruments/
    """

    def __init__(self):
        self._base_sound = _AudioSegment.from_file('instrument_audio_clips/piano-C4.wav', format="wav")
        self._base_frequency = 262

    def __str__(self):
        return "Piano"

class Trumpet(Instrument):
    """A generated trumpet from an actual middle C.
    
    Notes
    -----
    Audio of middle C taken from https://www.ee.columbia.edu/~dpwe/sounds/instruments/
    """

    def __init__(self):
        self._base_sound = _AudioSegment.from_file('instrument_audio_clips/trumpet-C4.wav', format="wav")
        self._base_frequency = 262

    def __str__(self):
        return "Trumpet"

class Violin(Instrument):
    """A generated violin from an actual middle C.
    
    Notes
    -----
    Audio of middle C taken from https://www.ee.columbia.edu/~dpwe/sounds/instruments/
    """

    def __init__(self):
        self._base_sound = _AudioSegment.from_file('instrument_audio_clips/violin-C4.wav', format="wav")
        self._base_frequency = 262

    def __str__(self):
        return "Violin"

class Flute(Instrument):
    """A generated flute from an actual middle C.
    
    Notes
    -----
    Audio of middle C taken from https://www.ee.columbia.edu/~dpwe/sounds/instruments/
    """

    def __init__(self):
        self._base_sound = _AudioSegment.from_file('instrument_audio_clips/flute-C4.wav', format="wav")
        self._base_frequency = 262
    
    def __str__(self):
        return "Flute"