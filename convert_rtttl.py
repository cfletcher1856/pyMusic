import re


class RTTTLError(Exception):
    pass


class NoteParseError(Exception):
    pass


def convert(rtttl):
    PACKAGE_BASE_OCTV = 5
    return_notes = []
    regex_rtttl = re.compile("d=([0-9]*),o=([0-9]*),b=([0-9]*):(.*)")
    regex_note = re.compile("(^[0-9]*)([a-gA-GpP]*)([b#]*)([.]*)([0-9]*$)")

    m = regex_rtttl.match(rtttl)
    if m:
        default_dur, default_octv, tempo, notes = m.groups()
    else:
        raise RTTTLError("RTTTL is malformed")

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
                return_notes.append('r')
        else:
            raise NoteParseError("Malformed note: {0}".format(note))

    return (int(tempo), ' '.join(return_notes))
