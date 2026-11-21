from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Calibrate(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Calibration against estimation", r"Borrow a number, or fit it?",
             "Chapter nine. Calibration against estimation.",
             lit={1982: r"Kydland and Prescott", 1996: r"Hansen and Heckman"}, scale=("nation",),
             horizon=("a decade",))
        self.debate()
        self.profile()

    def debate(self):
        cards = point_cards([
            (r"calibration", r"take each parameter from other evidence: \ micro studies, \ long-run averages; \ "
             r"then judge the model on what it was not built to match", PATIENCE),
            (r"estimation", r"fit the parameters to the data at hand, \ with standard errors and a test of fit",
             EST),
            (r"the compromise", r"calibrate what is well measured elsewhere, \ estimate the rest; \ or put the "
             r"outside evidence in as a prior, \ as Bayesian estimation does", GAIN),
        ], width=12.6, cols=3, font_size=21).move_to(UP * 0.4)
        tag = published_tag(r"Kydland and Prescott, \ Econometrica (1982), \ JEP 10(1) (1996); \ Hansen and "
                            r"Heckman, \ JEP 10(1) (1996)", corner=DR, font_size=12)
        with self.voiceover(
            "When Finn Kydland and Edward Prescott built the first real business cycle model in 1982, they did not "
            "estimate it. <bookmark mark='a'/> They calibrated it: each parameter was taken from other evidence, a "
            "long-run average or a study of households, and the model was then judged on things it had not been "
            "built to match, like how much consumption moves over the cycle. <bookmark mark='b'/> Lars Peter "
            "Hansen and James Heckman replied, in the same journal issue of 1996, that borrowed numbers come from "
            "other models and other populations, and that a model whose parameters are never confronted with the "
            "data cannot be told it is wrong. <bookmark mark='c'/> The modern practice is a compromise: calibrate "
            "what is well measured elsewhere and estimate the rest, or let the outside evidence enter as a prior, "
            "as the Bayesian estimation of central banks' models does. On the Island we can see what the choice "
            "costs."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def profile(self):
        L = load("lifecycle")
        P = L["profile"]
        g = np.array([p["gamma"] for p in P])
        b = np.array([p["beta"] for p in P])
        o = np.array([p["obj"] for p in P])
        axb = plane([0.9, 4.1], [0.92, 0.965], center=LEFT * 3.4 + DOWN * 0.5, x_length=5.4, y_length=4.2,
                    xticks=[1, 2, 3, 4], yticks=[0.93, 0.94, 0.95, 0.96], xlabel=r"caution $\gamma$, \ calibrated",
                    ylabel=r"patience $\beta$, \ estimated", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                    font_size=13)
        axo = plane([0.9, 4.1], [0, 3.6], center=RIGHT * 3.2 + DOWN * 0.5, x_length=5.4, y_length=4.2,
                    xticks=[1, 2, 3, 4], yticks=[0, 1, 2, 3], xlabel=r"caution $\gamma$, \ calibrated",
                    ylabel=r"misfit, \ $\log_{10}$ of the $J$ statistic", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=13)
        lb = path(axb, g, b, PATIENCE, 3.0, smooth=False)
        dots_b = VGroup(*[dot(axb, x, y, PATIENCE, 0.06) for x, y in zip(g, b)])
        lo = path(axo, g, np.log10(o), ERR, 3.0)
        crit = DashedLine(axo.ax.c2p(0.9, np.log10(L["crit"])), axo.ax.c2p(4.1, np.log10(L["crit"])), color=GAIN,
                          stroke_width=1.6)
        crit_l = label(r"the 5\% line", font_size=15, color=GAIN).next_to(axo.ax.c2p(4.1, np.log10(L["crit"])),
                                                                          UP, buff=0.08).shift(LEFT * 0.5)
        pick = {1.0: r"1: \ macro studies", 4.0: r"4: \ survey gambles"}
        marks = VGroup()
        for gg, txt in pick.items():
            k = int(np.argmin(np.abs(g - gg)))
            marks.add(VGroup(dot(axb, g[k], b[k], E.ACCENT, 0.1),
                             label(rf"{txt}: \ $\beta = {b[k]:.3f}$", font_size=15, color=E.ACCENT).next_to(
                                 axb.ax.c2p(g[k], b[k]), UR if gg < 2 else DL, buff=0.1)))
        head = label(r"fix caution from the Dials, \ estimate patience", font_size=24, color=E.ACCENT).to_edge(
            UP, buff=0.45)
        tag = island_tag(r"simulated: \ the Island's households", corner=DR, font_size=13)
        k1, k4 = int(np.argmin(np.abs(g - 1))), int(np.argmin(np.abs(g - 4)))
        k2 = int(np.argmin(np.abs(g - 2)))
        with self.voiceover(
            "Suppose we calibrate caution, taking it from the Dial of relative risk aversion, and estimate only "
            "patience. <bookmark mark='a'/> The left panel is the best patience for each calibrated caution. They "
            f"trade off along the ridge: calibrate caution at one, as studies of consumption and labour supply "
            f"suggest, and patience comes out at {b[k1]:.3f}; <bookmark mark='b'/> calibrate it at four, from "
            f"surveys of gambles over lifetime income, and patience is {b[k4]:.3f}. The borrowed number decides "
            "the estimated one. <bookmark mark='c'/> But the data are not silent. The right panel is how badly "
            "each pair fits, on a log scale. Only near caution two does the fit pass the test: at one the J "
            f"statistic is {o[k1]:.0f}, at four {o[k4]:.0f}, against {o[k2]:.0f} at two. <bookmark mark='d'/> So "
            "calibration hides nothing if you also report the fit; it misleads when the borrowed number is "
            "simply assumed, and the profiles the model was meant to explain are never looked at again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axb), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(dots_b), run_time=1.5)
            self.play(FadeIn(marks[0]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]))
            vo.wait_until("c")
            self.play(FadeIn(axo), Create(crit), FadeIn(crit_l))
            self.play(Create(lo), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(lo, color=WHITE, scale_factor=1.0))
        self.clear_scene()
