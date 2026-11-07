from __future__ import annotations

from videos.stats.stats56.common import *  # noqa: F403

PROBLEMS = [
    r"Show that $Z = Y - c\,\eta'Y$ with $c = \Sigma\eta/(\eta'\Sigma\eta)$ is independent of $\eta'Y$ when $Y \sim N(\mu, \Sigma)$.",
    r"For marginal screening $\{|Y_j| > t\}$, \ write the selection event as a union of polyhedra, \ and find $[\mathcal V^-, \mathcal V^+]$.",
    r"Show that the truncated-normal survival function $P_\mu(Y > y \mid Y \in [a, b])$ is increasing in $\mu$.",
    r"For $K$ i.i.d.\ $N(0, 1)$, \ show $E\max_k Y_k \le \sqrt{2\log K}$, \ an upper growth bound for the winner's curse.",
    r"Prove that fission's $f = X + \tau Z$ and $g = X - Z/\tau$ are independent, \ and find the $\tau$ minimizing $\mathrm{Var}\,g$ given $\mathrm{Var}\,f \le v$.",
    r"For IID calibration and test pairs, \ prove $P(p_j\le t, Y_j\le c)\le t$; \ explain why this is not conditional null validity.",
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
            (r"the winner's curse: \ selection inflates", SELC), (r"PoSI: \ cover every model, \ up to $\sqrt p$", SIMC),
            (r"the polyhedral lemma: \ truncated normals", CONDC), (r"the lasso's selective intervals", CONDC),
            (r"randomization and carving", SPLITC), (r"splitting, \ fission, \ thinning", SPLITC),
            (r"knockoffs: \ a supermartingale proof", HYBC), (r"conformal selection: \ BH on conformal $p$-values", HYBC),
            (r"winners: \ conditional and hybrid", HYBC), (r"after clustering: \ condition on the clusters", CONDC),
            (r"six open problems", S.ACCENT),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 56, \ in eleven lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-six in eleven lines. Selection inflates what it selects. PoSI covers every "
            "model you might have chosen, at a price of up to root p. The polyhedral lemma turns selection into a "
            "truncated normal, and gives the lasso's selective intervals. Randomization and carving soften the truncation. "
            "Splitting, fission and thinning separate selection from inference. <bookmark mark='b'/> Knockoffs control the "
            "false discovery rate through a supermartingale. Conformal selection does it for units. The hybrid interval "
            "makes inference on winners both valid and short. Conditioning on the clusters makes post-clustering tests "
            "honest. And six problems remain open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[:6]], lag_ratio=0.5), run_time=12.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[6:]], lag_ratio=0.5), run_time=10.0)
        self.wait(1.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(56, r"selective inference, \ exact under a model", r"a Gaussian model, \ or a known law of $X$",
                            r"Part 57: \ what can be guaranteed without a parametric model, \ and what cannot")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for the next part. Most of this part's exact results needed a model: Gaussian noise for the polyhedral lemma, a known covariate law for knockoffs. <bookmark mark='b'/> Only conformal selection asked for the stated independent or conditional exchangeability assumptions and separate predictor training. <bookmark mark='c'/> Part fifty-seven asks what can be guaranteed without a parametric model, and proves what cannot."
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
            (r"conformal inference, \ its limits", [57]), (r"e-values and derandomized knockoffs", [58]),
            (r"the lasso when $p/n$ is fixed", [59]), (r"selected subgroups in causal inference", [62]),
            (r"the dissertation's analysis plan", [65]),
        ], font_size=22)
        self.play(FadeIn(card.head))
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part fifty-seven takes conformal inference to its limits. Part "
            "fifty-eight builds e-values, which derandomize knockoffs. Part fifty-nine studies the lasso when p and n grow "
            "together. Part sixty-two returns to subgroups selected in causal analyses. And the dissertation, in Part "
            "sixty-five, writes its analysis plan with this part's lessons in mind."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The independence in the polyhedral lemma; "
            "the selection event of marginal screening; the monotonicity of the truncated pivot; the winner's curse rate; "
            "fission's independence and its best tau; and the validity of conformal p-values. Pause here if you want to try "
            "them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. Berk, \ L. Brown, \ A. Buja, \ K. Zhang \& L. Zhao, \ \emph{Ann. Stat.} (2013); \ W. Fithian, \ D. Sun \& J. Taylor (2014)",
             r"J. Lee, \ D. Sun, \ Y. Sun \& J. Taylor, \ \emph{Ann. Stat.} (2016); \ X. Tian \& J. Taylor, \ \emph{Ann. Stat.} (2018)",
             r"R. Foygel Barber \& E. Cand\`es, \ \emph{Ann. Stat.} (2015); \ E. Cand\`es, \ Y. Fan, \ L. Janson \& J. Lv, \ \emph{JRSS B} (2018)",
             r"I. Andrews, \ T. Kitagawa \& A. McCloskey, \ \emph{QJE} (2024); \ L. Gao, \ J. Bien \& D. Witten, \ \emph{JASA} (2024)"],
            [r"J. Ioannidis, \ \emph{Epidemiology} (2008); \ Y. Benjamini \& D. Yekutieli (2001, 2005); \ D. Cox (1975)",
             r"J. Leiner, \ B. Duan, \ L. Wasserman \& A. Ramdas, \ \emph{JASA} (2025); \ A. Neufeld et al., \ \emph{JMLR} (2024)",
             r"Y. Jin \& E. Cand\`es, \ \emph{JMLR} (2023); \ S. Bates et al. (2023); \ R. Barber, \ E. Cand\`es \& R. Samworth (2020)",
             r"D. Kivaranovic \& H. Leeb (2021); \ Y. Chen \& D. Witten (2023); \ Z. Ren \& R. Barber (2024); \ T. Stamey et al. (1989)"])
        with self.voiceover(
            "The papers behind this part: Berk and colleagues on PoSI; Fithian, Sun and Taylor, and Lee, Sun, Sun and Taylor, "
            "on conditional inference; Tian and Taylor on randomization; Barber and Candès, and Candès, Fan, Janson and Lv, "
            "on knockoffs; Andrews, Kitagawa and McCloskey on winners; Gao, Bien and Witten on clustering; Leiner and "
            "colleagues, and Neufeld and colleagues, on fission and thinning; and Jin and Candès on conformal selection."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=56, current=None)
        nxt = VGroup(label(r"Part 57", font_size=30, color=GREY_B), label(r"Distribution-Free Inference", font_size=48),
                     label(r"what can be guaranteed under exchangeability, \ and what is impossible?", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Fifty-six parts of sixty-five. <bookmark mark='a'/> The first research part is done. <bookmark mark='b'/> In 1956 Raghu Raj Bahadur and Leonard Savage proved that no informative finite-width uniformly honest confidence interval for a mean exists over the unrestricted class of finite-mean distributions. The whole real line is a valid but uninformative interval. Next, Part fifty-seven: distribution-free inference, what can be guaranteed under distribution-free sampling assumptions, and what cannot."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(56)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
