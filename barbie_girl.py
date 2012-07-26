#!/usr/bin/env python

from pyknon.genmidi import Midi
from pyknon.music import NoteSeq
from convert_rtttl import convert

tempo, notes = convert('d=4,o=5,b=125:8g#,8e,8g#,8c#6,a,p,8f#,8d#,8f#,8b,g#,8f#,8e,p,8e,8c#,f#,c#,p,8f#,8e,g#,f# ')

notes1 = NoteSeq(notes)
midi = Midi(1, tempo=tempo)
midi.seq_notes(notes1, track=0)
midi.write("barbie_girl.mid")
