from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403

LETTERS = "ABCDEF"


def study_card(k: int, r: dict, width: float = 3.9) -> VGroup:
    col = DESIGN_COL[r["design"]]
    box = RoundedRectangle(width=width, height=1.55, corner_radius=0.12, stroke_color=col, stroke_width=2.2,
                           fill_color=col, fill_opacity=0.08)
    p = r["p"]
    ptxt = rf"$p = {p:.3f}$" if p >= 0.001 else r"$p < 0.001$"
    body = VGroup(label(rf"Study {LETTERS[k]}", font_size=22, color=WHITE),
                  label(DESIGN_NAME[r["design"]], font_size=17, color=col),
                  label(rf"$z = {r['z']:.2f}$, \ {ptxt}", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.1)
    body.move_to(box)
    return VGroup(box, body)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ which results replicate?", r"Six published results: \ which would you bet on?",
             "Chapter one. Play it: which results replicate?", scale=("world",), horizon=("a decade",))
        self.stage()
        self.reveal()
        self.odds()

    def cards(self):
        P = load("playit")
        g = VGroup(*[study_card(k, r) for k, r in enumerate(P["rows"])]).arrange_in_grid(rows=2, cols=3, buff=0.35)
        return P, g.move_to(UP * 0.35)

    def stage(self):
        P, g = self.cards()
        rule = label(r"picked by rule: \ the published significant results at six evenly spaced ranks of $z$",
                     font_size=17, color=GREY_A).next_to(g, DOWN, buff=0.35)
        ask = label(r"each is repeated with a sample large enough for 90\% power \ against the published effect: \ "
                    r"which come back significant?", font_size=19, color=E.ACCENT).next_to(rule, DOWN, buff=0.25)
        tag = island_tag(r"the simulated field of the hook: \ agora.field", corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. Six results published in the simulated field, each with its design and its test statistic. "
            "<bookmark mark='a'/> They were picked by a rule, not for drama: the published significant results at "
            "six evenly spaced ranks, from the weakest to the strongest. <bookmark mark='b'/> Two use instruments, "
            "one a discontinuity, one a difference in differences, two randomized trials. Their p-values run from "
            "four in a hundred down to a few in a million. <bookmark mark='c'/> Each study is now repeated on new "
            "data, with a sample big enough to have a ninety percent chance of detecting the published effect, if "
            "the published effect is real. Which ones will come back significant, in the same direction? Pause, and "
            "write down your six bets."
        ) as vo:
            self.play(FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in g], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(*[Indicate(c[0], color=DESIGN_COL[r["design"]], scale_factor=1.03)
                        for c, r in zip(g, P["rows"])])
            vo.wait_until("c")
            self.play(FadeIn(ask, shift=UP * 0.1))
        self.wait(4.0)
        self.clear_scene()

    def reveal(self):
        P, g = self.cards()
        stamps = VGroup()
        for c, r in zip(g, P["rows"]):
            ok = r["replicated"]
            txt = (rf"replicated: \ effect {100 * r['rep_effect']:.0f}\% of the original" if ok
                   else rf"failed: \ $z = {r['rep_z']:.2f}$")
            stamps.add(label(txt, font_size=15, color=TRUE if ok else FAIL).next_to(c, DOWN, buff=0.08))
        n_ok = sum(r["replicated"] for r in P["rows"])
        rows = P["rows"]
        weak = rows[1]
        strong = rows[5]
        verdict = label(rf"{n_ok} of 6 replicated", font_size=26, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = island_tag(r"the truth is known: \ each study's true $z$ is stored with it", corner=DL, font_size=12)
        with self.voiceover(
            f"The results. <bookmark mark='a'/> {n_ok} of the six replicated. <bookmark mark='b'/> Study "
            f"B, an instrumental-variables result with z of {weak['z']:.2f}, failed: its true effect was small, "
            f"a true z of {weak['z_true']:.2f}, and it had cleared the line by luck and by search. <bookmark "
            f"mark='c'/> Study F is the surprise. Its z was {strong['z']:.1f}, the strongest of the six, and its "
            f"effect is real, a true z of about {strong['z_true']:.1f}. But even a strong published result is "
            "usually an overestimate, and the replication was sized for the published effect, not the true one. "
            f"So the repeat had less power than planned, and came back at {strong['rep_z']:.2f}, just short. "
            "<bookmark mark='d'/> A replication that fails does not prove the effect is zero, and one that succeeds "
            "does not prove the published size."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.05) for s in stamps], lag_ratio=0.25), FadeIn(verdict),
                      run_time=2.4)
            vo.wait_until("b")
            self.play(Indicate(g[1], color=FAIL, scale_factor=1.04), Indicate(stamps[1], color=FAIL))
            vo.wait_until("c")
            self.play(Indicate(g[5], color=FAIL, scale_factor=1.04), Indicate(stamps[5], color=FAIL))
        self.clear_scene()

    def odds(self):
        P = load("playit")
        B = P["by_z"]
        ax = plane([0, 5], [0, 1], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"share that replicate",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        names = [r"1.96--2.5", r"2.5--3", r"3--4", r"4--6", r"above 6"]
        b = bars(ax, [0.5 + k for k in range(5)], [r_["rate"] for r_ in B], [PUB] * 5, width=0.7)
        nums = VGroup(*[label(rf"{100 * r_['rate']:.0f}\%", font_size=16, color=PUB).next_to(bb, UP, buff=0.06)
                        for bb, r_ in zip(b, B)])
        xl = VGroup(*[label(n_, font_size=14, color=GREY_A).next_to(ax.ax.c2p(0.5 + k, 0), DOWN, buff=0.12)
                      for k, n_ in enumerate(names)])
        xt = label(r"the published $|z|$", font_size=15, color=GREY_A).next_to(xl, DOWN, buff=0.15)
        side = VGroup(
            label(r"the weakest published results \\ replicate about half the time", font_size=18, color=PUB),
            label(r"stronger evidence, \ better odds, \\ but never certainty", font_size=18, color=TRUE),
            label(r"the field's own odds \\ are a prior for any new result", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(ax.ax, RIGHT, buff=0.6)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        tag = island_tag(r"computed: \ every published significant result in the field, \ replicated at 90\% power",
                         corner=DL, font_size=12)
        with self.voiceover(
            "Now replicate every significant result in the field, not just six. <bookmark mark='a'/> Sort them by "
            "the strength of the original evidence. Results just past the line replicate "
            f"{100 * B[0]['rate']:.0f} percent of the time: a coin toss. <bookmark mark='b'/> The share rises "
            f"with the original z, to about {100 * B[3]['rate']:.0f} percent for z between four and six, but "
            "never reaches certainty. <bookmark mark='c'/> These are the field's own odds, and they are the right "
            "starting point for anyone reading a new result from it: a p-value of four in a hundred, in a field "
            "that searches and selects, is closer to a coin toss than to proof."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(xt), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(nums[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b[1:]], lag_ratio=0.25), FadeIn(nums[1:]),
                      FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
