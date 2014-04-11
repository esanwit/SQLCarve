
#
#  See ../LICENSE
#
# This file is the main support for recovery of InnoDB types, both Compact and Redundant.
# The differences there are in the header and layout of the fields.
#
#

import struct
import base64
from scanner_shared import BufferSizeException, FieldImpossibleException, ImplementationException, RecordImpossibleException, Field, Null
import datetime as dt
import mysql


#Used when debugging or developing, slows the matching significantly
def dbg(s):
  return #Disabled to reduce output, FIXME
  print(s)


def raw_to_uint16(raw):
    return raw[0] << 8 + raw[1]
def raw_to_uint24(raw):
    return (raw[0] << 16) + (raw[1] << 8) + raw[2]
def raw_to_uint32(raw):
    return (raw[0] << 24) + (raw[1] << 16) + (raw[2] << 8) + raw[3]

def read_integer(raw, is_signed=True):
    ##Based on mysql mach_read_int_type
    ret = 0xFFFFFFFFFFFFFF00
    i = 1

    if (not is_signed) or (raw[0] & 0x80):
        ret = 0

    if is_signed:
        ret = ret | (0x80 ^ raw[0] )
    else:
        ret = ret | raw[0]
    for b in raw[1:]:
        ret = ret << 8
        ret = ret | b
    return ret


def raw_to_uint64(raw):
    return raw[0] << 56 + raw[1] << 48 + raw[2] << 40 + raw[3] << 32+ \
           raw[4] << 24 + raw[5] << 16 + raw[6] << 8 + raw[7]


class InnoField(Field):
    def get_raw_length(self):
        return self.raw_len
    def __str__(self):
        return self.s

    pass

class Noise(Field):
    def __str__(self):
        return base64.b64encode(self.blob)
    def get_raw_length(self):
        return self.raw_len
    def get_raw_data(self):
        return self.blob
    def __init__(self, buf_data, int_idx, int_len, fld):
        #dbg("Noise:::: %x"%int_len)
        self.blob = struct.unpack_from("<%ds"%int_len, buf_data, int_idx)[0]
        self.raw_len = int_len

class InnoNumber(InnoField):
    def __str__(self):
        return "%d(0x%x)" % (self.value, self.value)
    def get_value(self):
        return self.value
    def get_raw_data(self):
        return self.raw_data

class TinyInt(InnoNumber):
    #8bit
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<1B", buf_data, int_idx)
        self.is_signed = dict_cfg.get("signed",True)
        self.value = read_integer(self.raw_data,self.is_signed)
    def get_raw_length(self):
        return 1

class SmallInt(InnoNumber):
    #16bit
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<2B", buf_data, int_idx)
        self.is_signed = dict_cfg.get("signed",True)
        self.value = read_integer(self.raw_data, self.is_signed )
    def get_raw_length(self):
        return 2

class MediumInt(InnoNumber):
    #24bit
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<3B", buf_data, int_idx)
        self.is_signed = dict_cfg.get("signed",True)
        self.value = read_integer(self.raw_data, self.is_signed )
    def get_raw_length(self):
        return 3

class Int(InnoNumber):
    #32bit
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<4B", buf_data, int_idx)
        self.is_signed = dict_cfg.get("signed",True)
        self.value = read_integer(self.raw_data, self.is_signed )
    def get_raw_length(self):
        return 4

class BigInt(InnoNumber):
    #64bit
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<8B", buf_data, int_idx)
        self.is_signed = dict_cfg.get("signed",True)
        self.value = read_integer(self.raw_data, self.is_signed)
    def get_raw_length(self):
        return 8


class InnoRollPointer(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<7B", buf_data, int_idx)

    def get_raw_length(self):
        return 7#Fixed length pointer
    def __str__(self):
        return ":".join(map(lambda x: "%02x" % x, self.raw_data))

class InnoTransactionID(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.raw_data = struct.unpack_from("<6B", buf_data, int_idx)

    def get_raw_length(self):
        return 6#Fixed length ID
    def __str__(self):
        return ":".join(map(lambda x: "%02x" % x, self.raw_data))

class InnoRedundantHeader(Field):
    def __init__(self, buf_data, int_idx, row_format):
        dbg("Running at %x"%int_idx)
        self.expectedfields = len(row_format) -1
        self.psize = 1
        if row_format[0].get("psize") == 2:
            self.psize = 2
        dbg("Psize %d, Fields %d"%(self.psize, self.expectedfields))

        self.d = {}
        self.d["null"] = []
        self.d["locs"] = []
        self.d["lengths"] = []
        for int_fieldnum in range(self.expectedfields):
            p = int_idx + self.psize * (self.expectedfields - int_fieldnum)
            dbg("FL: %d(%x)" %(p,p))
            fp = struct.unpack_from("<%dB"%self.psize, buf_data, p)
            inull = False
            le = -1
            if self.psize == 1:
                inull = bool(fp[0] & 0x80) #Isnull?
                le = fp[0] & 0b01111111
            if self.psize == 2:
                inull = bool(fp[0] & 0x80) #Isnull?
                le = (fp[0] & 0b01111111) << 8 + fp[1]

            dbg("Le: %d(%x) Inull: %d(%x)"%(le,le,inull,inull))
            self.d["null"].append(inull)
            self.d["locs"].append(le)
        dbg(self.d["locs"])
        pl = self.d["locs"][0]
        for a in self.d["locs"][1:]:
            val = a - pl
            self.d["lengths"].append(val)
            dbg("L pl:%x, a:%x, delt:%d"%(pl, a, val))
            pl = a

        dbg("Lengths: "+ ":".join(map(lambda x:"%x"%x, self.d["lengths"])))
        dbg("Nulls: " + ":".join(map(lambda x:"%s"%x, self.d["null"])))

    def __getitem__(self, key):
        return self.d[key]

    def get_raw_length(self):
        return 6 + self.expectedfields * self.psize #size+recdir
    def __str__(self):
        return "Header redundant 0:%s, l:%s L:%s"%(",".join(map(str,self.d["null"])), ",".join(map(str,self.d["lengths"])), ",".join(map(str,self.d["locs"])))
  
class InnoCompactHeader(InnoField):
    ##WILL TRY TO LOOK BEHIND ITS START (BY DESIGN)
    def __init__(self, buf_data, int_idx, row_format):
        self.raw_data = struct.unpack_from("<5B", buf_data, int_idx)

        self.d = {}
        self.d["null"] = []
        self.d["lengths"] = []
        self.d["nr_varlen"] = 0
        self.d["nr_null"] = 0

        int_nr_nullable = 0
        for fld in row_format:
            if fld.get("varlen", 0) > 0:
                self.d["nr_varlen"] += 1
            if fld.get("null", False):
                int_nr_nullable += 1

        int_nullb = int_nr_nullable/8
        if int_nr_nullable %8:
            int_nullb += 1

        int_eaten = int_nullb
        null_bytes = struct.unpack_from("<%dB"%int_nullb, buf_data, int_idx - int_eaten)
        #dbg(null_bytes)

        allbits = []
        #dbg("Nr null %d"%int_nullb)
        for bt in null_bytes:
            bn = bin(bt)[2:]
            bits = bn[::-1] + "00000000"
            bits = bits[:8]
            #dbg( bits)

            #dbg(bits)
            allbits += bits
        allbits += map(lambda x: 'x', range(len(row_format)))
        #dbg(allbits)

        for fld in row_format:
            thisnull = False
            if fld.get("null", False):
                tb, allbits = allbits[0],allbits[1:]
                thisnull = tb == "1"
            self.d["null"].append(thisnull)

            if thisnull or not fld.get("varlen", False):
                self.d["lengths"].append(0)
                continue

            if fld["varlen"] == 1:
                mval = 127
                int_eaten += 1
                val = struct.unpack_from("<B", buf_data, int_idx - int_eaten)[0]
            if fld["varlen"] == 2:
                mval = 127 << 8
                int_eaten += 2
                val = raw_to_uint16(struct.unpack_from("<2B", buf_data, int_ci))

            if val > mval:
                raise RecordImpossibleException("Length header overflow: %d > %d"%(val,mval))
            self.d["lengths"].append(val)
        self.d["lengths"] = self.d["lengths"][1:]
        self.d["null"] = self.d["null"][1:]


        self.parsed_numbers = ( #Used in __str__)
            self.raw_data[3],
            self.raw_data[4],
            self.raw_data[2] & 0x1,
            (self.raw_data[2] & 0x2)>>1,
            (self.raw_data[2] & 0x4)>>2,
            self.parse_statbits(self.raw_data[2] & 0x1,self.raw_data[2] & 0x2,self.raw_data[2] & 0x4),
            (self.raw_data[2] >> 3) | (self.raw_data[1] << 5),
            self.raw_data[0] & 0xf,
            (self.raw_data[0] >> 4)& 0xf,
            self.indicates_deleted()
        )

    def __getitem__(self, key):
        return self.d[key]

    def get_raw_length(self):
        return 5#Fixed length thing

    def __str__(self):
        return self.parsed()

    def indicates_deleted(self):
        return (self.raw_data[0] & 0x20) > 0

    def parsed(self):
        return """Rel. offset next record: 0x%02x%02x,Status(%d%d%d): %s,Heap number: 0x%x, n_owned: 0x%x, Info: 0x%x, is_deleted: %s""" % self.parsed_numbers

    def relative_offset_nxt(self):
        return (self.raw_data[3] << 8) +self.raw_data[4]

    def parse_statbits(self, a,b,c):
        if a:
            return "RESERVED"
        if b and a:
            return "SUPERNUM"
        if b:
            return "INFINUM"
        if c:
            return "Node pointer"
        return "Conventional"



class SmallEnum(InnoField):
    def __init__(self,buf_data, int_idx, dict_cfg):
        dict_mapping=dict_cfg.get("enum_mapping",None)
        require_map=dict_cfg.get("enum_map",False)

        self.raw_data = struct.unpack_from("<B", buf_data, int_idx)

        self.value_id = self.raw_data[0]

        if isinstance(dict_mapping, dict):
            self.value_mapped = dict_mapping.get(self.value_id, None)
        else:
            try:
                self.value_mapped = dict_mapping[self.value_id - 1]
            except IndexError as xx:
                raise FieldImpossibleException(xx)

        if require_map and self.value_mapped == None:
            raise FieldImpossibleException("Enum not mapped 0x%x %s"%(self.value_id, str(dict_mapping)))

    def get_value(self):
        return self.value_mapped

    def get_raw_length(self):
        return 1 #Small enum, fixed size
    def __str__(self):
        return "%s" % self.value_mapped

class BigEnum(InnoField):
    def __init__(self,buf_data, int_idx, dict_cfg):
        dict_mapping=dict_cfg.get("enum_mapping",None)
        require_map=dict_cfg.get("enum_map",False)

        self.raw_data = struct.unpack_from("<B", buf_data, int_idx)

        self.value_id = raw_to_uint16(self.raw_data)

        if isinstance(dict_mapping, dict):
            self.value_mapped = dict_mapping.get(self.value_id, None)
        else: #__getitem__ or bust
            try:
                self.value_mapped = dict_mapping[self.value_id - 1]
            except IndexError as xx:
                raise FieldImpossibleException(xx)

        if require_map and self.value_mapped == None:
            raise FieldImpossibleException("Enum not mapped")

    def get_value(self):
        return self.value_mapped

    def get_raw_length(self):
        return 2 #Big enum, fixed size
    def __str__(self):
        return "%s" % self.value_mapped

def Enum(buf_data, int_idx, dict_cfg):
    import math
    options = dict_cfg.get('enum_mapping')
    if not options:
        raise AttributeError('Options must contain at least one value')
    l = len(options)
    bytes_to_read = math.ceil(math.log(l,2) / 8)
    if bytes_to_read == 1:
        return SmallEnum(buf_data, int_idx, dict_cfg)
    if bytes_to_read == 2:
        return BiglEnum(buf_data, int_idx, dict_cfg)
    raise AttributeError("Enum size unclear %d"%bytes_to_read)



class InnoString(InnoField):
    def as_raw(self):
        return self.length, slf.raw_data
    def __str__(self):
        return self.s
    def get_raw_length(self):
        return self.length

class CharFixed(InnoString):
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.length = dict_cfg.get("char_length", False)
        if not self.length:
            raise FieldImpossibleException("Length CHAR field invalid")
        self.s = struct.unpack_from("<%ds"%self.length, buf_data, int_idx)[0]
        if not len(self.s) == self.length:
            dbg("ISSUE: %s"%(":".join(struct.unpack_from("<%dB"%self.length, buf_data, int_idx)[0])))
        self.raw_data = struct.unpack_from("<%dB"%self.length, buf_data, int_idx)

class SmallVarchar(InnoString):
    def __init__(self, buf_data, int_idx, length, dict_cfg):
        if length > 127:
            raise FieldImpossibleException("Length %d > 127"%length)
        self.length = length
        self.s = struct.unpack_from("<%ds"%length, buf_data, int_idx)[0]
        self.raw_data = struct.unpack_from("<%dB"%length, buf_data, int_idx)
        #dbg(":".join(map(str, self.raw_data)))

class BigVarchar(InnoString):
    def __init__(self, buf_data, int_idx, length, dict_cfg):
        if length > (256*127):#FIXME check if this is formally correct
            raise FieldImpossibleException("Length %d > 127"%length)
        self.length = length
        self.s = struct.unpack_from("<%ds"%length, buf_data, int_idx)[0]
        self.raw_data = struct.unpack_from("<%dB"%length, buf_data, int_idx)

def VarChar(buf_data, int_idx, dict_cfg):
    le = dict_cfg["varchar_length"]
    if le < 127:
        return SmallVarchar(buf_data, int_idx,le, dict_cfg)
    else:
        return BigVarchar(buf_data, int_idx,le, dict_cfg)


class Decimal(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        data, new_idx = mysql.decimal(buf_data, int_idx, dict_cfg)
        self.d = data
        self.s = str(data)
        self.raw_len = new_idx - int_idx


class Numeric(Decimal):
    pass

class DateTime(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        ispack = dict_cfg.get("is_packed", True)
        try:
            data, new_idx = mysql.datetime(buf_data, int_idx, {"packed": ispack})
        except ValueError:
            raise FieldImpossibleException("Date invalid")
        self.d = data
        self.s = str(data)
        self.raw_len = new_idx - int_idx 


class Date(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        mediumInt = MediumInt(buf_data, int_idx, dict_cfg)
        val = mediumInt.value
        day =    val & 0x00001f       # 0b000000000000000000011111
        month = (val & 0x0001e0) >> 5 # 0b000000000000000111100000
        year =  (val & 0xfffe00) >> 9 # 0b111111111111111000000000
        try:
            self.d = dt.date(year, month, day)
        except ValueError as xx:
            raise FieldImpossibleException(xx)
        self.raw_len = mediumInt.get_raw_length()
        self.s = str(self.d)
 
class Timestamp(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        int = Int(buf_data, int_idx, {"signed": False})
        self.raw_len = int.get_raw_length()
        self.d = dt.datetime.fromtimestamp(int.value)
        self.s = str(self.d)

class Year(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        ti = TinyInt(buf_data, int_idx, {"signed": False})
        self.d = ti.value + 1900
        self.s = str(self.d)
        self.raw_len = ti.get_raw_length()

class InnoFloat(InnoField):
    def __str__(self):
        return str(self.value)

class Float(InnoFloat):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            self.value = struct.unpack_from('f', buf_data, int_idx)[0]
        except struct.error as xx:
            raise FieldImpossibleException(xx)
    def get_raw_length(self):
        return 4

class Double(InnoFloat):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            self.value = struct.unpack_from('d', buf_data, int_idx)[0]
        except struct.error as xx:
            raise FieldImpossibleException(xx)
    def get_raw_length(self):
        return 8

class Real(InnoFloat):
    def __init__(self, buf_data, int_idx, dict_cfg):
        try:
            if dict_cfg.get("ansi", False):
                self.isfloat = True
                self.value = struct.unpack_from('f', buf_data, int_idx)[0]
                self.raw_len = 4
            else:
                self.isfloat = False
                self.value = struct.unpack_from('d', buf_data, int_idx)[0]
                self.raw_len = 8

        except struct.error as xx:
            raise FieldImpossibleException(xx)
 
class Bit(InnoField):
    def get_raw_length(self):
        return self.len_bytes
    def get_raw_data(self):
        return self.raw_data
    def get_value(self):
        return self.num
    def __str__(self):
        return bin(self.num)
    def __init__(self, buf_data, int_idx, dict_cfg):
        self.len_bytes = dict_cfg["length"]/8
        if dict_cfg["length"]%8:
            self.len_bytes += 1
        if self.len_bytes > 8:
            raise FieldImpossibleException("BIT field oversized")
        self.raw_data = struct.unpack_from('>%dB'%self.len_bytes, buf_data, int_idx)
        parts = list(self.raw_data)
        parts.reverse()
        self.num = 0
        for pos, byte in enumerate(parts):
            self.num |= byte << (pos*8)

        rn = list(bin(self.num)[2:])
        rn.reverse()
        rn = "".join(rn)
        br = int("0b%s" % rn, 2)
        self.num = br

        max = int("0b"+ "".join(map(lambda x: "1", range(dict_cfg["length"]))), 2)
        if self.num > max:
            raise FieldImpossibleException("BIT value %d > %d" % (self.num, max))
        self.s = bin(self.num)
 

class Time(InnoField):
    def __init__(self, buf_data, int_idx, dict_cfg):
        mediumInt = MediumInt(buf_data, int_idx, {"signed": True})
        val = mediumInt.value
 
        days = hours = minutes = seconds = 0
        seconds = val % (1 << 6)
        minutes = (val >> 6) % ( 1 << 6)
        hours = (val >> 12) 

        try:
            self.d = dt.timedelta(days, hours=hours, minutes=minutes, seconds=seconds)
        except OverflowError as domain:
            raise FieldImpossibleException(domain)
        self.raw_len = mediumInt.get_raw_length()
        self.s = str(self.d)




class Set(InnoField):
    def __str__(self):
        return "Set:"+",".join(self.values)
    def get_raw_length(self):
        return self.raw_len

    def __init__(self, buf_data, int_idx, dict_cfg):
        options = dict_cfg.get('set_mapping')
        if not options:
            raise AttributeError('Options must contain at least one value')
        copy = list(options)
        # get bit list (returned as string 0bXYZ)
        o = Bit(buf_data, int_idx, {'length': len(copy)})
        self.raw_len = o.get_raw_length()
        val = bin(o.get_value())
        outdata = []
        for v in val[2:]:
            item = copy.pop()
            if v == '1':
                outdata.append(item)
        self.values = outdata



#BLOBS ARE NOT IMPLEMENTED CORRECTLY

def TinyText(*args):
    return Null(args)
def SmallText(*args):
    return Null(args)
def MediumText(*args):
    return Null(args)
def LongText(*args):
    return Null(args)

def Blob(*args):
    return Null(args)
def Text(*args):
    return Null(args)
def TinyBlob(*args):
    return Null(args)
def SmallBlob(*args):
    return Null(args)
def MediumBlob(*args):
    return Null(args)
def LongBlob(*args):
    return Null(args)

