import abc as _abc
import requests as _requests
import io as _io
from pydub import AudioSegment as _AudioSegment, playback as _playback

from . import theory as _theory

_AUDIO_CLIPS_PATH = "https://github.com/nouturnsign/ihypy/raw/master/instrument_audio_clips/"

ASCENDING = 2
DESCENDING = -1

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
    play_arpeggio(chord: list[list[Note]], duration: int = 10000) -> None
        Play a list of singletons containing notes as an arpeggio for roughly duration number of milliseconds.
    play_chord(chord: list[list[Note]], duration: int = 10000) -> None
        Play a list of singletons containing notes as a chord for roughly duration number of milliseconds.
    play_interval(interval: list[list[Note]], duration: int = 10000) -> None
        Alias of play_chord for intervals.
    """

    @_abc.abstractmethod
    def __init__(self):
        pass

    @property
    def base_sound(self) -> _AudioSegment:
        if "_base_audio_segment" not in vars(self):
            r = _requests.get(_AUDIO_CLIPS_PATH + self._base_sound)
            f = _io.BytesIO(r.content)
            self._base_audio_segment = _AudioSegment.from_file(f)
        return self._base_audio_segment

    @property
    def base_frequency(self) -> float:
        return self._base_frequency

    @_abc.abstractmethod
    def __str__(self):
        pass

    def __get_audio(self, frequency: int | float, duration: int = 1000) -> _AudioSegment:
        new_sample_rate = int(self.base_sound.frame_rate * frequency / self.base_frequency)
        new_sound = self.base_sound._spawn(self.base_sound.raw_data, overrides={'frame_rate': new_sample_rate})
        new_sound = new_sound.set_frame_rate(self.base_sound.frame_rate)
        new_sound = new_sound[:duration]
        remaining = duration - len(new_sound)
        if remaining > 0:
            new_sound += _AudioSegment.silent(remaining)
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
        duration: int = 1000
            The number of milliseconds over which the note should be played.

        Returns
        -------
        None
        """
        self.play_frequency(note.frequency, duration)

    def play_scale(self, scale: list[_theory.Note], duration: int = 10000, direction: int | bool = ASCENDING) -> None:
        """Play the given instance of a scale of notes, generated using the timbre of the instrument.
        
        Parameters
        ----------
        scale: list[Note]
            The list of notes to be played.
        duration: int = 10000
            The number of milliseconds over which the scale should be played.
        direction: int | bool
            Whether to descend, ascend, descend and ascend, or ascend and descend the scale.

        Returns
        -------
        None

        Notes
        -----
        direction takes on the following values: 
            -1: descend
            0 | False: descend, then ascend
            1 | True: ascend, then descend
            2: ascend
        The constants DESCENDING = -1 and ASCENDING = 2 are defined to make this simpler, and this allows for inputs like DESCENDING > ASCENDING to mean "descending, then ascending", and ASCENDING > DESCENDING to mean "ascending, then descending". 
        """

        direction = int(direction)
        if direction == -1: # descend
            directional_scale = scale[::-1]
        elif direction == 0: # descend, then ascend
            directional_scale = scale[::-1] + scale[1:]
        elif direction == 1: # ascend, then descend
            directional_scale = scale + scale[-2::-1]
        elif direction == 2: # ascend
            directional_scale = scale
        else:
            raise ValueError(f"Invalid value for direction: {direction}. Pick -1, 0, 1, or 2.")

        note_duration = duration // len(directional_scale)

        # concatenates audio
        new_sound = sum(self.__get_audio(note.frequency, note_duration) for note in directional_scale)
        _playback.play(new_sound)

    def play_arpeggio(self, chord: list[list[_theory.Note]], duration: int = 10000, direction: int | bool = ASCENDING) -> None:
        """Play the given instance of a chord as an arpeggio, generated using the timbre of the instrument.
        
        Parameters
        ----------
        chord: list[list[Note]]
            The list of singletons containing notes to be played.
        duration: int = 10000
            The number of milliseconds over which the chord should be arpeggiated.
        direction: int | bool = 1
            See play_scale.

        Returns
        -------
        None
        """
        scale = list(voice[0] for voice in chord)
        # pseudo-scale
        self.play_scale(scale, duration, direction)

    def play_chord(self, chord: list[list[_theory.Note]], duration: int = 1000) -> None:
        """Play the given instance of a chord as an arpeggio, generated using the timbre of the instrument.
        
        Parameters
        ----------
        chord: list[list[Note]]
            The list of singletons containing notes to be played.
        duration: int = 1000
            The number of milliseconds over which the chord should be arpeggiated.

        Returns
        -------
        None
        """
        new_sound = self.__get_audio(chord[0][0].frequency, duration)
        # overlays audio
        for i in range(1, len(chord)):
            new_sound *= self.__get_audio(chord[i][0].frequency, duration)
        _playback.play(new_sound)

    def play_interval(self, interval: list[list[_theory.Note]], duration: int = 1000) -> None:
        """Play the given instance of an interval, generated using the timbre of the instrument.
        
        Parameters
        ----------
        interval: list[list[Note]]
            The list of singletons containing notes to be played.
        duration: int = 1000
            The number of milliseconds over which the chord should be arpeggiated.

        Returns
        -------
        None
        """
        self.play_chord(interval, duration)

class Piano(Instrument):
    """A generated piano from an actual middle C.
    
    Notes
    -----
    Audio of middle C taken from https://www.ee.columbia.edu/~dpwe/sounds/instruments/
    """

    def __init__(self):
        self._base_sound = 'piano-C4.wav'
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
        self._base_sound = 'trumpet-C4.wav'
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
        self._base_sound = 'violin-C4.wav'
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
        self._base_sound = 'flute-C4.wav'
        self._base_frequency = 262
    
    def __str__(self):
        return "Flute"

class Ukulele(Instrument):
    """A generated ukulele from an actual A4.
    
    Notes
    -----
    Audio of A4 taken from http://musicweb.ucsd.edu/~terbe/172/
    """

    def __init__(self):
        self._base_sound = 'ukulele-A4.wav'
        self._base_frequency = 432
    
    def __str__(self):
        return "Ukulele"

class Cello(Instrument):
    """A generated cello from an actual C3.
    
    Notes
    -----
    Audio of C3 taken from http://cd.textfiles.com/sbsw/INSTRMNT/
    """

    def __init__(self):
        self._base_sound = 'cello-E2.wav'
        self._base_frequency = 81
    
    def __str__(self):
        return "Cello"

class Triangle(Instrument):
    """A generated triangle from an actual D#6.
    
    Notes
    -----
    Audio of D#6 taken from https://philharmonia.co.uk/resources/sound-samples/
    """

    def __init__(self):
        # TODO: Fix the header after conversion from mp3
        self._base_sound = 'triangle-D#6.wav'
        self._base_frequency = 1224
    
    def __str__(self):
        return "Triangle"