
#
#  See ../LICENSE
#
# This file is a configuration example of a MyISAM table with various field types.
#
#
import config_base
import validators
import field_isam as isam
import scanner_shared

scanner_settings = config_base.base_config()

def validator_a(entry):
    todo = {
#     "name": validators.validate_ascii,
#     "email": validators.validate_email_crude,
#     "id": validators.validate_int4_x80,
    }
    sco = 0.0
    for k,v in todo.items():
        s = v(entry[k])
        print("Sco<%s> %s"%(k,str(s)))
        sco += s
    return sco

structure_a = scanner_shared.RowFormat("Isam_ALL", [
 {"name":"ign", "type": scanner_shared.Null}, #HEADER
 {"name":"fixchar_1","type": isam.CharFixed, "char_length": 3},
 {"name":"date","type": isam.Date},
 {"name":"fixchar_2","type": isam.CharFixed, "char_length": 3},
 #{"name":"datetime_nopack","type": isam.DateTime, "is_packed": False},
 {"name":"datetime_nopack","type": isam.DateTime, "is_packed": True},


 {"name":"fixchar_3","type": isam.CharFixed, "char_length": 3},
 {"name":"time_pack","type": isam.Time, "is_packed": True},
 {"name":"fixchar_4","type": isam.CharFixed, "char_length": 3},

 {"name":"timestamp","type": isam.Timestamp},
 {"name":"fixchar_5","type": isam.CharFixed, "char_length": 3},

 {"name":"year","type": isam.Year},
 {"name":"fixchar_6","type": isam.CharFixed, "char_length": 3},

 {"name":"float","type": isam.Float},
 {"name":"fixchar_7","type": isam.CharFixed, "char_length": 3},

 {"name":"double","type": isam.Double},
 {"name":"fixchar_8","type": isam.CharFixed, "char_length": 3},

 {"name":"real","type": isam.Real},
 {"name":"fixchar_9","type": isam.CharFixed, "char_length": 3},

 {"name":"decimal","type": isam.Decimal, 'scale':0, 'precision': 10},
 {"name":"fixchar_a","type": isam.CharFixed, "char_length": 3  },

 {"name":"numeric","type": isam.Numeric, 'scale':0, 'precision': 10},
 {"name":"fixchar_b","type": isam.CharFixed, "char_length": 3  },

 {"name":"fixchar_c","type": isam.CharFixed, "char_length": 3  },


 {"name":"fixchar_d","type": isam.CharFixed, "char_length": 3  },

 {"name":"bit_10","type": isam.Bit,'length':8},
 {"name":"fixchar_e","type": isam.CharFixed, "char_length": 3  },

 {"name":"int_tiny","type": isam.TinyInt},
 {"name":"fixchar_f","type": isam.CharFixed, "char_length": 3  },

 {"name":"int_small","type": isam.SmallInt},
 {"name":"fixchar_g","type": isam.CharFixed, "char_length": 3  },

 {"name":"int_medium","type": isam.MediumInt},
 {"name":"fixchar_h","type": isam.CharFixed, "char_length": 3  },

 {"name":"int_plain","type": isam.Int},
 {"name":"fixchar_i","type": isam.CharFixed, "char_length": 3  },

 {"name":"int_big","type": isam.BigInt},
 {"name":"fixchar_j","type": isam.CharFixed, "char_length": 3  },

 {"name":"enum_sml","type": isam.Enum, "enum_mapping":['small','medium','large']},
 {"name":"fixchar_k","type": isam.CharFixed, "char_length": 3  },

 {"name":"set_rgb","type": isam.Set, "set_mapping":['red','green','blue']},
 {"name":"fixchar_l","type": isam.CharFixed, "char_length": 3  },

 {"name":"varchar_l20_a","type": isam.VarChar, "varchar_length":20},
 {"name":"fixchar_m","type": isam.CharFixed, "char_length": 3  },

 {"name":"varchar_l20_b","type": isam.VarChar, "varchar_length":20},
 {"name":"fixchar_n","type": isam.CharFixed, "char_length": 3  },

 {"name":"tinytext_latin1","type": isam.TinyText, "text_encoding": "latin1"},
 {"name":"fixchar_o","type": isam.CharFixed, "char_length": 3  },

 {"name":"text_latin1","type": isam.Text, "text_encoding": "latin1"},
 {"name":"fixchar_p","type": isam.CharFixed, "char_length": 3  },

 {"name":"mediumtext_latin1","type": isam.MediumText, "text_encoding": "latin1"},
 {"name":"fixchar_r","type": isam.CharFixed, "char_length": 3  },

 {"name":"longtext_latin1","type": isam.LongText, "text_encoding": "latin1"},
 {"name":"fixchar_s","type": isam.CharFixed, "char_length": 3  },

 {"name":"tinyblob","type": isam.TinyBlob},
 {"name":"fixchar_t","type": isam.CharFixed, "char_length": 3  },

 {"name":"blob","type": isam.Blob},
 {"name":"fixchar_u","type": isam.CharFixed, "char_length": 3  },

 {"name":"mediumblob","type": isam.MediumBlob},
 {"name":"fixchar_v","type": isam.CharFixed, "char_length": 3  },

 {"name":"longblob","type": isam.LongBlob},
 {"name":"fixchar_w","type": isam.CharFixed, "char_length": 3  },
])

##Uses the same scheme as isam_a
scanner_settings["filename"] = '../datafiles/dumps/isam_b.MYD'#2 deleted entries, 1 remaining
scanner_settings["row_validator"] = validator_a
scanner_settings["accept_score"]  = lambda x: x > -2.5
scanner_settings["row_format"] = [structure_a]
scanner_settings["everybytemode"] = True
scanner_settings["initial_positions"] = [0x0]
scanner_settings["remember_done"] = False


