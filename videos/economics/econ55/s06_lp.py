from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Projections(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Local projections", r"Iterate a model forward, \ or ask each horizon directly?",
             "Chapter five. Local projections.", lit={2005: r"Jord\`a", 2021: r"Plagborg-M{\o}ller and Wolf"},
             scale=("nation",), horizon=("a decade",))
        self.idea()
        self.race()

    def idea(self):
        eqs = VGroup(
            MathTex(r"\text{VAR:}\quad \widehat{\text{response}}_h = \Big(\hat A^{\,h}\Big)\, \hat b \qquad "
                    r"\text{(iterate one step, } h \text{ times)}", font_size=34, color=DATA),
            MathTex(r"\text{local projection:}\quad y_{t+h} = \alpha_h + \beta_h\, z_t + \gamma_h' \,"
                    r"\text{controls}_t + e_{t+h}, \qquad \widehat{\text{response}}_h = \hat\beta_h", font_size=34,
                    color=EST),
        ).arrange(DOWN, buff=0.7).move_to(UP * 0.9)
        rows = VGroup(
            label(r"one regression per horizon, \ with the shock or its instrument on the right", font_size=21,
                  color=EST),
            label(r"in large samples, \ with enough lags, \ both estimate the same thing", font_size=21,
                  color=THEORY),
            label(r"in a real sample: \ a short VAR is biased but steady; \ a projection, \ unbiased but noisy",
                  font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(eqs, DOWN, buff=0.7)
        tag = published_tag(r"Jord\`a, \ AER 95(1) (2005); \ Plagborg-M{\o}ller and Wolf, \ Econometrica 89(2) "
                            r"(2021)", corner=DR, font_size=12)
        nodes = VGroup(*[VGroup(Circle(radius=0.34, color=DATA, stroke_width=2.2),
                                MathTex(str(k), font_size=28, color=WHITE)) for k in range(7)])
        nodes.arrange(RIGHT, buff=1.0).move_to(UP * 0.2)
        steps = VGroup()
        for a_, b_ in zip(nodes[:-1], nodes[1:]):
            ar = Arrow(a_.get_right(), b_.get_left(), buff=0.08, color=DATA, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.25)
            steps.add(VGroup(ar, MathTex(r"\hat A", font_size=26, color=DATA).next_to(ar, UP, buff=0.12)))
        start = VGroup(MathTex(r"\hat b", font_size=32, color=EST).next_to(nodes[0], DOWN, buff=0.3),
                       label(r"quarters after the shock", font_size=20, color=GREY_B).next_to(nodes, DOWN, buff=0.9))
        chain = VGroup(nodes, steps, start)
        with self.voiceover(
            "Every scheme so far identified a shock and then let the fitted autoregression carry it forward, one "
            "quarter at a time. <bookmark mark='a'/> That chains the answer at two years to the model's every "
            "step in between. <bookmark mark='b'/> Òscar Jordà proposed asking each horizon directly: regress "
            "output h quarters ahead on today's shock, or its instrument, with controls, and read the response off "
            "the coefficient. One regression per horizon. <bookmark mark='c'/> Mikkel Plagborg-Møller and "
            "Christian Wolf showed that, in large samples and with enough lags, the two estimate exactly the same "
            "thing. <bookmark mark='d'/> In a real sample they differ in a familiar way: a short autoregression is "
            "biased but steady; a projection is nearly unbiased but noisy."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(nodes[0]), FadeIn(start))
            for st, nd in zip(steps, nodes[1:]):
                self.play(GrowArrow(st[0]), FadeIn(st[1]), FadeIn(nd), run_time=0.7)
            vo.wait_until("a")
            self.play(chain.animate.scale(0.6).to_edge(DOWN, buff=0.35).set_opacity(0.5), run_time=0.8)
            self.play(Write(eqs[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(chain), FadeIn(eqs[1], shift=UP * 0.1), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def race(self):
        L = load("lpvar")
        tr = np.array(L["truth"])
        h = np.arange(len(tr))
        ax = plane([0, 16], [-0.8, 0.6], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.6, y_length=4.8,
                   xticks=[0, 4, 8, 12, 16], yticks=[-0.8, -0.4, 0, 0.4], xlabel=r"quarters",
                   ylabel=r"output, \ \% per point of the rate", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        z = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(16, 0), color=GREY_D, stroke_width=1)
        truth = path(ax, h, tr, TRUTHC, 3.0)
        groups = {}
        for m in ("var1", "var4", "lp"):
            d = L["methods"][m]
            groups[m] = VGroup(band(ax, h, d["lo"], d["hi"], METHOD[m], 0.15), path(ax, h, d["mean"], METHOD[m],
                                                                                       2.6))
        v1, lp = L["methods"]["var1"], L["methods"]["lp"]
        side = VGroup(
            label(rf"{L['reps']} histories of {L['T']} quarters; \\ the instrument in every method", font_size=18,
                  color=WHITE),
            label(rf"grey: \ a VAR with one lag \\ (the truth has two): \\ off by {abs(v1['bias'][-1]):.2f} at four "
                  r"years", font_size=18, color=METHOD["var1"]),
            label(r"blue: \ a VAR with four", font_size=18, color=METHOD["var4"]),
            label(rf"gold: \ local projections: \\ unbiased, \ but the band \\ twice as wide \ "
                  rf"({lp['sd'][-1]:.2f} against {v1['sd'][-1]:.2f})", font_size=18, color=METHOD["lp"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ the Island", corner=DR, font_size=13)
        with self.voiceover(
            f"A race on the Island: {L['reps']} histories of {L['T']} quarters, the effect of a one-point rise in "
            "the rate on output, every method using the same instrument. <bookmark mark='a'/> In white, the truth. "
            "<bookmark mark='b'/> In grey, an autoregression with one lag, when the Island's economy has two. Its "
            f"band is tight, but at four years its average is off by {abs(v1['bias'][-1]):.2f}: it carries its "
            "error forward. <bookmark mark='c'/> In blue, four lags: less bias, more spread. <bookmark mark='d'/> "
            "In gold, local projections: nearly unbiased, but by four years the band is twice as wide. Which to "
            "prefer depends on whether you fear bias or noise more. Dake Li, Plagborg-Møller and Wolf found the "
            "same trade-off across thousands of simulated economies: projections win on bias, autoregressions on "
            "variance."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(truth))
            vo.wait_until("b")
            self.play(FadeIn(groups["var1"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups["var4"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(groups["lp"]), FadeIn(side[3]))
        self.clear_scene()
