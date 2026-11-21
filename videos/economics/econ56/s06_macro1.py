from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"In the Ramsey model with $f(k) = k^{1/3}$, \ $\delta = 0.05$, \ $\rho = 0.03$ and $u(c) = c^{1-\theta}/(1 - "
    r"\theta)$ with $\theta = 2$ \ (no population or technology growth), \ the economy is at its steady state when "
    r"the government unexpectedly and permanently taxes the return to capital, \ net of depreciation, \ at 25\%, "
    r"\ rebating the revenue lump sum.",
    r"(a) \ Find the new steady state. \quad (8 marks)",
    r"(b) \ Draw the phase diagram and the transition. \quad (9 marks)",
    r"(c) \ What happens to consumption on impact and in the long run, \ and why? \quad (8 marks)",
]


class Macro1(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Macro: \ the Ramsey model with a tax on capital", r"What does a tax on capital do, at "
             r"once and in the end?", "Question five. Macroeconomics: the Ramsey model with a tax on capital.",
             lit={1928: r"Ramsey", 1965: r"Cass; \ Koopmans", 1986: r"Chamley"}, scale=("household", "nation"),
             horizon=("a decade", "a century"))
        self.statement()
        self.steady()
        self.phase()
        self.marks()

    def statement(self):
        paper = exam_paper(5, "macro", r"a tax on capital", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question five. A Ramsey economy, with a Cobb-Douglas technology, depreciation of five percent, a rate "
            "of time preference of three percent, and an elasticity of intertemporal substitution of one half, "
            "sits at its steady state. Without warning, the government taxes the net return to capital at "
            "twenty-five percent for ever, and hands the revenue back as a lump sum. <bookmark mark='a'/> Part a: "
            "the new steady state. <bookmark mark='b'/> Part b: the phase diagram and the transition. <bookmark "
            "mark='c'/> Part c: what happens to consumption, at once and in the long run. Pause, and decide which "
            "equation the tax enters."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def steady(self):
        M = load("macro1")
        tag = part_tag(5, "a", "macro")
        rows = steps([
            (r"\dot k = k^{1/3} - 0.05\,k - c",
             r"the resource constraint: \ the rebate returns the revenue, \ so the tax is not here"),
            (r"\frac{\dot c}{c} = \frac{(1 - \tau)\big(f'(k) - \delta\big) - \rho}{\theta}",
             r"the Euler equation: \ households earn the after-tax return"),
            (r"f'(k^*) = \delta + \frac{\rho}{1 - \tau} = 0.05 + \frac{0.03}{0.75} = 0.09",
             r"steady state: \ $\dot c = 0$"),
            (rf"k^* = \Big(\frac{{1/3}}{{0.09}}\Big)^{{3/2}} = {M['k_new']:.2f} \ \ (\text{{from }} "
             rf"{M['k_old']:.2f}), \qquad c^* = {M['c_new']:.3f} \ \ (\text{{from }} {M['c_old']:.3f})",
             r"from $\dot k = 0$", GAIN),
            (rf"f'(k) - \delta: \ {100 * M['r_old']:.0f}\% \ \to\ {100 * M['r_new']:.0f}\%, \qquad "
             rf"\text{{after tax: }} {100 * M['r_old']:.0f}\%", r"the after-tax return is pinned at $\rho$"),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[3][0])
        with self.voiceover(
            "Part a. <bookmark mark='a'/> The tax does not enter the resource constraint: what the government "
            "takes, it gives back, so output is still split between consumption and investment. <bookmark "
            "mark='b'/> It enters the Euler equation, because households save according to the return they keep. "
            "<bookmark mark='c'/> In the steady state consumption is constant, so the after-tax return equals the "
            "rate of time preference, and the pre-tax return must rise to three percent over three quarters, plus "
            f"depreciation: nine percent. <bookmark mark='d'/> Capital falls from {M['k_old']:.2f} to "
            f"{M['k_new']:.2f}, and steady-state consumption from {M['c_old']:.3f} to {M['c_new']:.3f}. <bookmark "
            f"mark='e'/> The pre-tax net return rises from {100 * M['r_old']:.0f} to {100 * M['r_new']:.0f} "
            "percent; the after-tax return ends where it began."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "d":
                    self.play(Create(box))
        self.clear_scene()

    def phase(self):
        M = load("macro1")
        tag = part_tag(5, "b, c", "macro")
        kg, cg = np.array(M["kdot0_k"]), np.array(M["kdot0_c"])
        pk, pc, pt = np.array(M["path_k"]), np.array(M["path_c"]), np.array(M["path_t"])
        ax = plane([3, 11], [1.3, 1.8], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.4, y_length=5.0,
                   xticks=[4, 6, 8, 10], yticks=[1.4, 1.5, 1.6, 1.7], xlabel=r"capital $k$",
                   ylabel=r"consumption $c$", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.1f}", font_size=15)
        kd = path(ax, kg, cg, WHITE, 2.4, xr=(3, 11), yr=(1.3, 1.8))
        kd_l = label(r"$\dot k = 0$", font_size=18, color=WHITE).next_to(ax.ax.c2p(10.6, float(np.interp(
            10.6, kg, cg))), UP, buff=0.12)
        c_old = vline(ax, M["k_old"], 1.3, 1.8, GREY_C, 1.8)
        c_new = vline(ax, M["k_new"], 1.3, 1.8, MACRO, 2.6)
        lo = label(r"old $\dot c = 0$", font_size=16, color=GREY_C).next_to(ax.ax.c2p(M["k_old"], 1.8), UP,
                                                                           buff=0.08).shift(RIGHT * 0.4)
        ln = label(r"new $\dot c = 0$", font_size=16, color=MACRO).next_to(ax.ax.c2p(M["k_new"], 1.8), UP,
                                                                          buff=0.08).shift(LEFT * 0.4)
        old = dot(ax, M["k_old"], M["c_old"], WHITE)
        new = dot(ax, M["k_new"], M["c_new"], MACRO)
        jump = Arrow(ax.ax.c2p(M["k_old"], M["c_old"]), ax.ax.c2p(M["k_old"], M["c0"]), buff=0.05, color=EST,
                     stroke_width=3, max_tip_length_to_length_ratio=0.3)
        saddle = path(ax, pk, pc, EST, 3.0, smooth=False)
        mover = Dot(ax.ax.c2p(M["k_old"], M["c0"]), radius=0.08, color=EST)
        # time path of consumption
        axr = plane([-10, 60], [1.5, 1.72], center=RIGHT * 3.7 + DOWN * 0.4, x_length=4.2, y_length=3.4,
                    xticks=[0, 20, 40, 60], yticks=[1.55, 1.6, 1.65, 1.7], xlabel=r"years after the tax",
                    ylabel=r"$c(t)$", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.2f}", font_size=13)
        sel = pt <= 60
        cpath = VGroup(seg(axr, -10, M["c_old"], 0, M["c_old"], WHITE, 2.4),
                       DashedLine(axr.ax.c2p(0, M["c_old"]), axr.ax.c2p(0, M["c0"]), color=EST, stroke_width=2),
                       path(axr, pt[sel], pc[sel], EST, 2.6, smooth=False))
        with self.voiceover(
            "Parts b and c. <bookmark mark='a'/> The phase diagram: the curve where capital is constant, and the "
            "vertical line where consumption is constant. <bookmark mark='b'/> The tax moves that vertical line "
            f"left, from {M['k_old']:.2f} to {M['k_new']:.2f}. The old steady state is now to the right of it. "
            "<bookmark mark='c'/> Capital cannot jump. Consumption can, and it must jump onto the new saddle path, "
            f"the only path that reaches the new steady state: up, from {M['c_old']:.3f} to {M['c0']:.3f}. "
            "Households consume more because saving now pays less after tax. <bookmark mark='d'/> Then capital is "
            f"run down, and consumption falls with it; half the fall in capital takes {M['half_life']:.0f} years. "
            "<bookmark mark='e'/> In the long run consumption ends lower than it began, because this economy has "
            f"less capital than the golden rule's {M['k_gold']:.1f}: less capital means less to consume. The tax "
            "brings consumption forward, and the bill comes later."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(kd), FadeIn(kd_l), Create(c_old), FadeIn(lo), FadeIn(old))
            vo.wait_until("b")
            self.play(Create(c_new), FadeIn(ln), FadeIn(new))
            vo.wait_until("c")
            self.play(GrowArrow(jump), FadeIn(axr), Create(cpath[0]), Create(cpath[1]))
            vo.wait_until("d")
            self.play(Create(saddle), MoveAlongPath(mover, saddle.copy()), Create(cpath[2]), run_time=4.0)
            vo.wait_until("e")
            self.play(Indicate(new, color=MACRO))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"putting the tax in the resource constraint: \ the rebate gives it back",
            r"letting capital jump, \ or consumption fall on impact",
            r"a path that does not reach the steady state: \ every other path breaks transversality or runs out",
            r"guessing the long run: \ compare $k^*$ with the golden rule before saying whether $c^*$ rises",
        ]).move_to(UP * 0.2)
        take = label(r"taxes on saving enter the Euler equation; \ only the jump variable jumps", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Putting the tax in the resource constraint. <bookmark "
            "mark='b'/> Letting capital jump, or getting the direction of consumption's jump wrong. <bookmark "
            "mark='c'/> Drawing a path that never arrives. <bookmark mark='d'/> And guessing the long run "
            "without comparing the steady state with the golden rule. <bookmark mark='e'/> The idea to keep, from "
            "Part twenty: a tax on saving enters the Euler equation, and only the variable that can jump does. "
            "Whether capital should be taxed at all in the long run is a famous argument, and it is still open."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
