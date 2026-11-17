from __future__ import annotations

import numpy as np

from videos.music.music27.common import *  # noqa: F403
from videos.music.variations import rows_before

ORDER = ["nocturne", "lied", "motif"]
NAME = {"nocturne": r"a nocturne: \ ornamented, \ a wide left hand, \ a phrase arch", "lied": r"a Lied: \ a voice over rustling triplets",
        "motif": r"a leitmotif: \ minor, \ augmented, \ darkening chords"}


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune")
        v = load("variation")
        c = clip("tune.variation27")
        head = VGroup(label(r"Variation 27", font_size=48, color=TUNE), label(r"the Tune, \ three Romantic ways", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        voices = {"nocturne": [d["nocturne"], d["lh"]], "lied": [d["lied"], d["rh"] + d["lb"]],
                  "motif": [d["motif"], [[m, t, 4] for t, ch in d["chords"] for m in ch]]}
        rows_ = VGroup()
        rolls = []
        for k in ORDER:
            g = voices_roll(voices[k], width=7.2, height=1.15, colors=[TUNE, GREY_A], lo=28, hi=86, bar_h=0.06)
            rows_.add(VGroup(label(NAME[k], font_size=19, color=GREY_A), g).arrange(RIGHT, buff=0.4))
            rolls.append(g)
        rows_.arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to(DOWN * 0.4 + RIGHT * 0.2)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> This time, three "
            "Romantic ways. A nocturne: the melody ornamented with turns, over a left hand spread across two octaves, the "
            "whole bending under a phrase arch. A Lied: the synthetic voice sings the Tune over rustling triplets, as in Der "
            "Lindenbaum. And a leitmotif transformed: the Tune's head in minor, at half speed, over chords that darken "
            "chromatically before they settle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"Variation 27", kind="synthesized", detail=r"piano, \ synthetic voice, \ bowed string", corner=DL, tag_corner=DR)
            for i, k in enumerate(ORDER):
                st = d["starts"][k]
                flash_voices(snd, rolls[i], voices[k], st, d["units"][k], colors=[TUNE, GREY_A])
                end = d["starts"][ORDER[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, rows_[i][0], st, end, buff=0.06)
        self.play(FadeOut(rows_))
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            f"Row twenty-seven of the ledger: {say(v['seconds'])} seconds. The measurement: the nocturne puts "
            f"{say(d['notes']['nocturne'])} melody notes over {say(d['notes']['left_hand'])} in the left hand, more than "
            "two to one, the accompaniment now busier than the tune it carries."
        ):
            self.play(FadeIn(led, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        lib = load("library")
        card = objectives_card([
            r"the piano grew from five octaves to seven and a quarter, \ and the scores climbed with it",
            r"a key-finder hears \textit{Der Lindenbaum}'s stanza turn from E major to E minor",
            r"rubato modelled two ways: \ a phrase arch, \ and Mozart's stolen time",
            r"a theme as a character \ (Berlioz) \ and a chord as a question \ (Wagner)",
            rf"instrumental chromaticism rose about {100 * lib['slope_i']:.0f} points a century, \ 1680 to 1900; \ songs stayed plain",
            r"after 1900, \ Schoenberg and Webern: \ 25 to 30 in 100, \ the key nearly gone",
        ], title=r"What we found", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? The piano grew from five octaves to more than seven, and the scores climbed with it. "
            "<bookmark mark='a'/> A key-finder hears Schubert turn a stanza from major to minor. <bookmark mark='b'/> Rubato "
            "can be modelled two ways, both heard. <bookmark mark='c'/> A theme became a character, and a chord became a "
            f"question. <bookmark mark='d'/> Across the Library, instrumental music grew more chromatic by about "
            f"{say(round(100 * lib['slope_i']))} notes in a hundred per century, while the selected songs had lower averages. "
            "<bookmark mark='e'/> And just after the century's end, the measure jumps: these selected post-tonal examples fit the key-profile model less well."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A window holds C, E, G for 10 beats and F$\sharp$, B$\flat$ for 2 beats, \ in C major. \ Compute its chromaticism.",
            r"Show that a phrase arch whose tempo is symmetric about the middle of the phrase leaves the phrase's midpoint where strict time puts it.",
            r"\textbf{Ear.} \ The lab plays eight versions of a phrase: \ strict, \ arched or stolen. \ Sort them.",
            r"\textbf{Build.} \ Add a third measure to the Library: \ the share of chords that are not triads or sevenths, \ and plot it by year.",
            r"$\bigstar$ \ When, \ and in which genres, \ did nineteenth-century harmony change fastest? \ Answer with intervals.",
        ], font_size=22)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"what is left when the key goes: \ Schoenberg, \ Debussy, \ Stravinsky", [28, 29]),
            (r"the song, \ in every tradition", [40]),
            (r"orchestration: \ Berlioz's treatise, \ and after", [41]),
            (r"performing: \ rubato, \ tempo and the evidence of recordings", [43]),
            (r"music that tells a story: \ film and games", [44]),
            (r"style and history as data", [62, 67]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? Next, in what is left when the key goes. In the song, in every tradition. In "
            "orchestration, which Berlioz also wrote the first great treatise on. In performing, where rubato meets the "
            "evidence of recordings. In music that tells a story, for film and games. And in research that treats style "
            "and history as data."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"pianists", r"bend a phrase: \ arch the tempo, \ or steal time over a steady bass"),
            (r"singers", r"hear what the piano says that the words do not"),
            (r"composers", r"transform a theme rather than repeat it"),
            (r"analysts", r"turn `harmony grew more chromatic' into a measured trend with an interval"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Pianists bend a phrase, either way. Singers listen to what the piano says. Composers transform "
            "a theme instead of repeating it. And analysts can turn a familiar story into a measured trend, with an interval."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"R. Taruskin, \ \textit{The Oxford History of Western Music}, \ vol. 3 \ (2005)",
             r"C. Rosen, \ \textit{The Romantic Generation} \ (1995)",
             r"C. Dahlhaus, \ \textit{Nineteenth-Century Music} \ (1980; \ trans. 1989)",
             r"W. Weber, \ \textit{The Great Transformation of Musical Taste} \ (2008)"],
            [r"N. P. M. Todd, \ `The dynamics of dynamics', \ \textit{JASA} \ (1992)",
             r"B. H. Repp, \ `Diversity and commonality in music performance', \ \textit{JASA} \ (1992)",
             r"C. Weiß, \ M. Mauch, \ S. Dixon, \ M. Müller, \ `Investigating style evolution of Western classical music', \ \textit{Musicae Scientiae} \ (2019)",
             r"M. S. Cuthbert and C. Ariza, \ `music21' \ (2010): \ the Library's encodings"],
            font_size=19)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 27, "Paris, 1889",
            "What is left when the key goes?",
            "That completes Act Four: a thousand years, from one line of chant to Mahler's orchestra. "
            "<bookmark mark='a'/> The last measurement in this part found the key loosening. What is left when it "
            "goes? In Paris in 1889 a young Debussy heard a Javanese gamelan at the World's Fair, tuned to scales no "
            "European piano could play. <bookmark mark='b'/> Act Five begins. Part 28: New Scales, New Rhythms.")
