from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Xenakis(SoundScene):
    def construct(self):
        chapter(self, 4, r"Xenakis: \ clouds and sieves", r"Can a composer write a cloud?", extra=((1954, r"\textit{Metastaseis}"),))
        self.engineer()
        self.gliss()
        self.quiz()
        self.poisson()
        self.density()
        self.sieves()
        self.upic()

    # ------------------------------------------------------------------
    def engineer(self):
        items = [
            (r"Iannis Xenakis, \ 1922--2001: \ resistance fighter in Greece, \ wounded, \ exiled to Paris in 1947", WHITE),
            (r"an engineer in Le Corbusier's office, \ a composition student of Messiaen", WHITE),
            (r"\textit{Metastaseis} \ (1954): \ 61 players; \ prominent independent string glissandi", WHITE),
            (r"the same ruled surfaces as the Philips Pavilion's roof: \ straight lines making curves", TUNE),
            (r"`stochastic music': \ compose the statistics of a mass, \ not each of its notes", EAR),
        ]
        rows_scene(self, r"Iannis Xenakis", items,
                   "The sharpest critic of total serialism was an engineer. <bookmark mark='b'/> Iannis Xenakis fought in the "
                   "Greek resistance, was badly wounded, and reached Paris as a refugee in 1947, <bookmark mark='c'/> where he "
                   "worked as an engineer for Le Corbusier and studied composition with Messiaen. <bookmark mark='d'/> His "
                   "Metastaseis, of 1954, uses a sixty-one-player ensemble with a prominent mass of independently moving string glissandi, <bookmark mark='e'/> drawn as the "
                   "same ruled surfaces, curves made of straight lines, that he would use for the Philips Pavilion's roof. "
                   "<bookmark mark='f'/> He called the method stochastic music: compose the statistics of a mass of sound, not "
                   "each of its notes.", marks="cdef")

    # ------------------------------------------------------------------
    def gliss(self):
        d = load("gliss")
        c = clip("gliss.cloud")
        W, H = 11.0, 3.6
        lo, hi = 45, 90
        lines = VGroup(*[Line([-W / 2 + W * g["t0"] / d["seconds"], -0.2 - H / 2 + H * (g["p0"] - lo) / (hi - lo), 0],
                              [-W / 2 + W * g["t1"] / d["seconds"], -0.2 - H / 2 + H * (g["p1"] - lo) / (hi - lo), 0], color=TUNE, stroke_width=2.5)
                         for g in d["glissandi"]])
        head = label(r"forty glissandi \ (ours): \ random starts, \ lengths and slopes", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is a cloud of glissandi of our own, forty of them, each a few harmonics sliding together, with random "
            "starting times, lengths and slopes. Drawn as Xenakis drew his, every line is a sliding pitch. Listen to the mass "
            "rather than the lines: its density, its register, the way it thickens and thins."
        ):
            self.play(FadeIn(head), Create(lines), run_time=2.0)
        with self.listen(c) as snd:
            window(snd, r"a cloud of glissandi \ (ours)", kind="synthesized", detail=r"additive synthesis", corner=DL, tag_corner=DR)
            flash(snd, list(lines), [g["t0"] for g in d["glissandi"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("clouds")
        c = clip("clouds.quiz")
        card = listen_card(r"Two clouds of the same plucked notes. \ In one the notes come at random moments; \ "
                           r"in the other they are evenly spaced. \ Which is random, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two clouds of the same plucked notes from Part 1's string. In one, the notes come at "
            "random moments; in the other they are evenly spaced in time. Which is the random one, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        def row(times):
            return VGroup(*[Line([-5 + 10 * t / d["seconds"], 0, 0], [-5 + 10 * t / d["seconds"], 0.6, 0], color=GREY_A, stroke_width=3) for t in times])
        rA = row(d["onsets"]).move_to(UP * 0.9)
        rB = row(d["even"]).move_to(DOWN * 1.1)
        la = label(r"A", font_size=36, color=GREY_A).next_to(rA, LEFT, buff=0.4)
        lb = label(r"B", font_size=36, color=GREY_A).next_to(rB, LEFT, buff=0.4)
        self.play(FadeOut(card), FadeIn(rA), FadeIn(rB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            flash(snd, list(rA), [d["starts"]["A"] + t for t in d["onsets"]], hot=WHITE, base=GREY_A)
            flash(snd, list(rB), [d["starts"]["B"] + t for t in d["even"]], hot=WHITE, base=GREY_A)
            pulse(snd, VGroup(rA, la), d["starts"]["A"], d["starts"]["B"] - 0.3, buff=0.12)
            pulse(snd, VGroup(rB, lb), d["starts"]["B"], c.duration, buff=0.12)
        ans = VGroup(label(r"A: \ random \ (a Poisson process): \ clumps and gaps", font_size=21, color=TUNE).next_to(rA, DOWN, buff=0.3),
                     label(r"B: \ evenly spaced: \ a pulse", font_size=21, color=BLUE).next_to(rB, DOWN, buff=0.3))
        with self.voiceover(
            "A is random. Random moments are not evenly spread: they clump together and leave gaps, and the ear hears the "
            "clumps as bursts. B, the same notes at equal spacing, is heard at once as a pulse. Randomness, to the ear, "
            "sounds lumpier than people expect."
        ):
            self.play(FadeIn(ans), *[x.animate.set_color(TUNE) for x in rA], *[x.animate.set_color(BLUE) for x in rB])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def poisson(self):
        d = load("clouds")
        ks = list(range(0, 14))
        bars = columns(d["hist"], [str(k) for k in ks], width=8.0, height=2.8, color=TUNE, fmt="{:.0f}", font_size=16)
        bars.move_to(LEFT * 1.8 + DOWN * 0.4)
        x0 = bars.get_left()[0]
        dots = VGroup()
        for k in ks:
            dots.add(Dot([x0 + (k + 0.5) * bars.width / 14, bars.get_bottom()[1] + 0.35 + 2.8 * d["expect"][k] / max(d["hist"]), 0], radius=0.07, color=EAR))
        t = label(r"notes per second, \ counted over ten minutes of a cloud at 5 a second", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"gold: seconds with 0, 1, 2 ... onsets", TUNE),
            (r"pink: Poisson, $e^{-\lambda}\lambda^k/k!$\\$\lambda = 5$ onsets per second", EAR),
            (rf"8-second example: gap SD / mean {d['gap_cv']:.2f}\\theoretical value: 1", WHITE),
            (r"Xenakis composed density cell by cell\\this model assumes steady rate\\and independent events", GREY_A))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.8))
        side.move_to(RIGHT * 4.3 + DOWN * 0.2)
        with self.voiceover(
            "Xenakis governed his clouds with a law from probability. Let the cloud run for ten minutes at an average of five notes a second, and count the notes in each second. <bookmark mark='a'/> The gold bars are the counts. <bookmark mark='b'/> The pink points are Poisson's law, the count distribution for the specified homogeneous Poisson-process model; the two agree. <bookmark mark='c'/> The gaps between notes vary as much as their average length, which is why the cloud clumps. <bookmark mark='d'/> In Achorripsis, of 1957, Xenakis chose the average density for each cell of his score and used probabilistic distributions in a composed density framework, not an assertion that all his music follows this one process."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars), FadeIn(dots))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sieves(self):
        d = load("sieves")
        c = clip("sieves.nonoctave")
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"a sieve: \ unions and intersections of residue classes, \ $an + b$", WHITE),
            (r"$2n$: \ the whole-tone scale; \ $3n \cup 3n{+}1$: \ the octatonic", WHITE),
            (r"C major, \ from moduli 3 and 4, \ needs seven terms: \ one for each note \ (the Chinese remainder theorem)", WHITE),
            (r"$5n \cup 7n{+}2$, \ from C3: \ repeats only every 35 semitones", TUNE))]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(UP, buff=0.45)
        rows_.scale_to_fit_width(min(rows_.width, 12.0))
        g = mroll(d["line"], width=10.0, height=1.6, lo=46, hi=86, color=TUNE, bar_h=0.12).move_to(DOWN * 2.0)
        with self.voiceover(
            "Xenakis also built scales and rhythms with sieves: unions and intersections of arithmetic sequences, a n "
            "plus b. <bookmark mark='a'/> Every second semitone is the whole-tone scale; every third, together with every "
            "third shifted by one, the octatonic. <bookmark mark='b'/> C major can be written with sequences of steps three "
            "and four, but needs seven terms, one for each note. <bookmark mark='c'/> Sieves come into their own for scales "
            "that do not repeat at the octave. Every fifth semitone, together with every seventh shifted by two, makes a "
            "scale that repeats only every thirty-five semitones. Here it is over three octaves."
        ) as vo:
            self.play(FadeIn(rows_[0]), FadeIn(g))
            for mark, r in zip("abc", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        with self.listen(c) as snd:
            window(snd, r"$5n \cup 7n{+}2$", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, g.notes, [n[1] * d["unit"] for n in d["line"]], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def density(self):
        d = load("density")
        c = clip("density.rise")
        W, H = 11.0, 3.0
        ticks = VGroup(*[Line([-W / 2 + W * t / d["seconds"], -0.2 - H / 2 + H * (p - 55) / 35, 0], [-W / 2 + W * t / d["seconds"], -0.2 - H / 2 + H * (p - 55) / 35 + 0.12, 0],
                              color=TUNE, stroke_width=3) for t, p in zip(d["onsets"], d["pitches"])])
        head = label(r"one parameter: \ density, \ rising from 1 to 24 notes a second", font_size=25, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(rf"notes in each second: \ {', '.join(str(x) for x in d['counts'])}", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In Xenakis's music density itself becomes a melody. Here a cloud of plucks whose rate rises steadily from one "
            "note a second to twenty-four over twelve seconds; every note's moment and pitch is random, but the rate is "
            "composed. Listen for the cloud thickening from separate drops to rain. The counts per second, below, wobble "
            "around the rising line, as Poisson's law says they should."
        ):
            self.play(FadeIn(head), FadeIn(ticks), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a thickening cloud", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            flash(snd, list(ticks), d["onsets"], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def upic(self):
        items = [
            (r"UPIC \ (1977): \ Xenakis's system for composing by drawing on a tablet", WHITE),
            (r"lines drawn are pitches over time; \ drawn shapes become waveforms and envelopes", WHITE),
            (r"\textit{Mycènes Alpha} \ (1978): \ a whole piece drawn", WHITE),
            (r"children in workshops used it too: \ composition without notation", TUNE),
            (r"the drawn glissandi of \textit{Metastaseis}, \ made audible directly", GREY_A),
        ]
        rows_scene(self, r"drawing sound", items,
                   "Xenakis also built a machine for composing by drawing. <bookmark mark='b'/> UPIC, finished in 1977, let a composer draw on a large tablet: <bookmark mark='c'/> lines became pitches moving in time, and drawn shapes became waveforms and envelopes. <bookmark mark='d'/> His Mycènes Alpha, of 1978, was drawn entirely this way. <bookmark mark='e'/> UPIC was used in workshops with children, composition without notation. <bookmark mark='f'/> It made the drawn glissandi of Metastaseis audible directly.", marks="cdef")
