
#
#  See ../LICENSE
#
# This file is a configuration example of an InnoDB Compact table with various types of fields.
#
#
import config_base
import validators
import field_inno_antelope as inno
import scanner_shared

scanner_settings = config_base.base_config()

def validate_ch(st):
    if validators.validate_null(st):
        return 0.0
    s = st.s
    if s == "FIL":
        return 1.0
    return 0.0
def validator_row(entry):
    todo = {
      "fixchar_1": validators.make_validator_null(0.0, 1.0),
    }
    sco = 0.0
    for k,v in todo.items():
        s = v(entry[k])
        #print("Sco<%s> %s"%(k,str(s)))
        sco += s
    return sco


structure_a = scanner_shared.RowFormat("Inno_ALL", [
 { "null": False, "varlen": False, "name": "header", "type": inno.InnoCompactHeader},
 { "null": False, "varlen": False, "name": "id", "type": inno.CharFixed, "char_length": 6},
 { "null": False, "varlen": False, "name": "TransactionID", "type": inno.InnoTransactionID},
 { "null": False, "varlen": False, "name": "RollPointer", "type": inno.InnoRollPointer},
 {"null":True,"name":"fixchar_1","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"date","type": inno.Date},
 {"null":True,"name":"fixchar_2","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"datetime_nopack","type": inno.DateTime, "is_packed": True},
 {"null":True,"name":"fixchar_3","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"time_pack","type": inno.Time, "is_packed": True},
 {"null":True,"name":"fixchar_4","type": inno.CharFixed, "char_length": 3},
 {"null":False,"name":"timestamp","type": inno.Timestamp}, ##SIZE ISSUE 1bytes
 {"null":True,"name":"fixchar_5","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"year","type": inno.Year},
 {"null":True,"name":"fixchar_6","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"float","type": inno.Float},
 {"null":True,"name":"fixchar_7","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"double","type": inno.Double},
 {"null":True,"name":"fixchar_8","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"real","type": inno.Real},
 {"null":True,"name":"fixchar_9","type": inno.CharFixed, "char_length": 3},
 {"null":True,"name":"decimal","type": inno.Decimal, 'scale':0, 'precision': 10},
 {"null":True,"name":"fixchar_a","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"numeric","type": inno.Numeric, 'scale':0, 'precision': 10},
 {"null":True,"name":"fixchar_b","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"bit_noisam1","type": inno.Bit,'length':1},
 {"null":True,"name":"fixchar_c","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"bit_noisam1","type": inno.Bit,'length':5},
 {"null":True,"name":"fixchar_d","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"bit_10","type": inno.Bit,'length':10},
 {"null":True,"name":"fixchar_e","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"int_tiny","type": inno.TinyInt},
 {"null":True,"name":"fixchar_f","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"int_small","type": inno.SmallInt},
 {"null":True,"name":"fixchar_g","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"int_medium","type": inno.MediumInt},
 {"null":True,"name":"fixchar_h","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"int_plain","type": inno.Int},
 {"null":True,"name":"fixchar_i","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"int_big","type": inno.BigInt},
 {"null":True,"name":"fixchar_j","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"enum_sml","type": inno.Enum, "enum_mapping":['small','medium','large']},
 {"null":True,"name":"fixchar_k","type": inno.CharFixed, "char_length": 3  },
 {"null":True,"name":"set_rgb","type": inno.Set, "set_mapping":['red','green','blue']},
 {"null":True,"name":"fixchar_l","type": inno.CharFixed, "char_length": 3  },

 {"null":True, "name":"char_l20_a","type": inno.CharFixed, "char_length":20},
 {"null":True, "name":"fixchar_m","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"varchar_l20_b", "varlen":True, "type": inno.SmallVarchar, "varchar_length":20},
 {"null":True, "name":"fixchar_n","type": inno.CharFixed, "char_length": 3  },

 {"null":True, "name":"tinytext_latin1","type": inno.TinyText, "text_encoding": "latin1"},
 {"null":True, "name":"fixchar_o","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"text_latin1","type": inno.Text, "text_encoding": "latin1"},
 {"null":True, "name":"fixchar_p","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"mediumtext_latin1","type": inno.MediumText, "text_encoding": "latin1"},
 {"null":True, "name":"fixchar_r","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"longtext_latin1","type": inno.LongText, "text_encoding": "latin1"},
 {"null":True, "name":"fixchar_s","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"tinyblob","type": inno.TinyBlob},
 {"null":True, "name":"fixchar_t","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"blob","type": inno.Blob},
 {"null":True, "name":"fixchar_u","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"mediumblob","type": inno.MediumBlob},
 {"null":True, "name":"fixchar_v","type": inno.CharFixed, "char_length": 3  },
 {"null":True, "name":"longblob","type": inno.LongBlob},
 {"null":True, "name":"fixchar_w","type": inno.CharFixed, "char_length": 3  },
])


scanner_settings["filename"] = '../datafiles/dumps/inno_c.ibd'
scanner_settings["row_format"] = [structure_a]
scanner_settings["initial_positions"] = [49289]#Start where the data should start, visually determined to speed up scan

scanner_settings["row_validator"] = validator_row
scanner_settings["accept_score"]  = lambda x: x > -0.5

