
#
#  See ../LICENSE
#
# This file is the main support for recovering MyISAM fields.
#
#
import struct
import base64

from scanner_shared import BufferSizeException, FieldImpossibleException, ImplementationException, RecordImpossibleException, Field

import mysql

class IsamField(Field):
    def get_raw_data(self):
        raise ImplementationException("Isam raw data not implemented")
    def get_value(self):
        return self.d
    def __str__(self):
        return str(self.d)
    def get_raw_length(self):
        return self.raw_len

class IsamStringField(IsamField):
    def get_value(self):
        return self.s
    def __str__(self):
        return self.s

class CharFixed(IsamStringField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        length = dict_cfg.get("char_length")
        data, new_idx = mysql.char(buf_data, int_idx, {"length": length})
        self.s = data
        self.raw_len = new_idx - int_idx

class VarChar(IsamStringField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        length = dict_cfg.get("varchar_length")
        try:
            data, new_idx = mysql.varchar(buf_data, int_idx, {"length": length})
        except ValueError:
            raise FieldImpossibleException("Varchar invalid (length?)")
        self.s = data
        self.raw_len = new_idx - int_idx

class IsamTextField(IsamStringField):
    def __unicode__(self):
        return self.s


class TinyText(IsamTextField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        encoding = dict_cfg.get("text_encoding")
        data, new_idx = mysql.tinytext(buf_data, int_idx, {"encoding": encoding})
        self.s = data
        self.raw_len = new_idx - int_idx

class Text(IsamTextField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        encoding = dict_cfg.get("text_encoding")
        data, new_idx = mysql.text(buf_data, int_idx, {"encoding": encoding})
        self.s = data
        self.raw_len = new_idx - int_idx

class MediumText(IsamTextField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        encoding = dict_cfg.get("text_encoding")
        data, new_idx = mysql.mediumtext(buf_data, int_idx, {"encoding": encoding})
        self.s = data
        self.raw_len = new_idx - int_idx

class LongText(IsamTextField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        encoding = dict_cfg.get("text_encoding")
        data, new_idx = mysql.longtext(buf_data, int_idx, {"encoding": encoding})
        self.s = data
        self.raw_len = new_idx - int_idx

class IsamBlobField(IsamField):
    def __str__(self):
        return base64.b64encode(self.blob)

class TinyBlob(IsamBlobField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.tinyblob(buf_data, int_idx)
        self.blob = data
        self.raw_len = new_idx - int_idx

class SmallBlob(IsamBlobField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.smallblob(buf_data, int_idx)
        self.blob = data
        self.raw_len = new_idx - int_idx

class Blob(IsamBlobField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.blob(buf_data, int_idx)
        self.blob = data
        self.raw_len = new_idx - int_idx

class MediumBlob(IsamBlobField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.mediumblob(buf_data, int_idx)
        self.blob = data
        self.raw_len = new_idx - int_idx

class LongBlob(IsamBlobField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.longblob(buf_data, int_idx)
        self.blob = data
        self.raw_len = new_idx - int_idx



class Date(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            data, new_idx = mysql.date(buf_data, int_idx)
        except ValueError as xx:
            print(xx)
            raise FieldImpossibleException("Date invalid")
        self.d = data
        self.raw_len = new_idx - int_idx

class DateTime(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        ispack = dict_cfg.get("is_packed", False)
        try:
            data, new_idx = mysql.datetime(buf_data, int_idx, {"packed": ispack})
        except ValueError:
            raise FieldImpossibleException("Date invalid")
        self.d = data
        self.raw_len = new_idx - int_idx

class Time(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        ispack = dict_cfg.get("is_packed", False)
        try:
            data, new_idx = mysql.time(buf_data, int_idx, {"packed": ispack})
        except ValueError:
            raise FieldImpossibleException("Date invalid")
        self.d = data
        self.raw_len = new_idx - int_idx

class Timestamp(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            data, new_idx = mysql.timestamp(buf_data, int_idx)
        except ValueError:
            raise FieldImpossibleException("Date invalid")
        self.d = data
        self.raw_len = new_idx - int_idx

class Year(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            data, new_idx = mysql.year(buf_data, int_idx)
        except ValueError:
            raise FieldImpossibleException("Date invalid")
        self.d = data
        self.raw_len = new_idx - int_idx

class Float(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.float(buf_data, int_idx)
        self.d = data
        self.raw_len = new_idx - int_idx


class Double(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.double(buf_data, int_idx)
        self.d = data
        self.raw_len = new_idx - int_idx

class Real(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.real(buf_data, int_idx)
        self.d = data
        self.raw_len = new_idx - int_idx

class Decimal(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.decimal(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx

class Numeric(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.numeric(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx

class Bit(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            data, new_idx = mysql.bit(buf_data, int_idx, dict_cfg)
        except ValueError as xx:
            raise FieldImpossibleException(xx)
        self.d = data
        self.raw_len = new_idx - int_idx

class TinyInt(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.tinyint(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx

class SmallInt(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.smallint(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx

class MediumInt(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.mediumint(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx

class Int(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.int(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx

class BigInt(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.bigint(buf_data, int_idx, dict_cfg)
        self.d = data
        self.raw_len = new_idx - int_idx


class Enum(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        options = dict_cfg["enum_mapping"]
        try:
            data, new_idx = mysql.enum(buf_data, int_idx, {"options": options})
        except ValueError:
            raise FieldImpossibleException("Enum invalid")
        self.d = data
        self.raw_len = new_idx - int_idx

class Set(IsamField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        options = dict_cfg["set_mapping"]
        try:
            data, new_idx = mysql.set(buf_data, int_idx, {"options": options})
        except ValueError as xx:
            raise FieldImpossibleException(xx)
        self.d = data
        self.raw_len = new_idx - int_idx

