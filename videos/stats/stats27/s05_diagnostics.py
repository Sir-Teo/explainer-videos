from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class Diagnostics(VoiceoverScene):
    def construct(self):
        self.card()
        self.ess()
        self.rhat_idea()
        self.ranks()
        self.chains("stuck")
        self.chains("good")
        self.advice()
        self.warmup()

    def card(self):
        card = chapter_card(4, r"Diagnostics", r"Did the chains find the posterior?", lit=(), part=PART)
        with self.voiceover("Chapter four. Diagnostics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ess(self):
        rows = [
            cmath(r"\mathrm{Var}(\bar f)", r"\approx", r"\dfrac{\sigma_f^2}{S}\Bigl(1 + 2\textstyle\sum_{t \ge 1} \rho_t\Bigr)", font_size=30),
            cmath(r"\text{ESS}", r"=", r"\dfrac{S}{1 + 2\sum_t \rho_t}", font_size=32),
            cmath(r"\text{MCSE}", r"=", r"\sigma_f/\sqrt{\text{ESS}}", font_size=32),
            cmath(r"\text{bulk and tail}", r":", r"\text{ESS for the centre; \ for the 5\% and 95\% quantiles}", font_size=28),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"autocorrelated draws carry less information"), why(r"Geyer's monotone sequence truncates the sum"),
                why(r"the Monte Carlo standard error"), why(r"rank-normalized, \ Vehtari et al.\ (2021)")]
        with self.voiceover(
            "<bookmark mark='a'/> Two questions after every run. First: how much information do the draws carry? A chain's "
            "draws are correlated, which inflates the variance of any average by one plus twice the sum of the "
            "autocorrelations. <bookmark mark='b'/> Dividing the number of draws by that factor gives the effective sample "
            "size. <bookmark mark='c'/> The Monte Carlo standard error of a posterior mean is the posterior SD over the root "
            "of the ESS. <bookmark mark='d'/> Aki Vehtari and colleagues recommend two versions: a bulk ESS computed on "
            "ranks, for the centre of the distribution, and a tail ESS for the quantiles that make intervals."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rhat_idea(self):
        rows = [
            cmath(r"\text{run}", r":", r"4 \text{ chains from scattered starting points}", font_size=30),
            cmath(r"\hat R", r"=", r"\sqrt{\dfrac{\tfrac{n - 1}{n}W + \tfrac1n B}{W}}", font_size=32),
            cmath(r"\hat R \approx 1", r":", r"\text{the chains agree with each other}", font_size=30),
            cmath(r"\text{rule}", r":", r"\hat R < 1.01 \text{ on ranks, \ split chains, \ and tails}", font_size=30),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"disagreement is detectable"), why(r"between-chain against within-chain variance"),
                why(r"Gelman \& Rubin (1992)"), why(r"Vehtari et al.\ (2021)")]
        with self.voiceover(
            "<bookmark mark='a'/> The second question: did the chains find the posterior at all? Run several chains from "
            "deliberately scattered starts. <bookmark mark='b'/> Andrew Gelman and Donald Rubin's R-hat compares the "
            "variance between the chains' means with the variance within each chain. <bookmark mark='c'/> If every chain "
            "has explored the same distribution, R-hat is close to one. <bookmark mark='d'/> The modern version splits each "
            "chain in half, so a chain that drifts disagrees with itself, works on ranks so heavy tails can't hide "
            "anything, and checks the tails separately; it should be below one point oh one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chains(self, which):
        d = load("diagnostics")[which]
        ch = np.asarray(d["chains"])
        n = ch.shape[1]
        A = axes([0, n], [-6.5, 6.5], x_length=8.0, y_length=4.2, xlabel=r"iteration", ylabel=r"$x$",
                 xticks=[], yticks=[-4, 0, 4], center=[-1.8, 0.3, 0])
        ax = A.ax
        lines = VGroup(*[polyline(ax, np.arange(n), c, CHAINS[k], 1.4, 0.85) for k, c in enumerate(ch)])
        modes = VGroup(*[DashedLine(ax.c2p(0, m), ax.c2p(n, m), color=EXACTC, stroke_width=1.5) for m in (-4, 4)])
        if which == "stuck":
            rows = fit_rows(VGroup(
                label(r"a target with two modes, \ at $-4$ and $+4$", font_size=22, color=EXACTC),
                label(r"random walk, \ small steps", font_size=22),
                label(r"three chains never leave $-4$; \ one never leaves $+4$", font_size=22, color=RES),
                label(rf"$\hat R = {d['rhat']:.2f}$; \ bulk ESS {d['ess_bulk']:.0f}", font_size=22, color=RES),
                label(rf"mean {d['mean']:.2f}: \ the truth is 0", font_size=22, color=RES),
            ), 3.6, 0.42, [5.0, 0.3, 0])
            text = ("<bookmark mark='a'/> A target with two equal modes, at minus four and plus four. <bookmark mark='b'/> "
                    "Four random-walk chains with small steps. <bookmark mark='c'/> Each stays in the mode where it "
                    "started: three chains below, one above. Any one of them, alone, looks perfectly healthy. "
                    "<bookmark mark='d'/> Together they disagree, and R-hat is one point five three, with an effective sample "
                    "size of seven. <bookmark mark='e'/> The pooled mean is minus two, where the truth is zero. Multiple chains exist to catch exactly this.")
        else:
            rows = fit_rows(VGroup(
                label(r"the same target", font_size=22, color=EXACTC),
                label(r"steps large enough to jump between modes", font_size=22),
                label(r"every chain visits both", font_size=22, color=HIT),
                label(rf"$\hat R = {d['rhat']:.3f}$; \ bulk ESS {d['ess_bulk']:.0f}", font_size=22, color=HIT),
                label(rf"mean {d['mean']:.2f}", font_size=22, color=HIT),
            ), 3.6, 0.42, [5.0, 0.3, 0])
            text = ("<bookmark mark='a'/> The same target, <bookmark mark='b'/> now with steps large enough to jump between "
                    "the modes. <bookmark mark='c'/> Every chain visits both. <bookmark mark='d'/> R-hat is one point oh oh "
                    "eight, and the effective sample size six hundred and thirty. <bookmark mark='e'/> The mean, point three "
                    "three, is within about two Monte Carlo standard errors of zero. A "
                    "warning, though: R-hat can only compare the chains you ran. If none of them ever finds a mode, nothing "
                    "will tell you it exists.")
        with self.voiceover(text) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(modes))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.25), FadeIn(rows[1]), run_time=3.0)
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def advice(self):
        rows = fit_rows(VGroup(
            label(r"4 or more chains, \ dispersed starts", font_size=24),
            label(r"$\hat R < 1.01$ \ for every quantity you report", font_size=24, color=HIT),
            label(r"bulk and tail ESS above about 400", font_size=24, color=HIT),
            label(r"look at trace and rank plots", font_size=24),
            label(r"and remember: \ diagnostics detect failure; \ they cannot prove success", font_size=24, color=RES),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The routine, then. Run four or more chains from dispersed starting points. "
            "<bookmark mark='b'/> Require R-hat below one point oh one for everything you report, <bookmark mark='c'/> and "
            "bulk and tail effective sample sizes above about four hundred. <bookmark mark='d'/> Look at the traces. "
            "<bookmark mark='e'/> And remember that diagnostics can show a run failed; they can never prove one succeeded."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def ranks(self):
        d = load("diagnostics")
        group = VGroup()
        anims = []
        for k, key in enumerate(("stuck", "good")):
            ch = np.asarray(d[key]["chains"])
            from scipy import stats as _st
            r = _st.rankdata(ch.ravel()).reshape(ch.shape)
            edges = np.linspace(0, ch.size, 11)
            for c in range(4):
                h, _ = np.histogram(r[c], edges)
                A = axes([0, 10], [0, 200], x_length=2.6, y_length=1.2, xlabel=r"", ylabel=r"", xticks=[], yticks=[],
                         center=[-4.6 + 3.05 * c, 1.6 - 2.9 * k, 0])
                bars = bars_at(A.ax, np.arange(10) + 0.5, h, 0.8, CHAINS[c], 0.85)
                group.add(A)
                anims.append(bars)
            group.add(label(r"stuck chains" if key == "stuck" else r"mixing chains", font_size=24,
                            color=RES if key == "stuck" else HIT).move_to([0, 2.65 - 2.9 * k, 0]))
        foot = label(r"rank all draws together; \ each chain's ranks should be uniform", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> A rank plot shows the same thing at a glance. Rank all the draws from all the chains "
            "together, and histogram each chain's ranks. <bookmark mark='b'/> For the stuck chains, three have only low ranks "
            "and one only high ones. <bookmark mark='c'/> For mixing chains, every histogram is flat: each chain has seen the "
            "same distribution. Rank plots are more sensitive than trace plots, which can look fine when they are not."
        ) as vo:
            self.play(FadeIn(group), FadeIn(foot))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in anims[:4]], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in anims[4:]], lag_ratio=0.2))
        self.clear_scene()

    def warmup(self):
        rows = [
            cmath(r"\text{warmup}", r":", r"\text{discard the start: \ it remembers where it began}", font_size=28),
            cmath(r"\text{thinning}", r":", r"\text{keeping every 10th draw loses information}", font_size=28),
            cmath(r"\text{only reason to thin}", r":", r"\text{storage, \ or expensive post-processing}", font_size=28),
            cmath(r"\text{MCSE}", r":", r"\text{report it: \ how many digits are real?}", font_size=30),
        ]
        rows[3][-1].set_color(HIT)
        whys = [why(r"not the same as convergence"), why(r"Link \& Eaton (2012)"), why(r"not accuracy"), why(r"the error of the Monte Carlo itself")]
        with self.voiceover(
            "<bookmark mark='a'/> Three more habits. Discard the warmup: early draws still remember where the chain began, "
            "and for NUTS they are also when the tuning happens. <bookmark mark='b'/> Don't thin to improve accuracy: keeping "
            "every tenth draw throws away information, and the effective sample size of what's left is never larger. "
            "<bookmark mark='c'/> Thin only to save storage or downstream computation. <bookmark mark='d'/> And report the "
            "Monte Carlo standard error, so readers know how many digits of a posterior mean are real."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
