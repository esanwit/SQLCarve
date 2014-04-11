#
#  See ../LICENSE
#
# This file is used to form a consistent base used by the specific field implementations.
# It was intended to, implementation might differ.
#
#



class Record:
    def __init__(self, henk):
        self.fields = {}
        self.origin = 0 #in file location
        self.raw_length = 0
        self.score = None #validation score

