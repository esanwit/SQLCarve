
#
#  See ../LICENSE
#
# This file is a configuration example of a simple InnoDB Compact table
#
#

import config_base
import validators
import field_inno_antelope as inno
import scanner_shared

scanner_settings = config_base.base_config()

def validator_a(entry):
    todo = {
      "name": validators.validate_ascii,
      "email": validators.validate_email_crude,
      "id": validators.validate_int_thing,
    }
    sco = 0.0
    for k,v in todo.items():
        s = v(entry[k])
        print("Sco<%s> %s"%(k,str(s)))
        sco += s
    return sco

structure_inno_a = scanner_shared.RowFormat("Inno simple", [
 { "null": False, "varlen": False, "name": "header", "type": inno.InnoCompactHeader},
 { "null": False, "varlen": False, "name": "id", "type": inno.Int, "signed": True},
 { "null": False, "varlen": False, "name": "TransactionID", "type": inno.InnoTransactionID},
 { "null": False, "varlen": False, "name": "RollPointer", "type": inno.InnoRollPointer},
 { "null": False, "varlen": True, "name": "name", "type": inno.SmallVarchar},
 { "null": True, "varlen": True, "name": "email", "type": inno.SmallVarchar},
 { "null": False, "varlen": False, "name": "gender", "type": inno.SmallEnum,
  "enum_map":True, "enum_mapping": {1:"male", 2:"female"}},
 { "null": False, "varlen": False, "name": "birthdate", "type": inno.Int},#Not the actual type, but the same size
])

scanner_settings["filename"] = '../datafiles/dumps/inno_a.partial.ibd' #A cut from an ibd file
scanner_settings["row_validator"] = validator_a
scanner_settings["accept_score"]  = lambda x: x > 2.5
scanner_settings["row_format"] = [structure_inno_a]
scanner_settings["everybytemode"] = True
