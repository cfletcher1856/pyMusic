#!/usr/bin/env python

from pyknon.genmidi import Midi
from pyknon.music import NoteSeq
from convert_rtttl import convert

tempo, notes = convert('d=4,o=4,b=125:8c6,8c6,8a#5,8c6,8p,8g5,8p,8g5,8c6,8f6,8e6,8c6,2p,8c6,8c6,8a#5,8c6,8p,8g5,8p,8g5,8c6,8f6,8e6,8c6')

notes1 = NoteSeq(notes)
midi = Midi(1, tempo=tempo)
midi.seq_notes(notes1, track=0)
midi.write("funkytown.mid")
