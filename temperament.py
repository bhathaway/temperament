import re

class Temperament():
    '''
    This class represents a deviation from 12-tone equal temperament.
    '''
    note_format = re.compile('([A-G])(#{0,2}|b{0,2})([0-8])$')
    note_to_index = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}
    interval_to_semitone_offset =\
        {'m3':3, 'M3':4, 'P4':5, 'P5':7, 'm6':8, 'M6':9}
    interval_to_overtone_match =\
        {'m3':(5,6), 'M3':(4, 5), 'P4':(3, 4), 'P5':(2, 3),
         'm6':(5, 8), 'M6':(3, 5)}
    accidental_to_index = {'':0, '#':1, '##':2, 'b':-1, 'bb':-2}
    standard_C4_freq = 261.6255653005986
    
    def __init__(self, deviations):
        '''
        "deviations" should be a list of floats in cents starting from "C".
        '''
        assert isinstance(deviations, list)
        assert len(deviations) == 12
        assert all([type(i) == float for i in deviations])
        self.deviations = deviations

    def _getC4IndexFromNoteName(self, note):
        assert type(note) == str
        fields = Temperament.note_format.match(note)
        assert fields != None
        name, accidental, octave = fields.groups()
        
        index = Temperament.note_to_index[name] +\
            Temperament.accidental_to_index[accidental]
        return 12*(int(octave) - 4) + index

    def _getFrequencyFromC4Index(self, idx):
        exponent = idx / 12
        base_frequency = Temperament.standard_C4_freq * 2**exponent
        return base_frequency * 2**(self.deviations[idx%12] / 1200)

    def getFrequency(self, note):
        '''
        Gets the frequency of a standard note name as input based on the
        deviations. Note names must be capitalized, sharps are denoted by
        "#" and flats by "b". Double sharps and flats are simply repeated.
        Examples would be Ab1, C#6, Bbb2, etc. The valid range of pitches
        are A0 - C8
        '''
        return self._getFrequencyFromC4Index(self._getC4IndexFromNoteName(note))

    def getBeatFrequency(self, bottom_note, interval):
        '''
        Gets the beat frequency that should be heard when bottom_note is
        played simultaneously with an upper note spaced by "interval".
        In this case only harmonic intervals make sense. So, "interval"
        may be one of m3, M3, P4, P5, m6, or M6.
        '''
        bottom_index = self._getC4IndexFromNoteName(bottom_note)
        top_index = bottom_index +\
          Temperament.interval_to_semitone_offset[interval]
        bottom_f = self._getFrequencyFromC4Index(bottom_index)
        top_f = self._getFrequencyFromC4Index(top_index)
        top_partial, bottom_partial =\
          Temperament.interval_to_overtone_match[interval]
        return top_f*top_partial - bottom_f*bottom_partial

