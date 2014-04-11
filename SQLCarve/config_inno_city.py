
#
#  See ../LICENSE
#
# This file is a configuration example for an InnoDB table with cities, with several validators.
#
#
import config_base
import field_inno_antelope as inno
import scanner_shared

import validators
import scanner_shared

import validators


validate_pop = validators.make_validator_int_range(1, 1.0*10001000*1000)
def validate_cc(f):
    if validators.validate_null(f):
        return 0.0
    s = f.s
    
    if all(map(str.isupper, s)):
        return 1.0
    return 0.0 

_validate_ID = validators.make_validator_int_range(1, 10000)
def validate_id(f,n):
    return _validate_ID(f)
 
def validate_city(f):
    s = f.s
    if s.rstrip().count(' ') >  7 :
      return 0.0
    return 1.0

def plain_ascii(f):
    s = f.s.rstrip()
    if len(s) < 1:
        return 0.0
    c = len( filter(lambda x: x.isalnum() or x in " -,", s))/(1.0*len(s))
    return c

def validator(entry):
    score = validate_cc(entry["CountryCode"])
    score += plain_ascii(entry["Name"])
    score += plain_ascii(entry["District"])
    score += validate_pop(entry["Population"])
    return score


scanner_settings = config_base.base_config()
scanner_settings["row_format"] = [
  scanner_shared.RowFormat("Inno City", [
     { "name": "header", "type": inno.InnoCompactHeader},

     { "name": "ID", "type": inno.Int, "signed": True, "validator": validate_id, "min_validation": 0.5},
     { "name": "TransactionID", "type": inno.InnoTransactionID},
     { "name": "RollPointer", "type": inno.InnoRollPointer},

     { "name": "Name", "type": inno.CharFixed, "char_length": 35},
     { "name": "CountryCode", "type": inno.CharFixed, "char_length": 3},
     { "name": "District", "type": inno.CharFixed, "char_length": 20},
     { "name": "Population", "type": inno.Int, "signed":True},
  ])
]

scanner_settings["filename"] = '../datafiles/dumps/inno_city.ibd'
scanner_settings["everybytemode"] = True
scanner_settings["initial_positions"] = [81904]

scanner_settings["row_validator"] = validator
scanner_settings["accept_score"]  = lambda x: x > 3.5
