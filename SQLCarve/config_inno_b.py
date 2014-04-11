
#
#  See ../LICENSE
#
# This file is a configuration example for an InnoDB Compact table which had multiple NULLable fields.
#
#
import config_base
import validators
import field_inno_antelope as inno
import scanner_shared

structure_inno = scanner_shared.RowFormat("Inno Compact SomeNULL", [
 { "null": False, "varlen": False, "name": "header", "type": inno.InnoCompactHeader},
 { "null": False, "varlen": False, "name": "id", "type": inno.Int, "signed":True},
 { "null": False, "varlen": False, "name": "TransactionID", "type": inno.InnoTransactionID},
 { "null": False, "varlen": False, "name": "RollPointer", "type": inno.InnoRollPointer},
 { "null": False, "varlen": True, "name": "name", "type": inno.SmallVarchar},
 { "null": True, "varlen": True, "name": "last", "type": inno.SmallVarchar},
 { "null": True, "varlen": True, "name": "email", "type": inno.SmallVarchar},
 { "null": False, "varlen": False, "name": "gender", "type": inno.SmallEnum,
  "enum_map":True, "enum_mapping": {1:"male", 2:"female"}},
 { "null": False, "varlen": False, "name": "other", "type": inno.SmallEnum,
  "enum_map":True, "enum_mapping": {1:"male", 2:"female",3:"Wookie",4:"Anon"}},
 { "null": True, "varlen": False, "name": "birthdate", "type": inno.Noise, "max_len":4, "min_len":4},
 {"name":"ignoreme", "type": scanner_shared.Null},
 { "null": True, "varlen": False, "name": "favedate", "type": inno.Noise, "max_len":4, "min_len":4},
 {"name":"ignoreme", "type": scanner_shared.Null},
])

val_id = validators.make_validator_int_range(1,10000)
val_name = validators.validate_ascii

def validator(entry):
    return val_id(entry["id"]) + val_name(entry["name"])


scanner_settings = config_base.base_config()

scanner_settings["filename"] = '../datafiles/dumps/inno_b.ibd'#Some deleted rows, one not deleted
scanner_settings["row_validator"] = validator
scanner_settings["accept_score"]  = lambda x: x > 1.5
scanner_settings["row_format"] = [structure_inno]
scanner_settings["everybytemode"] = True
