from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord import tune
from videos.music.music1.common import (EAR, FREQ, GOOD, HIST, PART, RATIO, STR, TUNE, clip, load, ring, say, window)


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
        c = clip("tune.variation1")
        head = VGroup(label(r"Variation 1", font_size=48, color=TUNE),
                      label(r"the Tune on one string", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        head.to_edge(UP, buff=0.4)
        mono = MonochordView(width=11.0).move_to(UP * 0.9)
        stops = {}
        for chk in d["checks"]:
            p, q = chk["ratio"]
            frac = q / p
            tex = rf"\tfrac{{{q}}}{{{p}}}" if p != 1 else r"1"
            mk = mono.mark(frac, tex, font_size=30)
            nm = label(chk["name"], font_size=30, color=GREY_B).next_to(mk, DOWN, buff=0.12)
            stops[chk["name"]] = VGroup(mk, nm)
        marks = VGroup(*stops.values())
        slots = VGroup(*[label("C", font_size=44, color=GREY_D) for _ in range(7)]).arrange(RIGHT, buff=0.7)
        slots.move_to(DOWN * 2.6)
        with self.voiceover(
            "Every part of this series ends the same way: by doing something to the Tune with what the part has "
            "just built. Today we built exactly one thing. <bookmark mark='a'/> So this is Variation 1: the Tune on "
            "one simulated string, with one bridge and six places to put it. <bookmark mark='b'/> Each place is a "
            "ratio of whole numbers. Nothing else is on this recording."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mono))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2), run_time=2.0)
        prev = None
        row = None
        with self.listen(c) as snd:
            window(snd, r"Variation 1")
            phrase = -1
            k_in = 0
            for k, n in enumerate(c.notes):
                snd.wait_until(f"n{k}")
                if n["phrase"] != phrase:
                    phrase = n["phrase"]
                    k_in = 0
                    names = [m["name"] for m in c.notes if m["phrase"] == phrase]
                    new = VGroup(*[label(t, font_size=44, color=GREY_D) for t in names]).arrange(RIGHT, buff=0.7)
                    new.move_to(DOWN * 2.6)
                    if row is not None:
                        self.remove(row)
                    row = new
                    self.add(row)
                if prev is not None:
                    self.remove(prev)
                mono.set_stop(n["stop"])
                for name, grp in stops.items():
                    grp.set_color(TUNE if name == n["name"] else GREY_B)
                    grp[0][0].set_color(TUNE if name == n["name"] else RATIO)
                    grp[0][1].set_color(TUNE if name == n["name"] else RATIO)
                prev = mono.lens(n["stop"], amp=0.2)
                self.add(prev)
                snd.drive(prev, ring(at=n["t"], rate=1.8))
                row[k_in].set_color(TUNE)
                k_in += 1
        if prev is not None:
            self.remove(prev)
        led = variations_ledger([{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}],
                                highlight=(0,)).move_to(DOWN * 2.5)
        with self.voiceover(
            f"That goes into the ledger as row one. {say(v['seconds'])} seconds, six positions of one bridge, and "
            f"every interval within {say(max(d['worst_cents'], 0.1), 1)} cents of its ratio. There are sixty-seven "
            "rows to go."
        ):
            self.play(FadeOut(row), FadeIn(led, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"a string's pitch is the rate at which a wave makes the round trip: \ $f = \frac{1}{2L}\sqrt{T/\mu}$",
            r"Newton's law for one small piece of string is the wave equation: \ acceleration $= c^2 \times$ curvature",
            r"one motion, two pictures: \ two travelling shapes (d'Alembert), \ or a sum of standing modes (Bernoulli)",
            r"a pluck at the fraction $\beta$ has $\sin(n\pi\beta)/n^2$ of mode $n$: \ one string is already a chord",
            r"strings in simple ratios share partials, \ and shared partials do not beat: \ a first answer",
            r"real strings fade, \ are stiff, \ and stretch: \ three corrections, \ each heard later in the series",
        ], title=r"What we found", font_size=26).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? A string has a pitch because a wave on it keeps making the same round trip, and "
            "counting the trips gives Mersenne's law. <bookmark mark='a'/> Newton's law for one small piece of "
            "string is the wave equation: a string accelerates where it is curved. <bookmark mark='b'/> Its motion "
            "can be told two ways, as travelling shapes or as standing modes, and the two are the same. "
            "<bookmark mark='c'/> A plucked string contains modes in amounts we can calculate, so one string is "
            "already a chord. <bookmark mark='d'/> Strings in simple ratios share partials, which is a first answer "
            "to Pythagoras. <bookmark mark='e'/> And real strings fade, resist bending and stretch."
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
            r"A string $65$ cm long with a mass of $3$ g per metre is tuned to $110$ Hz. \ Find its tension and "
            r"the speed of a wave on it. \ What interval does it rise by if the tension is doubled?",
            r"Show that the force a plucked ideal string puts on its bridge is a rectangular wave that is high for "
            r"the fraction $\beta$ of each period, \ and recover the amplitudes $\sin(n\pi\beta)/n$ from it.",
            r"\textbf{Ear.} \ The lab plays three plucks of one note. \ One was plucked a quarter of the way along. "
            r"\ Which, \ and which partials told you?",
            r"\textbf{Build.} \ A hammer gives a string speed, \ not shape. \ Add a struck start to "
            r"\texttt{simulate} and show that its modes fall as $1/n$ where a pluck's fall as $1/n^2$.",
            r"$\bigstar$ \ Model a string that meets a curved bridge as it swings, \ with a scheme whose energy "
            r"balance is exact, \ and compare its spectrum over time with a tanpura's.",
        ], font_size=24)
        with self.voiceover(
            "Five problems. One to compute, one to derive, one for your ears, one to build in the repository, and "
            "a research problem, marked with a star. Full solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"modes and harmonics", [3, 5, 8]),
            (r"beats", [5, 6]),
            (r"stiff strings, stretched partials", [6, 7]),
            (r"beads and Newton's law", [7, 9, 52]),
            (r"the plucking point", [7, 51]),
            (r"the Tune", [26, 68]),
        ], font_size=26)
        with self.voiceover(
            "Where does this come back? Modes and harmonics are the subject of Part 3, the foundation of Part 5 on "
            "consonance, and the whole physics of pipes in Part 8. Beats are how Part 6 tunes a keyboard. Stiff "
            "strings return in the piano of Part 7. And the bead simulation is how this series will build every "
            "instrument it plays."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"instrument makers", r"string scaling: \ a length, \ a gauge and a tension for every note; \ why bass "
             r"strings are wound"),
            (r"players", r"where to pluck or bow for a tone; \ harmonics; \ tuning by beats"),
            (r"piano technicians", r"stiff strings, \ stretched octaves, \ unisons tuned by ear"),
            (r"audio programmers", r"physical-modelling synthesis: \ every plucked-string algorithm starts from "
             r"d'Alembert's two travelling waves"),
        ], font_size=26)
        with self.voiceover(
            "And in practice. This is the daily arithmetic of anyone who designs a stringed instrument: a length, a "
            "thickness and a tension for every note. Players use the plucking point and the harmonics. Piano "
            "technicians live with stiff strings and tune by beats. And every plucked-string synthesizer is "
            "d'Alembert's two travelling waves, run in a loop."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"N. H. Fletcher and T. D. Rossing, \ \textit{The Physics of Musical Instruments} \ (2nd ed., 1998), ch.\ 2",
             r"A. H. Benade, \ \textit{Fundamentals of Musical Acoustics} \ (1976)",
             r"S. Bilbao, \ \textit{Numerical Sound Synthesis} \ (2009), ch.\ 6--8",
             r"H. von Helmholtz, \ \textit{On the Sensations of Tone} \ (1863; tr.\ Ellis)",
             r"H. F. Cohen, \ \textit{Quantifying Music} \ (1984): \ Galilei, Mersenne and the first acoustics"],
            [r"M. Mersenne, \ \textit{Harmonie universelle} \ (1636)",
             r"J. le Rond d'Alembert, \ ``Recherches sur la courbe que forme une corde tendue mise en vibration'' \ (1747)",
             r"D. Bernoulli, \ ``R\'eflexions et \'eclaircissements sur les nouvelles vibrations des cordes'' \ (1753)",
             r"K. A. Legge and N. H. Fletcher, \ ``Nonlinear generation of missing modes on a vibrating string'', \ "
             r"\textit{JASA} 76 (1984)",
             r"S. Bilbao, A. Torin and V. Chatziioannou, \ ``Numerical modeling of collisions in musical "
             r"instruments'', \ \textit{Acta Acustica} 101 (2015)",
             r"C. Issanchou et al., \ ``A modal-based approach to the nonlinear vibration of strings against a "
             r"unilateral obstacle'', \ \textit{J. Sound Vib.} (2017)"],
            font_size=22)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        mono = MonochordView(width=9.0, ruler=False).move_to(UP * 1.4)
        bare = VGroup(Line(LEFT * 4.5, RIGHT * 4.5, color=STR, stroke_width=3.5),
                      *[Polygon(p + DOWN * 0.3 + LEFT * 0.1, p + DOWN * 0.3 + RIGHT * 0.1, p, stroke_width=0,
                                fill_color=GREY_A, fill_opacity=1) for p in (LEFT * 4.5, RIGHT * 4.5)]).move_to(DOWN * 1.2)
        t1 = label(r"with its box: \ a note", font_size=28, color=GREY_A).next_to(mono, UP, buff=0.3)
        t2 = label(r"without it: \ almost nothing", font_size=28, color=GREY_A).next_to(bare, DOWN, buff=0.4)
        nxt = VGroup(label(r"Part 2", font_size=34, color=GREY_B), label(r"Waves in Air", font_size=54, color=TUNE)
                     ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "One thing we stepped around all the way through. A string is thin. It slices through the air and moves "
            "almost none of it. <bookmark mark='a'/> Take the monochord's string off its box and stretch it between "
            "two nails, and you can barely hear it. So what does the box do? What is it that actually travels "
            "from the instrument to your ear, how fast, and how does it get round corners? "
            "<bookmark mark='b'/> That is Part 2: Waves in Air."
        ) as vo:
            self.play(FadeIn(mono), FadeIn(t1))
            vo.wait_until("a")
            self.play(FadeIn(bare), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeOut(t2), FadeOut(bare), FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
