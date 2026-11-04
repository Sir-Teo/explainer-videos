from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403


class Studies(VoiceoverScene):
    def construct(self):
        self.card()
        self.ademp()
        self.wald()
        self.mcse()
        self.streams_()
        self.harness()

    def card(self):
        card = chapter_card(6, r"Simulation studies done right", r"Experiments on methods, \ with error bars", part=PART)
        with self.voiceover("Chapter six. Simulation studies, done right."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ademp(self):
        items = [("A", r"Aims", r"what question about which methods?"),
                 ("D", r"Data-generating mechanisms", r"the worlds you simulate: \ sample sizes, \ effect sizes, \ tails"),
                 ("E", r"Estimands", r"the true quantity each method targets"),
                 ("M", r"Methods", r"the procedures compared, \ on the same data sets"),
                 ("P", r"Performance measures", r"bias, \ empirical SE, \ coverage, \ power, \ each with its Monte Carlo SE")]
        rows = VGroup()
        for k, (L, nm, desc) in enumerate(items):
            rows.add(VGroup(MathTex(L, font_size=48, color=S.ACCENT), label(nm, font_size=28), label(desc, font_size=22, color=GREY_A))
                     .arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.2, 0])
        hc = note(r"T. Morris, I. White \& M. Crowther, \ ``Using simulation studies to evaluate statistical methods'', \ "
                  r"\emph{Statistics in Medicine} 38 (2019)").to_edge(DOWN, buff=0.3)
        head = label(r"a simulation study is an experiment, \ and needs a protocol", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "A simulation study is an experiment whose subjects are statistical methods, and like any experiment it "
            "needs a protocol, written down before you look at results. Tim Morris, Ian White and Michael Crowther "
            "summarized one in 2019 with the word ADEMP. <bookmark mark='a'/> Aims: what question, about which "
            "methods. <bookmark mark='b'/> Data-generating mechanisms: the worlds you'll simulate, with their sample "
            "sizes, effect sizes and tails. <bookmark mark='c'/> Estimands: the true quantity each method is trying "
            "to recover. <bookmark mark='d'/> Methods: the procedures, applied to the same simulated data sets. "
            "<bookmark mark='e'/> Performance measures: bias, standard error, coverage, power; and every one of "
            "them reported with its own Monte Carlo error, because a simulation is itself a random sample."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def wald(self):
        d = load("simstudy")
        ps, cov, mcse, ex, wil = (np.asarray(d[k]) for k in ("ps", "cover", "mcse", "exact", "wilson"))
        A = axes([0, 1], [0.4, 1.0], x_length=6.8, y_length=4.6, xlabel=r"true $p$", ylabel=r"coverage of a nominal 95\% interval",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.4, 0.6, 0.8, 0.95, 1.0], center=[-2.6, -0.4, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(0, 0.95), ax.c2p(1, 0.95), color=GREY_B, stroke_width=1.5)
        bars_ = VGroup(*[Line(ax.c2p(p, c - 2 * s), ax.c2p(p, c + 2 * s), color=BAD, stroke_width=2) for p, c, s in zip(ps, cov, mcse)])
        dots = VGroup(*[Dot(ax.c2p(p, c), radius=0.05, color=BAD) for p, c in zip(ps, cov)])
        exl = polyline(ax, ps, ex, EXACT, 2)
        wl = polyline(ax, ps, wil, GOOD, 2.5)
        rows = fit_rows(VGroup(
            MathTex(r"\text{Wald: } \hat p \pm 1.96\sqrt{\hat p(1 - \hat p)/n}", font_size=26, color=BAD),
            label(r"$n = 30$; \ 4,000 replicates per $p$; \ bars: \ $\pm 2$ Monte Carlo SE", font_size=22, color=GREY_A),
            label(r"gold: \ the exact coverage, \ by summing the binomial", font_size=22, color=EXACT),
            label(r"green: \ Wilson's interval (1927)", font_size=22, color=GOOD),
            label(r"the Wald interval is broken: \ Part 11", font_size=24, color=S.ACCENT),
        ), 4.6, 0.28, [4.6, 0.4, 0])
        with self.voiceover(
            "Here's a small simulation study with a big result. <bookmark mark='a'/> The aim: does the textbook "
            "interval for a proportion, the sample share plus or minus one point nine six standard errors, cover the "
            "truth ninety-five percent of the time? The data: thirty binomial trials, for forty-nine values of p. "
            "<bookmark mark='b'/> For each p, four thousand simulated samples. Red: the coverage, with bars of two "
            "Monte Carlo standard errors. It's rarely ninety-five, it's ragged, and near zero and one it collapses "
            "below fifty percent. <bookmark mark='c'/> The gold line is the exact coverage, which for this simple "
            "problem we can compute by summing the binomial: the simulation agrees, within its error bars. "
            "<bookmark mark='d'/> Edwin Wilson's interval from 1927, in green, does far better. Part 11 explains why."
        ) as vo:
            self.play(FadeIn(A), Create(nom))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(bars_), FadeIn(dots, lag_ratio=0.02))
            vo.wait_until("c")
            self.play(Create(exl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(wl), FadeIn(rows[3:]))
        self.clear_scene()

    def mcse(self):
        rows = [
            cmath(r"\mathrm{MCSE}(\widehat{\text{coverage}})", r"=", r"\sqrt{\frac{c(1 - c)}{R}}", font_size=32),
            cmath(r"c = 0.95,\ R = 4000:\quad \mathrm{MCSE}", r"=", r"0.0034", font_size=32),
            cmath(r"R", r"=", r"\frac{c(1 - c)}{\mathrm{MCSE}^2}", r"\quad\Rightarrow\quad", r"\mathrm{MCSE} = 0.0025 \text{ needs } R = 7{,}600",
                  font_size=30),
            cmath(r"\mathrm{MCSE}(\widehat{\text{bias}})", r"=", r"\frac{\widehat{\mathrm{SE}}_{\text{emp}}}{\sqrt R}", font_size=32),
        ]
        rows[1][2].set_color(S.ACCENT)
        whys = [why(r"coverage is a proportion of $R$ replicates"), why(r"so a reported 94.8\% means $94.8 \pm 0.7$"),
                why(r"plan $R$ for the precision you need: \ to tell 94\% from 95\%"), why(r"a bias is a mean of $R$ errors")]
        with self.voiceover(
            "Every number a simulation produces is an estimate, and needs an error bar. <bookmark mark='a'/> A "
            "coverage is a proportion of R replicates, so its Monte Carlo standard error is root c times one minus c "
            "over R. <bookmark mark='b'/> With four thousand replicates and coverage near ninety-five percent, "
            "that's about a third of a percentage point: a reported ninety-four point eight means ninety-four point "
            "eight plus or minus point seven. <bookmark mark='c'/> Turn it around to plan the study: to resolve a "
            "quarter of a point, you need about seventy-six hundred replicates. <bookmark mark='d'/> A bias is an "
            "average of R errors, so its standard error is the empirical standard error over root R. Report them; "
            "otherwise a difference between methods might be nothing but simulation noise."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.4, buff=0.65, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def streams_(self):
        code = code_block([
            "from explainer.stats.kit.random import streams",
            "rngs = streams(seed=2019, k=3)       # one per scenario",
            "for rng, p in zip(rngs, scenarios):",
            "    data = [rng.binomial(30, p) for r in range(R)]",
            "    for method in (wald, wilson):    # same data for every method",
            "        results[p, method] = evaluate(method, data)",
        ], font_size=22).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"one seed, \ written down: \ anyone can rerun the study exactly", font_size=26),
            label(r"independent streams per scenario: \ changing one never changes another", font_size=26, color=GOOD),
            label(r"the same data sets for every method: \ comparisons are paired, \ and far less noisy", font_size=26,
                  color=GOOD),
            label(r"never reseed in a loop, \ never pick the seed that gives the nicest answer", font_size=26, color=BAD),
        ), 12.6, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "Randomness in a study must be controlled. <bookmark mark='a'/> Use one seed, and write it down: anyone "
            "can then rerun the study and get the same numbers. <bookmark mark='b'/> Give each scenario its own "
            "independent stream, spawned from that seed, so that adding or changing a scenario never changes the "
            "others. <bookmark mark='c'/> Apply every method to the same simulated data sets. The comparison is then "
            "paired, like a crossover trial, and the noise in the difference between methods is much smaller than "
            "the noise in each. <bookmark mark='d'/> And never pick the seed that gives the nicest answer: that's "
            "Lazzarini's needle again."
        ) as vo:
            self.play(FadeIn(code, shift=UP * 0.2))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def harness(self):
        from explainer.stats.kit.random import simulate

        def wald(x):
            n = len(x)
            ph = x.mean()
            se = np.sqrt(max(ph * (1 - ph), 1e-12) / n)
            return ph, ph - 1.96 * se, ph + 1.96 * se
        out = simulate(lambda rng: rng.binomial(1, 0.1, 30), wald, 0.1, 4000, seed=2019)
        rows = fit_rows(VGroup(
            MathTex(r"\texttt{simulate(dgp, method, truth, reps, seed)}", font_size=30, color=S.ACCENT),
            MathTex(rf"\text{{Wald}},\ p = 0.1,\ n = 30:\ \ \text{{coverage}} = {out['coverage']:.3f} \pm {out['coverage_mcse']:.3f}",
                    font_size=30, color=BAD),
            MathTex(rf"\text{{bias}} = {out['bias']:+.4f} \pm {out['bias_mcse']:.4f},\ \ \text{{SE}}_{{\text{{emp}}}} = {out['emp_se']:.4f}",
                    font_size=28),
            label(r"the Coverage Board: \ every interval in this series, \ run through this harness", font_size=24, color=GREY_A),
        ), 12.6, 0.4, [0, 0.4, 0])
        built = label(r"Built: \ \texttt{statkit.random.simulate}", font_size=24, color=S.ACCENT).to_corner(UR, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/> All of this is packed into one function in statkit: give it a data-generating "
            "mechanism, a method, the true value, the number of replicates and a seed. <bookmark mark='b'/> For the "
            "Wald interval at p equal to point one with thirty trials, its coverage is about eighty-one percent, "
            "plus or minus about point six. <bookmark mark='c'/> It reports bias and empirical standard error, each "
            "with its Monte Carlo error. <bookmark mark='d'/> The Coverage Board that appears throughout this series "
            "is this harness, run on every interval we build."
        ) as vo:
            self.play(FadeIn(built))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
