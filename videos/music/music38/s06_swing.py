from __future__ import annotations

import numpy as np

from videos.music.music38.common import *  # noqa: F403
from explainer.music.monochord import blues as BL


class Swing(SoundScene):
    def construct(self):
        chapter(self, 5, r"Swing, \ measured", r"Can swing be measured?")
        self.ratio_plot()
        self.tempos()
        self.studies()
        self.delay()
        self.groove()

    # ------------------------------------------------------------------
    def ratio_plot(self):
        d = load("swing")
        tab = d["table"]
        x0, x1, y0, y1 = -5.6, -0.4, -2.2, 1.8
        def X(b):
            return x0 + (x1 - x0) * (b - 100) / 220.0
        def Y(r):
            return y0 + (y1 - y0) * (r - 0.8) / 2.8
        ax = VGroup(Line([x0, y0, 0], [x1, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y1, 0], color=GREY_B))
        for b in (100, 160, 220, 280):
            ax.add(label(str(b), font_size=16, color=GREY_A).move_to([X(b), y0 - 0.3, 0]))
        for r in (1, 2, 3):
            ax.add(label(f"{r}:1", font_size=16, color=GREY_A).move_to([x0 - 0.45, Y(r), 0]))
            ax.add(DashedLine([x0, Y(r), 0], [x1, Y(r), 0], color=GREY_D, stroke_width=1))
        curve = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([[X(t["bpm"]), Y(t["ratio"]), 0] for t in tab])
        xl = label(r"tempo \ (beats a minute)", font_size=17, color=GREY_A).move_to([(x0 + x1) / 2, y0 - 0.7, 0])
        tl = label(r"long : short", font_size=19, color=TUNE).move_to([x0 + 1.0, y1 + 0.3, 0])
        # the short note's length in milliseconds
        u0, u1 = 0.8, 5.8
        def U(b):
            return u0 + (u1 - u0) * (b - 100) / 220.0
        def V(ms):
            return y0 + (y1 - y0) * (ms - 60) / 100.0
        ax2 = VGroup(Line([u0, y0, 0], [u1, y0, 0], color=GREY_B), Line([u0, y0, 0], [u0, y1, 0], color=GREY_B))
        for b in (100, 160, 220, 280):
            ax2.add(label(str(b), font_size=16, color=GREY_A).move_to([U(b), y0 - 0.3, 0]))
        for ms in (80, 100, 120, 140):
            ax2.add(label(str(ms), font_size=16, color=GREY_A).move_to([u0 - 0.4, V(ms), 0]))
        curve2 = VMobject(color=EAR, stroke_width=4).set_points_as_corners([[U(t["bpm"]), V(t["short_ms"]), 0] for t in tab])
        xl2 = label(r"tempo \ (beats a minute)", font_size=17, color=GREY_A).move_to([(u0 + u1) / 2, y0 - 0.7, 0])
        tl2 = label(r"the short note \ (milliseconds)", font_size=19, color=EAR).move_to([u0 + 1.8, y1 + 0.3, 0])
        head = label(r"the model: \ a straight line through the measured trend", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Monochord's swing model is deliberately simple. <bookmark mark='a'/> The ratio of long to short is three to one "
            "at a hundred and twenty beats a minute and falls in a straight line to one to one, even eighths, at three "
            "hundred. That is the trend that Anders Friberg and Johan Sundström measured in 2002 on drummers' ride cymbals in "
            "jazz recordings, drawn as a line rather than fitted to their points. <bookmark mark='b'/> Now look at what it "
            "implies for the short note: above about a hundred and sixty beats a minute it stays close to a tenth of a "
            "second, whatever the tempo. Friberg and Sundström reported the same: at medium and fast tempos the short note "
            "keeps a roughly constant length, as if it were a unit of its own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(ax, curve).copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(tl), Create(curve))
            vo.wait_until("b")
            self.play(FadeIn(ax2), FadeIn(xl2), FadeIn(tl2), Create(curve2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tempos(self):
        d = load("swing")
        c = clip("swing.tempos")
        rows_ = VGroup()
        for b in d["tempos"]:
            r = d["ratios"][str(b)]
            beat = 60.0 / b
            ts = BL.swing_times(d["pattern"], b) % (4 * beat)
            W = 7.0
            ticks = VGroup(*[Line([W * k / 4, -0.3, 0], [W * k / 4, 0.3, 0], color=GREY_B, stroke_width=2) for k in range(5)])
            dots = VGroup(*[Dot([W * t / (4 * beat), 0, 0], radius=0.1, color=TUNE) for t in ts])
            row = VGroup(label(rf"{b} a minute: \ {r:.1f} to 1", font_size=19, color=WHITE), VGroup(ticks, dots)).arrange(RIGHT, buff=0.5)
            row.dots = dots
            rows_.add(row)
        rows_.arrange(DOWN, buff=0.6, aligned_edge=RIGHT).move_to(UP * 0.2)
        head = label(r"the ride pattern, \ one bar, \ three tempos", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"ding, \ ding-a ding, \ ding-a: \ the second note of each pair moves towards the middle as the tempo rises", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Hear the model at three tempos: the ride cymbal's pattern, ding, ding-a ding, with walking bass and hi-hat, at a "
            "hundred, a hundred and eighty, and two hundred and sixty beats a minute. Watch the short note of each pair: at "
            "the slow tempo it hugs the next beat; at the fast tempo it moves nearly to the middle."
        ):
            self.play(FadeIn(head), FadeIn(rows_), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"three tempos", detail=r"string and cymbal models", corner=DL, tag_corner=DR)
            for i, b in enumerate(d["tempos"]):
                t0 = d["starts"][str(b)]
                beat = 60.0 / b
                for bar in range(4):
                    ts = BL.swing_times(d["pattern"], b) + t0 + bar * 4 * beat
                    flash(snd, list(rows_[i].dots), list(ts), hot=WHITE, base=TUNE)
                end = d["starts"][str(d["tempos"][i + 1])] - 0.4 if i < 2 else c.duration
                pulse(snd, rows_[i][0], t0, end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def studies(self):
        items = [
            (r"Friberg and Sundstr\"om \ (2002): \ drummers' ride cymbals in recordings, \ measured note by note", WHITE),
            (r"the ratio falls as the tempo rises; \ soloists often swing less than their drummers", WHITE),
            (r"Fernando Benadon \ (2006): \ soloists' ratios vary widely within a single solo", WHITE),
            (r"swing is not one ratio: \ it is a range, \ tied to tempo, \ player and phrase", TUNE),
            (r"a written `triplet feel' is a rough guide, \ not a description", GREY_A),
        ]
        rows_scene(self, r"what the measurements say", items,
                   "What else did the measurements find? <bookmark mark='b'/> Friberg and Sundström measured drummers' ride "
                   "cymbals in recordings, note by note. <bookmark mark='c'/> The ratio falls as the tempo rises, and soloists "
                   "often swing less than their drummers. <bookmark mark='d'/> Fernando Benadon found in 2006 that soloists' "
                   "ratios vary widely even within one solo. <bookmark mark='e'/> So swing is not one ratio but a range, tied to "
                   "tempo, player and phrase, <bookmark mark='f'/> and the triplet feel written at the top of a jazz chart is a "
                   "rough guide, not a description.", marks="cdef")

    # ------------------------------------------------------------------
    def delay(self):
        d = load("delay")
        W = 11.0
        beat = 60.0 / d["bpm"]
        r = d["ratio"]
        def row(delay, col, name):
            ticks = VGroup(*[Line([W * k / 8 - W / 2, -0.35, 0], [W * k / 8 - W / 2, 0.35, 0], color=GREY_B, stroke_width=2) for k in range(9)])
            dots = VGroup()
            for k in range(8):
                for e, dl in ((0, delay), (r / (1 + r), 0.0)):
                    x = W * (k + e + dl / 1000.0 / beat * 6) / 8 - W / 2
                    dots.add(Dot([x, 0, 0], radius=0.09, color=col))
            return VGroup(label(name, font_size=19, color=col), VGroup(ticks, dots)).arrange(DOWN, buff=0.2)
        a = row(0.0, BLUE, r"on time")
        b = row(d["delay_ms"], TUNE, rf"downbeats {d['delay_ms']:.0f} ms late \ (drawn six times larger)")
        g = VGroup(a, b).arrange(DOWN, buff=0.5).move_to(UP * 0.3)
        head = label(r"late downbeats, \ on-time off-beats", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "There is a second ingredient. A 2022 study by Corentin Nelias, Theo Geisel and colleagues measured jazz "
            "soloists against their rhythm sections, and reported that soloists' downbeats came slightly late while their "
            "off-beats stayed in time with the band; in their listening tests, delaying downbeats made solos swing more. "
            "Here is a line of ours played both ways, the second with its on-beat notes thirty milliseconds late, a value "
            "chosen to illustrate the idea, not taken from the study."
        ):
            self.play(FadeIn(head), FadeIn(g))
        for name, row_ in (("ontime", a), ("late", b)):
            c = clip("delay.ontime") if name == "ontime" else clip("delay.late")
            with self.listen(c) as snd:
                window(snd, {"ontime": r"on time", "late": r"late downbeats"}[name], kind="synthesized", detail=r"an additive saxophone, \ string and cymbal models", corner=DL, tag_corner=DR)
                pulse(snd, row_, 0.0, c.duration, buff=0.1)
            self.wait(0.3)
        ans = label(r"the late version sits back: \ `laid back', \ in players' words", font_size=21, color=TUNE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "To many listeners the second version sits back from the beat, the effect players call laid back. Thirty "
            "milliseconds is far too short to hear as lateness; it is heard as feel."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groove(self):
        items = [
            (r"Charles Keil \ (1987): \ `participatory discrepancies', \ the small timing differences between players", WHITE),
            (r"a groove is made of agreements and disagreements about where the beat is", WHITE),
            (r"perfect quantization, \ every note on the grid, \ tends to sound stiff", WHITE),
            (r"swing lives in tens of milliseconds, \ below the threshold of hearing a delay as a delay", TUNE),
            (r"chapter 10 asks what corpora of recorded jazz can settle", GREY_A),
        ]
        rows_scene(self, r"groove", items,
                   "The ethnomusicologist Charles Keil argued in 1987 that groove comes from participatory discrepancies, the "
                   "small timing differences between players. <bookmark mark='b'/> A groove is made of agreements and "
                   "disagreements about where the beat is. <bookmark mark='c'/> Perfect quantization, every note on the grid, "
                   "tends to sound stiff. <bookmark mark='d'/> Swing lives in tens of milliseconds, below the threshold at which "
                   "a delay is heard as a delay. <bookmark mark='e'/> Chapter ten asks what large collections of recorded jazz "
                   "can settle.", marks="bcde")
