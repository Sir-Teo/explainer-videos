from __future__ import annotations

from videos.stats.stats50.common import *  # noqa: F403

PROBLEMS = [
    r"For $y_k = \theta_k + \varepsilon z_k$ and $\hat\theta_k = c_k y_k$, \ find the worst $\theta$ on $\sum a_k^2\theta_k^2 \le C^2$ for given $c$.",
    r"Show that the Bayes rule for $\theta_k \sim N(0, \tau_k^2)$ is $\tau_k^2 y_k/(\tau_k^2 + \varepsilon^2)$, \ and find its Bayes risk.",
    r"Prove Le Cam's bound: \ $\max_j E_j(\hat\theta - \theta_j)^2 \ge \tfrac{\delta^2}{2}(1 - \mathrm{TV}(P_0, P_1))$.",
    r"Show $\mathrm{TV}(N(0,1), N(d,1)) = 2\Phi(|d|/2) - 1$, \ and check Pinsker's inequality for it.",
    r"With $f_1 = f_0 + h\,b((x - x_0)/w)$, \ $h = Lw^s$, \ choose $w$ to get the rate $n^{-2s/(2s+1)}$ at $x_0$.",
    r"For the sparse mixture, \ show that the maximum statistic detects iff $r > (1 - \sqrt{1 - \beta})^2$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Farrell and Stone: \ a speed limit", LOWC), (r"the Gaussian sequence model", HYPC),
            (r"Pinsker: \ an exact constant", LINC), (r"Le Cam: \ two points", LOWC), (r"Fano: \ packings, \ $s\log(p/s)$", LOWC),
            (r"Assouad: \ hypercubes of bumps", LOWC),
            (r"block James--Stein, \ thresholding", UPC), (r"Lepski: \ adaptation, \ and its price", ADAPTC),
            (r"minimax testing; \ higher criticism", HYPC), (r"statistical--computational gaps", LOWC),
            (r"honest intervals, \ on the Board", ADAPTC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 50, \ in eleven lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty in eleven lines. Farrell's and Stone's speed limits. The Gaussian sequence "
            "model, which stands for regression and densities. Pinsker's exact minimax constant. Lower bounds by Le Cam's "
            "two points, Fano's packings and Assouad's hypercubes. <bookmark mark='b'/> Upper bounds that match, by blockwise "
            "James–Stein and thresholding. Lepski's adaptation and its price. Minimax testing and higher criticism. The gaps "
            "between what is possible and what is efficiently computable. And honest intervals on the Board."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.3), run_time=5.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(50, r"the limits of estimation, \ with the dimension fixed",
                            r"that the number of parameters stays put as $n$ grows",
                            r"Parts 51--52: \ high-dimensional probability and statistics, \ where $p$ grows with $n$")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next parts. This one found the limits of estimation. <bookmark "
            "mark='b'/> Except for the sparse means, the dimension stayed fixed while n grew. <bookmark mark='c'/> Parts "
            "fifty-one and fifty-two let the dimension grow with the sample: the probability of high dimensions, with "
            "concentration of measure and random matrices, and then high-dimensional statistics, where Fano's s log p over s "
            "becomes the central rate."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"concentration and chaining in high dimensions", [51]), (r"$s \log(p/s)$ for the lasso, \ restricted eigenvalues", [52]),
            (r"posterior contraction rates match minimax", [53]), (r"learning-theory lower bounds; \ VC and Fano", [54]),
            (r"private estimation's minimax rates", [63]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-one develops concentration and chaining in high dimensions. "
            "Part fifty-two proves that the lasso attains Fano's s log p over s. Part fifty-three asks when Bayesian posteriors "
            "contract at the minimax rate. Part fifty-four gives the lower bounds of learning theory. And Part sixty-three "
            "finds the minimax price of privacy."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The worst parameter for a linear rule; the "
            "Gaussian prior's Bayes rule; Le Cam's two-point bound; the total variation between normals; Farrell's "
            "construction; and the maximum statistic's detection boundary. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"A. Tsybakov, \emph{Introduction to Nonparametric Estimation} (2009); \ I. Johnstone, \emph{Gaussian Estimation: Sequence and Wavelet Models} (2019)",
             r"E. Giné \& R. Nickl, \emph{Mathematical Foundations of Infinite-Dimensional Statistical Models} (2016)",
             r"Y. Polyanskiy \& Y. Wu, \emph{Information Theory: From Coding to Learning} (2024); \ B. Yu, \emph{Assouad, Fano, and Le Cam} (1997)"],
            [r"R. Farrell (1972); \ C. Stone (1980, 1982); \ M. Pinsker (1980); \ P. Assouad (1983); \ O. Lepski (1990)",
             r"D. Donoho \& I. Johnstone (1994, 1998); \ L. Brown \& M. Low (1996); \ M. Nussbaum (1996); \ M. Low (1997)",
             r"Yu. Ingster (1982, 1997); \ D. Donoho \& J. Jin (2004); \ T. Cai (1999); \ L. Cavalier \& A. Tsybakov (2002)",
             r"Q. Berthet \& P. Rigollet (2013); \ S. Hopkins (2018); \ M. Brennan \& G. Bresler (2020)"])
        with self.voiceover(
            "The books this part follows: Tsybakov's Introduction to Nonparametric Estimation, Johnstone's Gaussian "
            "Estimation, Giné and Nickl, and Polyanskiy and Wu on information theory; with Bin Yu's essay, and the papers "
            "from Farrell to Brennan and Bresler."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=50, current=None)
        nxt = VGroup(label(r"Part 51", font_size=30, color=GREY_B), label(r"High-Dimensional Probability", font_size=48),
                     label(r"what happens to randomness when the dimension is large?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty parts of sixty-five. <bookmark mark='a'/> Every rate has two halves: a method that achieves it, and an "
            "argument that nothing can do better, built by finding hypotheses the data cannot tell apart. When the two "
            "meet, the question is closed; when they do not, there is research to do, and the gap between them is often "
            "where the most interesting statistics lives. <bookmark mark='b'/> "
            "Next, Part fifty-one: high-dimensional probability."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(50)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
