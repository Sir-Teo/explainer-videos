"""Lab 10: what a notation keeps: melodies that fit a contour, dots and ties, a tablature chosen by dynamic programming, round trips, bits, and a page read back."""

import math
from fractions import Fraction

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord import score as S
from explainer.music.monochord.partkit import organ_tone
from explainer.music.monochord.score import codes, perform, raster, read, tab, write

TITLE = "Notation, measured: what each way of writing keeps"
GOAL = ("Count the melodies that fit a row of neumes, write any length with dots and ties, let dynamic programming choose a "
        "guitar fingering, send the Tune through MusicXML and MIDI and see what comes back, count its bits against its "
        "sound, and watch a simple reader fail on a tilted page.")
TASKS = [
    "Set CONTOUR to (0, 1, 0, 1, 0, -1), the Tune's first phrase, and NOTES to 6, 8 and 12. How fast does the count grow? What does that say about neumes for a singer with a wide range?",
    "Set OPEN to 3.0, so that an open string costs as much as three frets of travel. Where on the neck does the Tune go now, and how many frets does the hand span?",
    "Set TILTS to end at 0.6 and SPACE to 8 and then 16. Does a finer scan (a bigger SPACE) break at a smaller or a larger tilt? Why?",
]
CONTOUR = (1, 1, -1, -1, 1)     # Problem 1: up, up, down, down, up
NOTES = 7                       # how many notes of a scale the singer may use
LENGTH = Fraction(11, 16)       # a length to write with dots and ties, in whole notes
OPEN = 0.0                      # the cost of playing an open string (Problem 4)
TILTS = np.arange(0.0, 1.21, 0.1)
SPACE = 12                      # pixels between two staff lines in the scan
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()
    tune = S.tune_score(words=True)
    keys = [n.pitch.midi for n in tune.voices[0].notes]

    # 1. neumes (Problem 1): how many melodies have this contour?
    ways = codes._ways(list(CONTOUR), NOTES)
    lab.row(f"melodies on {NOTES} notes with the contour {CONTOUR}", f"{codes.count_contour(list(CONTOUR), NOTES)}  (ways to finish from each first note: {', '.join(str(int(w)) for w in ways[0])})")
    lab.row("one of them, drawn at random", " ".join("CDEFGABcdefgab"[s] for s in codes.with_contour(list(CONTOUR), NOTES, seed)))
    if (CONTOUR, NOTES) == ((1, 1, -1, -1, 1), 7):
        assert codes.count_contour(list(CONTOUR), NOTES) == 1799

    # 2. dots and ties (Problem 2)
    parts = codes.binary_values(LENGTH)
    lab.row(f"{LENGTH} of a whole note, written", " tied to ".join(("a " + codes.value_name(v, d) + " note") for v, d in parts))
    lab.row("a note with 1, 2, 3 dots lasts", ", ".join(str(codes.dotted(k)) for k in (1, 2, 3)) + " times its plain length")
    assert sum(v * codes.dotted(d) for v, d in parts) == LENGTH

    # 3. a tablature by dynamic programming (Problem 4)
    def cost(a, b):
        return tab._cost(a, b) + (OPEN if b[1] == 0 else 0.0)

    f = tab.fingering(keys, cost=cost, first=lambda a: 0.15 * a[1] + (OPEN if a[1] == 0 else 0.0))
    frets = [fr for _, fr in f["positions"]]
    lab.row("tablatures of the whole Tune", f"{tab.count_fingerings(keys):.3g}")
    lab.row("the cheapest, as string/fret (first phrase)", " ".join(f"{'EADGBe'[s]}{fr}" for s, fr in f["positions"][:7]))
    lab.row("frets used", f"{min(frets)} to {max(frets)}; open strings: {frets.count(0)}")
    assert tab.sounded(f["positions"]) == keys

    # 4. round trips: what comes back
    via_xml = read.musicxml(write.musicxml(tune))
    via_midi = read.midi(write.midi(S.Score([S.Voice([S.Note(S.Pitch.parse(n), S.Q) for n in ("Eb4", "G4", "Bb4")])], key=-3)))
    same = all((a.pitch, a.dur, a.lyric) == (b.pitch, b.dur, b.lyric) for a, b in zip(tune.voices[0].events, via_xml.voices[0].events))
    lab.row("the Tune through MusicXML and back", "identical" if same else "changed")
    lab.row("E flat, G, B flat through MIDI and back", ", ".join(n.pitch.name for n in via_midi.voices[0].notes))
    assert same

    # 5. bits
    sizes = codes.sizes(tune)
    d = codes.description_bits(tune)
    seconds = tune.seconds(tune.length)
    audio_bits = seconds * SR * 16
    lab.row("bytes: jianpu, ABC, MIDI, MEI, MusicXML", ", ".join(str(sizes[k]) for k in ("jianpu", "ABC", "MIDI", "MEI", "MusicXML")))
    lab.row("bits the notes need", f"{d['plain_bits']} spelled out; {d['entropy_bits']:.0f} coded by frequency")
    lab.row("the sound of the page, as on a CD", f"{audio_bits / 1e6:.1f} million bits: {audio_bits / d['plain_bits']:,.0f} times the page")
    dv = perform.deviations(perform.expressive(tune))
    lab.row("a performance by four rules strays from the page by", f"up to {dv['largest_ms']:.0f} ms and {dv['db_range']:.1f} dB")

    # 6. a page read back
    notes = [(n.pitch.staff_position(), bool(n.dur < S.H)) for n in tune.voices[0].notes]
    img = raster.page(notes, space=SPACE)
    naive, fixed = [], []
    for a in TILTS:
        t = raster.distort(img, float(a))
        naive.append(raster.accuracy(raster.read_page(t), notes))
        fixed.append(raster.accuracy(raster.read_page(raster.deskew(t)[0]), notes))
    broke = next((float(a) for a, v in zip(TILTS, naive) if v < 0.5), None)
    lab.row("a clean page: notes read", f"{round(42 * naive[0])} of 42")
    lab.row("the reader fails at a tilt of", f"{broke:.1f} degrees" if broke is not None else "not in this range")
    assert naive[0] == 1.0

    # 7. the ear problem (Problem 3): a sharp and its flat neighbour, or the same note twice?
    c4 = 261.6255653005986
    g_sharp, a_flat = c4 * 25 / 16, c4 * 8 / 5
    kinds = rng.integers(0, 2, 6)
    if kinds.min() == kinds.max():
        kinds[0] = 1 - kinds[0]
    tone = lambda hz: Clip(organ_tone(hz, 1.0, partials=6), SR).fade(0.03, 0.1).at_level(-20.0)       # noqa: E731
    pairs = []
    for k in kinds:
        first = float(rng.choice([g_sharp, a_flat]))
        second = (a_flat if first == g_sharp else g_sharp) if k else first
        pairs.append(concat([tone(first), tone(second)], gap=0.15))
    lab.audio = concat(pairs, gap=0.9)
    lab.row("ear problem, the six pairs (listen first)", "; ".join("different" if k else "the same" for k in kinds))
    lab.row("G sharp and A flat in quarter-comma meantone", f"{g_sharp:.1f} and {a_flat:.1f} Hz: {1200 * math.log2(a_flat / g_sharp):.0f} cents apart")

    fig, (p, q) = labs.figure(2)
    p.plot(TILTS, naive, color=labs.RED, lw=1.6, marker="o", ms=3, label="read as scanned")
    p.plot(TILTS, fixed, color=labs.GOLD, lw=1.6, marker="o", ms=3, label="straightened first")
    p.set_title("A toy reader and a tilted page")
    p.set_xlabel("tilt of the page (degrees)")
    p.set_ylabel("fraction of the notes read")
    p.legend()
    names = ["page, spelled out", "jianpu", "ABC", "MIDI", "MEI", "MusicXML", "sound, as on a CD"]
    vals = [d["plain_bits"] / 8, sizes["jianpu"], sizes["ABC"], sizes["MIDI"], sizes["MEI"], sizes["MusicXML"], audio_bits / 8]
    q.barh(range(len(vals)), vals, color=[labs.GOLD] * 6 + [labs.RED])
    q.set_xscale("log")
    q.set_yticks(range(len(vals)))
    q.set_yticklabels(names)
    q.invert_yaxis()
    q.set_title("The Tune, in bytes")
    q.set_xlabel("bytes (each grid line is ten times the last)")
    lab.fig = fig
    lab.note = ("Every notation is a code that keeps some of the music and leaves the rest to a reader who knows the tradition. "
                "Counting makes the bargain visible: neumes fit hundreds of melodies, a staff fits billions of fingerings, a "
                "key number fits two spellings, and a whole page is a hundred-thousandth of its sound.")
    return lab
