from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Equal(SoundScene):
    def construct(self):
        chapter(self, 6, r"Equal", r"What if every key is treated the same?", lit=(1584,), extra=((1636, r"Mersenne prints the numbers"),))
        self.idea()
        self.zhu()
        self.cost()
        self.tuner()
        self.won()

    # ------------------------------------------------------------------
    def idea(self):
        d = load("equal")
        circ = FifthsCircle(radius=1.8).move_to(LEFT * 4.0 + DOWN * 0.4)
        edges = VGroup(*[circ.edge(k, color=error_color(-2.0, 8.0), stroke_width=6) for k in range(12)])
        steps = VGroup(*[MathTex(rf"{s['ratio']:.4f}", font_size=24, color=TUNE if s["k"] in (0, 12) else GREY_A) for s in d["steps"]]).arrange_in_grid(2, 7, buff=(0.35, 0.25))
        steps.move_to(RIGHT * 2.6 + DOWN * 1.9)
        eq = VGroup(MathTex(r"r \times r \times \cdots \times r = r^{12} = 2", font_size=40), MathTex(r"r = \sqrt[12]{2} = " + d["root"][:12] + r"\ldots", font_size=40, color=TUNE)).arrange(DOWN, buff=0.3).move_to(RIGHT * 2.6 + UP * 1.5)
        sl = label(r"each note is the one before, \ times $r$:", font_size=24, color=GREY_B).next_to(steps, UP, buff=0.25).align_to(steps, LEFT)
        card = history_card(1584, r"Zhu Zaiyu", r"computes $r$, and builds pipes and strings to the lengths it gives. In Europe, Simon Stevin works out the same scheme within a few years.", width=5.2, font_size=20)
        card.to_corner(UL, buff=0.35)
        with self.voiceover(
            "The third answer is the simplest of all, and the most radical. Stop choosing. Take the Pythagorean "
            "comma and share it equally among all twelve fifths: two cents from each. <bookmark mark='a'/> Then "
            "every fifth is the same, every key is the same, and the twelve notes divide the octave into twelve "
            "identical steps. <bookmark mark='b'/> Each step multiplies the frequency by the same number, and "
            "twelve steps must make exactly two. So that number is the twelfth root of two. This is what Zhu "
            "Zaiyu computed in 1584, by taking square roots and cube roots on his abacus. <bookmark mark='c'/> In "
            "Europe the Flemish engineer Simon Stevin worked out the same scheme within a few years, less "
            "accurately, and never published it. Note what kind of number this is. Every earlier tuning was "
            "built from ratios of whole numbers. This one has no whole-number ratios in it at all, except the "
            "octave."
        ) as vo:
            self.play(FadeIn(circ))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(eq[0]))
            self.play(FadeIn(eq[1]), FadeIn(sl), LaggedStart(*[FadeIn(x) for x in steps], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("c")
            self.play(circ.animate.shift(DOWN * 0.9), edges.animate.shift(DOWN * 0.9), FadeIn(card))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zhu(self):
        d = load("equal")
        r = d["roots"]
        title = label(r"A worked example: \ a twelfth root on an abacus, \ and a guitar", font_size=36).to_edge(UP, buff=0.4)
        roots = VGroup(MathTex(rf"\sqrt{{2}} = {r['sqrt2']:.5f}", font_size=34), MathTex(rf"\sqrt{{{r['sqrt2']:.5f}}} = {r['sqrt_sqrt2']:.5f}", font_size=34),
                       MathTex(rf"\sqrt[3]{{{r['sqrt_sqrt2']:.5f}}} = {r['cbrt']:.5f}", font_size=34, color=TUNE),
                       label(r"a square root, \ a square root, \ a cube root: \ $2 \times 2 \times 3 = 12$", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(LEFT * 3.6 + UP * 1.2)
        neck = Rectangle(width=9.6, height=0.7, stroke_color=GREY_B, stroke_width=2, fill_color="#3B2A1A", fill_opacity=0.6).move_to(DOWN * 1.9)
        left = neck.get_left()
        frets = VGroup(*[Line(left + RIGHT * 9.6 * (f["from_nut_mm"] / (d["scale_mm"] / 2)) * 0.5 * 2 * 0.5 + UP * 0.35, left + RIGHT * 9.6 * (f["from_nut_mm"] / (d["scale_mm"] / 2)) * 0.5 + DOWN * 0.35,
                               color=GREY_A, stroke_width=3) for f in d["frets"][1:]])
        for ln, f in zip(frets, d["frets"][1:]):
            x = left + RIGHT * 9.6 * f["from_nut_mm"] / (d["scale_mm"] / 2)
            ln.put_start_and_end_on(x + UP * 0.35, x + DOWN * 0.35)
        nl = label(r"nut", font_size=20, color=GREY_B).next_to(left, LEFT, buff=0.12)
        tw = label(r"12th fret: \ half the string", font_size=20, color=GREY_B).next_to(neck.get_right(), UP, buff=0.45).shift(LEFT * 0.7)
        ask = pause_card(rf"A guitar string is {d['scale_mm']:.0f} mm long. \\ Each fret must raise the pitch by one equal semitone. \ How far from the nut is the first fret?", width=6.6, font_size=26).move_to(RIGHT * 3.3 + UP * 1.2)
        ans = VGroup(MathTex(rf"L\,\bigl(1 - \tfrac{{1}}{{{r['cbrt']:.5f}}}\bigr) = {d['first_fret_mm']:.1f}\ \text{{mm}}", font_size=34, color=GOOD),
                     label(rf"each fret: \ $\tfrac{{1}}{{{d['rule']:.2f}}}$ of what is left", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.3 + UP * 1.1)
        with self.voiceover(
            "How do you take a twelfth root with an abacus? Twelve is two times two times three. "
            "<bookmark mark='a'/> So take the square root of two, which is one point four one four. Take the "
            "square root of that: one point one eight nine. Then take the cube root of that, and you have it: "
            "one point nought five nine five. Zhu did each step by hand, digit by digit, to twenty-five figures. "
            "<bookmark mark='b'/> And here is where that number is used every day. A guitar's frets cross all "
            "six strings, so each fret must raise every string by the same interval: one equal semitone. On a "
            f"string {say(d['scale_mm'])} millimetres long, how far from the nut does the first fret go? Pause "
            "and work it out."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in roots], lag_ratio=0.7), run_time=7.0)
            vo.wait_until("b")
            self.play(FadeIn(neck), FadeIn(nl), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            "A string sounds a semitone higher when it is shorter by the twelfth root of two. So the sounding "
            f"length becomes the full length divided by one point nought five nine five, and the fret sits "
            f"{say(d['first_fret_mm'], 1)} millimetres from the nut. <bookmark mark='a'/> The second fret takes "
            "the same fraction of what is left, and so on, each fret a little closer than the last, until the "
            "twelfth lands exactly on the middle of the string. Instrument makers call it the rule of eighteen, "
            f"because each fret takes off about one part in {say(d['rule'], 1)}. Every guitar in the world is a "
            "ruler marked in twelfth roots of two."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans[0]), Create(frets[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(f) for f in frets[1:]], lag_ratio=0.25), FadeIn(ans[1]), FadeIn(tw), run_time=4.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        d = load("equal")
        c = clip("equal.third")
        q = listen_card(r"Two major thirds on middle C, \ A and B. \\ One is pure. \ The other is the piano's. \ Which is which?", width=9.2).to_edge(UP, buff=0.4)
        bx = boxes(buff=1.8, width=3.0, height=1.4).move_to(DOWN * 0.2)
        with self.voiceover(
            "What does it cost? Two cents on every fifth is almost nothing: a beat every second or so. The cost "
            "is in the thirds. Here are two major thirds on middle C. One is pure. The other is the third of "
            "every piano you have ever heard. Which is which?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"third A, \ then third B", kind="synthesized", detail=r"tones of seven partials", corner=DL, tag_corner=DR)
            for ev, b in zip("AB", bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.6)
        ans = VGroup(VGroup(label(r"pure: \ 5 to 4", font_size=30, color=GOOD), label(r"still", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.1).next_to(bx[0], DOWN, buff=0.25),
                     VGroup(label(rf"equal: \ {d['third_error']:.1f} cents wide", font_size=30, color=BAD), label(rf"beats {abs(d['third_beat']):.0f} times a second", font_size=26, color=GREY_A)
                            ).arrange(DOWN, buff=0.1).next_to(bx[1], DOWN, buff=0.25))
        table = VGroup(label(rf"every fifth: \ {abs(d['fifth_error']):.1f} cents narrow", font_size=28, color=NARROW),
                       label(rf"every major third: \ {d['third_error']:.1f} cents wide", font_size=28, color=BAD),
                       label(r"every key: \ exactly the same", font_size=28, color=GOOD)).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A was pure. B is equal-tempered, and it shimmers: its partials beat about ten times a second. "
            f"<bookmark mark='a'/> Every major third in equal temperament is {say(d['third_error'], 1)} cents "
            "wide, two thirds of a comma, in every key. If you have never noticed, it is because you have never "
            "heard anything else from a piano. It is a real loss, and many musicians of the eighteenth century "
            "refused to accept it. <bookmark mark='b'/> What you buy with it is complete freedom. Any piece can "
            "be played in any key, and sounds the same in all of them."
        ) as vo:
            self.play(FadeOut(q), FadeIn(ans))
            vo.wait_until("a")
            self.play(FadeIn(table[0]), FadeIn(table[1]))
            vo.wait_until("b")
            self.play(FadeIn(table[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tuner(self):
        d = load("equal")
        w = d["worked"]
        title = label(r"A worked example: \ how do you tune a twelfth root of two by ear?", font_size=34).to_edge(UP, buff=0.4)
        ask = pause_card(rf"In equal temperament, \ A below middle C is {w['low_hz']:.0f} Hz and the E above it is {w['high_hz']:.2f} Hz. \\ "
                         r"A pure fifth would have its second partial on the lower note's third. \ How fast does this one beat?", width=10.4, font_size=26).move_to(UP * 1.4)
        work = VGroup(MathTex(rf"3 \times {w['low_hz']:.0f} = {3 * w['low_hz']:.2f}", font_size=34), MathTex(rf"2 \times {w['high_hz']:.2f} = {2 * w['high_hz']:.2f}", font_size=34),
                      MathTex(rf"\text{{difference: }} {abs(w['beats']):.2f}\ \text{{beats a second}}", font_size=36, color=GOOD)).arrange(DOWN, buff=0.22).move_to(LEFT * 3.4 + UP * 0.9)
        rows = VGroup()
        for r in d["table"]:
            rows.add(VGroup(label(rf"{r['low']} -- {r['high']}", font_size=24), label(r["kind"], font_size=24, color=GREY_A),
                            label(rf"{abs(r['beats']):.1f} a second, \ " + (r"wide" if r["beats"] > 0 else r"narrow"), font_size=24, color=WIDE if r["beats"] > 0 else NARROW)))
        for k, r in enumerate(rows):
            r[0].move_to(RIGHT * 0.4 + UP * (1.9 - 0.52 * k), aligned_edge=LEFT)
            r[1].move_to(RIGHT * 2.3 + UP * (1.9 - 0.52 * k), aligned_edge=LEFT)
            r[2].move_to(RIGHT * 4.3 + UP * (1.9 - 0.52 * k), aligned_edge=LEFT)
        note = label(r"a tuner carries this table in the head, \ and counts", font_size=28, color=EAR).move_to(DOWN * 2.6)
        with self.voiceover(
            "A worked example, because it answers an obvious question. Nobody can hear a twelfth root of two. So "
            "how is a piano tuned to it? By the beats of Part 5. Take the A below middle C, two hundred and "
            f"twenty hertz, and the E above it, which should be {say(w['high_hz'], 2)}. If the fifth were pure, "
            "the second partial of the E would sit exactly on the third partial of the A. How fast does the "
            "tempered fifth beat? Pause and work it out."
        ):
            self.play(FadeIn(title), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"Three times two hundred and twenty is six hundred and sixty. Twice the E is {say(2 * w['high_hz'], 2)}. "
            f"<bookmark mark='a'/> They differ by {say(abs(w['beats']), 2)} hertz: three beats in four seconds. A "
            "tuner sets the E so that the fifth beats at just that rate, slightly narrow. <bookmark mark='b'/> "
            "And so on through the middle octave: each fifth a little narrow, each fourth a little wide, with "
            "the major thirds as a check, beating seven, eight, ten times a second as they climb. "
            "<bookmark mark='c'/> A piano tuner carries this table in the head, and counts. The twelfth root of "
            "two is tuned with a watch."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(work[0]), FadeIn(work[1]))
            vo.wait_until("a")
            self.play(FadeIn(work[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def won(self):
        rows = rows_card([
            (r"1584", r"Zhu Zaiyu computes it; \ within a few years, \ Stevin"),
            (r"1636", r"Mersenne prints the string lengths in \textit{Harmonie universelle}; \\ lutes and viols, \ whose frets cross all the strings, \ already use it, \ roughly"),
            (r"1700s", r"keyboards are tuned in meantone and well temperaments; \\ equal temperament is known, \ and widely disliked for its thirds"),
            (r"1800s", r"music modulates everywhere; \ pianos are made in factories; \\ by the end of the century equal temperament is the standard"),
        ], left=-6.3, text_left=-4.3, top=1.7, step=1.3, name_size=30, text_size=24, color=HIST)
        head = label(r"Three centuries to win", font_size=38, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "It took three centuries to win. <bookmark mark='a'/> The arithmetic was known by the 1580s. "
            "<bookmark mark='b'/> By 1636 Marin Mersenne had printed the string lengths, and fretted instruments "
            "were already close to it for a practical reason: a fret crosses all the strings, so every string "
            "must use the same steps. <bookmark mark='c'/> But keyboards went on being tuned in meantone and "
            "then in well temperaments through the eighteenth century. Equal temperament was known, and widely "
            "disliked for its thirds. <bookmark mark='d'/> It won in the nineteenth century, when music began to "
            "modulate without limit and pianos began to be made in factories. By the end of that century it was "
            "the standard, and it has stayed so. It is not the tuning in which most of the classical repertoire "
            "was conceived. It is the one in which all of it can be played."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
