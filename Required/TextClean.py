# -*- coding: utf8 -*-

## Copyright (c) 2011 Astun Technology

## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.

### TextClean.py - Class to clean erroneous characters and html entities from a
### text string before entering it into a database

import re
import unicodedata


class ClassTextClean:

    def __init__(self, Out):

        #Output
        self.out = Out

    def Cleanup(self, text):

        def htmlstrip(m):
                text = m.group(0)
                if text[:1] == "<":
                    return ""
                    if text[:2] == "&#":
                        try:
                            if text[:3] == "&#x":
                                return unichr(int(text[3:-1], 16))
                            else:
                                return unichr(int(text[2:-1]))
                        except ValueError:
                            pass
                elif text[:1] == "&":
                    import htmlentitydefs
                    entity = htmlentitydefs.entitydefs.get(text[1:-1])
                    if entity:
                        if entity[:2] == "&#":
                            try:
                                return unichr(int(entity[2:-1]))
                            except ValueError:
                                pass
                            else:
                                return unicode(entity, "iso-8859-1")
                    return text

        dirty = re.sub("(?s)<[^>]*>|&#?\w+;", htmlstrip, text)
        ctrlstrip = re.compile(r'[\n\r\t\\]')
        dirty = ctrlstrip.sub(' ', dirty)
        dirty = dirty.replace(u"â??", "'")
        encodings = ('cp1252', 'iso8859_15', 'iso8859_14', 'latin_1', 'utf_8','iso8859_2')

        for enc in encodings:
            try:
                clean = dirty.decode(enc)
                break
            except:
                clean = unicodedata.normalize('NFKD', dirty)

        clean = clean.replace("'", "''")
        return clean








