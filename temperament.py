import re

'''
This class represents a deviation from 12-tone equal temperament.
'''
class Temperament():
    note_format = re.compile('([A-G])(#{0,2}|b{0,2})([0-8])$')
    note_to_index = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}
    accidental_to_index = {'':0, '#':1, '##':2, 'b':-1, 'bb':-2}
    standard_C4_freq = 261.6255653005986
    
    '''
    Constructor. Deviations should be floats in cents starting from 'C'
    '''
    def __init__(self, deviations):
        assert isinstance(deviations, list)
        assert len(deviations) == 12
        assert all([type(i) == float for i in deviations])
        self.deviations = deviations

    '''
    Gets the frequency of a standard note name as input based on the
    deviations. Note names must be capitalized, sharps are denoted by
    "#" and flats by "b". Double sharps and flats are simply repeated.
    Examples would be Ab1, C#6, Bbb2, etc. The valid range of pitches
    are A0 - C8
    '''
    def getFrequency(self, note):
        assert type(note) == str
        fields = Temperament.note_format.match(note)
        assert fields != None
        name, accidental, octave = fields.groups()
        
        index = Temperament.note_to_index[name] +\
            Temperament.accidental_to_index[accidental]
        exponent = index / 12
        base_frequency = Temperament.standard_C4_freq * 2**exponent
        base_frequency *= 2**(float(octave) - 4)
        mod_index = (12 + index) % 12
        return base_frequency * 2**(self.deviations[mod_index] / 1200)

