from __future__ import annotations

import numpy as np

from videos.music.music2.common import *  # noqa: F403


class Decibel(SoundScene):
    def construct(self):
        chapter(self, 4, r"How loud", r"How do you put a number on loudness?", lit=(1863,),
                extra=((1928, r"the decibel, \ at Bell Laboratories"),))
        self.range()
        self.rules()
        self.choir()
        self.quiz()

    # ------------------------------------------------------------------
    def range(self):
        d = load("decibel")
        x0, x1 = -5.6, 5.6
        y0 = 0.9
        line = Line([x0, y0, 0], [x1, y0, 0], color=GREY_C, stroke_width=2)

        def X(db):
            return x0 + (x1 - x0) * db / 130.0

        ticks = VGroup(*[VGroup(Line([X(v), y0 - 0.1, 0], [X(v), y0 + 0.1, 0], color=GREY_C),
                                label(str(v), font_size=20, color=GREY_B).move_to([X(v), y0 - 0.35, 0])) for v in range(0, 131, 10)])
        unit = label(r"sound level, \ in decibels", font_size=22, color=LEVEL).move_to([0, y0 - 0.8, 0])
        short = [r"the faintest sound \\ a young ear hears", r"a whisper", r"talking, \\ at a metre", r"a full orchestra, \\ from the stalls", r"pain"]
        marks = VGroup()
        for i, r in enumerate(d["rows"]):
            dot = Dot([X(r["db"]), y0, 0], radius=0.08, color=LEVEL)
            t = label(short[i], font_size=24).next_to(dot, UP, buff=0.35)
            w = MathTex(r"10^{%d}\ \text{W/m}^2" % round(np.log10(r["w_m2"])), font_size=28, color=GREY_A).next_to(t, UP, buff=0.12)
            g = VGroup(t, w)
            if g.get_left()[0] < -6.8:
                g.shift(RIGHT * (-6.8 - g.get_left()[0]))
            if g.get_right()[0] > 6.8:
                g.shift(LEFT * (g.get_right()[0] - 6.8))
            marks.add(VGroup(dot, t, w))
        card = definition_card(
            r"Sound level, \ in decibels",
            MathTex(r"L \;=\; 10 \log_{10}\frac{I}{I_0} \;=\; 20 \log_{10}\frac{p}{p_0}", r"\qquad I_0 = 10^{-12}\ \text{W/m}^2,\quad "
                    r"p_0 = 20\ \mu\text{Pa}", font_size=34), width=11.6).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The honest measure of a sound's strength is its intensity: the power it carries through each square "
            "metre. <bookmark mark='a'/> The trouble is the range. The faintest sound a young ear can detect carries "
            "a millionth of a millionth of a watt per square metre. A sound that hurts carries ten watts. That is "
            "thirteen powers of ten, and the ear takes them all in its stride. <bookmark mark='b'/> So we count the "
            "powers of ten instead. Ten times the intensity is one bel, named for Alexander Graham Bell by "
            "telephone engineers in the nineteen twenties. A tenth of that is the decibel. <bookmark mark='c'/> "
            "Zero decibels is the threshold of hearing. Because intensity goes as pressure squared, the same number "
            "is twenty times the logarithm of the pressure."
        ) as vo:
            self.play(Create(line), FadeIn(ticks), FadeIn(unit), FadeIn(marks[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[1:]], lag_ratio=0.5), run_time=max(vo.until("b") - 0.3, 3.0))
            vo.wait_until("c")
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        c = clip("decibel.steps")
        rules = VGroup(
            VGroup(MathTex(r"+10\ \text{dB}", font_size=44, color=LEVEL), label(r"ten times the power", font_size=30)),
            VGroup(MathTex(r"+3\ \text{dB}", font_size=44, color=LEVEL), label(r"twice the power", font_size=30)),
            VGroup(MathTex(r"+6\ \text{dB}", font_size=44, color=LEVEL), label(r"twice the pressure, \ four times the power", font_size=30)),
        )
        for r in rules:
            r.arrange(RIGHT, buff=0.6)
        rules.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(LEFT * 2.6 + UP * 1.2)
        bars = VGroup(*[Rectangle(width=0.7, height=3.0 * 0.5 ** k, stroke_width=0, fill_color=LEVEL, fill_opacity=0.25)
                        for k in range(4)]).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to(RIGHT * 4.0 + DOWN * 0.2)
        tags = VGroup(*[label(t, font_size=22, color=GREY_B).next_to(b, DOWN, buff=0.12)
                        for t, b in zip(("0", "$-6$", "$-12$", "$-18$"), bars)])
        cap = label(r"pressure: \ halved at each step", font_size=24, color=GREY_A).next_to(bars, UP, buff=0.3)
        with self.voiceover(
            "Three rules of thumb are worth carrying for the rest of this series. Ten decibels is ten times the "
            "power. <bookmark mark='a'/> Three decibels is twice the power. <bookmark mark='b'/> And six decibels is "
            "twice the pressure, which is four times the power. <bookmark mark='c'/> Here is our string four times, "
            "each time with half the pressure of the time before: six decibels down, at every step."
        ) as vo:
            self.play(FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(FadeIn(rules[2]))
            vo.wait_until("c")
            self.play(FadeIn(bars), FadeIn(tags), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"0, \ $-6$, \ $-12$, \ $-18$ decibels", detail=r"each half the pressure of the last")
            for k in range(4):
                t0 = snd.time_of(f"s{k}")
                snd.wait_until(t0)
                snd.drive(bars[k], lambda m, t, t0=t0: m.set_fill(opacity=0.25 + 0.7 * float(np.exp(-1.6 * max(t - t0, 0)))
                                                                    if t0 <= t < t0 + 1.2 else 0.25))
                snd.wait_until(t0 + 1.15)
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choir(self):
        d = load("decibel")
        c = clip("decibel.choir")
        groups = VGroup()
        for k in (1, 2, 10):
            lines = VGroup(*[Line(LEFT * 1.3, RIGHT * 1.3, color=STR, stroke_width=3) for _ in range(k)]).arrange(DOWN, buff=0.16)
            groups.add(VGroup(lines, label(f"{k} string" + ("s" if k > 1 else ""), font_size=28).next_to(lines, UP, buff=0.25)))
        groups.arrange(RIGHT, buff=1.3, aligned_edge=UP).move_to(UP * 1.4)
        table = VGroup()
        for i, k in enumerate((1, 2, 10)):
            col = VGroup(
                MathTex(r"10\log_{10}%d = %.0f\ \text{dB}" % (k, d["expected"][str(k)]), font_size=30, color=GREY_A),
                label(rf"this group: \ $+{d['measured'][str(k)]:.1f}$ dB", font_size=26, color=LEVEL),
                label(rf"average of {d['trials']} groups: \ $+{d['mean'][str(k)]:.1f}$ dB" if k > 1 else r"", font_size=26, color=GOOD),
            ).arrange(DOWN, buff=0.18)
            col.next_to(groups[i], DOWN, buff=0.45)
            table.add(col)
        with self.voiceover(
            "Now a question with a surprising answer. If one string makes a certain level, what do ten strings "
            "make? <bookmark mark='a'/> Strings that are not exactly in step add their powers, not their pressures. "
            "So two strings give twice the power: three decibels. Ten give ten decibels. Listen: one, two, ten."
        ) as vo:
            self.play(FadeIn(groups))
            vo.wait_until("a")
            self.play(*[FadeIn(col[0]) for col in table])
        with self.listen(c) as snd:
            window(snd, r"one string, \ two, \ ten")
            for i, ev in enumerate(("one", "two", "ten")):
                t0 = snd.time_of(ev)
                snd.wait_until(t0)
                for ln in groups[i][0]:
                    lens = Lens(ln.get_start(), ln.get_end(), amp=0.07, color=TUNE)
                    snd.show(lens)
                    snd.drive(lens, ring(at=t0, rate=1.3, stop_at=t0 + 2.25))
                self.add(table[i][1])
        with self.voiceover(
            f"Ten strings, and the level rose by {say(d['measured']['10'], 1)} decibels, not by ten. Was the rule "
            "wrong? <bookmark mark='a'/> No. Strings that are nearly in tune add like dice. One group lands a little "
            f"high, another a little low. Average {say(d['trials'])} different groups and you get "
            f"{say(d['mean']['2'], 1)} and {say(d['mean']['10'], 1)}. <bookmark mark='b'/> Either way, ten players "
            "are nowhere near ten times as loud as one. Why ten decibels sounds only about twice as loud is a "
            "question about ears, and that is Part 4."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(table[1][2]), FadeIn(table[2][2]))
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("decibel")
        c = clip("decibel.quiz")
        q = listen_card(r"Two pairs of notes, \ A and B. \ In each pair the second note is louder. \\ "
                        r"In one pair it has twice the power, \ in the other four times. \ Which is which?", width=10.6)
        q.to_edge(UP, buff=0.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, stroke_color=GREY_C, stroke_width=2),
                                label(t, font_size=60, color=GREY_A)) for t in ("A", "B")]).arrange(RIGHT, buff=1.4).shift(DOWN * 0.7)
        with self.voiceover("A question for your ears. Two pairs of notes. In one pair the second note has twice the "
                            "power of the first. In the other it has four times. Which pair is which?"):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))
        with self.listen(c) as snd:
            window(snd, r"pair A, \ then pair B", tag_corner=DR)
            for key, box in zip("AB", boxes):
                for sub in ("a", "b"):
                    t0 = snd.time_of(f"{key}.{sub}")
                    snd.wait_until(t0)
                    box[1].set_color(EAR)
                    glow = box[0].copy().set_stroke(EAR, width=5)
                    snd.show(glow)
                    snd.drive(glow, lambda m, t, t0=t0: m.set_stroke(opacity=float(np.exp(-2.0 * max(t - t0, 0))) if t < t0 + 1.1 else 0.0))
                    snd.wait_until(t0 + 1.1)
                box[1].set_color(GREY_A)
        ans = VGroup(MathTex(r"+%d\ \text{dB}" % d["quiz_db"][0], font_size=44, color=LEVEL).next_to(boxes[0], DOWN, buff=0.3),
                     MathTex(r"+%d\ \text{dB}" % d["quiz_db"][1], font_size=44, color=LEVEL).next_to(boxes[1], DOWN, buff=0.3))
        with self.voiceover(
            f"{d['quiz_answer']} was the bigger step: six decibels, four times the power. A was three. If you found "
            "that hard, good. A change of one decibel is about the smallest you can notice at all, and three is a "
            "small step. Mixing engineers work in exactly these units."
        ):
            self.play(FadeIn(ans), boxes[1][0].animate.set_stroke(GOOD, width=4))
        self.wait(0.3)
        self.clear_scene()
