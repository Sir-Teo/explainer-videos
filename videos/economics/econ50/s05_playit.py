from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


def _boxes(items, w=2.85, h=1.25, fs=19):
    g = VGroup()
    for t, c in items:
        b = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=c, stroke_width=2.2, fill_color=c,
                             fill_opacity=0.1)
        g.add(VGroup(b, label(t, font_size=fs, color=c).move_to(b)))
    return g.arrange(RIGHT, buff=0.3)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Play it: \ your advice, \ before the analysis", r"Yes, \ no, \ or yes with conditions?",
             "Chapter four. Play it: your advice, before the analysis.", lit={2021: r"the payments"},
             scale=("nation",), horizon=("a year",))
        self.advice()
        self.forecast()
        self.kept()

    def advice(self):
        head = label(r"Your advice to the minister, \ now", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        opts = _boxes([(r"yes, \\ as designed", NEW), (r"yes, \ but keep \\ a work requirement", WORK),
                       (r"yes, \ but \\ smaller", CHILD), (r"no: \ spend it \\ another way", LOSS)])
        opts.move_to(UP * 0.6)
        know = VGroup(
            label(r"what you know so far:", font_size=19, color=GREY_A),
            label(r"the 2021 payments: \ child poverty 9.7\% $\to$ 5.2\% \ (SPM), \ while other pandemic aid also "
                  r"flowed", font_size=18, color=SPM),
            label(r"for the parent of two: \ 6,600 more at no earnings, \ a tenth less reward for working"
                  .replace("6,600", "6{,}600"), font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(opts, DOWN, buff=0.55)
        ring = countdown().scale(0.6).to_edge(DOWN, buff=0.35)
        why = label(r"a memo is easier to bend towards what you already believe \\ than to write honestly: \ "
                    r"write your advice down first", font_size=22, color=GREY_A).move_to(UP * 0.6)
        with self.voiceover(
            "Before the analysis, your advice. Write it down now, because a memo is easier to bend towards what "
            "you already believe than to write honestly, and the only defence is to know what you believed before "
            "you looked. <bookmark mark='a'/> Yes, as designed. <bookmark mark='b'/> Yes, but keep a work "
            "requirement, so the payment still rises with earnings at the bottom. <bookmark mark='c'/> Yes, but "
            "smaller. <bookmark mark='d'/> Or no: spend the money another way. <bookmark mark='e'/> What you know "
            "so far: in 2021 the payments came while child poverty, on the measure that counts credits, fell from "
            "9.7 to 5.2 percent, although other pandemic aid was flowing too. And for one family, a large gain at "
            "the bottom and a somewhat smaller reward for working. Choose."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(why, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(why), FadeIn(opts[0], shift=UP * 0.1))
            for mk, o in zip("bcd", opts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(o, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(know, shift=UP * 0.1), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def forecast(self):
        I = load("island")
        head = label(rf"And a forecast: \ on the Island, \ {100 * I['old']['child_poverty']:.1f}\% of children are "
                     r"poor under the old credit.", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.6)
        sub = label(r"With the allowance, \ by how much will child poverty fall?", font_size=26,
                    color=WHITE).next_to(head, DOWN, buff=0.3)
        opts = _boxes([(r"by less \\ than a tenth", GREY_A), (r"by a tenth \\ to a quarter", EITC),
                       (r"by a quarter \\ to two fifths", NEW), (r"by more than \\ two fifths", CHILD)])
        opts.move_to(DOWN * 0.3)
        hint = label(r"the 2021 headline was a fall of almost half", font_size=20, color=GREY_B).next_to(
            opts, DOWN, buff=0.5)
        ring = countdown().scale(0.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And a forecast, which the Island will check. Under the old credit, "
            f"{100 * I['old']['child_poverty']:.1f} percent of the Island's children are below its poverty line. "
            "<bookmark mark='a'/> With the allowance, after families have responded, by how much will that fall? "
            "By less than a tenth, <bookmark mark='b'/> by a tenth to a quarter, <bookmark mark='c'/> by a "
            "quarter to two fifths, <bookmark mark='d'/> or by more than two fifths? <bookmark mark='e'/> "
            "Remember that the 2021 headline was a fall of almost half. Pause, and choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(opts[0], shift=UP * 0.1))
            for mk, o in zip("bcd", opts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(o, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(hint), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def kept(self):
        slip = VGroup(
            label(r"kept", font_size=40, color=E.ACCENT),
            label(r"your advice \ $\to$ \ chapter twelve", font_size=26, color=WHITE),
            label(r"your forecast \ $\to$ \ chapter eight", font_size=26, color=WHITE),
            label(r"a memo that only confirms what you believed before \\ is worth checking twice", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        frame = SurroundingRectangle(slip, buff=0.5, corner_radius=0.14, color=E.ACCENT, stroke_width=1.6)
        with self.voiceover(
            "Both answers are kept. <bookmark mark='a'/> The forecast comes back in chapter eight, when the "
            "Island runs the policy, and the advice in chapter twelve, when the memo is written. <bookmark "
            "mark='b'/> If the memo ends up saying exactly what you believed before you started, that is not proof "
            "that you were wrong; but it is a reason to check it twice."
        ) as vo:
            self.play(Create(frame), FadeIn(slip[0]))
            vo.wait_until("a")
            self.play(FadeIn(slip[1]), FadeIn(slip[2]))
            vo.wait_until("b")
            self.play(FadeIn(slip[3], shift=UP * 0.1))
        self.wait(1.0)
        self.clear_scene()
