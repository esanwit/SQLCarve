#
#  See ../LICENSE
#
# This file is used in low level access to some datatypes, most importantly MyISAM fields.
#
#


import struct
import datetime as dt
import math

from scanner_shared import FieldImpossibleException


def data_sizecheck(data, idx, needed):
    if len(data) < (idx + needed):
        raise FieldImpossibleException("Out of data") 


MYSQL_DATETIME_PACKED_OFFSET = 0x8000000000L
def date(data, idx, options={}):
    val, new_idx = mediumint(data, idx)
    day =    val & 0x00001f       # 0b000000000000000000011111
    month = (val & 0x0001e0) >> 5 # 0b000000000000000111100000
    year =  (val & 0xfffe00) >> 9 # 0b111111111111111000000000
    return dt.date(year, month, day), new_idx

def datetime(data, idx, options={}):
    '''
    8 byte format is LONG. with date in numerical format
    YYYYMMDDhhmmss
    '''
    new_idx = year = month = day = hour = minute = second = 0
    if options.get('packed'):
        data_sizecheck(data,idx, 5)
        tmpdata = data[idx:idx+5]
        new_idx = idx + 5
        tmpdata = tmpdata + "\x00\x00\x00" 
        nr = struct.unpack_from('>Q',tmpdata, 0)[0]
        ymdhms = (nr >> 24) - MYSQL_DATETIME_PACKED_OFFSET
        ymd = ymdhms >> 17
        ym = ymd >> 5
        hms = ymdhms % (1 << 17)
        
        day = ymd % (1<<5)
        month =  ym % 13
        year = ym / 13 
        second = hms % (1 << 6)
        minute = (hms >> 6) % ( 1 << 6)
        hour = (hms >> 12)
    else:
        val, new_idx = bigint(data, idx, {'unsigned': True})
        if val <= 69*10000000000+1231235959:
            val += 20000000000000
        if val < 991231235959:
            val += 19000000000000 
        
        date = val / 1000000
        time = val - date * 1000000
        year = date / 10000; date %= 10000
        month = date / 100; 
        day = date % 100
        
        hour = time / 10000; time %= 10000
        minute = time / 100; 
        second = time % 100
    return dt.datetime(year, month, day, hour, minute, second), new_idx

def time(data, idx, options={}):
    #TODO: Fix negative days...
    val, idx = mediumint(data, idx)
    days = hours = minutes = seconds = 0
    if options.get('packed'):
        days = val / 1000000
        val %= 1000000
        hours = val / 10000
        val %= 10000
        minutes = val / 100
        seconds = val %100
    else:
        days = val / (24 * 3600)
        val %= 24 * 3600
        hours = val / 3600
        val %= 3600
        minutes = val / 60
        seconds = val % 60
    return dt.timedelta(days, hours=hours, minutes=minutes, seconds=seconds), idx

def timestamp(data, idx, options={}):
    time_since_epoch, new_idx = int(data, idx)
    time = dt.datetime.fromtimestamp(time_since_epoch)
    return time, new_idx

def year(data, idx, options={}):
    val, idx = tinyint(data, idx, {'unsigned':True})
    return val + 1900, idx

#FLOATING POINTS
def float(data, idx, options={}):
    try:
        outdata = struct.unpack_from('<f', data, idx)
    except struct.error as xx:
        raise FieldImpossibleException(xx)
    return outdata[0], idx+4

def double(data, idx, options={}):
    try:
        outdata = struct.unpack_from('<d', data, idx)
    except struct.error as xx:
        raise FieldImpossibleException(xx)
    return outdata[0], idx+8

def real(data, idx, options={}):
    '''
    Validate ANSI setting.
    '''
    if options.get('ansi'):
        val, new_idx = float(data, idx)
    else:
        val, new_idx = double(data, idx)
    return val, new_idx

def decimal(data, idx, options={}):
    '''
    TODO validate for negative numbers.
    We may have to ^ -1 all parts..
    '''
    if not ('scale' in options and 'precision' in options):
        raise AttributeError('Decimal requires precision, scale arguments.')
    precision = options.get('precision')
    scale = options.get('scale')
    precision -= scale
    
    #Determine number of bytes
    integer_bytes = (precision / 9)
    integer_remainder = [0,1,1,2,2,3,3,4,4,4][precision % 9]
    decimal_bytes = (scale / 9)
    decimal_remainder = [0,1,1,2,2,3,3,4,4,4][scale % 9]
    integer_format='>%dB%dI' %(integer_remainder, integer_bytes)
    decimal_format='>%dB%dI' %(decimal_remainder, decimal_bytes)
    
    #Determine idx for future use.
    idx2 = idx + struct.calcsize(integer_format)
    new_idx = idx2 + struct.calcsize(decimal_format)

    if new_idx > len(data):
        raise FieldImpossibleException("Out of data")

    #Get parts.
    integer_parts = list(struct.unpack_from(integer_format, data, idx))
    decimal_parts = list(struct.unpack_from(decimal_format, data, idx2))
    
    #Check if positive/negative
    output = ""
    if not options.get('unsigned'):
        #Check left most flag bit.
        if ord(data[idx]) & 0x80:
            invmask = [0x7F,0x7FFFFFFF][integer_remainder==0]
            integer_parts[0] = integer_parts[0] & invmask
        else:
            output = "-"
    
    if integer_remainder:
        #Determine remainder as integer value.
        tmp = integer_parts[:integer_remainder]
        integer_parts = integer_parts[integer_remainder:]
        tmp.reverse()
        part1 = 0
        for pos, byte in enumerate(tmp):
            part1 |= byte << (pos*8)
        output += str(part1)
        
    # Add all other parts to the output
    if integer_parts:
        for part in integer_parts:
            output += str(part)
    
    if decimal_parts:
        output += '.'
        if decimal_remainder:
            tmp = decimal_parts[:decimal_remainder]
            decimal_parts = decimal_parts[decimal_remainder:]
            tmp.reverse()
            part1 = 0
            for pos, byte in enumerate(tmp):
                part1 |= byte << (pos*8)
            output += str(part1)
        for part in decimal_parts:
            output += str(part)
        
    return output, new_idx

# INTEGERS
def tinyint(data, idx, options={}):
    data_sizecheck(data, idx, 1)
    format = '<b'
    if options.get('unsigned'):
        format = '<B'
    outdata = struct.unpack_from(format, data, idx)
    return outdata[0], idx+1

def smallint(data, idx, options={}):
    data_sizecheck(data, idx, 2)
    format = '<h'
    if options.get('unsigned'):
        format = '<H'
    outdata = struct.unpack_from(format, data, idx)
    return outdata[0], idx+2

def mediumint(data, idx, options={}):
    data_sizecheck(data, idx, 3)
    tmpdata = data[idx:idx+3]
    tmpdata = tmpdata + "\x00"
    format = '<i'
    if options.get('unsigned'):
        format = '<I'
    outdata = struct.unpack_from(format, tmpdata)
    return outdata[0], idx+3

def int(data, idx, options={}):
    data_sizecheck(data, idx, 4)
    format = '<i'
    if options.get('unsigned'):
        format = '<I'
    outdata = struct.unpack_from(format, data, idx)
    return outdata[0], idx+4

def bigint(data, idx, options={}):
    data_sizecheck(data, idx, 8)
    format = '<q'
    if options.get('unsigned'):
        format = '<Q'
    outdata = struct.unpack_from(format, data, idx)
    return outdata[0], idx +8

def numeric(data, idx, options={}):
    return decimal(data, idx, options)

def bit(data, idx, options={}):
    '''
    TODO validate byte order
    '''
    size = options.get('length')
    bytes = (size + 7)/8
    data_sizecheck(data, idx, bytes)
    if bytes > 8:
        raise ValueError('BIT field exceeds maximum allowed size')
    parts = list(struct.unpack_from('>%dB' % bytes, data, idx))
    parts.reverse()
    val = 0
    for pos, byte in enumerate(parts):
        val |= byte << (pos*8)

    import __builtin__
    max = __builtin__.int("0b"+ "".join(map(lambda x: "1", range(size))), 2)
    if val > max:
        raise ValueError("BIT value %d > %d" % (val,max))

    return bin(val), idx + bytes


# ENUM and SET
def enum(data, idx, options={}):
    import math
    options = options.get('options')
    if not options:
        raise AttributeError('Options must contain at least one value')
    l = len(options)
    bytes_to_read = math.ceil(math.log(l,2) / 8)

    data_sizecheck(data, idx, bytes_to_read)

    val, new_idx = tinyint(data, idx, {'unsigned': True})
    if bytes_to_read == 2:
        val, new_idx = smallint(data, idx, {'unsigned': True})
    # ENUM only support upto 2^16 options max.
    #if bytes_to_read == 3:
    #    val, new_idx = mediumint(data, idx)
    #if bytes_to_read == 4:
    #    val, new_idx = int(data, idx)
    if not 1 <= val <= l:
        raise ValueError('Index out of options range')
    return options[val-1], new_idx

def set(data, idx, options={}):
    options = options.get('options')
    if not options:
        raise AttributeError('Options must contain at least one value')
    copy = list(options)
    # get bit list (returned as string 0bXYZ)
    val, idx = bit(data, idx, {'length': len(copy)})
    outdata = []
    for v in val[2:]:
        item = copy.pop()
        if v == '1':
            outdata.append(item)
    return ",".join(outdata), idx

# (VAR)CHARs
def char(data, idx, options={}):
    if 'length' not in options:
        raise AttributeError('Options must contain length attribute')
    length = options.get('length')
    data_sizecheck(data, idx, length)
    outdata = struct.unpack_from('<%ds' % length, data, idx)
    return outdata[0], idx + length

def varchar(data, idx, options={}):
    if 'length' not in options:
        raise AttributeError('Options must contain length attribute')
    set_length = ord(data[idx])
    if options['length'] > 255:
        set_length = smallint(data, idx, {'unsigned':True})
        idx +=1
    idx +=1
        
    if set_length > options['length']:
        raise ValueError('Retrieved length is invalid.')
    data_sizecheck(data, idx, set_length)
    outdata = struct.unpack_from('<%ds' % set_length, data, idx)
    return outdata[0], idx + set_length

# BLOBS   
def tinyblob(data, idx, options={}):
    length, idx = tinyint(data,idx, {'unsigned': True})
    data_sizecheck(data, idx, length)
    outdata = data[idx:idx+length]
    return outdata, idx+length

def blob(data, idx, options={}):
    length, idx = smallint(data,idx, {'unsigned': True})
    data_sizecheck(data, idx, length)
    outdata = data[idx:idx+length]
    return outdata, idx+length

def mediumblob(data, idx, options={}):
    length, idx = mediumint(data,idx, {'unsigned': True})
    data_sizecheck(data, idx, length)
    outdata = data[idx:idx+length]
    return outdata, idx+length

def longblob(data, idx, options={}):
    length, idx = int(data,idx, {'unsigned': True})
    data_sizecheck(data, idx, length)
    outdata = data[idx:idx+length]
    return outdata, idx+length

# TEXT
def tinytext(data, idx, options={}):
    outdata, idx = tinyblob(data, idx)
    outdata = unicode(outdata,options.get('encoding'))
    return outdata, idx

def text(data, idx, options={}):
    outdata, idx = blob(data, idx)
    outdata = unicode(outdata,options.get('encoding'))
    return outdata, idx

def mediumtext(data, idx, options={}):
    outdata, idx = mediumblob(data, idx)
    outdata = unicode(outdata,options.get('encoding'))
    return outdata, idx

def longtext(data, idx, options={}):
    outdata, idx = longblob(data, idx)
    outdata = unicode(outdata,options.get('encoding'))
    return outdata, idx


if __name__ == '__main__':
    fp = open('myisam_all.MYD', 'rb')
    buf = buffer(fp.read())
    buf_options = {'length':3}
    data, new_idx = char(buf,0x288,buf_options)
    print data, hex(new_idx)
    data, new_idx = date(buf,new_idx)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = datetime(buf,new_idx,{'packed':False})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = time(buf,new_idx,{'packed':True})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = timestamp(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = year(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = float(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = double(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = real(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = decimal(buf,new_idx,{'scale':0, 'precision': 10})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = numeric(buf,new_idx,{'scale':0, 'precision': 10})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options) #20
    print data, hex(new_idx)
    #Bit not present probably stored in header.!?
    #data, new_idx = bit(buf,new_idx,{'length':1})
    #print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    #Bit not present probably stored in header.!?
    #data, new_idx = bit(buf,new_idx,{'length':5})
    #print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    
    #BIT present but only 8 bits.. not 10...
    print data, hex(new_idx)
    data, new_idx = bit(buf,new_idx,{'length':8})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    
    #INTEGERS
    data, new_idx = tinyint(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = smallint(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = mediumint(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = int(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = bigint(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options) 
    print data, hex(new_idx)
    
    #ENUM and SETS
    data, new_idx = enum(buf,new_idx,{'options':['small','medium','large']})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = set(buf,new_idx,{'options':['red','green','blue']})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options) #40
    print data, hex(new_idx)
    
    #(VAR)CHARS and text
    # in dynamic table char is stored as varchar...
    data, new_idx = varchar(buf,new_idx,{'length':20})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = varchar(buf,new_idx,{'length':20})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = tinytext(buf,new_idx,{'encoding':'latin1'})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = text(buf,new_idx,{'encoding':'latin1'})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = mediumtext(buf,new_idx,{'encoding':'latin1'})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = longtext(buf,new_idx,{'encoding':'latin1'})
    print data, hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options) #52
    print data, hex(new_idx)
    
    # BLOBS
    import base64
    data, new_idx = tinyblob(buf,new_idx)
    print base64.b64encode(data), hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = blob(buf,new_idx)
    print base64.b64encode(data), hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = mediumblob(buf,new_idx)
    print base64.b64encode(data), hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options)
    print data, hex(new_idx)
    data, new_idx = longblob(buf,new_idx)
    print base64.b64encode(data), hex(new_idx)
    data, new_idx = char(buf,new_idx,buf_options) #60
    print data, hex(new_idx)
    
