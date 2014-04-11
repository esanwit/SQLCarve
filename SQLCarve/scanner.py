#!/usr/bin/env python2.7

#
#  See ../LICENSE
#
# This file is the main executable, it accepts commandline arguments and could be used via an import statement.
# Run: python2.7 scanner.py --help
#

from mysql import *
import mysql
import sys
import struct

from scanner_shared import BufferSizeException, FieldImpossibleException, ImplementationException, RecordImpossibleException, ParserException, ValidationImpossibleException, Null, Field

class ScannerTodo:

    def __init__(self):
        self.nr_got = 0
        self.todo = []
        self.li_blacklist = {}
    
    def blacklist(self, pos):
        self.li_blacklist[pos] = True
        if pos in self.todo:
            self.todo.remove(pos)
    
    def add(self, num):
        if self.li_blacklist.get(num, False):
            return
        self.todo.append(num)
    
    def get(self):
        num = self.todo.pop()
        self.nr_got += 1
        return num

class ScannerResults:
    def __init__(self):
        self.nr_found = 0
        self.nr_scored= 0
        self.nr_validation_failed= 0
        self.found_scored = []
        self.found_all = []
        self.row_validator = None
        self.found_callbacks = []
        self.validation_failed = []
        
        self.accept_score = lambda x: True

    def found_validated(self, entry, score):
        if scanner_settings["remember_unvalidated"]:
            self.found_all.append((entry, score))
        if not self.accept_score or self.accept_score(score):
            self.found_scored.append((entry, score))
            self.nr_scored += 1
            for cb in self.found_callbacks:
                cb(entry, score)

    def found(self, entry):
        self.nr_found += 1
        if self.row_validator:
            try:
                score = self.row_validator(entry)
            except ValidationImpossibleException as xx:
                dbg(xx)
                self.validation_failed.append((entry, xx))
                self.nr_validation_failed += 1
                return
        else:
            score = None
        self.found_validated(entry,score)



def dbg(msg):
    if scanner_settings["Debug"]:
        print("Dbg: %s" % msg)
def output(msg):
    if scanner_settings["PrintRecords"]:
        if scanner_settings["PrintFancy"]:
            def gr(x):
                if isinstance(x, Field):
                    return x.get_raw_length()
                return 0
            summ = sum(map(gr, msg.values()))
            print("Entry:\nSize %d(0x%x)\n  %s\n" % (
summ, summ,
"\n  ".join(map(lambda x: "%s: %s"%(str(x[0]), str(x[1])), msg.items())))
)
        else:
            print(msg)


def check_args(args):
    if len(args) < 2 or args[1] == '-h' or args[1] == '--help':
        print("Run as %s config.py [arguments] FILENAME")

        print("-d --d enable,disable debugging")
        print("-s --s enable,disable printint total counts at the end")
        print("-r --d enable,disable output of the found records")
        print("-B --B enable,disable forced byte-by-byte mode (false positives and slow)")
        print("-f --f enable,disable fancy printing")
        print("-d --d enable,disable debugging")
    
    global scanner_settings
    uconfig = __import__(args[1][:-2]) 
    scanner_settings = uconfig.scanner_settings

    for a in args[2:]:
        if "-d" == a:
            scanner_settings["Debug"] = True
            continue
        if "--d" == a:
            scanner_settings["Debug"] = False
            continue

        if "-s" == a:
            scanner_settings["PrintStats"] = True
            continue
        if "--s" == a:
            scanner_settings["PrintStats"] = False
            continue

        if "-r" == a:
            scanner_settings["PrintRecords"] = True
            continue
        if "--r" == a:
            scanner_settings["PrintRecords"] = False
            continue

        if "-B" == a:
            scanner_settings["everybytemode"] = True
            continue
        if "--B" == a:
            scanner_settings["everybytemode"] = False
            continue

        if "-f" == a:
            scanner_settings["PrintFancy"] = True
            continue
        if "--f" == a:
            scanner_settings["PrintFancy"] = False
            continue

        scanner_settings["filename"] = a


def parse_record(buf_data, int_offset, row_format):
    ##Some form of header is parsed, for Isam might be 'discard' fixed size
    ##For Inno this is required to pase the record as correctly as possible, even deleted records have this data
    dbg("Parse record %d(0x%x) Row format %s"%(int_offset,int_offset,str(row_format)  ))

    header = row_format[0]["type"](buf_data, int_offset, row_format)
    result_record = {"Offset": int_offset, "Row_Format": row_format}
    result_record[row_format[0]["name"]] = header
    eaten = header.get_raw_length()


    min_noise = 0
    max_noise = 0
    noise_fld = False
    for int_row_idx, fld in enumerate(row_format[1:]):
        dbg("Field format %d: %s"%(int_row_idx, fld))
        if fld.has_key("min_len") and fld.has_key("max_len"):
            min_noise = fld["min_len"]
            max_noise = fld["max_len"]
            noise_fld = fld
            dbg("Possible noise field of %d,%d"% (min_noise, max_noise))
            continue
        found_field = False
        for skipped_noise in range(min_noise, max_noise+1):
            num = int_offset + skipped_noise + eaten
            dbg("Probing at %d(0x%x)"%(num,num))
            try:
                fnd = None
                if fld.get("null", False):
                    if header["null"][int_row_idx]:
                        fnd = Null()

                if not fnd: #No NULL was found
                    if fld.get("varlen", False): #varlen==length in HEADER, not ...<length>DATA...
                       fnd = fld["type"](buf_data, int_offset + skipped_noise + eaten, header["lengths"][int_row_idx], fld)
                    else:
                       fnd = fld["type"](buf_data, int_offset + skipped_noise + eaten, fld)
                
                if fld.get("validator", False): #Early validate, in order for noise to be detected as 'terminated' 
                    score = fld["validator"](fnd, fld)
                    if score < fld["min_validation"]:
                        #raise ParserException("Validation score too low")    
                        fnd = None #not good enough, discard


                if fnd: #If we have a result (and no exceptions thrown), enter it
                    num = int_offset + skipped_noise + eaten
                    dbg("Result was parsed and validated at %d(0x%x)"%(num,num))
                    if noise_fld:
                        nf = noise_fld["type"](buf_data, int_offset + eaten, skipped_noise, fld)
                        if noise_fld.get("validator", False): 
                            score = noise_fld["validator"](nf, noise_fld)
                            if score < noise_fld["min_validation"]:
                                #raise ParserException("Validation score too low")
                                continue

                        #Record the noise, and move the cursor. If there was noise
                        result_record[noise_fld["name"]] =  nf
                        eaten += skipped_noise

                    result_record[fld["name"]] = fnd
                    eaten += fnd.get_raw_length()
                    #Noise clear
                    min_noise = 0
                    max_noise = 0
                    noise_fld = False
                    found_field = True
                    break
                       
            except ParserException as xx:
                #If we ARE considering noise at this location, pass the exception,
                # without noise, however, raise it up to stop this unparsable row
                dbg("PE:")
                dbg(xx)
                if not skipped_noise < max_noise:
                    raise
                pass

        if noise_fld or not found_field:
            ##Noise not terminated by valid field, abork
            raise RecordImpossibleException("Noise not terminated with valid field or No field found")
    dbg("Record being returned, ate %d(0x%x)"%(eaten,eaten))
    return eaten, result_record       
 
    

    return suggested_rel_offset, record

def main():
    check_args(sys.argv)

    todo = ScannerTodo()
    results = ScannerResults()

    #results.found_callbacks.append(lambda x,y: output(x))
    results.row_validator = scanner_settings["row_validator"]
    results.accept_score = scanner_settings["accept_score"]

    for pos in scanner_settings["initial_positions"]:
       todo.add(pos)
    for pos in scanner_settings["skip_positions"]:
       todo.blacklist(pos)

    datafilename = scanner_settings["filename"]
    dbg("Opening %s" % datafilename)
    datafile = open(datafilename, 'rb')
    data = buffer(datafile.read())
    datafile.close()
    datafile = None

    while True:
        if todo.nr_got % 1000 == 0:
            if scanner_settings["PrintStats"]:
                print("\nFound so far: %d\nValidated %d\nValidations Failed %d\nTried %d" % (
          results.nr_found,
          results.nr_scored,
          results.nr_validation_failed,
          todo.nr_got
          )
        )
     
        try:
            idx = todo.get()
        except IndexError:
            break
        dbg("Scanning %d" %idx)

        if idx > len(data):
            break

        for row_format in scanner_settings["row_format"]:
            try:
                int_n, rec = parse_record(data, idx, row_format)
                results.found(rec)

            except struct.error as xx:
                dbg(xx)
                int_n = 1
            except FieldImpossibleException as xx:
                dbg(xx)
                int_n = 1
            except RecordImpossibleException as xx:
                dbg(xx)
                int_n = 1
            except BufferSizeException as ss:
                dbg(ss)
                continue

                
            if int_n and (int_n > 0) and int_n < len(data):
                if scanner_settings["everybytemode"]:
                    int_n = 1
                todo.add(idx + int_n)

    for a in results.found_scored:
        s = a[1]
        e = a[0]
        print("\nScore: %s" % str(s))
        output(e)

    dbg("Done")

    if scanner_settings["PrintStats"]:
        print("Found: %d\nValidated %d\nValidations Failed %d\nTried %d" % (
          results.nr_found,
          results.nr_scored,
          results.nr_validation_failed,
          todo.nr_got
          )
        )


if __name__ == "__main__":
    main()
