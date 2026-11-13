from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Meehl(VoiceoverScene):
    def construct(self):
        self.card()
        self.crud()
        self.paradox()

    def card(self):
        card = chapter_card(7, r"Meehl's warning", r"What does rejecting ``no effect'' tell you about a theory?",
                            lit={1967: r"Meehl's paradox"}, part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter seven. Meehl's warning."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def crud(self):
        d = load("meehl")
        head = heading(r"In people, everything is a little related to everything")
        ns, sig = np.asarray(d["ns"]), np.asarray(d["significant"])
        xs = np.log10(ns)
        A = axes([1.6, 5.05], [0, 1.0], x_length=7.2, y_length=3.8, xticks=[2, 3, 4, 5],
                 xfmt=lambda v: fmt_int(int(round(10 ** v))), yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 xlabel=r"people in the study", ylabel=r"chance of $p < .05$", center=[-2.7, -0.5, 0])
        ax = A.ax
        line = curve(ax, np.log10(np.asarray(d["curve_n"])), np.asarray(d["curve"]), SIG, stroke_width=4)
        names = [r"birth order", r"shoe size", r"breakfast", r"how you vote", r"income", r"temperament",
                 r"hours of sleep", r"years of school"]
        ang = [PI / 2 - 2 * PI * i / len(names) for i in range(len(names))]
        pts = [np.array([-2.3 + 2.5 * np.cos(a), -0.5 + 1.75 * np.sin(a), 0]) for a in ang]
        nodes = VGroup(*[Dot(p_, radius=0.09, color=NULLC) for p_ in pts])
        nlab = VGroup(*[label(t, font_size=23, color=GREY_A).move_to(
            p_ + np.array([0.95 * np.cos(a), 0.36 * np.sin(a), 0])) for t, p_, a in zip(names, pts, ang)])
        threads = VGroup(*[Line(pts[i], pts[j], color=SIG, stroke_width=1.2, stroke_opacity=0.55)
                           for i in range(len(pts)) for j in range(i + 1, len(pts))])
        web = VGroup(threads, nodes, nlab)
        side = VGroup(
            wrapped_label(rf"Two things that have almost nothing to do with each other: \ a correlation of "
                          rf"{d['r']}, which explains {pct(d['variance_explained'], 2)} of the variation.", 5.0, 27,
                          WHITE),
            wrapped_label(rf"With {fmt_int(d['n_for_80'])} people it is ``significant'' four times in five.", 5.0,
                          27, SIG),
            wrapped_label(r"With enough people, the hypothesis of exactly no relation is always rejected. \ It was "
                          r"never true to begin with.", 5.0, 27, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, 0.0, 0])
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "So far the trouble has been in how tests are used. The next warning is about what a test can tell "
            "you even when it's used perfectly, and it came from Paul Meehl, whom you met in Part 3, in 1967. "
            "<bookmark mark='a'/> In physics, two quantities can have exactly nothing to do with each other. In "
            "people, that almost never happens. Birth order, shoe size, what you eat for breakfast, how you vote: "
            "everything is tied to everything else by some thin thread of upbringing or income or temperament. "
            f"<bookmark mark='r'/> Take a correlation of {d['r']}. It explains a quarter of one per cent of the variation. It's "
            "nothing. <bookmark mark='b'/> Now ask how often a study declares it significant. With a hundred "
            "people, hardly ever. <bookmark mark='c'/> With a few thousand, four times in five. With a hundred "
            "thousand, always. <bookmark mark='d'/> So the hypothesis of exactly zero is one we knew was false "
            "before the study began. Rejecting it tells you that your sample was large. It tells you very little "
            "about your theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(nodes, lag_ratio=0.1), FadeIn(nlab, lag_ratio=0.1), run_time=2.0)
            self.play(Create(threads, lag_ratio=0.2), run_time=9.0)
            vo.wait_until("r")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeOut(web), FadeIn(A), run_time=0.8)
            self.play(Create(line), run_time=7.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[1], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def paradox(self):
        head = heading(r"The same improvement, with opposite effects")

        def gauge(x, text, sub, color, lo, hi, band):
            line = Line([x - 2.6, 0, 0], [x + 2.6, 0, 0], color=GREY_B, stroke_width=3)
            zone = Rectangle(width=5.2 * (band[1] - band[0]), height=0.5, stroke_width=0, fill_color=color,
                             fill_opacity=0.85).move_to([x - 2.6 + 5.2 * (band[0] + band[1]) / 2, 0, 0])
            ends = VGroup(label(lo, font_size=20, color=GREY_B).next_to(line, LEFT, buff=0.1),
                          label(hi, font_size=20, color=GREY_B).next_to(line, RIGHT, buff=0.1))
            t = label(text, font_size=28, color=color).next_to(line, UP, buff=0.45)
            s_ = wrapped_label(sub, 5.4, 24, GREY_A).next_to(line, DOWN, buff=0.45)
            return VGroup(line, zone, ends, t, s_)

        phys = VGroup(
            label(r"physics", font_size=36, color=TRUTH),
            gauge(0, r"the theory predicts a value", r"better instruments narrow the range the data allow: \ the "
                  r"theory is easier to refute", TRUTH, r"", r"", (0.46, 0.5)),
        ).arrange(DOWN, buff=0.5).move_to([-3.6, 0.3, 0])
        psy = VGroup(
            label(r"psychology", font_size=36, color=BAD),
            gauge(0, r"the theory predicts ``more than zero''", r"better instruments make any difference "
                  r"detectable: \ the theory is easier to confirm", BAD, r"$-$", r"$+$", (0.5, 1.0)),
        ).arrange(DOWN, buff=0.5).move_to([3.6, 0.3, 0])
        end = VGroup(
            label(r"A prediction that half of all possible outcomes would satisfy is a weak test.", font_size=29,
                  color=P.ACCENT),
            label(r"The series' answer: \ models that predict numbers, tested against the numbers.", font_size=28,
                  color=WHITE),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.6)
        tag = note(r"schematic").to_corner(UR, buff=0.2)
        with self.voiceover(
            "Meehl put it as a paradox. <bookmark mark='a'/> In physics, a theory predicts a value: this "
            "constant should be so much. As instruments improve, the range of values the data allow gets "
            "narrower, and the theory has less and less room to hide. Better measurement makes a physical "
            "theory easier to refute. <bookmark mark='b'/> In psychology, a theory usually predicts only a "
            "direction: this group will score higher than that one. Half of all possible outcomes agree with it "
            "before you start. And as instruments improve and samples grow, any difference at all becomes "
            "detectable. So better measurement makes the theory easier to confirm. The same progress, with the "
            "opposite effect. <bookmark mark='c'/> The lesson isn't to stop testing. It's that a prediction "
            "satisfied by half the possible worlds is a weak test, however small the p-value. "
            "<bookmark mark='d'/> And this is why the series keeps building models. Psyche doesn't predict that "
            "reaction time will go up with the number of choices. She predicts by how many milliseconds, and "
            "can be wrong by a visible amount. That's the kind of prediction Meehl was asking for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(phys, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(psy, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(end[0], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(end[1]))
        self.clear_scene()
