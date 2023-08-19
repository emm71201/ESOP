# create the binary class
# Author: Edison Murairi

from itertools import product as itproduct

class BString:

    def __init__(self, input):

        self.string = input
        self.int_repr = int(input, 2)
    
    def __len__(self):

        return len(input)

    def covering(self):
        """ return the cubes that evaluate this binary string to 1 """

        tmplist = [["-", ch] for ch in self.string]

        return ["".join(list(cover)) for cover in itproduct(*tmplist)]
    

