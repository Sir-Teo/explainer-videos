from __future__ import annotations

from videos.stats.stats48.common import *  # noqa: F403


class BootstrapProcess(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.multiplier()
        self.table()
        self.faithful()
        self.board()

    def card(self):
        card = chapter_card(11, r"The bootstrap empirical process", r"Resampling a whole random function", lit=(1990,), part=PART)
        with self.voiceover("Chapter eleven. The bootstrap empirical process: resampling a whole random function."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\hat{\mathbb G}_n", r"=", r"\sqrt n\,(P^*_n - P_n): \ \text{resample, \ recentre at the data}", font_size=34),
            cmath(r"\mathcal F \text{ Donsker}", r"\Leftrightarrow", r"\hat{\mathbb G}_n \Rightarrow \mathbb G \ \text{conditionally, \ in outer probability}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\sqrt n(\phi(P^*_n) - \phi(P_n)) \ \text{mimics} \ \sqrt n(\phi(P_n) - \phi(P)) \ \ (\phi \text{ Hadamard})", font_size=30),
            cmath(r"\text{fails}", r":", r"\phi \text{ not Hadamard differentiable: \ the max, \ Grenander, \ boundaries}", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"the bootstrap world"), why(r"Giné \& Zinn (1990)"), why(r"the delta method, \ for the bootstrap"), why(r"Part 47's chapter 13; \ chapter 9")]
        with self.voiceover(
            "<bookmark mark='a'/> Resample the data, and form the empirical process of the resample around the original "
            "empirical distribution. <bookmark mark='b'/> Evarist Giné and Joel Zinn proved in 1990 a theorem of rare "
            "elegance: the bootstrap empirical process converges, conditionally on the data, to the same Gaussian limit "
            "exactly when the class is Donsker. The bootstrap works precisely where the central limit theorem does. "
            "<bookmark mark='c'/> Combined with the functional delta method, the bootstrap distribution of any Hadamard "
            "differentiable functional mimics its sampling distribution. <bookmark mark='d'/> And it fails for "
            "functionals that are not, like Part forty-seven's sample maximum and this part's Grenander estimator."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def multiplier(self):
        rows = [
            cmath(r"\xi_1, \dots, \xi_n \ \text{i.i.d.}, \ E\xi = 0, \ \mathrm{Var}\,\xi = 1", r":", r"\tfrac{1}{\sqrt n}\textstyle\sum_i \xi_i (\delta_{X_i} - P_n)", font_size=30),
            cmath(r"\text{multinomial weights}", r":", r"\text{the ordinary bootstrap; \ Gaussian: \ the multiplier}", font_size=32),
            cmath(r"\text{multiplier CLT}", r":", r"\text{the same limit } \mathbb G, \ \text{for any Donsker class}", font_size=32),
            cmath(r"\text{why use it}", r":", r"\text{no resampling of the data: \ only of weights; \ high dimensions}", font_size=30),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"random weights"), why(r"two choices of $\xi$"), why(r"van der Vaart \& Wellner, \ 2.9"), why(r"Chernozhukov et al.\ (2013)")]
        with self.voiceover(
            "<bookmark mark='a'/> A cousin is the multiplier bootstrap. Instead of resampling, give each observation an "
            "independent random weight with mean zero and variance one, and form the weighted empirical process. <bookmark "
            "mark='b'/> Multinomial counts, recentred, give the ordinary bootstrap; Gaussian weights give the multiplier "
            "bootstrap. <bookmark mark='c'/> The multiplier central limit theorem says that for any Donsker class it has "
            "the same limit. <bookmark mark='d'/> It never touches the data, only the weights, and Victor Chernozhukov, "
            "Denis Chetverikov and Kengo Kato showed in 2013 that it works for maxima over thousands of statistics at once, "
            "the basis of modern simultaneous inference in high dimensions."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("bands")
        names = [("kolmogorov", r"Kolmogorov's limit"), ("exact", r"exact finite-$n$"), ("dkw", r"DKW, \ Massart"),
                 ("bootstrap", r"bootstrap"), ("multiplier", r"multiplier")]
        rows = [[r"95\% KS band", r"$n = 20$", r"$n = 100$"]]
        for k, nm in names:
            rows.append([nm, f"{100 * d['20'][k]:.1f}\\%", f"{100 * d['100'][k]:.1f}\\%"])
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.34, colors=[GREY_B, None, None, None, BADC, BADC])
        tab.move_to([0, 0.8, 0])
        foot = label(rf"coverage of $F$, \ $N(0,1)$ data; \ {d['reps']['20']:,} and {d['reps']['100']:,} samples; \ 499 resamples each", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"the bootstraps are first-order right: \ at $n = 20$ they undercover, \ because $F_n$ is a step function", font_size=24, color=BADC).move_to([0, -2.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> How do bands built five ways cover the true distribution function? Normal data, twenty "
            f"and a hundred observations. Kolmogorov's limit, the exact finite-sample quantile, and the DKW bound all cover "
            f"at least ninety-five percent. The bootstrap and multiplier bands cover {100 * d['20']['bootstrap']:.0f} and "
            f"{100 * d['20']['multiplier']:.0f} percent at twenty, and {100 * d['100']['bootstrap']:.0f} percent at a hundred. "
            f"<bookmark mark='b'/> They are right to first order and slow to converge. Resampling from a step function "
            f"produces ties, and the bootstrap maximum is systematically a little too small. For the plain KS band, with its "
            f"distribution-free exact law, there is no reason to bootstrap at all. The bootstrap earns its place where no "
            f"exact law exists."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def faithful(self):
        d = load("bands")["faithful"]
        rows = [[r"Old Faithful, \ 272 waits", r"half-width of the 95\% band"],
                [r"Kolmogorov's limit", f"{d['kolm']:.4f}"], [r"exact finite-$n$", f"{d['exact']:.4f}"], [r"DKW", f"{d['dkw']:.4f}"],
                [r"bootstrap \ (1,999)", f"{d['boot']:.4f}"], [r"multiplier \ (1,999)", f"{d['mult']:.4f}"]]
        tab = table_rows(rows, font_size=30, col_buff=0.9, row_buff=0.34, colors=[GREY_B, None, None, None, CLASSC, CLASSC])
        tab.move_to([0, 0.6, 0])
        foot = label(r"at $n = 272$ all five agree to within 0.002: \ the asymptotics have arrived", font_size=24, color=GOODC).move_to([0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> On the Old Faithful waits, two hundred and seventy-two of them, the five half-widths are "
            f"{say(d['kolm'], 3)} from the limit, {say(d['exact'], 3)} exact, {say(d['dkw'], 3)} from DKW, and "
            f"{say(d['boot'], 3)} and {say(d['mult'], 3)} from the two bootstraps. <bookmark mark='b'/> All within two "
            f"thousandths of each other: at this sample size, the asymptotics have arrived."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(museum_tag(r"Old Faithful (Azzalini \& Bowman 1990)")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def board(self):
        rows = board_rows("KS band", "DKW band")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board, at twenty normal observations: the bands from Kolmogorov's limit, "
                   "the exact quantile and the DKW inequality keep their promise of ninety-five percent. <bookmark mark='b'/> The "
                   "ordinary and multiplier bootstrap bands break it at this sample size, undercovering by several points. They "
                   "are asymptotically valid, but asymptotics is a statement about the limit.",
                   [("a", [0, 1, 2]), ("b", [3, 4])])
