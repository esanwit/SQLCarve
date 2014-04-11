
#
#  See ../LICENSE
#
# This file contains the default configuration settings, not all settings may be used at runtime.
#
#


def base_config():
    conf_base = {}

    conf_base["Debug"] = False
    conf_base["remember_done"] = False
    conf_base["remember_unvalidated"] = False
    conf_base["PrintRecords"] = True
    conf_base["PrintStats"] =True
    conf_base["PrintFancy"] = True
    conf_base["everybytemode"] = False
    conf_base["accept_score"] = None
    conf_base["row_validator"] = None
    conf_base["initial_positions"] = [0]
    conf_base["skip_positions"] = []
    conf_base["easter"] = "Egg"
    return conf_base
