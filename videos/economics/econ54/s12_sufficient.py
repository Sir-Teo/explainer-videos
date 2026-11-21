from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Sufficient(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Sufficient statistics", r"Can two numbers stand in for a whole model?",
             "Chapter ten. Sufficient statistics.", lit={1978: r"Baily", 2009: r"Chetty"}, scale=("nation",),
             horizon=("a year",))
        self.idea()
        self.check()
        self.limit()

    def idea(self):
        eq = MathTex(r"\frac{dW}{db} \;\propto\; \underbrace{\frac{u'(c_u) - u'(c_e)}{u'(c_e)}}_{\text{the gain: the "
                     r"consumption drop}} \;-\; \underbrace{\frac{\varepsilon_{1-e,\,b}}{e}}_{\text{the cost: an "
                     r"elasticity}}", font_size=38, color=THEORY).move_to(UP * 1.4)
        rows = VGroup(
            label(r"Part 42's formula for unemployment insurance: \ two numbers, \ measured directly", font_size=22,
                  color=WHITE),
            label(r"true in any model of search, \ saving or borrowing that leads to the same two numbers",
                  font_size=22, color=GAIN),
            label(r"the bridge: \ structural logic, \ reduced-form evidence", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(eq, DOWN, buff=0.8)
        tag = published_tag(r"Chetty, \ Annual Review of Economics 1 (2009)", corner=DR, font_size=12)
        with self.voiceover(
            "Structural estimation asks a lot: every primitive of the model, measured. Raj Chetty pointed to a "
            "shortcut. <bookmark mark='a'/> For many policy questions, the welfare effect of a small change "
            "depends only on a few numbers that can be measured directly. Part forty-two's formula for "
            "unemployment insurance is the example: a slightly higher benefit is worth it if the gain, the drop in "
            "consumption when people lose their jobs valued in marginal utility, exceeds the cost, the "
            "elasticity of unemployment to the benefit. <bookmark mark='b'/> The formula holds in any model that "
            "produces those two numbers, whatever the details of search, saving or borrowing. <bookmark mark='c'/> "
            "Chetty called these sufficient statistics: a bridge between structural logic and reduced-form "
            "evidence."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def check(self):
        S = load("sufficient")
        b = np.array(S["b"])
        w = 1000 * (np.array(S["welfare"]) - max(S["welfare"]))
        f = np.array(S["formula"])
        axw = plane([0, 0.62], [-2.4, 0.2], center=UP * 1.6 + LEFT * 1.2, x_length=8.6, y_length=2.4,
                    xticks=[], yticks=[-2, -1, 0], xlabel=r"",
                    ylabel=r"welfare, \ thousandths below its best", xfmt=lambda v: f"{v:.1f}",
                    yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=13)
        axf = plane([0, 0.62], [-1.9, 0.9], center=DOWN * 1.95 + LEFT * 1.2, x_length=8.6, y_length=2.4,
                    xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[-1.5, -0.5, 0.5],
                    xlabel=r"the benefit, \ as a share of the wage", ylabel=r"the formula: \ gain minus cost",
                    xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}"), font_size=13)
        cw = path(axw, b, w, MODEL, 3.0)
        cf = path(axf, b, f, THEORY, 3.0)
        z = DashedLine(axf.ax.c2p(0, 0), axf.ax.c2p(0.62, 0), color=GREY_D, stroke_width=1.2)
        v1 = vline(axw, S["bstar"], -2.4, 0.2, E.ACCENT, 1.6)
        v2 = vline(axf, S["bstar"], -1.9, 0.9, E.ACCENT, 1.6)
        side = VGroup(
            label(r"top: \ the whole model's \\ welfare", font_size=18, color=MODEL),
            label(r"bottom: \ the formula, \\ from two numbers \\ at each benefit", font_size=18, color=THEORY),
            label(rf"both say: \ {100 * S['bstar']:.0f}\% \\ of the wage", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: \ Part 42's model", corner=DR, font_size=13)
        with self.voiceover(
            "Check it on Part forty-two's model, where we know everything. <bookmark mark='a'/> On top, welfare "
            "computed from the whole model, for every benefit level. <bookmark mark='b'/> Below, the formula, "
            "computed at each benefit from just the two numbers an economist could measure there. <bookmark "
            f"mark='c'/> They agree: the formula crosses zero exactly where welfare peaks, at {100 * S['bstar']:.0f} "
            "percent of the wage. Nothing else about the model was needed."
        ) as vo:
            self.play(FadeIn(axw), FadeIn(axf), Create(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(cw), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cf), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(v1), Create(v2), FadeIn(side[2]))
        self.clear_scene()

    def limit(self):
        S = load("sufficient")
        b = np.array(S["b"])
        e = np.array(S["eps"])
        ax = plane([0, 0.62], [0, 1.6], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 0.5, 1.0, 1.5],
                   xlabel=r"the benefit, \ as a share of the wage", ylabel=r"the elasticity of unemployment",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        ce = path(ax, b, e, MODEL, 3.0)
        flat = seg(ax, 0, S["eps0"], 0.62, S["eps0"], ERR, 2.4, dashed=True)
        p0 = dot(ax, S["b0"], S["eps0"], DATA, 0.1)
        vs = vline(ax, S["bstar"], 0, 1.5, E.ACCENT, 1.6)
        vc = vline(ax, S["b_const"], 0, 1.5, ERR, 1.6)
        side = VGroup(
            label(rf"one experiment at {100 * S['b0']:.0f}\%: \\ elasticity {S['eps0']:.2f}", font_size=19,
                  color=DATA),
            label(r"red: \ assume it never changes", font_size=19, color=ERR),
            label(rf"the formula then says {100 * S['b_const']:.0f}\% \\ the truth: \ {100 * S['bstar']:.0f}\%",
                  font_size=19, color=E.ACCENT),
            label(r"purple: \ the elasticity rises \\ with the benefit", font_size=19, color=MODEL),
            label(r"local answers: \ sufficient; \\ far from the data: \ a model", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ Part 42's model", corner=DR, font_size=13)
        with self.voiceover(
            "What it cannot do. <bookmark mark='a'/> Suppose the one experiment we have was run at a benefit of "
            f"{100 * S['b0']:.0f} percent of the wage, and measured an elasticity of {S['eps0']:.2f}. <bookmark "
            "mark='b'/> To find the best benefit, the formula needs the elasticity at other benefits too. Assume "
            "it is the same everywhere, <bookmark mark='c'/> and the formula puts the best benefit at "
            f"{100 * S['b_const']:.0f} percent, against {100 * S['bstar']:.0f} in truth. <bookmark mark='d'/> In "
            "the model, the elasticity rises steeply as benefits rise: the closer the benefit comes to the wage, "
            "the larger the share of what a job adds that each further rise takes away. <bookmark mark='e'/> "
            "Sufficient statistics "
            "answer local questions without a model; for a change far from the data, you need to know how the "
            "statistics themselves would move, and that is a model again."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(p0, scale=1.5), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(flat), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(vc), Create(vs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ce), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
