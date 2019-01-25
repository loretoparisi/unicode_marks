# -*- coding: utf-8 -*-

import struct
import sys
import unicode_marks as MARKS
from unicodedata import category

MARK_SET = set(unichr(c) for c in range(sys.maxunicode + 1) if category(unichr(c))[0] == 'M')


def unichar_narrow(i):
    try:
        return unichr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')

indian_script_range = range(0x0900, 0x0E00) # doesn't include all indic scripts (eg. Thai)
basic_multilingual_plane = range(0x0000, 0x10000)  
# use the latter if you want to be more thorough and include all indic scripts and non-indic scripts
codepoint_range = indian_script_range

codepoints = []

with open('UnicodeData.txt') as f:
    for line in f:
        data = line.strip().split(';')
        hex_string = data[0]
        name = data[1]
        category = data[2]
        codepoint_number = int(hex_string, base=16)
        if (
            category in ('Mn', 'Mc', 'Me')
            and (
                codepoint_number in codepoint_range
                or name.startswith('VARIATION SELECTOR') # you seemed to want to include these
            )
        ):
            codepoints.append( unichar_narrow(codepoint_number) )

missing = set(codepoints) - set(MARKS.UNICODE_NSM)

ALL_SET =  set( list(MARKS.UNICODE_NSM) + list(MARK_SET) + list(missing) )

print( "NON SPACING MARK %d" % len(MARKS.UNICODE_NSM) )
print( "MARK_SET %d" % len(MARK_SET) )
print( "MISSING SET %d" % len(missing) )
print( "ALL SET %d" % len(ALL_SET) )
print( "ALL SET %d" % len(MARKS.UNICODE_NSM_ALL) )

def count_len(s,my_set):
    return len([c for c in s if c not in my_set])

s=u"अब यहां से कहा जाएँ हम"
l=count_len(s,MARKS.UNICODE_NSM_ALL)
print( u"अब यहां से कहा जाएँ हम len:%d len-mark:%d" % (len(s),l) )

import json
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

with open('data.json', 'w') as outfile:
    json.dump(MARKS.UNICODE_NSM_ALL, outfile, cls=SetEncoder)

