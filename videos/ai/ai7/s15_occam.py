from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import DICKENS, HIDDEN, PART, card_in, load

FIT = C.TRUE_P  # the data-fit term
COMP = C.SURPRISE  # the complexity penalty
EVID = C.BITS  # the evidence (marginal likelihood)


class Occam(VoiceoverScene):
    def construct(self):
        card_in(self, 14, r"Bayesian Occam's razor", r"Why does the evidence prefer simple explanations?",
                "Chapter fourteen. Bayesian Occam's razor.")
        self.derive()
        self.lengths()
        self.mackay()
        self.poly()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"-\tfrac12 \mathbf{y}^{\top} (K_\theta + \sigma_n^2 I)^{-1} \mathbf{y}": FIT,
                  r"-\tfrac12 \log |K_\theta + \sigma_n^2 I|": COMP, r"p(\mathbf{y} \mid \theta)": EVID}
        rows = [
            cmath(r"p(\mathbf{y} \mid \theta)", r"=", r"\int p(\mathbf{y} \mid f)\, p(f \mid \theta)\, df", colors=colors,
                  font_size=38),
            cmath(r"p(\mathbf{y} \mid \theta)", r"=", r"\mathcal{N}\big(\mathbf{y};\; 0,\; K_\theta + \sigma_n^2 I\big)",
                  colors=colors, font_size=38),
            cmath(r"\log p(\mathbf{y} \mid \theta)", r"=", r"-\tfrac12 \mathbf{y}^{\top} (K_\theta + \sigma_n^2 I)^{-1} \mathbf{y}",
                  r"-\tfrac12 \log |K_\theta + \sigma_n^2 I|", r"-\tfrac{n}{2} \log 2\pi", colors=colors, font_size=34),
        ]
        rows[2][0].set_color(EVID)
        whys = [why(r"the evidence: \ average the fit \\ over every function the prior allows"),
                why(r"Gaussian prior, Gaussian noise: \\ Gaussian"),
                None]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.2, buff=0.7, edge=6.8)
        head = label(r"The marginal likelihood, \ or evidence", font_size=32).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Chapter thirteen chose its length scale by a quantity we haven't explained: the marginal likelihood, also "
            "called the evidence. It is the probability of the data under the model, averaged over every function "
            "the prior allows. <bookmark mark='a'/> For a Gaussian process the average can be done exactly: the data "
            "is Gaussian, with the kernel matrix plus noise as covariance. <bookmark mark='b'/> Take the log, and it "
            "splits in two. <bookmark mark='c'/> One term measures the fit: how well the data agrees with the model's "
            "covariances. <bookmark mark='d'/> The other is a penalty for complexity: the log-determinant measures how "
            "many different datasets the model could have produced. A flexible model spreads its probability thin."
        ) as vo:
            self.play(FadeIn(head))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            b1 = brace_note(rows[2][2], r"data fit", color=FIT, font_size=24)
            b2 = brace_note(rows[2][3], r"complexity penalty", color=COMP, font_size=24)
            vo.wait_until("c")
            self.play(FadeIn(b1))
            vo.wait_until("d")
            self.play(FadeIn(b2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lengths(self):
        o = load("occam")
        ells, fit, comp, tot = (np.asarray(o[k]) for k in ("ells", "fit", "comp", "total"))
        le = np.log10(ells)
        lo = float(min(fit.min(), comp.min(), tot.min())) - 20
        hi = float(max(fit.max(), comp.max(), tot.max())) + 20
        g = axes([float(le.min()), float(le.max()), 1], [lo, hi, 100], x_length=8.4, y_length=4.8,
                 xlabel=r"length scale $\ell$ (pages)", ylabel=r"nats", xticks=[0, 1, 2], log_x=True,
                 yticks=[round(v, -2) for v in np.linspace(lo + 50, hi - 50, 4)], center=[-1.4, -0.4, 0])
        ax = g.ax
        cf, cc, ct = curve(ax, le, fit, FIT, 3), curve(ax, le, comp, COMP, 3), curve(ax, le, tot, EVID, 5)
        best = float(o["best_ell"])
        ib = int(np.argmax(tot))
        pk = Dot(ax.c2p(le[ib], tot[ib]), radius=0.1, color=EVID)
        lg = legend([(FIT, r"data fit"), (COMP, r"complexity penalty"), (EVID, r"the sum: \ log evidence")], font_size=22)
        lg.move_to([4.9, 1.6, 0])
        res = label(rf"best: \ $\ell = {best:.1f}$ pages", font_size=28, color=EVID).move_to([4.9, -0.2, 0])
        pics = VGroup(label(r"short $\ell$: \ wiggly, \ fits everything", font_size=20, color=GREY_A),
                      label(r"long $\ell$: \ smooth, \ misses the pages", font_size=20, color=GREY_A))
        pics.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.9, -1.6, 0])
        with self.voiceover(
            "Here are the two terms for the rate of 'her' in Great Expectations, as the length scale varies, the noise "
            "and signal levels held where they were fitted. <bookmark mark='a'/> Short length scales make wiggly "
            "functions that can follow every page: the fit is good. Long ones are smooth and miss the pages. "
            "<bookmark mark='b'/> But wiggly functions could have made so many other datasets that they pay a large "
            f"complexity penalty. <bookmark mark='c'/> The sum peaks in between, at about {best:.1f} pages. No "
            "held-out data was needed: the evidence trades fit against complexity by itself. That's Bayesian Occam's "
            "razor."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg))
            vo.wait_until("a")
            self.play(Create(cf), FadeIn(pics[0]))
            vo.wait_until("b")
            self.play(Create(cc), FadeIn(pics[1]))
            vo.wait_until("c")
            self.play(Create(ct), run_time=1.5)
            self.play(FadeIn(pk, scale=1.5), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mackay(self):
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1.1, 0.5], x_length=9.0, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-0.8, -0.4, 0])
        xs = np.linspace(0, 10, 300)

        def bump(m, s):
            return np.exp(-(xs - m) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))

        specs = [(bump(2.5, 0.8), GREY_A, r"simple"), (bump(4.5, 1.5) * 0.9 + 0.1 * bump(6, 2), EVID, r"just right"),
                 (np.full_like(xs, 0.1), COMP, r"flexible")]
        curves = VGroup(*[curve(ax, xs, y, col, 4) for y, col, _ in specs])
        names = VGroup(*[label(nm, font_size=24, color=col) for _, col, nm in specs])
        names[0].next_to(ax.c2p(2.5, specs[0][0].max()), UP, buff=0.1)
        names[1].next_to(ax.c2p(4.6, specs[1][0].max()), UR, buff=0.1)
        names[2].next_to(ax.c2p(9.0, 0.1), UP, buff=0.1)
        d0 = DashedLine(ax.c2p(5.2, 0), ax.c2p(5.2, 1.05), color=WHITE, stroke_width=2)
        dl = label(r"the data we saw", font_size=22).next_to(d0, UP, buff=0.05)
        xl = label(r"all the datasets a model could produce \ $\longrightarrow$", font_size=22, color=GREY_A)
        xl.next_to(ax, DOWN, buff=0.2)
        yl = label(r"$p(\text{data} \mid \text{model})$: \ each curve has area $1$", font_size=22, color=GREY_A)
        yl.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        tag = schematic_tag(UR)
        h = history_card(1992, r"David MacKay", r"\textit{Bayesian Interpolation}", width=3.8).to_corner(UR, buff=0.3)
        h.shift(DOWN * 0.4)
        with self.voiceover(
            "David MacKay drew the reason in 1992. Spread out every dataset a model could produce, and plot how "
            "probable the model makes each one. Every curve has area one. <bookmark mark='a'/> A simple model "
            "predicts a few datasets strongly. A flexible one can produce almost anything, so it gives each only a "
            "little. <bookmark mark='b'/> For the data we actually saw, the model in between wins: flexible enough "
            "to explain it, not so flexible that it bets on everything."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(tag), FadeIn(h))
            self.play(LaggedStart(*[Create(c_) for c_ in curves], lag_ratio=0.4), FadeIn(names), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(curves[0], color=WHITE), Indicate(names[0]))
            self.play(Indicate(curves[2], color=COMP), Indicate(names[2]))
            vo.wait_until("b")
            self.play(Create(d0), FadeIn(dl))
            self.play(Indicate(curves[1], color=EVID))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def poly(self):
        o = load("occam")
        xp, yp, xg = np.asarray(o["xp"]), np.asarray(o["yp"]), np.asarray(o["xg"])
        fits, ev, rmse = np.asarray(o["fits"]), np.asarray(o["evidence"]), np.asarray(o["rmse"])
        degs, best, true = list(o["degs"]), int(o["best_deg"]), int(o["true_deg"])
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[float(yp.min()) - 0.5, float(yp.max()) + 0.5, 1], x_length=5.4,
                  y_length=4.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -0.4, 0])
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=DICKENS) for a, b in zip(xp, yp)])
        k = ValueTracker(0)
        fc = always_redraw(lambda: curve(ax, xg, np.clip(fits[int(round(k.get_value()))], ax.y_range[0], ax.y_range[1]),
                                         HIDDEN, 4, smooth=True))
        dv = Integer(0, font_size=30, color=HIDDEN)
        dlab = VGroup(label(r"polynomial of degree", font_size=24, color=GREY_A), dv).arrange(RIGHT, buff=0.15)
        dlab.next_to(ax, UP, buff=0.2)
        tag = note(rf"${len(xp)}$ points from a cubic, plus noise \ (seeded)", font_size=20).next_to(ax, DOWN, buff=0.2)
        g1 = axes([0, degs[-1], 2], [float(ev.min()) - 2, float(ev.max()) + 2, 5], x_length=4.6, y_length=2.2,
                  ylabel=r"log evidence", xticks=[0, 3, 6, 9, 12], center=[3.6, 1.5, 0])
        g2 = axes([0, degs[-1], 2], [0, float(rmse.max()) * 1.1, 0.1], x_length=4.6, y_length=1.8, xlabel=r"degree",
                  ylabel=r"training error (RMS)", xticks=[0, 3, 6, 9, 12], center=[3.6, -1.7, 0])
        ce = curve(g1.ax, degs, ev, EVID, 4)
        cr = curve(g2.ax, degs, rmse, GREY_B, 3)
        pk = Dot(g1.ax.c2p(best, ev[best]), radius=0.09, color=EVID)
        verdict = (f"The evidence peaks at degree {best}, the true degree, while the training error keeps falling all "
                   f"the way to degree {degs[-1]}." if best == true else
                   f"The evidence peaks at degree {best}; the true degree was {true}. The training error keeps falling "
                   f"all the way to degree {degs[-1]}.")
        with self.voiceover(
            f"One more test, where we know the answer: {len(xp)} points from a cubic curve, plus noise. Fit "
            "polynomials of every degree, from a flat line up to degree twelve, by Bayesian linear regression. "
            "<bookmark mark='a'/> Higher degrees always fit the training points better. <bookmark mark='b'/> " +
            verdict + " <bookmark mark='c'/> Fit against complexity: the same trade-off, seen from the other side, is "
            "the subject of part eight."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), FadeIn(tag), FadeIn(dlab), FadeIn(fc))
            for dg in (1, 2, 3, 6, 9, 12):
                self.play(k.animate.set_value(dg), ChangeDecimalToValue(dv, dg), run_time=0.7)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(cr))
            vo.wait_until("b")
            self.play(FadeIn(g1), Create(ce))
            self.play(FadeIn(pk, scale=1.5), k.animate.set_value(best), ChangeDecimalToValue(dv, best))
        fc.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
