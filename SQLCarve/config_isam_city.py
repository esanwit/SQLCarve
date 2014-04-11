
#
#  See ../LICENSE
#
# This file is a configuration example for a MyISAM table with cities, considering Deleted and Non deleted as distinct objects.
#
#
import config_base
import field_isam as isam
import field_inno_antelope as inno
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

def validate_isamdel(f, n):
    d = map(ord, f.get_raw_data())
    if d[0] == 0:
        return 1.0
    return 0.0

def validate_isamnotdel(f, n):
    return 1.0 - validate_isamdel(f, n)
 
_validate_ID = validators.make_validator_int_range(1, 10000)
def validate_id(f,n):
    return _validate_ID(f)

def validate_city(f):
    s = f.s
    if s.rstrip().count(' ') >  7 :
      return 0.0
    return 1.0

def validator(entry):
    score = validate_cc(entry["CountryCode"])
    score += validate_city(entry["Name"])
    score += validate_pop(entry["Population"])
    return score


scanner_settings = config_base.base_config()
scanner_settings["row_format"] = [
scanner_shared.RowFormat("Not deleted City", [
   { "name":"ignoreme", "type": scanner_shared.Null}, #HEADER
   { "name": "header", "type": inno.Noise, "min_len": 1, "max_len":1, "validator": validate_isamnotdel, "min_validation": 0.5},

   { "name": "ID", "type": isam.Int, "signed": True, "validator": validate_id, "min_validation": 0.5},

   { "name": "Name", "type": isam.CharFixed, "char_length": 35},
   { "name": "CountryCode", "type": isam.CharFixed, "char_length": 3},
   { "name": "District", "type": isam.CharFixed, "char_length": 20},
   { "name": "Population", "type": isam.Int, "signed":True},
]),
  scanner_shared.RowFormat("Deleted City", [
     { "name":"ignoreme", "type": scanner_shared.Null}, #HEADER
     { "name": "header", "type": inno.Noise, "min_len": 7, "max_len":7, "validator": validate_isamdel, "min_validation": 0.5},
  
     { "name": "ID", "type": scanner_shared.Null},
  
     { "name": "Name", "type": isam.CharFixed, "char_length": 33},
     { "name": "CountryCode", "type": isam.CharFixed, "char_length": 3},
     { "name": "District", "type": isam.CharFixed, "char_length": 20},
     { "name": "Population", "type": isam.Int, "signed":True},
  ]),
 
]

scanner_settings["filename"] = '../datafiles/dumps/isam_city.MYD'
scanner_settings["everybytemode"] = True

scanner_settings["row_validator"] = validator
scanner_settings["accept_score"]  = lambda x: x > 2.9
