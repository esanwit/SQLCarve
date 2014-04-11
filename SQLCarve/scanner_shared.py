
#
#  See ../LICENSE
#
# This file contains a number of shared objects/classes.
#
#

class ParserException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class FieldImpossibleException(ParserException):
    def __init__(self, msg):
        ParserException.__init__(self, msg)

class RecordImpossibleException(ParserException):
    def __init__(self, msg):
        ParserException.__init__(self, msg)


class ValidationImpossibleException(ParserException):
    def __init__(self, msg):
        ParserException.__init__(self, msg)


class ImplementationException(Exception):
    def __init__(self, msg):
        print("Implementation Exception created, expect errors popping up: %s"%msg)
        Exception.__init__(self, msg)

class BufferSizeException(Exception):
    def __init__(self, msg):
        ParserException.__init__(self, msg)


class Field:
    is_null = False
    def __str__(self):
        raise ImplementationException("Unimplemented str %s"%repr(self))

    def get_value(self):
        raise ImplementationException("Unimplemented get value")

    def get_raw_length(self):
        raise ImplementationException("Unimplemented get raw length")

    def get_raw_data(self):
        return self.raw_data


class Null(Field):
    def __init__(self, a=1, b=2, c=3):
        self.is_null = True
        pass
    def get_raw_length(self):
        return 0
    def __str__(self):
        return "NullField"



class RowFormat(tuple):
    def __init__(self, name, *args):
        self.name = name
        print(self)
        tuple.__init__(self, args)

    def __new__(cls, name, ini):
        item = tuple.__new__(cls, ini)
        return item

    def __str__(self):
        return self.name
