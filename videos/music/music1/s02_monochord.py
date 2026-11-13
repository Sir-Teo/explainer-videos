from __future__ import annotations

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (EAR, FREQ, GOOD, HIST, PART, RATIO, STR, TUNE, PairView, clip, load, ring,
                                        say, window)


class Monochord(SoundScene):
    def construct(self):
        self.card()
        self.instrument()
        self.stops()
        self.arithmetic()
        self.quiz()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"One string, four numbers", r"What can be measured on a monochord?", lit=(-530,),
                            part=PART)
        with self.voiceover("Chapter one. One string, four numbers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def instrument(self):
        c = clip("ratios.open")
        mono = MonochordView(width=11.0).shift(UP * 0.4)
        parts = VGroup(
            label(r"one string", font_size=28, color=STR).next_to(mono.x(0.5), UP, buff=0.45),
            label(r"a hollow box, \ to make it loud", font_size=26, color=GREY_A).next_to(mono.box, DOWN, buff=0.7),
            label(r"fixed here", font_size=24, color=GREY_B).next_to(mono.x(0.0), UP, buff=0.35),
            label(r"and here", font_size=24, color=GREY_B).next_to(mono.x(1.0), UP, buff=0.35),
        )
        name = VGroup(label(r"\textit{monochord}", font_size=54, color=STR),
                      label(r"Greek: \ one string. \quad The Greeks also called it the \textit{kanon}: the ruler.",
                            font_size=26, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The instrument could hardly be simpler. One string, stretched over a hollow box that makes it loud "
            "enough to hear, <bookmark mark='a'/> and fixed at both ends. Monochord just means one string. "
            "<bookmark mark='b'/> The Greeks had a second name for it, the kanon, which means the ruler, and that "
            "name is the better one. This is a measuring instrument. It turns a sound into a length you can read off "
            "a scale. <bookmark mark='c'/> Here is the open string."
        ) as vo:
            self.play(FadeIn(mono), FadeIn(parts[0]), FadeIn(parts[1]))
            vo.wait_until("a")
            self.play(FadeIn(parts[2]), FadeIn(parts[3]))
            vo.wait_until("b")
            self.play(FadeIn(name, shift=DOWN * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(parts))
        with self.listen(c) as snd:
            window(snd, r"the open string")
            lens = mono.lens(1.0, amp=0.22)
            snd.show(lens)
            snd.drive(lens, ring(rate=1.1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def stops(self):
        d = load("ratios")
        pair = PairView(0.5, width=5.9).move_to(LEFT * 3.5 + UP * 0.9)
        pair.bottom.set_stop(1.0)
        head = VGroup(*[label(t, font_size=26, color=GREY_B) for t in (r"length", r"interval", r"hertz", r"ratio")])
        xs = [0.9, 2.3, 4.2, 5.9]
        for h, x in zip(head, xs):
            h.move_to([x, 2.6, 0])
        rule = Line([0.4, 2.3, 0], [6.7, 2.3, 0], color=GREY_D, stroke_width=1)
        open_row = VGroup(MathTex(r"1", font_size=42, color=RATIO), label(r"(open)", font_size=30, color=GREY_A),
                          label(say(d["open_hz"], 1), font_size=34, color=FREQ), MathTex(r"1", font_size=42, color=FREQ))
        for cell, x in zip(open_row, xs):
            cell.move_to([x, 1.7, 0])
        with self.voiceover(
            "Now a second string just like it, with a bridge we can slide. The Greeks could measure only lengths. "
            "We can also measure how many times a second the string goes back and forth, its frequency, "
            f"<bookmark mark='a'/> in hertz. Our simulated string, open, makes {say(d['open_hz'], 1)} round trips "
            "a second."
        ) as vo:
            self.play(FadeIn(pair))
            vo.wait_until("a")
            self.play(FadeIn(head), Create(rule), FadeIn(open_row))
        lines = {
            "octave": "Stop it at one half. The octave: the same note, an octave up.",
            "fifth": "Two thirds of the string. The fifth: the jump that opens the Tune.",
            "fourth": "Three quarters. The fourth.",
        }
        names = {"octave": r"octave", "fifth": r"fifth", "fourth": r"fourth"}
        mark = None
        for i, key in enumerate(("octave", "fifth", "fourth")):
            r = d["rows"][key]
            p, q = r["stop"]
            frac = p / q
            new_mark = pair.bottom.mark(frac, rf"\tfrac{{{p}}}{{{q}}}", font_size=36)
            row = VGroup(MathTex(rf"\tfrac{{{p}}}{{{q}}}", font_size=42, color=RATIO),
                         label(names[key], font_size=30, color=WHITE),
                         label(say(r["hz"], 1), font_size=34, color=FREQ),
                         MathTex(rf"{r['ratio']:.3f}", font_size=38, color=FREQ))
            for cell, x in zip(row, xs):
                cell.move_to([x, 1.7 - 0.85 * (i + 1), 0])
            with self.voiceover(lines[key]):
                anims = [pair.bottom.move_bridge(frac), FadeIn(new_mark)]
                if mark is not None:
                    anims.append(FadeOut(mark))
                self.play(*anims, run_time=0.9)
                pair.stop = frac
                mark = new_mark
            with self.listen(clip(f"ratios.{key}")) as snd:
                window(snd, r"whole, \ stopped, \ both", detail=r"two strings, \ left and right")
                pair.play(self, snd)
                snd.wait_until("b")
                self.play(FadeIn(row[0]), FadeIn(row[1]), FadeIn(row[2]), run_time=0.5)
                snd.wait_until("both")
                self.play(FadeIn(row[3]), run_time=0.5)
        law = VGroup(label(r"frequency ratio", font_size=30, color=FREQ), MathTex(r"=", font_size=36),
                     MathTex(r"\frac{1}{\text{length ratio}}", font_size=38, color=RATIO)).arrange(RIGHT, buff=0.25)
        law.move_to([3.55, -2.4, 0])
        box = SurroundingRectangle(law, color=GOOD, buff=0.2, corner_radius=0.1, stroke_width=2)
        worst = max(abs(r["cents_off"]) for r in d["rows"].values())
        with self.voiceover(
            "Read the last column. Half the length, twice the frequency. Two thirds of the length, three halves the "
            "frequency. Three quarters, four thirds. <bookmark mark='a'/> The frequency ratio is the length ratio "
            f"turned upside down, and on our string it holds to within {say(max(worst, 0.1), 1)} cents, where a "
            "cent is a hundredth of a semitone. Nobody told the simulation that. We will see what it was told."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(law), Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def arithmetic(self):
        d = load("ratios")
        defn = definition_card(r"Interval", r"the ratio of two frequencies. \ An octave is $2:1$, \ a fifth $3:2$, \ "
                               r"a fourth $4:3$.", color=RATIO, width=7.6, font_size=28).to_edge(UP, buff=0.4)
        mono = MonochordView(width=10.4).shift(DOWN * 0.4)
        a = mono.brace(0.0, 2 / 3, r"\tfrac{2}{3}", up=True)
        b = mono.brace(0.0, 0.5, r"\tfrac{3}{4} \text{ of } \tfrac{2}{3} = \tfrac{1}{2}", up=True)
        eq = MathTex(r"\tfrac{3}{2}", r"\times", r"\tfrac{4}{3}", r"=", r"2", font_size=54).move_to(DOWN * 2.6)
        eq[0].set_color(RATIO), eq[2].set_color(RATIO), eq[4].set_color(GOOD)
        words = VGroup(label(r"a fifth,", font_size=26, color=GREY_A), label(r"then a fourth,", font_size=26, color=GREY_A),
                       label(r"is an octave", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.25)
        words.next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "So here is the definition the whole series will use. An interval is a ratio of two frequencies. "
            "<bookmark mark='a'/> And ratios do not add, they multiply. Go up a fifth: keep two thirds of the string. "
            "<bookmark mark='b'/> Then up a fourth from there: keep three quarters of what is left. Three quarters "
            "of two thirds is one half. <bookmark mark='c'/> A fifth and then a fourth make exactly an octave."
        ) as vo:
            self.play(FadeIn(defn, shift=DOWN * 0.2), FadeIn(mono))
            vo.wait_until("a")
            self.play(mono.move_bridge(2 / 3), FadeIn(a), FadeIn(eq[0]), FadeIn(words[0]))
            vo.wait_until("b")
            self.play(mono.move_bridge(0.5), ReplacementTransform(a, b), FadeIn(eq[1:3]), FadeIn(words[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq[3:]), FadeIn(words[2]))
        eq2 = MathTex(r"\tfrac{3}{2}", r"\div", r"\tfrac{4}{3}", r"=", r"\tfrac{9}{8}", font_size=54).move_to(eq)
        eq2[0].set_color(RATIO), eq2[2].set_color(RATIO), eq2[4].set_color(TUNE)
        tone = label(r"the tone: \ the step from the fourth to the fifth", font_size=28, color=TUNE)
        tone.next_to(eq2, DOWN, buff=0.3)
        tet = VGroup(*[VGroup(*[Dot(radius=0.07, color=HIST) for _ in range(k)]).arrange(RIGHT, buff=0.22)
                       for k in (1, 2, 3, 4)]).arrange(DOWN, buff=0.2).to_corner(DR, buff=0.7)
        tname = label(r"1, 2, 3, 4", font_size=26, color=HIST).next_to(tet, UP, buff=0.2)
        with self.voiceover(
            "And the gap between them, a fifth divided by a fourth, <bookmark mark='a'/> is nine to eight. The Greeks "
            "called it the tone. It is the step between the fourth and the fifth notes of the scale."
        ) as vo:
            self.play(FadeOut(eq), FadeOut(words), FadeOut(b), mono.move_bridge(0.75))
            vo.wait_until("a")
            self.play(FadeIn(eq2), FadeIn(tone))
        with self.listen(clip("ratios.tone")) as snd:
            window(snd, r"the fourth, \ then the fifth")
            l1, l2 = mono.lens(0.75, amp=0.2), mono.lens(2 / 3, amp=0.2)
            snd.show(l1, l2)
            snd.drive(l1, ring(at=snd.time_of("fourth"), rate=1.8, stop_at=snd.time_of("fifth")))
            snd.drive(l2, ring(at=snd.time_of("fifth"), rate=1.8))
            snd.wait_until("fifth")
            mono.set_stop(2 / 3)
        with self.voiceover(
            "Octave, fifth, fourth and tone: all of it from the numbers one, two, three and four. "
            "<bookmark mark='a'/> The Pythagoreans drew those numbers as a triangle of ten dots and swore oaths by "
            "it. You can see why they thought they had found the key to everything."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tet), FadeIn(tname))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("ratios")
        q = listen_card(r"Two pairs of notes, \ A and B. \ Each starts on the open string. \\ "
                        r"Which pair is the fifth?", width=9.2).to_edge(UP, buff=0.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.6, corner_radius=0.15, stroke_color=GREY_C,
                                                 stroke_width=2), label(t, font_size=60, color=GREY_A))
                         for t in ("A", "B")]).arrange(RIGHT, buff=1.4).shift(DOWN * 0.8)
        with self.voiceover(
            "Before we go on, a first question for your ears. Two pairs of notes. Which pair is the fifth?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))
        with self.listen(clip("ratios.quiz")) as snd:
            window(snd, r"A, \ then B")
            for key, box in zip("AB", boxes):
                snd.wait_until(key)
                self.play(box[0].animate.set_stroke(EAR, width=4), box[1].animate.set_color(EAR), run_time=0.2)
                snd.wait_until(snd.time_of(key) + 2.6)
                self.play(box[0].animate.set_stroke(GREY_C, width=2), box[1].animate.set_color(GREY_A), run_time=0.2)
        ans = VGroup(MathTex(r"\tfrac{3}{4}", font_size=44, color=RATIO), label(r"the fourth", font_size=28)).arrange(DOWN, buff=0.15)
        ans.next_to(boxes[0], DOWN, buff=0.3)
        ans2 = VGroup(MathTex(r"\tfrac{2}{3}", font_size=44, color=RATIO), label(r"the fifth", font_size=28, color=GOOD)).arrange(DOWN, buff=0.15)
        ans2.next_to(boxes[1], DOWN, buff=0.3)
        with self.voiceover(
            f"It was {d['quiz_answer']}. The second pair went further up: the bridge at two thirds. "
            "<bookmark mark='a'/> If you sang the Tune's first jump to yourself to check, that is exactly what a "
            "musician does. So, four numbers and three intervals. But why should length set the pitch at all, and is "
            "length the only thing that does?"
        ) as vo:
            self.play(FadeIn(ans), FadeIn(ans2), boxes[1][0].animate.set_stroke(GOOD, width=4))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()
