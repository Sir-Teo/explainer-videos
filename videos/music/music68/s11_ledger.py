from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403
from videos.music.variations import LEDGER


class Ledger(SoundScene):
    def construct(self):
        chapter(self, 10, r"The ledger", r"What was done to the Tune, and what was measured each time?")
        self.pages()
        self.kinds()

    # ------------------------------------------------------------------
    def page(self, rows, head_text, script, marks=""):
        led = variations_ledger(rows, font_size=17, width=13.0)
        if led.height > 6.3:
            led.scale_to_fit_height(6.3)
        led.move_to(DOWN * 0.3)
        head = label(head_text, font_size=22, color=GREY_A).to_edge(UP, buff=0.2)
        with self.voiceover(script) as vo:
            self.play(FadeIn(head), FadeIn(led.head), FadeIn(led[1]))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in led.rows], lag_ratio=0.12), run_time=2.0)
            for m in marks:
                vo.wait_until(m)
        self.wait(0.6)
        self.clear_scene()

    def pages(self):
        v = load("variation")
        rows = [r for r in LEDGER if r["part"] < 68] + [{"part": 68, "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        by = lambda a, b: [r for r in rows if a <= r["part"] <= b]
        self.page(by(1, 11), r"the ledger: \ Parts 1 to 11",
                  "Every Variation added a row to a ledger: what was done to the Tune, how long it lasts, and what was measured. "
                  "Here is the whole ledger, page by page. The first page is physics: one string with every interval within "
                  "a fraction of a cent of its ratio; six bottles; the Tune built from pure tones; fundamentals the ear "
                  "supplies; eight tunings; the instruments family by family; then notation and meter.")
        self.page(by(12, 22), r"Parts 12 to 22",
                  "Then the theory: modes from brightest to darkest; chords that move sixty semitones instead of three hundred "
                  "and seventy-two once re-voiced; a melody model's surprise; a key finder right on fourteen phrases of fourteen; "
                  "species counterpoint, a chorale corrected to no parallel fifths, basses, chromatic chords, a canon, a sonata "
                  "and a reduction.")
        self.page(by(23, 33), r"Parts 23 to 33",
                  "A thousand years in five Variations, each measured by its technique: an isorhythm whose color and talea meet "
                  "after twenty-eight notes, a point of imitation, a ground, a Classical set, a nocturne. Then after tonality: "
                  "planing, a row, phasing, the Tonnetz and the geometry of chords, and a Vuza canon in which every pulse is "
                  "struck exactly once.")
        self.page(by(34, 44), r"Parts 34 to 44",
                  "Many musics, each measured in its own terms: a tihai whose last stroke lands on sam, notes moved off the "
                  "piano's keys in three maqamat, harmonics on the qin, an inherent pattern, blue thirds thirty-five cents low, "
                  "a bebop chorus on chord tones, a pop single. Then the craft: orchestrations matched to a vowel, a searcher "
                  "that threw away nearly three thousand drafts, a performance, a film cue on its hit point.")
        self.page(by(45, 56), r"Parts 45 to 56",
                  "The mind: a tune hidden in another, three endings measured in bits, thirty singers in a chain. Then electric "
                  "sound and the studio: bits and dither, reverberation times, pitch correction, synthesizers, FM checked against "
                  "Bessel's functions to a few millionths, a tracker, microphones and loudspeakers, rooms, a mix.")
        self.page(by(57, 68), r"Parts 57 to 68",
                  "Mastering's loudness, a codec's noise against its mask, an arena's back row, a stream's money. Then the "
                  "machines: a transcription that decays when it is repeated, a follower, a fingerprinter, a separator, a model "
                  "that composes and one that sings, and a critical edition. And the last row, this part's: the suite, and the "
                  "round trip's count of wrong notes.")

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"every row measures its Variation \ by the idea of its part, \ not by taste", WHITE),
            (r"the measures are of many kinds: \ cents, \ decibels, \ bits, \ counts of rules broken, \ seconds, \ dollars", WHITE),
            (r"some are verdicts the series later checked: \ Part 67 re-ran five \ and found one weaker than it had said", WHITE),
            (r"each row's sound, \ score and numbers are in its part's cache, \ and its claim in that part's tests", TUNE),
        ]
        rows_scene(self, r"what the ledger is", items,
                   "What is the ledger, then? <bookmark mark='b'/> Every row measures its Variation by the idea of its part, not by "
                   "taste. <bookmark mark='c'/> The measures are of many kinds: cents, decibels, bits, counts of rules broken, "
                   "seconds and dollars. <bookmark mark='d'/> Some are verdicts that the series later checked: Part 67 re-ran five, "
                   "and found one weaker than had been said. <bookmark mark='e'/> And every row's sound, score and numbers are kept "
                   "in its part's files, with its claim held by that part's tests.", marks="bcde")
