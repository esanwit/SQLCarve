
#
#  See ../LICENSE
#
# This file is a configuration example for an InnoDB table in Redundant row format.
#
#

import config_base
import validators
import field_inno_antelope as inno
import scanner_shared

scanner_settings = config_base.base_config()

import struct
import base64
from scanner_shared import BufferSizeException, FieldImpossibleException, ImplementationException, RecordImpossibleException, Field, Null
import datetime as dt
import mysql
 



def validator_a(entry):
    todo = [
      ("name", validators.validate_ascii_12),
      ("email", validators.make_validator_null(1.0,0.0)),
      ("email", validators.validate_email_crude),
      ("id", validators.make_validator_int_range(1,10000)),
    ]
    sco = 0.0
    for k,v in todo:
        s = v(entry[k])
        print("Sco<%s> %s"%(k,str(s)))
        sco += s
    return sco
 
structure_inno_a = scanner_shared.RowFormat("Inno redundant experimental", [
 {"name": "header", "type": inno.InnoRedundantHeader, "psize": 1}, 

 { "null": False, "varlen": False, "name": "id", "type": inno.Int, "signed": True},
 { "null": False, "varlen": False, "name": "TransactionID", "type": inno.InnoTransactionID},
 { "null": False, "varlen": False, "name": "RollPointer", "type": inno.InnoRollPointer},
 
 { "null": False, "varlen": True, "name": "name", "type": inno.SmallVarchar},
 { "null": True, "varlen": True, "name": "email", "type": inno.SmallVarchar},
 { "null": False, "varlen": False, "name": "gender", "type": inno.SmallEnum,
 
 "enum_map":True, "enum_mapping": {1:"male", 2:"female"}},
 
 { "null": False, "varlen": False, "name": "birthdate", "type": inno.Int},#FIXME
])

scanner_settings["filename"] = '../datafiles/dumps/innor_a.ibd'
scanner_settings["row_validator"] = validator_a
scanner_settings["accept_score"]  = lambda x: x > 2.5
scanner_settings["row_format"] = [structure_inno_a]
scanner_settings["everybytemode"] = True


