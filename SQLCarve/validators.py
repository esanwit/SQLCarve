
#
#  See ../LICENSE
#
# This file contains some of the simple validators, generally usable but not tweaked for any specific table.
#
#

import scanner_shared
def validate_null(st):
    if not st:
        return True
    if st.is_null:
        return True
    return False

def make_validator_null(score_good=1.0, score_bad=0.0):
    def thefun(rc):
        if validate_null(rc):
            return score_bad
        return score_good
    return thefun
 

def validate_ascii_12(st):
    if validate_null(st):
        return 0.0
    try:
        a = st.s.decode('ascii')
        if len(a) == 0:
            return 0.0
        sco = len( filter(lambda x: x.isalnum(), a))/(1.0*len(a))
    except UnicodeDecodeError:
        return 0.0
    return sco
 
def validate_ascii(st):
    if validate_null(st):
        return 0.0
    try:
        a = st.s.decode('ascii')
    except UnicodeDecodeError:
        return 0.0
    return 1.0
 
def validate_int4_x80(it):
    if validate_null(it):
        return 0.0
    if 0x80000000 == (it.get_value() & 0xff000000):
        return 1.0
    return 0.0

def validate_int_thing(it):
   if validate_null(it):
        return 0.0
   try:
       val = it.get_value()
   except scanner_shared.ImplementationException:
       raise scanner_shared.ValidationImpossibleException("Int thing needs value")
   return 1.0


def make_validator_distance(avg, dev, score_good=1.0, score_bad=0.0):
    def thefun(rc):
        if validate_null(rc):
            return score_bad
        try:
            val = rc.get_value()
        except scanner_shared.ImplementationException:
            raise scanner_shared.ValidationImpossibleException("Range needs value")

        score_g = score_good - score_bad
        return score * score_g + score_bad
    return thefun


def make_validator_int_range(mi, ma, score_good=1.0, score_bad=0.0):
    def thefun(rc):
        if validate_null(rc):
            return score_bad
        try:
            val = rc.get_value()
        except scanner_shared.ImplementationException:
            raise scanner_shared.ValidationImpossibleException("Range needs value")
        if val < mi:
            return score_bad
        if val > ma:
            return score_bad
        return score_good
    return thefun


def make_validator_is_in(inwhat, score_good=1.0, score_bad=0.0):
    def thefun(rc):
        if validate_null(rc):
            return score_bad
        try:
            val = rc.get_value()
        except scanner_shared.ImplementationException:
            raise scanner_shared.ValidationImpossibleException("In needs value")
        if val in inwhat:
            return score_good
        return score_bad
    return thefun




def validate_email_crude(st):
    if validate_null(st):
        return 0.0
    if validate_ascii(st) < 0.5:
        return 0.0
    if not "@" in st.s:
        return 0.0

    if st.s.count(".") < 1:
        return 0.0
    return 1.0



