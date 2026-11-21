from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403


class Replication(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Replication in the lab", r"When economics experiments are run again, \ how many hold up, \ "
             r"and could anyone tell in advance?", "Chapter two. Replication in the lab.",
             lit={2016: "Camerer et al."}, scale=("person", "world"), horizon=("a decade",))
        self.eighteen()
        self.shrink()
        self.called()

    def eighteen(self):
        R = load("replication")
        C = R["camerer"]
        n, k = C["studies"], C["replicated"]
        dots = VGroup(*[Circle(radius=0.27, stroke_width=2.4, stroke_color=TRUE if i < k else FAIL,
                               fill_color=TRUE if i < k else FAIL, fill_opacity=0.35) for i in range(n)])
        dots.arrange_in_grid(rows=2, cols=9, buff=0.25).move_to(UP * 1.4)
        lab = label(r"18 laboratory experiments, \ AER and QJE, \ 2011--2014", font_size=21, color=GREY_A).next_to(
            dots, UP, buff=0.3)
        rows = VGroup(
            label(r"each repeated by a preregistered plan, \ with at least 90\% power for the original effect",
                  font_size=20, color=GREY_A),
            label(rf"{k} of {n} significant again, \ in the same direction: \ {100 * C['rate']:.0f}\%",
                  font_size=22, color=TRUE),
            label(rf"the replicated effects: \ on average {100 * C['effect_ratio']:.0f}\% of the originals",
                  font_size=22, color=PUB),
            label(rf"the simulated field: \ {100 * R['rate']:.0f}\% replicate, \ effects {100 * R['ratio']:.0f}\% "
                  r"of the originals", font_size=22, color=FIRST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(dots, DOWN, buff=0.55)
        tag = published_tag(r"Camerer et al., \ \emph{Science} 351(6280) (2016)", corner=DL, font_size=12)
        with self.voiceover(
            "In 2016 a team led by Colin Camerer and Anna Dreber did for experimental economics what the hook did "
            "in simulation. <bookmark mark='a'/> They took all eighteen laboratory experiments published in the "
            "American Economic Review and the Quarterly Journal of Economics from 2011 to 2014, and ran each again "
            "with a plan written down in advance. <bookmark mark='b'/> Every replication had at least a ninety "
            "percent chance of detecting the original effect, if it was real. <bookmark mark='c'/> Eleven of the "
            "eighteen were significant again, in the same direction: sixty-one percent. <bookmark mark='d'/> And "
            "the effects they found were, on average, two thirds the size of the originals. <bookmark mark='e'/> "
            f"The simulated field of the hook, built before looking, gives {100 * R['rate']:.0f} percent and "
            f"{100 * R['ratio']:.0f} percent. Search and selection of the kind it assumes are enough to produce "
            "what the laboratories found."
        ) as vo:
            self.play(FadeIn(lab), FadeIn(tag),
                      LaggedStart(*[FadeIn(d.copy().set_stroke(GREY_B).set_fill(GREY_B, 0.15)) for d in dots],
                                  lag_ratio=0.03), run_time=1.6)
            vo.wait_until("a")
            self.play(Indicate(lab))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=1.2) for d in dots], lag_ratio=0.05), FadeIn(rows[1]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def shrink(self):
        R = load("replication")
        B = R["by_z"]
        ax = plane([0, 5], [0, 1], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.6, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"true effect as a share of the published one",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        names = [r"1.96--2.5", r"2.5--3", r"3--4", r"4--6", r"above 6"]
        b = bars(ax, [0.5 + k for k in range(5)], [r_["true_over_orig"] for r_ in B], [FIRST] * 5, width=0.7)
        nums = VGroup(*[label(rf"{100 * r_['true_over_orig']:.0f}\%", font_size=16, color=FIRST).next_to(
            bb, UP, buff=0.06) for bb, r_ in zip(b, B)])
        xl = VGroup(*[label(n_, font_size=14, color=GREY_A).next_to(ax.ax.c2p(0.5 + k, 0), DOWN, buff=0.12)
                      for k, n_ in enumerate(names)])
        xt = label(r"the published $|z|$", font_size=15, color=GREY_A).next_to(xl, DOWN, buff=0.15)
        full = seg(ax, 0, 1, 5, 1, GREY_B, 1.6, dashed=True)
        side = VGroup(
            label(r"the winner's curse: \\ a result is published \\ because its estimate came out high", font_size=18,
                  color=FIRST),
            label(r"so the next estimate \\ falls back towards the truth", font_size=18, color=PUB),
            label(r"a failed replication \\ is not proof of no effect", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(ax.ax, RIGHT, buff=0.6)
        if side.get_right()[0] > 6.9:
            side.scale_to_fit_width(6.9 - side.get_left()[0])
        tag = island_tag(r"computed: \ the simulated field, \ true over published $z$ by the published $|z|$",
                         corner=DL, font_size=12)
        with self.voiceover(
            "Why are replicated effects smaller? <bookmark mark='a'/> Because publication picks winners. A study is "
            "published when its estimate came out high, and an estimate that came out high was, on average, lucky. "
            "In the simulated field, where the truth is known, the true effect of a result that barely cleared the "
            f"line is {100 * B[0]['true_over_orig']:.0f} percent of the published one. <bookmark mark='b'/> For "
            f"stronger results the exaggeration is smaller, but even above six it is about "
            f"{100 - 100 * B[4]['true_over_orig']:.0f} percent. This is the winner's curse of auctions, Part "
            "sixteen, in a new place: the next estimate falls back towards the truth. <bookmark mark='c'/> It is "
            "why a failed replication is not proof that the effect is zero, and why an honest replication is sized "
            "for an effect smaller than the published one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(xt), FadeIn(full), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(nums[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b[1:]], lag_ratio=0.25), FadeIn(nums[1:]),
                      FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def called(self):
        M = load("markets")
        c = calls.CALLS["replication_markets_2016"]
        cc = call_card(tex_safe(c.who), tex_safe(c.when), tex_safe(c.said), tex_safe(c.outcome), c.verdict,
                       width=12.6, font_size=17)
        cc.move_to(UP * 0.5)
        lesson = label(r"crowds of experts knew the field was shaky, \ but not which results", font_size=21,
                       color=E.ACCENT).next_to(cc, DOWN, buff=0.5)
        tag = published_tag(r"Camerer et al. (2016) \ and the authors' working paper, \ MPRA 75461", corner=DL,
                            font_size=12)
        with self.voiceover(
            "Could anyone have said in advance? Called it? <bookmark mark='a'/> Before the replications were run, "
            f"the team opened a prediction market for each study, and {M['traders']} economists traded in them. "
            f"The average price said there was a {100 * M['market']:.0f} percent chance that each result would "
            "replicate, and every market was above one half. <bookmark mark='b'/> The outcome: sixty-one percent. "
            f"And the prices ranked the studies only weakly, a rank correlation of {M['rho_market']:.2f}, not "
            "significant; the traders' own answers to a simple survey did better. <bookmark mark='c'/> Partly "
            "right: the traders knew the field was imperfect, and erred on the side of optimism. Two years later a "
            "similar market on social-science experiments in Nature and Science predicted the replication rate "
            "almost exactly. <bookmark mark='d'/> The crowd knew the field was shaky, but not yet which results."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cc.left))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.4))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()
