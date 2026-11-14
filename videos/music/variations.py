"""The Variations ledger: one row per finished part (what was done to the Tune, how long it runs, what was measured).

A part's own row comes from its ``compute.py`` (``load("variation")``); the rows of the parts before it are kept
here, copied from those parts' results when they were finished, so that a part's film does not need another part's
cache."""

LEDGER = [
    {"part": 1, "title": r"on one simulated string: six positions of one bridge", "seconds": 28.65,
     "measure": r"every interval within 0.6 cents of its ratio"},
    {"part": 2, "title": r"on six bottles, tuned by how much water is in them", "seconds": 26.4,
     "measure": r"every bottle within 1 cent of its note"},
    {"part": 3, "title": r"assembled from pure tones: 1, 2, 3, 5, 8 and 16 partials, phrase by phrase", "seconds": 27.95,
     "measure": r"its brightness rises 2.2 times from the first phrase to the last"},
    {"part": 4, "title": r"with no fundamentals, then with no octaves: the notes the ear supplies", "seconds": 27.105,
     "measure": r"the pitch model finds every missing fundamental within a cent"},
    {"part": 5, "title": r"in a bent timbre, in parallel `fifths' that only that timbre makes smooth", "seconds": 27.55,
     "measure": r"the same intervals are 4 times rougher with ordinary partials"},
    {"part": 6, "title": r"with chords, in eight tunings: Pythagorean, meantone and its wolf, Werckmeister, 12, 19, 31 and 53", "seconds": 38.05,
     "measure": r"its chords are from 1 to 31 cents out of tune"},
    {"part": 7, "title": r"for plucked, struck and bowed strings: a guitar, a piano and a violin built from one string", "seconds": 28.8,
     "measure": r"the bowed string's force is a sawtooth to within 0.2 dB"},
    {"part": 8, "title": r"for a flute, a clarinet, a saxophone, a trumpet and a voice: five valves on five columns of air", "seconds": 27.28,
     "measure": r"every wind note within 8 cents of its pitch"},
    {"part": 9, "title": r"for marimba, bells, steelpan and kettledrums: four instruments that had to be tuned against their nature", "seconds": 29.5,
     "measure": r"its marimba's bars have overtones at 4.00 and 10.0 times their notes"},
    {"part": 10, "title": r"in ten notations, and then as none of them says", "seconds": 28.45,
     "measure": r"its page is 168 bits; its sound, \ 127{,}000 times as many"},
    {"part": 11, "title": r"straight, as a waltz, in five, in seven, swung, and with a hemiola", "seconds": 32.01,
     "measure": r"its bars are counted in 4, 3, 5 and 7, and in six two ways"},
    {"part": 12, "title": r"in the seven modes, brightest to darkest, then pentatonic, whole-tone and octatonic", "seconds": 41.2,
     "measure": r"from Lydian to Locrian, 6 notes fall a semitone, one at a time"},
    {"part": 13, "title": r"over block triads, then re-voiced, spread, and with sevenths", "seconds": 30.4,
     "measure": r"re-voiced, the chords' three voices travel 60 semitones over the Tune instead of 372"},
]


def rows_before(part: int) -> list[dict]:
    return [r for r in LEDGER if r["part"] < part]
