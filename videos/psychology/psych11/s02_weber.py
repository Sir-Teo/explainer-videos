from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


def _weight(mass: float, color, scale: float = 1.0) -> VGroup:
    h = 0.5 + 0.35 * np.log10(mass)
    body = RoundedRectangle(width=1.0 * scale, height=h * scale, corner_radius=0.12, color=color, stroke_width=3,
                            fill_color=color, fill_opacity=0.35)
    handle = Arc(radius=0.22 * scale, start_angle=0, angle=PI, color=color, stroke_width=4).next_to(body, UP, buff=0)
    return VGroup(body, handle, label(rf"{mass:g} g", font_size=26, color=color).move_to(body))


class Weber(VoiceoverScene):
    def construct(self):
        self.card()
        self.weights()
        self.law()
        self.fraction()

    def card(self):
        card = chapter_card(1, r"Weber's fraction", r"Is the smallest noticeable difference a fixed amount, or a fixed share?",
                            lit={1834: r"Weber's fraction"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter one. Weber's fraction."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def weights(self):
        w = archive.WEBER_1834.data
        head = heading(rf"Leipzig, \ {w['year']}: \ two weights in the hand")
        pairs = VGroup()
        for i, (base, extra, col) in enumerate(((100, 3, WEBERC), (1000, 3, BAD), (1000, 30, WEBERC))):
            a, b = _weight(base, STD), _weight(base + extra, CMP)
            pair = VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
            verdict = label(r"felt" if col == WEBERC else r"not felt", font_size=30, color=col)
            pairs.add(VGroup(pair, verdict.next_to(pair, DOWN, buff=0.3)))
        pairs.arrange(RIGHT, buff=0.9, aligned_edge=DOWN).move_to([0, 0.75, 0])
        rows = rows_of([
            (r"Ernst Heinrich Weber, \ an anatomist: \ lift one weight, \ then another, \ and say which is heavier", WHITE),
            (r"the difference you can just notice is not a fixed number of grams: \ it grows with the weight", WEBERC),
            (r"what stays fixed is the ratio", THRESH),
        ], 12.6, 30, 0.22).to_edge(DOWN, buff=0.75)
        src = historical_tag(archive.WEBER_1834.cite)
        tag = note(r"the weights: \ an illustration of the rule, \ not Weber's numbers").to_corner(DR, buff=0.3)
        with self.voiceover(
            f"Fechner's starting point was the work of a colleague in Leipzig. In {w['year']} the "
            "anatomist Ernst Heinrich Weber published experiments on touch, in Latin, among them "
            "experiments with weights. <bookmark mark='a'/> Lift one weight, then another, and say "
            "which is heavier. <bookmark mark='b'/> Weber found that the difference you can just "
            "notice is not a fixed number of grams. If three grams on a hundred can be felt, three grams "
            "on a thousand cannot. <bookmark mark='c'/> It takes about thirty. The difference grows with "
            "the weight. What stays fixed is the ratio. The numbers here are an illustration of the "
            "rule. Weber's own figure for weights is quoted differently by different histories, so we "
            "won't put one on the screen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(pairs[0], shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(pairs[1], shift=UP * 0.15), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pairs[2], shift=UP * 0.15), FadeIn(rows[2]))
        self.clear_scene()

    def law(self):
        d = load("weber")
        head = heading(r"Weber's law")
        law = MathTex(r"\Delta I", r"=", r"k", r"\,I", font_size=72)
        law[0].set_color(WEBERC)
        law[2].set_color(THRESH)
        law.move_to([0, 1.7, 0])
        parts = rows_of([
            (r"$I$: \ the intensity you start from (the standard)", STD),
            (r"$\Delta I$: \ the smallest increase you can notice (the just noticeable difference)", WEBERC),
            (r"$k$: \ Weber's fraction, \ the same at every $I$", THRESH),
        ], 11.6, 31, 0.28).next_to(law, DOWN, buff=0.6)
        eg = wrapped_label(r"so the noticeable difference is a fixed share: \ $\Delta I / I = k$. \ A weight of $10\times$ "
                           r"needs a difference $10\times$ as large", 12.0, 31, GREY_A).next_to(parts, DOWN, buff=0.5)
        with self.voiceover(
            "Written as a law: the just noticeable difference, delta I, is a constant fraction k of the "
            "intensity I you start from. <bookmark mark='a'/> I is the standard. Delta I is the smallest "
            "increase you can notice. And k is Weber's fraction, the same at every intensity. "
            "<bookmark mark='b'/> Divide both sides by I, and the law says that the noticeable difference "
            "is a fixed share. Ten times the weight needs ten times the difference."
        ) as vo:
            self.play(Write(law), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in parts], lag_ratio=0.8), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(eg, shift=UP * 0.1))
        self.clear_scene()

    def fraction(self):
        d = load("weber")
        head = heading(r"On Psyche: \ a law in the middle, \ and two edges")
        A = log_axes((-1, 5), (-2, 1), x_length=7.4, y_length=4.2, xlabel=r"the standard, $I$", ylabel=r"Weber's fraction, "
                     r"$\Delta I / I$", center=[-2.7, -0.3, 0])
        ax = A.ax
        lx = np.log10(d["standards"])
        flat = curve(ax, lx, np.log10(d["fraction"]), WEBERC, stroke_width=5)
        near = curve(ax, lx, np.log10(d["fraction_near"]), STEVC, stroke_width=4)
        weber_line = DashedLine(ax.c2p(-1, np.log10(d["w"])), ax.c2p(5, np.log10(d["w"])), color=THRESH, stroke_width=2)
        floor = DashedLine(ax.c2p(np.log10(d["floor_at"]), -2), ax.c2p(np.log10(d["floor_at"]), 1), color=GREY_C, stroke_width=2)
        fl = label(r"the noise floor", font_size=25, color=GREY_A).next_to(ax.c2p(np.log10(d["floor_at"]), 1), DOWN, buff=0.1).shift(RIGHT * 1.1)
        wl = label(rf"$k = {d['w']:.3f}$", font_size=28, color=THRESH).next_to(ax.c2p(3.2, np.log10(d["w"])), UP, buff=0.12)
        nl = label(r"a near miss", font_size=26, color=STEVC).next_to(ax.c2p(4.4, np.log10(d["fraction_near"][-5])), DOWN, buff=0.15)
        rows = rows_of([
            (r"Psyche: \ noise in the head with a fixed floor, \ plus noise that grows in proportion to the stimulus", WHITE),
            (rf"over the middle of the range, \ a constant fraction: \ ${d['w']:.3f}$", WEBERC),
            (rf"near the absolute threshold the fraction grows: \ ${d['at_1']:.2f}$ at an intensity of 1", BAD),
            (r"for loud tones, \ people do slightly better than Weber: \ a near miss (1968)", STEVC),
            (r"and every sense has its own fraction", GREY_A),
        ], 4.9, 28, 0.25).move_to([4.35, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's observer")
        src = published_tag(archive.MCGILL_GOLDBERG_1968.cite)
        with self.voiceover(
            "Weber's law can be built. Give Psyche a head in which every intensity arrives with some "
            "noise: a fixed floor, plus a part that grows in proportion to the stimulus. Then compute the "
            "just noticeable difference at every standard, over six powers of ten. <bookmark mark='a'/> "
            f"Over the middle of the range, the fraction is constant: {d['w']:.3f}. That's Weber's law. "
            "<bookmark mark='b'/> But near the bottom, where the fixed floor dominates, the fraction "
            f"grows. At an intensity of one it's {d['at_1']:.2f}. Every sense shows this: the law fails "
            "near the absolute threshold. <bookmark mark='c'/> And at the top there's a second, smaller "
            "failure. For the loudness of pure tones, people do slightly better than Weber's law allows "
            "as the tone gets louder. In 1968 it was named the near miss to Weber's law. "
            "<bookmark mark='d'/> Every sense also has its own fraction. Textbook tables disagree about "
            "the values, so here's the safer statement: within a sense, over the middle of its range, "
            "the fraction is roughly constant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(flat), FadeIn(weber_line), FadeIn(wl), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(floor), FadeIn(fl), FadeIn(rows[2]), Indicate(flat, color=BAD, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(near), FadeIn(nl), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
