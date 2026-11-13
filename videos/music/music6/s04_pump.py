from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Pump(SoundScene):
    def construct(self):
        chapter(self, 3, r"The comma pump", r"Why did the music sink?", lit=(1584,), extra=((1585, r"Benedetti's puzzle"),))
        self.worked()
        self.rounds()
        self.moral()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("pump")
        chain = d["chain"]
        title = label(r"A worked example: \ once round, \ in pure chords", font_size=36).to_edge(UP, buff=0.4)
        names = {"C": r"C major", "A": r"A minor", "D": r"D minor", "G": r"G major"}
        order = {"C": ("C", "E", "G"), "A": ("A", "C", "E"), "D": ("D", "F", "A"), "G": ("G", "B", "D")}
        cols = VGroup()
        for k, ch in enumerate(chain):
            col = VGroup(label(names[ch["root"]], font_size=28, color=TUNE))
            for n in order[ch["root"]]:
                p, q = ch["notes"][n]
                col.add(VGroup(label(n, font_size=30), MathTex(rf"\tfrac{{{p}}}{{{q}}}" if q != 1 else str(p), font_size=30, color=RATIO)).arrange(RIGHT, buff=0.25))
            col.arrange(DOWN, buff=0.28)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.75, aligned_edge=UP).move_to(UP * 0.7)
        rule = label(r"the rule: \ a note that two chords share keeps its pitch", font_size=26, color=GREY_A).next_to(cols, DOWN, buff=0.4)
        ask = pause_card(r"The last chord is C major again, \ built on the G that was held. \\ What is its C, \ compared with the C we started on?", width=9.0).move_to(DOWN * 2.6)
        cp, cq = d["comma"]
        ans = MathTex(rf"\tfrac{{160}}{{81}} \div 2 = \tfrac{{80}}{{81}}: \quad \text{{a comma flat, }} {abs(d['per_round']):.1f}\ \text{{cents}}", font_size=38, color=BAD).move_to(DOWN * 2.6)
        links = VGroup()
        held = [("C", 0, 1), ("E", 0, 1), ("A", 1, 2), ("D", 2, 3), ("G", 3, 4)]
        for n, a, b in held:
            ia, ib = order[chain[a]["root"]].index(n) + 1, order[chain[b]["root"]].index(n) + 1
            links.add(Line(cols[a][ia].get_right(), cols[b][ib].get_left(), color=GOOD, stroke_width=2.5, buff=0.08))
        with self.voiceover(
            "Go round the progression once, slowly, in pure chords, keeping one rule: a note that two "
            "neighbouring chords share keeps its pitch. <bookmark mark='a'/> C major: C, E and G, at one, five "
            "quarters and three halves. <bookmark mark='b'/> A minor keeps the C and the E, and adds an A a pure "
            "fourth above the E: five thirds. <bookmark mark='c'/> D minor keeps that A, and needs a D a pure "
            "fifth below it. That is ten ninths. Not nine eighths, the D of the scale: ten ninths, a comma "
            "lower, because this D has to be in tune with A. <bookmark mark='d'/> G major keeps the D, so its G "
            "is a pure fourth above ten ninths: forty twenty-sevenths. <bookmark mark='e'/> And the last chord, "
            "C major, is built on that G. So what is its C, compared with the C we began on? Pause and work it "
            "out."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rule))
            for k, mark in enumerate("abcd"):
                vo.wait_until(mark)
                self.play(FadeIn(cols[k]), *([Create(l) for l, h in zip(links, held) if h[2] == k]), run_time=0.8)
            vo.wait_until("e")
            self.play(FadeIn(cols[4][0]), FadeIn(cols[4][3]), Create(links[4]), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A pure fifth below forty twenty-sevenths is eighty over eighty-one. <bookmark mark='a'/> The C has "
            f"come back one syntonic comma flat: {say(abs(d['per_round']), 1)} cents. Every step was a pure "
            "interval. The comma was hiding in the D. Going from C up a sixth, down a fifth, up a fourth and down "
            "a fifth is the same as going up one third and down four fifths, and we already know those do not "
            "cancel."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(cols[4][1]), FadeIn(cols[4][2]))
            vo.wait_until("a")
            self.play(FadeIn(ans), Indicate(cols[2][1], color=BAD, scale_factor=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rounds(self):
        d = load("pump")
        g = axes([0, 4.3], [-110, 8], x_length=8.4, y_length=3.6, xlabel=r"times round the progression", ylabel=r"the note C (cents)", xticks=[0, 1, 2, 3, 4],
                 yticks=[-100, -75, -50, -25, 0], font_size=20)
        g.move_to(LEFT * 1.4 + DOWN * 0.3)
        pts = [g.ax.c2p(k, v) for k, v in enumerate(d["drift"])]
        line = VMobject(stroke_color=BAD, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.08, color=BAD) for p in pts])
        semi = DashedLine(g.ax.c2p(0, -100), g.ax.c2p(4.3, -100), color=GREY_B, stroke_width=1.5)
        sl = label(r"a semitone flat", font_size=22, color=GREY_B).next_to(g.ax.c2p(4.3, -100), UP, buff=0.08).shift(LEFT * 1.0)
        card = history_card(1585, r"Giovanni Battista Benedetti",
                            r"a mathematician, in letters to the composer Cipriano de Rore: singers who keep their chords pure must drift, a comma at a time.",
                            width=4.6, font_size=20).to_corner(UR, buff=0.4)
        fact = VGroup(label(rf"once round: \ {abs(d['per_round']):.1f} cents", font_size=28, color=BAD), label(rf"four times: \ {abs(d['total']):.0f} cents", font_size=28, color=BAD),
                      label(r"five times: \ more than a semitone", font_size=28, color=BAD)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(card, DOWN, buff=0.5).align_to(card, LEFT)
        with self.voiceover(
            "That is what you heard at the start of this part. <bookmark mark='a'/> Each time round, another "
            f"comma. After four rounds, {say(abs(d['total']))} cents. A fifth time round, and the choir is more "
            "than a semitone flat, singing in a different key from the one it began in, and every chord on the "
            "way was flawless. <bookmark mark='b'/> The effect was worked out in the sixteenth century by the "
            "mathematician Giovanni Battista Benedetti, who sent it as a puzzle to the composer Cipriano de "
            "Rore. Musicians now call a progression like this a comma pump."
        ) as vo:
            self.play(FadeIn(g), FadeIn(semi), FadeIn(sl))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(p) for p in dots], lag_ratio=0.5), LaggedStart(*[FadeIn(f) for f in fact], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(card))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moral(self):
        rows = VGroup(
            label(r"pure fifths, \ all the way round", font_size=30, color=AIR), label(r"$\Rightarrow$ \ a wolf fifth, \ and restless thirds \quad (Pythagorean)", font_size=28, color=GREY_A),
            label(r"pure fifths and pure thirds", font_size=30, color=GOOD), label(r"$\Rightarrow$ \ two versions of some notes, \ and a pitch that will not stay put \quad (just)", font_size=28, color=GREY_A),
            label(r"so: \ which intervals shall we spoil, \ and by how much?", font_size=36, color=TUNE),
        ).arrange(DOWN, buff=0.3)
        rows[4].shift(DOWN * 0.4)
        with self.voiceover(
            "So here is where we stand. <bookmark mark='a'/> Keep every fifth pure, and you get a wolf, and "
            "thirds that will not sit still. <bookmark mark='b'/> Keep the fifths and the thirds both pure, and "
            "you need two versions of some notes, and the pitch will not stay put. For voices and violins, which "
            "can bend, that is a nuisance. For anything with fixed notes, an organ, a harpsichord, a fretted "
            "lute, it is fatal. <bookmark mark='c'/> A fixed instrument has to make some intervals deliberately "
            "impure, so that the commas are spread out and disappear. That is called tempering, and the only "
            "questions are which intervals to spoil, and by how much. History gave three answers."
        ) as vo:
            head = label(r"Where we stand", font_size=38, color=GREY_A).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), run_time=0.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()
