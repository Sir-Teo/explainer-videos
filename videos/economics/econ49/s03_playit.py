from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ the chance or the sentence?", r"Which deters more, if you can double only one?",
             "Chapter two. Play it: double the chance, or double the sentence?", lit={2013: r"Nagin",
                                                                                     2017: r"Lee and McCrary"},
             scale=("person", "city"), horizon=("a year",))
        self.ask()
        self.reveal()
        self.evidence()

    def ask(self):
        O = load("offenders")
        head = label(rf"Caught one time in {1 / O['p']:.0f}, \ {O['sentence']:.0f} years if caught. \ "
                     r"You may double one.", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        opts = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.6, corner_radius=0.12, stroke_color=c,
                                                stroke_width=2.4, fill_color=c, fill_opacity=0.12),
                               label(t, font_size=24, color=c))
                        for t, c in ((r"double the chance: \\ one in " + f"{1 / (2 * O['p']):.1f}".rstrip("0")
                                      .rstrip(".") + r", \ " + f"{O['sentence']:.0f}" + r" years", CHANCE),
                                     (r"double the sentence: \\ one in " + f"{1 / O['p']:.0f}" + r", \ " +
                                      f"{2 * O['sentence']:.0f}" + r" years", FINE),
                                     (r"it makes \\ no difference", GREY_B))])
        for o in opts:
            o[1].move_to(o[0])
        opts.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        note = label(r"either way, \ the expected punishment doubles", font_size=22, color=GREY_A).next_to(
            opts, DOWN, buff=0.5)
        ring = countdown().scale(0.6).next_to(note, DOWN, buff=0.5)
        with self.voiceover(
            "Your turn. You run the Island's justice system, and you can afford one change. The police catch one "
            f"offender in {1 / O['p']:.0f}, and the sentence is {O['sentence']:.0f} years. <bookmark mark='a'/> You "
            "may double the chance of being caught, by putting more police on the streets, <bookmark mark='b'/> or "
            "double the sentence, by passing a law. <bookmark mark='c'/> Either way the expected punishment, the "
            "chance times the sentence, doubles. <bookmark mark='d'/> Which cuts crime more: the chance, the "
            "sentence, or does it make no difference? Pause, and choose."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(o) for o in opts], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(opts[0], color=WHITE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(Indicate(opts[1], color=WHITE, scale_factor=1.05))
            vo.wait_until("c")
            self.play(FadeIn(note, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Indicate(opts[2], color=WHITE, scale_factor=1.05), FadeIn(ring), run_time=1.0)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        O = load("offenders")
        kinds = O["kinds"]
        ax = plane([0, 3 * len(kinds)], [0, 0.9], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6,
                   y_length=4.4, xticks=[], yticks=[0, 0.25, 0.5, 0.75], ylabel=r"share who offend",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        groups = VGroup()
        for i, k in enumerate(kinds):
            r = O["play"][k]
            bars = VGroup()
            for j, (key, col) in enumerate((("start", GREY_B), ("double_p", CHANCE), ("double_s", FINE))):
                x = 3 * i + 1.5 + (j - 1) * 0.8
                p0, p1 = ax.ax.c2p(x - 0.36, 0), ax.ax.c2p(x + 0.36, r[key])
                b = Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to((p0 + p1) / 2)
                v = label(rf"{100 * r[key]:.0f}\%", font_size=14, color=WHITE).next_to(b, UP, buff=0.06)
                bars.add(VGroup(b, v))
            name = label(k, font_size=19, color=KIND_COLS[k]).next_to(ax.ax.c2p(3 * i + 1.5, 0), DOWN, buff=0.25)
            groups.add(VGroup(bars, name))
        key = VGroup(*[VGroup(Square(side_length=0.2, fill_color=c, fill_opacity=0.85, stroke_width=0),
                              label(t, font_size=16, color=c)).arrange(RIGHT, buff=0.1)
                       for t, c in ((r"now", GREY_B), (r"chance doubled", CHANCE), (r"sentence doubled", FINE))])
        key.arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.25)
        side = VGroup(
            label(r"no mind for risk: \\ only $p \times S$ \\ matters", font_size=17, color=KIND_COLS["risk-neutral"]),
            label(r"dislikes risk: \\ a long sentence is \\ the worse prospect", font_size=17,
                  color=KIND_COLS["risk-averse"]),
            label(r"counts later years \\ for less: \\ the extra years are \\ far away", font_size=17,
                  color=KIND_COLS["present-minded"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        pm = O["play"]["present-minded"]
        ra = O["play"]["risk-averse"]
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The answer depends on who the offenders are. <bookmark mark='a'/> For someone who weighs only the "
            "expected punishment, it makes no difference: either change cuts the share who offend from "
            f"{100 * O['play']['risk-neutral']['start']:.0f} to "
            f"{100 * O['play']['risk-neutral']['double_p']:.0f} percent. <bookmark mark='b'/> For someone who "
            "dislikes risk, the longer sentence deters more, because a small chance of a very long sentence is the "
            f"more frightening gamble: {100 * ra['double_s']:.0f} percent offend, against "
            f"{100 * ra['double_p']:.0f}. <bookmark mark='c'/> For someone who counts each later year of prison "
            "for less than the one before, as most of us count the future, the extra years at the end of a longer "
            "sentence are far away and weigh little; doubling the chance, which brings the first years forward for "
            f"twice as many, wins: {100 * pm['double_p']:.0f} percent against {100 * pm['double_s']:.0f}. "
            "<bookmark mark='d'/> So the question is not one of theory. It has to be answered with data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag), run_time=1.0)
            for i, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in groups[i][0]], lag_ratio=0.3),
                          LaggedStart(*[FadeIn(b[1]) for b in groups[i][0]], lag_ratio=0.3), FadeIn(groups[i][1]),
                          FadeIn(side[i]), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(groups[2], color=WHITE, scale_factor=1.03))
        self.clear_scene()

    def evidence(self):
        T = tables.CERTAINTY_49.data
        cards = point_cards([
            (r"Nagin's review", r"the evidence that \\ being caught deters \\ is far more consistent \\ than "
                                r"for longer \\ sentences", CHANCE),
            (r"Lee and McCrary", r"at 18, \ Florida's \\ penalties jump; \\ offending falls " + rf"{T['lm_drop']}\%"
                                 r" \\ (no more than " + rf"{T['lm_bound']}\%)", FINE),
            (r"the young", r"an elasticity to \\ sentence length no \\ more negative than \\ " +
                           f"{T['lm_elasticity']:.2f}".replace("-", "{-}"), FINE),
            (r"Becker's reading", r"if the chance deters \\ more, \ offenders act \\ as if they like risk, \\ or "
                                  r"discount the future", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"what the data say: \ certainty over severity", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                      buff=0.6)
        tag = published_tag(tables.CERTAINTY_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The data have answered fairly consistently. <bookmark mark='a'/> Daniel Nagin's review of the evidence "
            "concluded that the chance of being caught deters far more reliably than the severity of the "
            "punishment, and that long sentences cannot be justified as deterrents. <bookmark mark='b'/> David Lee "
            "and Justin McCrary used Florida's eighteenth birthday, when offenders suddenly face adult courts and "
            f"much longer sentences. Offending barely changes: a fall of about {T['lm_drop']} percent in the odds, "
            f"ruling out falls of {T['lm_bound']} percent or more. <bookmark mark='c'/> They put the response of "
            f"young offenders to the length of a sentence at no more than {say_num(T['lm_elasticity'])}. <bookmark "
            "mark='d'/> Becker had seen this coming: if the chance deters more than the penalty, offenders behave "
            "as if they like risk, or, as the Island's present-minded offenders show, as if the far end of a long "
            "sentence hardly counts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
