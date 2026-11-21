from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403

YTICKS = ([-2.0, -1.0, 0], [-0.4, -0.2, 0, 0.2], [0, 0.5, 1.0])


class Matching(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Matching impulse responses", r"Can a model be fitted to what a shock does?",
             "Chapter ten. Matching impulse responses.", lit={2005: r"Christiano, Eichenbaum and Evans"},
             scale=("nation",), horizon=("a year",))
        self.idea()
        self.fit()

    def idea(self):
        eq = MathTex(r"\hat\theta = \arg\min_\theta \; \big(\hat\psi - \psi(\theta)\big)'\, V^{-1}\, "
                     r"\big(\hat\psi - \psi(\theta)\big)", font_size=42, color=THEORY).move_to(UP * 1.4)
        rows = VGroup(
            label(r"$\hat\psi$: \ the responses to a monetary shock, \ estimated with an instrument", font_size=21,
                  color=DATA),
            label(r"$\psi(\theta)$: \ the same responses, \ computed from the model", font_size=21, color=MODEL),
            label(r"$V$: \ how noisy each estimated response is", font_size=21, color=GREY_A),
            label(r"Part 54's simulated moments, \ with responses as the moments", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(eq, DOWN, buff=0.7)
        tag = published_tag(r"Christiano, \ Eichenbaum and Evans, \ JPE 113(1) (2005)", corner=DR, font_size=12)
        with self.voiceover(
            "There is a middle way between estimating a whole model and estimating a single response. Lawrence "
            "Christiano, Martin Eichenbaum and Charles Evans first identified the effects of a monetary shock with "
            "an autoregression, then chose the parameters of a model to reproduce them. <bookmark mark='a'/> "
            "Estimate how the economy responds to the shock. <bookmark mark='b'/> Compute the same responses from "
            "the model, for any parameters. <bookmark mark='c'/> Weight each by how precisely it was measured, "
            "<bookmark mark='d'/> and minimize the distance: Part fifty-four's method of moments, with the "
            "responses as the moments."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.5)
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def fit(self):
        M = load("irfmatch")
        tgt, se = np.array(M["target"]), np.array(M["se"])
        fit, start, tr = np.array(M["fitted"]), np.array(M["start_irf"]), np.array(M["truth_irf"])
        h = np.arange(M["h"] + 1)
        names = (r"output gap", r"inflation", r"the rate")
        cols = (OUT, INFL, RATE)
        ranges = ((-2.2, 0.8), (-0.6, 0.3), (-0.4, 1.2))
        panels = VGroup()
        for k in range(3):
            ax = plane([0, M["h"]], list(ranges[k]), x_length=3.9, y_length=3.0, xticks=[0, 4, 8, 12],
                       yticks=YTICKS[k], xlabel=r"quarters", ylabel=r"", xfmt=lambda v: f"{v:.0f}",
                       yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=11)
            z = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(M["h"], 0), color=GREY_D, stroke_width=1)
            errs = VGroup(*[Line(ax.ax.c2p(t, max(tgt[t, k] - se[t, k], ranges[k][0])),
                                 ax.ax.c2p(t, min(tgt[t, k] + se[t, k], ranges[k][1])), color=cols[k],
                                 stroke_width=1.6) for t in h])
            pts = VGroup(*[Dot(ax.ax.c2p(t, tgt[t, k]), radius=0.045, color=cols[k]) for t in h
                           if ranges[k][0] <= tgt[t, k] <= ranges[k][1]])
            s0 = path(ax, h, start[:, k], GREY_B, 2.0, yr=ranges[k])
            f1 = path(ax, h, fit[:, k], EST, 2.6, yr=ranges[k])
            t1 = path(ax, h, tr[:, k], TRUTHC, 1.6, yr=ranges[k])
            nm = label(names[k], font_size=18, color=cols[k]).next_to(ax, UP, buff=0.12)
            panels.add(VGroup(ax, z, errs, pts, s0, f1, t1, nm))
        panels.arrange(RIGHT, buff=0.45).move_to(UP * 0.55)
        e, t_ = M["estimate"], M["truth"]
        rows = VGroup(
            label(r"dots: \ estimated responses, \ one standard error \qquad grey: \ the model at a poor start "
                  r"\qquad gold: \ fitted \qquad white: \ the truth", font_size=16, color=GREY_A),
            label(rf"$\sigma$: \ {e['sigma']:.2f} \ (truth {t_['sigma']:.1f}); \ across 60 histories "
                  rf"{M['sigma_5_95'][0]:.2f} to {M['sigma_5_95'][1]:.2f}", font_size=20, color=EST),
            label(rf"$\kappa$: \ {e['kappa']:.3f} \ (truth {t_['kappa']:.1f}); \ across 60 histories "
                  rf"{M['kappa_5_95'][0]:.3f} to {M['kappa_5_95'][1]:.3f}", font_size=20, color=INFL),
        ).arrange(DOWN, buff=0.22).next_to(panels, DOWN, buff=0.5)
        tag = island_tag(r"simulated: \ the Island's model, \ 400 quarters", corner=DR, font_size=13)
        with self.voiceover(
            "On the Island: four hundred quarters of an economy like the one estimated in Chapter seven, but whose "
            "central bank surprises more often, and a market surprise as the instrument. <bookmark mark='a'/> The "
            "dots are the estimated responses of the output gap, inflation and the rate to a one-point surprise, "
            "with their standard errors. <bookmark mark='b'/> In grey, the model at a poor starting guess. "
            "<bookmark mark='c'/> In gold, the model after matching, with two parameters free: the curvature that "
            "governs how spending responds to the rate, and the slope of the Phillips curve. <bookmark mark='d'/> "
            f"Sigma comes out at {e['sigma']:.2f}, against {t_['sigma']:.1f}. The Phillips slope comes out at "
            f"{e['kappa']:.3f}, against {t_['kappa']:.1f}, and across sixty histories it ranges from "
            f"{M['kappa_5_95'][0]:.2f} to {M['kappa_5_95'][1]:.2f}: inflation's response is small and noisy, so "
            "the slope it implies is uncertain. The method can only be as sharp as the responses it matches."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(VGroup(p_[0], p_[1], p_[7])) for p_ in panels])
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(p_[2], p_[3])) for p_ in panels], FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[Create(p_[4]) for p_ in panels])
            vo.wait_until("c")
            self.play(*[Create(p_[5]) for p_ in panels], *[Create(p_[6]) for p_ in panels], run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.clear_scene()
