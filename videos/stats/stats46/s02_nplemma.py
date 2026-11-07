from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class NPLemma(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.proof()
        self.bars()
        self.power()
        self.general()
        self.randomization()

    def card(self):
        card = chapter_card(1, r"The Neyman--Pearson lemma in general", r"The most powerful test, \ and why it exists", lit=(1933,), part=PART)
        with self.voiceover("Chapter one. The Neyman–Pearson lemma in general: the most powerful test, and why it exists."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lemma(self):
        rows = [
            cmath(r"\text{a test}", r":", r"\phi(x) \in [0, 1], \ \text{the chance of rejecting at } x", font_size=32),
            cmath(r"\text{size}", r"=", r"E_0\phi, \ \ \text{power} = E_1 \phi", font_size=34),
            cmath(r"\phi^*(x)", r"=", r"\begin{cases} 1 & f_1(x) > k f_0(x) \\ \gamma & f_1(x) = k f_0(x) \\ 0 & f_1(x) < k f_0(x) \end{cases}", font_size=32),
            cmath(r"E_0\phi^* = \alpha", r"\Rightarrow", r"E_1 \phi^* \ge E_1 \phi \ \text{for every } \phi \text{ with } E_0\phi \le \alpha", font_size=30),
        ]
        rows[2][-1].set_color(UMPC)
        rows[3][-1].set_color(UMPC)
        whys = [why(r"randomized, \ in general"), why(r"two numbers"), why(r"reject where the likelihood ratio is large"), why(r"Neyman \& Pearson (1933)")]
        with self.voiceover(
            "<bookmark mark='a'/> A test, in general, is a function phi giving the probability of rejecting at each data "
            "point: one for reject, zero for accept, and possibly something in between. <bookmark mark='b'/> Its size is "
            "its mean under the null, its power its mean under the alternative. <bookmark mark='c'/> For a simple null "
            "against a simple alternative, Neyman and Pearson's test rejects where the likelihood ratio f one over f nought "
            "exceeds a constant k, accepts where it falls below, and randomizes on the boundary. <bookmark mark='d'/> If its "
            "size is alpha, its power is at least that of any other test of size at most alpha. And for every alpha, k and "
            "gamma can be chosen to make the size exactly alpha."
        ) as vo:
            heading=label('A likelihood-ratio threshold is most powerful for simple hypotheses',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"(\phi^* - \phi)(f_1 - k f_0)", r"\ge", r"0 \ \text{everywhere}", font_size=34),
            cmath(r"\textstyle\int (\phi^* - \phi)(f_1 - k f_0)", r"\ge", r"0", font_size=34),
            cmath(r"E_1\phi^* - E_1\phi", r"\ge", r"k\,(E_0\phi^* - E_0\phi) \ge 0", font_size=34),
            cmath(r"\text{necessity}", r":", r"\text{any most powerful test equals a.e. } \phi^* \text{ where } f_1 \ne k f_0", font_size=30),
        ]
        rows[2][-1].set_color(UMPC)
        whys = [why(r"check the three cases"), why(r"integrate"), why(r"rearrange; \ sizes $\alpha$ vs $\le \alpha$"), why(r"strict unless equal")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof is one line. Where f one exceeds k f nought, phi star is one, so phi star"
            " minus phi is at least zero; where it falls short, phi star is zero and the difference is at most zero. "
            "Either way the product is non-negative. <bookmark mark='b'/> Integrate. <bookmark mark='c'/> The power "
            "of phi star minus that of phi is at least k times the difference in sizes, which is non-negative. "
            "<bookmark mark='d'/> If phi is also most powerful, the integral must be zero, so phi agrees with phi "
            "star almost everywhere, with respect to the dominating measure, where f one differs from k times f "
            "nought: the lemma's form is necessary as well as sufficient."
        ) as vo:
            heading=label('The sign of the likelihood gap proves optimality',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bars(self):
        d = load("np")
        n = d["n"]
        x = np.arange(n + 1)
        A = axes([-0.6, 20.6], [0, 0.23], x_length=7.4, y_length=4.4, xlabel=r"successes $x$ in 20 trials", ylabel=r"probability",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 0.1, 0.2], center=[-2.5, 0.2, 0])
        ax = A.ax
        b0 = bars_at(ax, x - 0.2, d["pmf0"], 0.38, H0C, opacity=0.8)
        b1 = bars_at(ax, x + 0.2, d["pmf1"], 0.38, H1C, opacity=0.8)
        phi = np.asarray(d["phi"])
        rej = VGroup(*[b0[i].copy().set_fill(REJC, opacity=0.95) for i in range(n + 1) if phi[i] == 1])
        part = b0[d["c"]].copy().set_fill(REJC, opacity=0.95)
        part.stretch(d["gamma"], 1, about_edge=DOWN)
        side = fit_rows(VGroup(
            label(r"$H_0$: \ $p = 0.3$ \ (blue); \ \ $H_1$: \ $p = 0.5$ \ (teal)", font_size=22),
            label(r"the ratio $f_1/f_0$ increases in $x$: \ reject large $x$", font_size=22, color=GREY_A),
            label(rf"red: \ $x \ge {d['c'] + 1}$, \ and at $x = {d['c']}$ \ with chance {d['gamma']:.3f}", font_size=22, color=REJC),
            label(rf"without randomizing: \ size {100 * d['size_nr']:.1f}\% \ or {100 * d['size_nr2']:.1f}\%", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A discrete example. Twenty trials; the null says the success probability is point three, "
            f"the alternative point five. <bookmark mark='b'/> The likelihood ratio increases with the number of successes, "
            f"so the most powerful test rejects for large counts. <bookmark mark='c'/> To have size exactly five percent it "
            f"rejects at {d['c'] + 1} or more, and at exactly {d['c']} it rejects with probability {say(d['gamma'], 3)}, a "
            f"coin flip of its own. <bookmark mark='d'/> Without the randomization, the available sizes jump from "
            f"{100 * d['size_nr']:.1f} percent to {100 * d['size_nr2']:.1f} percent; five percent lies between them."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ binomial probabilities")))
            vo.wait_until("a")
            self.play(FadeIn(b0), FadeIn(b1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(rej), FadeIn(part), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def power(self):
        d = load("np")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"$P_p(\text{reject})$",
                 xticks=[0, 0.3, 0.5, 0.75, 1], yticks=[0, 0.05, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cu = polyline(ax, ps, d["power"], UMPC, 4)
        cn = polyline(ax, ps, d["power_nr"], H0C, 3)
        a = DashedLine(ax.c2p(0, 0.05), ax.c2p(1, 0.05), color=GREY_B, stroke_width=2)
        v = DashedLine(ax.c2p(0.3, 0), ax.c2p(0.3, 1), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"green: \ the randomized test, \ size exactly 5\%", font_size=22, color=UMPC),
            label(r"blue: \ reject only at $x \ge 10$, \ size 4.8\%", font_size=22, color=H0C),
            label(r"the same test is most powerful \ for every $p_1 > 0.3$", font_size=22, color=S.ACCENT),
            label(r"so it is UMP for $p \le 0.3$ \ vs \ $p > 0.3$: \ chapter 2", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The power functions. In green, the randomized test: exactly five percent at point three, "
            "rising toward one. <bookmark mark='b'/> In blue, the slightly smaller non-randomized test, just below it "
            "everywhere. <bookmark mark='c'/> Notice that the test did not depend on the alternative's value, point five, "
            "only on its side: the same test is most powerful against every p above point three. <bookmark mark='d'/> So it "
            "is uniformly most powerful for the one-sided problem. When that happens, and why, is chapter two."
        ) as vo:
            self.play(FadeIn(A), Create(a), Create(v))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cn), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def general(self):
        rows = [
            cmath(r"\max_\phi \textstyle\int \phi f_1", r"\ \text{s.t.}\ ", r"\textstyle\int \phi\, g_i = c_i, \ i = 1, \ldots, m", font_size=32),
            cmath(r"\phi^*", r"=", r"\mathbf 1\{f_1 > \textstyle\sum_i k_i g_i\} \ (+\ \gamma \text{ on equality})", font_size=32),
            cmath(r"\text{existence}", r":", r"\{0 \le \phi \le 1\} \text{ is weak-* compact in } L^\infty", font_size=32),
            cmath(r"\text{a linear programme}", r":", r"\text{feasible integrable constraints; \ suitable dual multipliers (Part 21)}", font_size=32),
        ]
        rows[1][-1].set_color(UMPC)
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"several side conditions"), why(r"Dantzig \& Wald (1951)"), why(r"Banach--Alaoglu"), why(r"the simplex, \ again")]
        with self.voiceover(
            "<bookmark mark='a'/> The general version allows several side conditions: maximize the power subject to m"
            " linear constraints on phi, not just the size. <bookmark mark='b'/> George Dantzig and Wald showed in "
            "1951 that whenever suitable multipliers exist, a rule rejecting where f one exceeds a combination of the"
            " constraint functions is optimal if it satisfies the side conditions. <bookmark mark='c'/> With "
            "integrable objective and constraint functions and nonempty feasible constraints, the feasible set is "
            "weak-star closed inside the compact set of tests between zero and one. The continuous objective "
            "therefore attains its maximum. Multiplier representations require a further supporting-hyperplane "
            "condition. <bookmark mark='d'/> For discrete data it is literally a linear programme, the one Dantzig's "
            "simplex method solves, and the multipliers are its dual variables: Part twenty-one's dual, at work in "
            "testing. Chapter three uses it with two constraints."
        ) as vo:
            heading=label('Linear side conditions define a compact feasible testing problem',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def randomization(self):
        rows = fit_rows(VGroup(
            label(r"randomized tests: \ a theoretical device, \ rarely a practical one", font_size=26),
            label(r"they fill discrete gaps in attainable size; \ nonrandomized binomial power is also smooth", font_size=26, color=UMPC),
            label(r"exact tail p-value: \ super-uniform; \ mid-p $P(X>x)+\tfrac12P(X=x)$: \ may exceed level", font_size=26, color=S.ACCENT),
            label(r"or condition, \ or accept a conservative size: \ chapter 3's Fisher exact test", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Few statisticians would actually flip a coin to decide a test. Randomized tests are"
            " a device of the theory. <bookmark mark='b'/> They fill gaps in attainable size and allow exact level "
            "alpha at discrete boundaries. Nonrandomized binomial tests also have smooth power functions. <bookmark "
            "mark='c'/> In practice one reports a p-value, or Lancaster's mid-p value, which counts half the "
            "probability of the observed point but need not be super-uniform and can exceed nominal type-one error, "
            "<bookmark mark='d'/> or accepts a conservative size, as Fisher's exact test of chapter three does."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
