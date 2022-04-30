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
# abstract class Scale(Piece)
# class MajorScale(Scale)

# class Chord:

#     def __init__(self, note_list):
#         self.note_list = note_list