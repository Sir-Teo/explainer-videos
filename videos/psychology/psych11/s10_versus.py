from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Versus(VoiceoverScene):
    def construct(self):
        self.card()
        self.two()
        self.curves()
        self.middle()
        self.range_()

    def card(self):
        card = chapter_card(9, r"Fechner against Stevens", r"A logarithm or a power: \ which is the law of sensation?",
                            lit={1860: r"Fechner", 1957: r"Stevens"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter nine. Fechner against Stevens."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two(self):
        d = load("fechner")
        head = heading(r"Same Weber, \ two assumptions")
        left = VGroup(
            label(r"Fechner", font_size=36, color=FECHC),
            wrapped_label(r"every just noticeable step is the same amount of sensation", 5.4, 29, WHITE),
            MathTex(r"\Delta S = \text{const}", font_size=40, color=FECHC),
            MathTex(r"\frac{dS}{dI} \propto \frac{1}{I}", font_size=40),
            MathTex(r"S \propto \ln I", font_size=48, color=THRESH),
        ).arrange(DOWN, buff=0.35)
        right = VGroup(
            label(r"Ekman, \ for Stevens", font_size=36, color=STEVC),
            wrapped_label(r"every step is a fixed share of the sensation already there", 5.4, 29, WHITE),
            MathTex(r"\Delta S = c\,S", font_size=40, color=STEVC),
            MathTex(r"\frac{dS}{S} = \frac{c}{k}\,\frac{dI}{I}", font_size=40),
            MathTex(r"S \propto I^{\,c/k}", font_size=48, color=THRESH),
        ).arrange(DOWN, buff=0.35)
        for g in (left, right):
            if g[1].width > 5.8:
                g[1].width = 5.8
        left.move_to([-3.4, 0.0, 0])
        right.move_to([3.4, 0.0, 0])
        both = MathTex(r"\text{both start from Weber:}\ \ \Delta I = k\,I", font_size=34, color=WEBERC).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here's the quarrel, and it fits on one screen. Both sides accept Weber's law. "
            "<bookmark mark='a'/> Fechner assumed every just noticeable step is the same amount of "
            "sensation. Integrate, and you get a logarithm. <bookmark mark='b'/> Stevens's camp, in the "
            "form the Swedish psychologist Gösta Ekman gave it, assumed instead that every step is a fixed "
            "share of the sensation already there: a big sensation has big steps. Integrate that, and you "
            "get a power law, with an exponent equal to the ratio of the two fractions. "
            "<bookmark mark='c'/> The same Weber's law, and two laws of sensation. What decides between "
            "them is not the steps, but an assumption about what a step is worth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(both))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in left], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.1) for x in right], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("c")
            self.play(Indicate(left[-1], color=WHITE), Indicate(right[-1], color=WHITE))
        self.clear_scene()

    def curves(self):
        d = load("fechner")
        head = heading(r"Over the range people use, \ hard to tell apart")
        A = axes([0, 1000], [0, 1.05], x_length=7.0, y_length=4.2, xticks=[0, 250, 500, 750, 1000], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", xlabel=r"intensity", ylabel=r"sensation, \ as a share of its value at 1{,}000",
                 center=[-2.8, -0.35, 0])
        ax = A.ax
        lg = curve(ax, d["i"], d["log_norm"], FECHC, stroke_width=5)
        pw = curve(ax, d["i"], d["power_norm"], STEVC, stroke_width=5)
        leg = legend([(FECHC, r"Fechner: \ a logarithm"), (STEVC, rf"Stevens: \ a power, \ $a = {d['power_exponent']:.2f}$")],
                     font_size=27).move_to(ax.c2p(640, 0.3))
        rows = rows_of([
            (r"both rise steeply and then flatten", WHITE),
            (r"a logarithm keeps flattening; \ a power with a small exponent flattens more slowly", GREY_A),
            (r"just noticeable steps cannot decide: \ both are built from the same steps", THRESH),
            (r"so each side won with its own method: \ steps for Fechner, \ numbers for Stevens", BAD),
        ], 5.0, 28, 0.3).move_to([4.3, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: both from the same Weber fraction")
        with self.voiceover(
            "Draw both on the same axes. <bookmark mark='a'/> Both rise steeply and then flatten. The "
            "logarithm keeps flattening, and a power with a small exponent flattens more slowly. "
            "<bookmark mark='b'/> Just noticeable differences can't decide between them, because both "
            "curves are built from the same steps. <bookmark mark='c'/> So each side won with its own "
            "method. Count steps, and you find Fechner. Ask for numbers, and you find Stevens. The law "
            "you get depends partly on the question you ask."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(lg), Create(pw), FadeIn(leg), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def middle(self):
        d = load("bisection")
        src = archive.PLATEAU_1872

        def grey(y):
            v = 12.92 * y if y <= 0.0031308 else 1.055 * y ** (1 / 2.4) - 0.055  # the screen's encoding of a reflectance
            return rgb_to_color([v, v, v])

        def patch(y, side=1.15):
            return Square(side_length=side, stroke_width=1.5, stroke_color=GREY_C, fill_color=grey(y), fill_opacity=1.0)

        head = heading(r"Plateau's painters, \ 1872: \ paint the grey in the middle")
        ends = VGroup(patch(d["black"]), patch(d["white"])).arrange(RIGHT, buff=4.2).move_to([-2.6, 1.45, 0])
        el = VGroup(label(rf"black: \ {100 * d['black']:.0f}\% of the light", font_size=24, color=GREY_A).next_to(ends[0], DOWN, buff=0.15),
                    label(rf"white: \ {100 * d['white']:.0f}\%", font_size=24, color=GREY_A).next_to(ends[1], DOWN, buff=0.15))
        q = label(r"?", font_size=60, color=YOU).move_to(ends.get_center())
        cands = VGroup()
        for y, txt, col in ((d["mean"], r"half the light", GREY_A), (d["power"], r"a power law, \ exponent $\tfrac13$", STEVC),
                            (d["fechner"], r"Fechner's logarithm", FECHC)):
            pt = patch(y, 0.95)
            cands.add(VGroup(pt, label(txt, font_size=23, color=col).next_to(pt, DOWN, buff=0.12),
                             label(rf"{100 * y:.0f}\%", font_size=24, color=col).next_to(pt, UP, buff=0.1)))
        cands.arrange(RIGHT, buff=0.75).move_to([-2.6, -1.35, 0])
        rows = rows_of([
            (r"Plateau gave painters a black and a white, \ and asked for the grey midway between them", WHITE),
            (r"half the light looks far too pale: \ the middle of sensation is not the middle of the stimulus", GREY_A),
            (r"from such judgments Plateau argued for a power law: \ the first, \ 85 years before Stevens", STEVC),
            (r"Delboeuf repeated it with better apparatus: \ the midpoints moved with the lighting", BAD),
            (rf"colour science's lightness scale is a cube root with an offset, \ and puts middle grey at {100 * d['cie_50']:.0f}\% of "
             rf"white's light: \ the photographer's grey card", THRESH),
        ], 4.6, 26, 0.24).move_to([4.5, -0.2, 0])
        keep_in_frame(rows)
        tags = VGroup(historical_tag(src.cite), note(r"the greys: \ computed for this screen, \ approximately").to_corner(DR, buff=0.3))
        with self.voiceover(
            "One more way to ask, older than Stevens and gentler than numbers. <bookmark mark='a'/> In 1872, "
            "twelve years after Fechner's book, the Belgian physicist Joseph Plateau gave painters a black "
            "and a white and asked each to paint the grey that lies exactly midway between them. "
            "<bookmark mark='b'/> Here are three candidates. Half the light, the physical middle, looks "
            "far too pale. The middle of sensation is not the middle of the stimulus. Fechner's logarithm "
            "puts the middle at the geometric mean, "
            f"{100 * d['fechner']:.0f} percent. A power law with brightness's exponent of a third puts it at "
            f"{100 * d['power']:.0f}. <bookmark mark='c'/> From his painters' greys Plateau argued for a power "
            "law, the first one, eighty-five years before Stevens. <bookmark mark='d'/> And the method met "
            "the same trouble every method meets. Joseph Delboeuf repeated it with better apparatus and found "
            "that the midpoints moved with the lighting. <bookmark mark='e'/> Today colour science uses a "
            "lightness scale built on a cube root, a power law, and it puts middle grey at "
            f"{100 * d['cie_50']:.0f} percent of white's light. That is the grey card photographers meter "
            "against. Notice that it's close to the logarithm's answer above. Given an offset at the dark "
            "end, a power law and a logarithm can be made to agree, which is the quarrel's whole difficulty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(ends), FadeIn(el), FadeIn(q), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cands], lag_ratio=0.6), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(Indicate(cands[1][0], color=STEVC), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def range_(self):
        d = load("stevens")
        head = heading(r"And the numbers bend to the experiment")
        bars = VGroup()
        for i, (r, a) in enumerate(zip(d["range_ratios"], d["range_exponents"])):
            y = 1.75 - 1.15 * i
            bar = Rectangle(width=a * 3.2, height=0.6, stroke_width=0, fill_color=STEVC, fill_opacity=0.85).move_to([-2.4, y, 0],
                                                                                                              aligned_edge=LEFT)
            nm = label(rf"stimuli spanning a ratio of {int(r):,}".replace(",", "{,}"), font_size=29, color=WHITE)
            nm.next_to(bar, LEFT, buff=0.3)
            bars.add(VGroup(nm, bar, label(rf"$a = {a:.2f}$", font_size=30, color=STEVC).next_to(bar, RIGHT, buff=0.2)))
        keep_in_frame(bars)
        truth = DashedLine([-2.4 + 0.67 * 3.2, 2.45, 0], [-2.4 + 0.67 * 3.2, -0.9, 0], color=WHITE, stroke_width=2)
        tl = label(r"the built-in exponent, 0.67", font_size=24, color=WHITE).next_to(truth, UP, buff=0.08)
        rows = rows_of([
            (r"a simulated observer who spreads any range of stimuli over much the same range of numbers", WHITE),
            (r"narrow ranges give steep exponents; \ wide ranges, \ shallow ones", STEVC),
            (r"Poulton (1968): \ range, \ the first stimulus and the order all move real exponents", DATA),
        ], 12.6, 29, 0.22).to_edge(DOWN, buff=0.85)
        src = published_tag(archive.POULTON_1968.cite)
        tag = psyche_tag(r"computed: half the true exponent, \ half a fixed span of numbers")
        with self.voiceover(
            "There's a second difficulty, and it's with the numbers themselves. <bookmark mark='a'/> "
            "People tend to spread whatever range of stimuli they're shown over much the same range of "
            "numbers. Simulate an observer who does that half the time, with a true exponent of two "
            "thirds. <bookmark mark='b'/> Show stimuli spanning a ratio of ten, and the exponent comes "
            "out at 1.34. A ratio of a hundred, 0.84. A ratio of a thousand, 0.67. Same observer. "
            "<bookmark mark='c'/> This is not just a simulation. In 1968 the British psychologist "
            "E. C. Poulton gathered the evidence that the range, the first stimulus, and the order "
            "of the stimuli all move real exponents. The power form repeats; the exponents are partly "
            "made by the experiment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(rows[0]), FadeIn(truth), FadeIn(tl))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bars], lag_ratio=0.7), FadeIn(rows[1]), run_time=5.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
