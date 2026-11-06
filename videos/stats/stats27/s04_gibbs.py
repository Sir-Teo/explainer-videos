from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class Gibbs(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.zigzag()
        self.augmentation()
        self.probit()
        self.blocking()
        self.limits()

    def card(self):
        card = chapter_card(3, r"Gibbs sampling", r"One coordinate at a time", lit=(1990,), part=PART)
        with self.voiceover("Chapter three. Gibbs sampling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"x_1^{(t+1)}", r"\sim", r"\pi(x_1 \mid x_2^{(t)}, \dots, x_d^{(t)})", font_size=30),
            cmath(r"x_2^{(t+1)}", r"\sim", r"\pi(x_2 \mid x_1^{(t+1)}, x_3^{(t)}, \dots)", font_size=30),
            cmath(r"\text{acceptance}", r"=", r"1: \ \text{an MH step with } q = \pi(\cdot \mid \text{rest})", font_size=30),
            cmath(r"\text{needs}", r":", r"\text{full conditionals you can sample: \ conjugacy}", font_size=30),
        ]
        rows[2][2].set_color(HIT)
        whys = [why(r"draw each coordinate given the others"), why(r"using the newest values"),
                why(r"the Hastings ratio is exactly one"), why(r"Part 26's conjugate pieces")]
        with self.voiceover(
            "<bookmark mark='a'/> Stuart and Donald Geman's Gibbs sampler of 1984, brought to statistics by Alan Gelfand "
            "and Adrian Smith in 1990, updates one coordinate at a time, drawing it from its distribution given all the "
            "others. <bookmark mark='b'/> Then the next coordinate, using the newest values. <bookmark mark='c'/> Each update "
            "is a Metropolis–Hastings step whose proposal is the conditional itself, so its acceptance probability is "
            "exactly one. <bookmark mark='d'/> It needs full conditionals you can sample, which is where Part 26's "
            "conjugate pairs earn their keep: inside a big model, each piece is often conjugate given the rest."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def zigzag(self):
        d = load("gibbs")
        rho = d["rho"]
        A = axes([-3.5, 3.5], [-3.5, 3.5], x_length=4.8, y_length=4.8, xlabel=r"$x_1$", ylabel=r"$x_2$", xticks=[-3, 0, 3],
                 yticks=[-3, 0, 3], center=[-3.0, 0.1, 0])
        ax = A.ax
        L = Landscape(ax, lambda X, Y: np.exp(-0.5 * (X ** 2 - 2 * rho * X * Y + Y ** 2) / (1 - rho ** 2)), (-3.5, 3.5), (-3.5, 3.5),
                      levels=[0.6, 0.3, 0.1, 0.02], color=EXACTC, stroke_width=1.6)
        path = np.asarray(d["path"])
        zig = polyline(ax, path[:, 0], path[:, 1], SAMPLER, 2.2)
        rows = fit_rows(VGroup(
            label(rf"a normal with correlation {rho}", font_size=22, color=EXACTC),
            label(r"each move parallel to an axis", font_size=22, color=SAMPLER),
            label(r"steps as wide as the ridge, \ not as long", font_size=22, color=RES),
            label(rf"ESS: \ {d['ess_x1']:.0f} from {d['n']:,} sweeps", font_size=22, color=RES),
            label(r"reparametrize: \ move along the ridge", font_size=22, color=HIT),
        ), 5.8, 0.42, [3.6, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Gibbs sampling's weakness shows on a correlated target: a normal with correlation point nine "
            "five. <bookmark mark='b'/> Every move is parallel to an axis, so the chain zigzags. <bookmark mark='c'/> Each "
            "step can only be as large as the ridge is wide, while the ridge is long. <bookmark mark='d'/> Two thousand "
            "sweeps are worth thirty-three independent draws. <bookmark mark='e'/> The cure is to reparametrize, or to "
            "update correlated parameters together, a block, so that moves can run along the ridge."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(L.levels))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(zig), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def augmentation(self):
        rows = [
            cmath(r"y_i", r"=", r"1\{z_i > 0\}, \ \ z_i \sim N(x_i^\top\beta, 1)", font_size=30),
            cmath(r"z_i \mid \beta, y_i", r"\sim", r"N(x_i^\top\beta, 1) \text{ truncated to the side } y_i \text{ says}", font_size=28),
            cmath(r"\beta \mid z", r"\sim", r"N\bigl((X^\top X)^{-1}X^\top z, \ (X^\top X)^{-1}\bigr)", font_size=30),
            cmath(r"\text{the trick}", r":", r"\text{add latent variables until every conditional is easy}", font_size=28),
        ]
        rows[2][2].set_color(SAMPLER)
        whys = [why(r"probit as a latent threshold: \ Part 24's tolerance"), why(r"a truncated normal"),
                why(r"ordinary least squares on $z$, \ flat prior"), why(r"Tanner \& Wong (1987): \ data augmentation")]
        with self.voiceover(
            "<bookmark mark='a'/> Gibbs sampling becomes powerful with data augmentation. James Albert and Siddhartha Chib "
            "wrote probit regression as a latent threshold: each binary outcome records whether a hidden normal variable "
            "exceeds zero, Part 24's tolerance distribution. <bookmark mark='b'/> Given the coefficients, each hidden "
            "variable is a normal truncated to the side its outcome says. <bookmark mark='c'/> Given the hidden variables, "
            "the coefficients are an ordinary least-squares posterior. <bookmark mark='d'/> Neither conditional is hard, "
            "though the posterior of beta alone has no closed form: add latent variables until every conditional is easy."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def probit(self):
        d = load("gibbs")["probit"]["centred"]
        tr = np.asarray(d["trace_slope"])
        A = axes([0, 400], [15, 25], x_length=7.4, y_length=3.6, xlabel=r"iteration", ylabel=r"slope on log dose",
                 xticks=[0, 200, 400], yticks=[16, 20, 24], center=[-2.0, 0.6, 0])
        ax = A.ax
        c = polyline(ax, np.arange(len(tr)), tr, SAMPLER, 1.6)
        mle = DashedLine(ax.c2p(0, d["mle"][1]), ax.c2p(400, d["mle"][1]), color=EXACTC, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"Bliss's 481 beetles, \ Part 24: \ probit by Gibbs", font_size=22, color=PATH),
            label(rf"posterior mean slope {d['mean'][1]:.2f} \ (SD {d['sd'][1]:.2f})", font_size=22, color=SAMPLER),
            label(rf"gold: \ the MLE, \ {d['mle'][1]:.2f} \ (SE {d['mle_se'][1]:.2f})", font_size=22, color=EXACTC),
            label(rf"ESS {d['ess_slope']:.0f} of {d['n']:,}: \ the latent $z$'s slow it", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On Bliss's beetles from Part 24, four hundred and eighty-one of them, the Gibbs sampler "
            "for the probit model. <bookmark mark='b'/> The posterior mean slope is nineteen point eight, <bookmark mark='c'/> "
            "beside the maximum likelihood estimate of nineteen point seven three, with matching uncertainty, as "
            "Bernstein–von Mises promised for this much data. <bookmark mark='d'/> But the trace wanders: two thousand five "
            "hundred iterations are worth about two hundred and thirty independent draws, because beta and the hidden z's "
            "are strongly dependent and each conditional update can only move a little."
        ) as vo:
            self.add(historical_tag(r"Bliss (1935)", corner=DR))
            self.play(FadeIn(A), Create(mle))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"BUGS (1989): \ Gibbs for any conjugate graphical model", font_size=24, color=SAMPLER),
            label(r"Metropolis-within-Gibbs for the pieces that are not conjugate", font_size=24),
            label(r"slow when parameters are strongly dependent", font_size=24, color=RES),
            label(r"the eight schools: \ $\theta \mid \tau$ and $\tau \mid \theta$ lock each other near $\tau = 0$", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The BUGS project, from 1989, automated this: describe a graphical model, and the software "
            "derives and samples every conditional. <bookmark mark='b'/> Pieces that aren't conjugate get Metropolis steps "
            "inside the sweep. <bookmark mark='c'/> Its weakness is dependence between parameters. <bookmark mark='d'/> In "
            "the eight schools, when tau is small the effects are pinned near mu, and when the effects are close together "
            "tau stays small: each conditional traps the other, the geometry chapter seven returns to."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def blocking(self):
        rows = [
            cmath(r"\text{block}", r":", r"\text{update correlated parameters together}", font_size=30),
            cmath(r"\text{collapse}", r":", r"\text{integrate a parameter out analytically}", font_size=30),
            cmath(r"\text{reparametrize}", r":", r"\text{make the coordinates nearly independent}", font_size=30),
            cmath(r"\text{eight schools}", r":", r"\text{draw } \mu \text{ and } \theta \text{ jointly given } \tau", font_size=30),
        ]
        rows[3][-1].set_color(HIT)
        whys = [why(r"the zigzag, \ straightened"), why(r"Liu (1994): \ fewer, \ freer parameters"), why(r"chapter seven's non-centring"), why(r"Part 26's exact factorization")]
        with self.voiceover(
            "<bookmark mark='a'/> Three standard cures for slow Gibbs samplers. Block: update strongly correlated "
            "parameters together, drawing them jointly from their conditional. <bookmark mark='b'/> Collapse: integrate a "
            "parameter out analytically, so the remaining ones move more freely. <bookmark mark='c'/> Reparametrize, so that "
            "the coordinates are nearly independent, chapter seven's trick. <bookmark mark='d'/> Part 26's exact sampler for "
            "the eight schools was the extreme case: given tau, it drew mu and every effect jointly, collapsing the whole "
            "problem to one dimension."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
