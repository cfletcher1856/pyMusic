#!/usr/bin/env python

import re
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq


class RTTTLError(Exception):
    pass


class NoteParseError(Exception):
    pass


class Generate(object):

    def __init__(self, rtttl):
        self.rtttl = rtttl
        self.song_name, self.tempo, self.notes = self.convert()
        self.create_midi()

    def convert(self):
        PACKAGE_BASE_OCTV = 5
        return_notes = []
        regex_rtttl = re.compile("(\w*)\s*:\s*d=([0-9]*)\s*,\s*o=([0-9]*)\s*,\s*b=([0-9]*)\s*:\s*(.*)")
        regex_note = re.compile("(^[0-9]*)([a-gA-GpP]*)([b#]*)([.]*)([0-9]*$)")

        m = regex_rtttl.match(self.rtttl)
        if m:
            song_name, default_dur, default_octv, tempo, notes = m.groups()
        else:
            raise RTTTLError("RTTTL is malformed: ex: Name:d=4,o=5,b=125:8g#")

        for note in notes.split(','):
            m = regex_note.match(note.strip())

            if m:
                dur, pitch, acc, dots, octv = m.groups()

                if not dur:
                    dur = default_dur

                octv = octv or default_octv

                octv = int(octv)

                if octv > PACKAGE_BASE_OCTV:
                    octv = "'" * (octv - PACKAGE_BASE_OCTV)
                elif octv == PACKAGE_BASE_OCTV:
                    octv = ""
                else:
                    octv = "," * (PACKAGE_BASE_OCTV - octv)

                # In rtttl format p is a pause
                if pitch.lower() != 'p':
                    return_notes.append(pitch + acc + dur + dots + octv)
                else:
                    return_notes.append('r' + dur)
            else:
                raise NoteParseError("Malformed note: {0}".format(note))

        return (song_name.lower().replace(' ', '_'), int(tempo), ' '.join(return_notes))

    def create_midi(self):
        notes_seq = NoteSeq(str(self.notes))
        midi = Midi(1, tempo=self.tempo)
        midi.seq_notes(notes_seq, track=0)
        midi.write('songs/' + str(self.song_name) + '.mid')
