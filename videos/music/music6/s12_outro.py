from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403
from videos.music.variations import rows_before


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
        c = clip("tune.variation6")
        rows = d["rows"]
        head = VGroup(label(r"Variation 6", font_size=48, color=TUNE),
                      label(r"one tune, \ eight tunings", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.4)
        short = [r"Pythagorean", r"meantone, \ in C", r"meantone, \ in A$\flat$: \ the wolf", r"Werckmeister III", r"12 equal", r"19 equal", r"31 equal", r"53 equal"]
        names = VGroup(*[label(t, font_size=26, color=GREY_D) for t in short]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 4.3 + DOWN * 0.3)
        top = 34.0
        bars = VGroup()
        for k, r in enumerate(rows):
            w = 5.6 * r["error"] / top
            b = Rectangle(width=max(w, 0.03), height=0.3, stroke_width=0, fill_color=error_color(r["error"], 16.0), fill_opacity=0.9)
            b.next_to(names[k], RIGHT, buff=0.0).set_x(-1.4 + w / 2)
            b.set_y(names[k].get_y())
            bars.add(VGroup(b, label(rf"{r['error']:.0f}", font_size=22, color=GREY_A).next_to(b, RIGHT, buff=0.12)))
        bl = label(r"how far its chords are from pure (cents)", font_size=22, color=GREY_B).next_to(bars, UP, buff=0.3).align_to(bars, LEFT)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it has built. This part built tunings, so "
            "here is the Tune with simple chords under it, eight times over, a phrase at a time. "
            "<bookmark mark='a'/> Pythagorean. Meantone in C, and then in the key that crosses the wolf. "
            "Werckmeister. Then twelve, nineteen, thirty-one and fifty-three equal steps. The notes on the page "
            "never change. Listen to the chords."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.12), FadeIn(bl), run_time=2.5)
        for b in bars:
            b.set_opacity(0)
            self.add(b)
        version = -1
        with self.listen(c) as snd:
            window(snd, r"Variation 6", kind="synthesized", detail=r"the Tune with chords, \ in eight tunings", corner=DL, tag_corner=DR)
            for k, nt in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if nt["version"] != version:
                    if version >= 0:
                        names[version].set_color(GREY_B)
                    version = nt["version"]
                    names[version].set_color(TUNE)
                    bars[version].set_opacity(1)
                self.play(bars[version][0].animate(rate_func=there_and_back).set_fill(opacity=0.5), run_time=min(0.4, nt["dur"] * 0.7))
        names[version].set_color(GREY_B)
        rws = rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).to_edge(DOWN, buff=0.2)
        lo, hi = d["range"]
        with self.voiceover(
            f"Row six of the ledger. {say(v['seconds'])} seconds. The chords of the fifty-three-step version are "
            f"within {say(max(lo, 1))} cent of pure. Those of the wolf key are {say(hi)} cents out. Twelve equal "
            "steps, the tuning you have heard all your life, sits in the middle, at about ten."
        ):
            self.play(VGroup(names, bars, bl).animate.scale(0.52).move_to(UP * 1.75), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        e, m = load("equal"), load("meantone")
        card = objectives_card([
            r"twelve pure fifths overshoot seven octaves by 23.5 cents; \ no stack of fifths ever closes",
            r"four pure fifths overshoot a pure third by 21.5 cents; \ pure chords with held notes drift",
            rf"meantone: \ fifths {m['narrow_by']:.1f} cents narrow, \ eight pure thirds, \ one wolf",
            r"well temperaments: \ the error graded round the circle; \ every key usable, \ each different",
            rf"equal temperament: \ every fifth {abs(e['fifth_error']):.0f} cents narrow, \ every third {e['third_error']:.0f} cents wide; \ tuned by counting beats",
            r"twelve comes from $\log_2\tfrac32 \approx \tfrac7{12}$; \ pianos stretch; \ free instruments adjust",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Twelve pure fifths overshoot seven octaves, and no stack of fifths can ever close, "
            "because no power of three is a power of two. <bookmark mark='a'/> Four pure fifths overshoot a "
            "pure third, and so pure chords with held notes drift. <bookmark mark='b'/> Meantone makes the "
            "thirds pure for eight keys, and pays with a wolf. <bookmark mark='c'/> The well temperaments grade "
            "the error round the circle, so that every key can be used and each has a character. "
            "<bookmark mark='d'/> Equal temperament makes every key the same, at the price of thirds fourteen "
            "cents wide, and is tuned by counting beats. <bookmark mark='e'/> The number twelve comes from the "
            "best small fraction for a fifth. And in practice pianos stretch their octaves, and voices and "
            "strings adjust every note as they go."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, r in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"In equal temperament with A4 = 440 Hz, \ find the frequencies of F3 and A3 and the beat rate of the major third between them. \ "
            r"How fast does the same third beat an octave higher?",
            r"Show that in quarter-comma meantone the diminished sixth G$\sharp$--E$\flat$ exceeds a pure fifth by 35.7 cents, \ "
            r"and that three pure major thirds fall short of an octave by $\tfrac{128}{125}$.",
            r"\textbf{Ear.} \ The lab plays the major chord on C in four tunings, \ in a random order. \ Rank them from stillest to busiest, \ "
            r"and name the equal-tempered one.",
            r"\textbf{Build.} \ Add sixth-comma meantone and Vallotti's temperament to \texttt{tuning.py}, \ and draw their thirds round the circle. \ "
            r"Which keys does each favour?",
            r"$\bigstar$ \ Write an adaptive tuner: \ given the notes sounding, \ choose the pitches that minimise Part 5's roughness, \ "
            r"with a penalty for moving a held note. \ Run it on the comma pump. \ How small can the penalty be before the pitch drifts?",
        ], font_size=23)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, "
            "marked with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"stiff strings and stretched octaves", [7]),
            (r"the twelve notes, \ scales and keys", [12, 15]),
            (r"the lattice of fifths and thirds", [13, 31, 32]),
            (r"temperaments as arithmetic: \ commas, \ continued fractions", [33]),
            (r"other divisions of the octave, \ other tunings", [34, 35, 36]),
            (r"tuning tables, \ pitch bend, \ retuning in software", [50, 53]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? The stretched octave returns in Part 7, when we build the piano's "
            "string. The twelve notes that this part has justified become scales and keys. The grid of fifths "
            "and thirds returns as a map of chords. Commas and continued fractions return when we treat scales "
            "as mathematics. Other divisions of the octave are the daily material of Indian, Arabic and "
            "Indonesian music. And every synthesizer carries a tuning table."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"piano technicians", r"set a temperament octave by beat rates, \ then stretch octaves to suit each piano's strings"),
            (r"harpsichordists and organists", r"choose a temperament for the repertoire: \ meantone for 1600, \ a well temperament for Bach"),
            (r"choir directors and string coaches", r"tune held thirds low and fifths wide, \ and rehearse the places where the pitch sags"),
            (r"producers and synth programmers", r"retune samples and oscillators with tuning tables; \ detune pairs by a few cents for warmth"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. A piano technician sets one octave by beat rates and stretches the rest to suit "
            "the strings. A harpsichordist chooses a temperament to match the music: meantone for 1600, a well "
            "temperament for Bach. A choir director tunes held thirds low, and rehearses the bars where the "
            "pitch is known to sag. And a producer detunes two oscillators by a few cents, on purpose, because "
            "slow beats are warm."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J. M. Barbour, \ \textit{Tuning and Temperament: A Historical Survey} \ (1951)",
             r"R. W. Duffin, \ \textit{How Equal Temperament Ruined Harmony (and Why You Should Care)} \ (2007)",
             r"W. A. Sethares, \ \textit{Tuning, Timbre, Spectrum, Scale} \ (2nd ed., 2005)",
             r"G. J. Cho, \ \textit{The Discovery of Musical Equal Temperament in China and Europe} \ (2003)"],
            [r"Zhu Zaiyu, \ \textit{L\"ul\"u jingyi} \ (1584--96)",
             r"A. Werckmeister, \ \textit{Musicalische Temperatur} \ (1691)",
             r"C. Huygens, \ ``Lettre touchant le cycle harmonique'' \ (1691)",
             r"O. L. Railsback, \ ``Scale temperament as applied to piano tuning'', \ \textit{JASA} 9 (1938)",
             r"B. Lehman, \ ``Bach's extraordinary temperament: our Rosetta Stone'', \ \textit{Early Music} 33 (2005)",
             r"D. M. Howard, \ ``Intonation drift in a capella soprano, alto, tenor, bass quartet singing with key modulation'', \ \textit{J. Voice} 21 (2007)",
             r"S. D'Amario et al., \ ``A longitudinal study of intonation in an a cappella singing quintet'', \ \textit{J. Voice} 34 (2020)"],
            font_size=21)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        c = clip("next.pluck")
        s = StringView(width=9.0).move_to(UP * 1.2)
        lens = Lens(s.p(0.0), s.p(1.0), amp=0.3, color=TUNE)
        ways = VGroup(label(r"plucked", font_size=34, color=TUNE), label(r"struck", font_size=34, color=GREY_B), label(r"bowed", font_size=34, color=GREY_B)).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.6)
        with self.voiceover(
            "One last sound, and it is where the series began: Part 1's string, plucked."
        ):
            self.play(FadeIn(s), FadeIn(ways))
        with self.listen(c) as snd:
            window(snd, r"one string, \ plucked", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            pulse(snd, ways[0], 0.0, 2.6)
            snd.show(lens)
            snd.drive(lens, ring(0.0, 1.3))
        nxt = VGroup(label(r"Part 7", font_size=34, color=GREY_B), label(r"Strings, \ Hammers and Bows", font_size=50, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "For six parts that has been our only instrument. We know its partials, how the ear sorts them, why "
            "they make some intervals smooth, and how to tune twelve of them. But a string can be set going in "
            "three ways. <bookmark mark='a'/> It can be plucked, like this one. It can be struck by a hammer, "
            "and then it is a piano. Or it can be bowed, and then it never dies away. Same string, three "
            "instruments, and from here on we build them. That is Part 7: Strings, Hammers and Bows."
        ) as vo:
            vo.wait_until("a")
            self.play(ways[1].animate.set_color(TUNE), ways[2].animate.set_color(TUNE), FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
