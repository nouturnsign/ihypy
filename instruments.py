import abc
from pydub import AudioSegment, playback

from .theory import *

class Instrument(abc.ABC):
    """Abstract class for instruments."""

    def __init__(self):
        pass

    @property
    def base_sound(self):
        return self._base_sound

    @property
    def base_frequency(self):
        return self._base_frequency

    @abc.abstractmethod
    def __str__(self):
        pass

    def play_frequency(self, frequency: int | float) -> None:
        """Play the given frequency, generated using the timbre of the instrument.
        
        Parameters
        ----------
        frequency: int | float
            The frequency to be played.

        Returns
        -------
        None
        """
        new_sample_rate = int(self._base_sound.frame_rate * frequency / self.base_frequency)
        hipitch_sound = self._base_sound._spawn(self._base_sound.raw_data, overrides={'frame_rate': new_sample_rate})
        hipitch_sound = hipitch_sound.set_frame_rate(44100)
        playback.play(hipitch_sound)

    def play_note(self, note: Note) -> None:
        """Play the given note, generated using the timbre of the instrument.
        
        Parameters
        ----------
        frequency: int | float
            The frequency to be played.

        Returns
        -------
        None
        """
        self.play_frequency(note.frequency)

class Piano(Instrument):
    """A generated piano from an actual middle C.
    
    Notes
    -----
    Audio of middle C taken from https://www.ee.columbia.edu/~dpwe/sounds/instruments/
    """

    def __init__(self):
        self._base_sound = AudioSegment.from_file('instrument_audio_clips/piano-C4.wav', format="wav")
        self._base_frequency = 261
        super().__init__()

    def __str__(self):
        return "Piano"

if __name__ == "__main__":
    piano = Piano()
    piano.play_frequency(440)
    piano.play_frequency()