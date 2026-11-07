from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403


class Decided(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_check()
        self.verdicts()
        self.logistic()
        self.words()
        self.joint()
        self.robust()
        self.conclusion()

    def card(self):
        card = chapter_card(9, r"The \emph{Federalist} decided", r"Twelve papers, \ one author", lit=(1964,), part=PART)
        with self.voiceover("Chapter nine. The Federalist decided."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_check(self):
        d = load("nbvslr")
        rows = [
            cmath(r"\text{train}", r":", r"\text{51 Hamilton, \ 14 Madison papers; \ 91 words}", font_size=30),
            cmath(r"\text{check}", r":", rf"\text{{leave-one-out: }} {int(d['nb_err'] * d['m'])}\ \text{{errors in}}\ {d['m']}", font_size=30),
            cmath(r"\text{apply}", r":", r"\text{the 12 disputed papers, \ never used in training}", font_size=30),
            cmath(r"\text{report}", r":", r"\text{log odds, \ Madison vs Hamilton, \ base 10}", font_size=30),
        ]
        rows[2][2].set_color(DISP)
        whys = [why(r"chapter five's Poisson naive Bayes"), why(r"honest error on papers like these"),
                why(r"held out completely"), why(r"$+1$: \ 10 to 1 for Madison; \ $-1$: \ 10 to 1 for Hamilton")]
        intro = label('Apply the fitted models to the disputed papers', font_size=36)
        with self.voiceover(
            "<bookmark mark='a'/> Now the verdict. Train chapter five's Poisson naive Bayes on the sixty-five papers of known "
            "authorship, using ninety-one words. <bookmark mark='b'/> Its leave-one-out error on those papers is zero. "
            "<bookmark mark='c'/> Apply it to the twelve disputed papers, which played no part in training. "
            "<bookmark mark='d'/> We'll report the log odds in base ten: plus one means ten to one for Madison, minus one ten to "
            "one for Hamilton, with equal prior odds."
        ) as vo:
            intro.scale_to_fit_width(min(intro.width, 12.5))
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def verdicts(self):
        d = load("decided")
        no = d["papers"]
        lo = np.asarray(d["log10_odds"])
        A = axes([-0.6, 11.6], [-2, 21], x_length=10.0, y_length=4.2, xlabel=r"disputed paper", ylabel=r"$\log_{10}$ odds, \ Madison : Hamilton",
                 yticks=[0, 5, 10, 15, 20], center=[0, 0.5, 0])
        ax = A.ax
        A.xlabel.shift(DOWN * 0.3)
        bars = VGroup(*[Rectangle(width=ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0], height=max(0.02, ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]),
                                  stroke_width=0, fill_color=MAD, fill_opacity=0.9).move_to(ax.c2p(k, 0), aligned_edge=DOWN)
                        for k, v in enumerate(lo)])
        names = VGroup(*[MathTex(str(n), font_size=22, color=GREY_A).next_to(ax.c2p(k, -2), DOWN, buff=0.1) for k, n in enumerate(no)])
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(11.6, 0), color=GREY_C, stroke_width=1.5)
        k55 = no.index(55)
        rows = fit_rows(VGroup(
            label(r"all twelve favour Madison", font_size=24, color=MAD),
            MathTex(rf"\text{{No. 55: \ only}}\ {lo[k55]:.1f}", font_size=26, color=RES),
            label(r"chapter five's caveat: \ these odds are far too extreme", font_size=20, color=GREY_A),
        ), 12.4, 0.2, [0, -3.05, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here they are. Every one of the twelve disputed papers comes out for Madison, most "
            "by overwhelming margins. <bookmark mark='b'/> The exception is number fifty-five, where the evidence is "
            "weak: log odds of point six, about four to one. <bookmark mark='c'/> Remember chapter five's warning: "
            "naive Bayes counts correlated words as independent evidence, so these magnitudes are far too extreme. "
            "The broad direction is a useful model-dependent indication, and even the direction for fifty-five is "
            "uncertain."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(bars[k55], color=RES), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def logistic(self):
        d = load("decided")
        no = d["papers"]
        p = np.asarray(d["lr_prob"])
        A = axes([-0.6, 11.6], [0, 1], x_length=10.0, y_length=3.8, xlabel=r"disputed paper", ylabel=r"$P(\text{Madison})$, \ ridge logistic",
                 yticks=[0, 0.5, 1], center=[0, 0.6, 0])
        ax = A.ax
        A.xlabel.shift(DOWN * 0.3)
        half = DashedLine(ax.c2p(-0.6, 0.5), ax.c2p(11.6, 0.5), color=GREY_C, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.1, color=MAD if v > 0.5 else HAM) for k, v in enumerate(p)])
        names = VGroup(*[MathTex(str(n), font_size=22, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.12) for k, n in enumerate(no)])
        k55 = no.index(55)
        rows = fit_rows(VGroup(
            label(r"the discriminative model: \ 11 of 12 for Madison, \ with modest probabilities", font_size=22, color=MAD),
            MathTex(rf"\text{{No. 55}}: P(\text{{Madison}}) = {p[k55]:.2f}", font_size=26, color=HAM),
            label(r"two honest methods, \ one hard case", font_size=22, color=OBS),
        ), 12.4, 0.2, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A second opinion from the discriminative model: ridge logistic regression on the same word "
            "rates. Its probabilities are far more modest, between seventy-four and ninety-nine percent for Madison on eleven "
            "papers. <bookmark mark='b'/> On number fifty-five it leans the other way, thirty percent for Madison. "
            "<bookmark mark='c'/> Two reasonable methods agree on eleven papers and disagree on one. That's useful information: "
            "fifty-five is genuinely the hardest case, and any conclusion about it rests on the model."
        ) as vo:
            self.play(FadeIn(A), Create(half), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.08), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(dots[k55], color=HAM), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def words(self):
        d = load("decided")
        w = d["top_words"]
        c = np.asarray(d["top_contrib"]) / np.log(10)
        A = axes([-0.6, 7.6], [0, 2.6], x_length=9.0, y_length=3.8, xlabel=r"", ylabel=r"average contribution, \ $\log_{10}$ odds",
                 yticks=[0, 1, 2], center=[0, 0.6, 0])
        ax = A.ax
        bars = VGroup(*[Rectangle(width=ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0], height=max(0.02, ax.c2p(0, max(v, 0))[1] - ax.c2p(0, 0)[1]),
                                  stroke_width=0, fill_color=MAD, fill_opacity=0.9).move_to(ax.c2p(k, 0), aligned_edge=DOWN)
                        for k, v in enumerate(c)])
        names = VGroup(*[label(rf"\emph{{{x}}}", font_size=22, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k, x in enumerate(w)])
        rows = fit_rows(VGroup(
            label(r"the absence of \emph{upon} does the most work", font_size=24, color=MAD),
            label(r"then Madison's heavy use of \emph{on} and \emph{by}, \ and fewer \emph{to}s", font_size=22),
            label(r"no single word decides; \ dozens of small habits agree", font_size=22, color=OBS),
        ), 12.4, 0.25, [0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which words did the work? Averaged over the twelve papers, the biggest contribution comes from "
            "upon, or rather from its absence: Hamilton's papers would be expected to contain several, and these contain almost "
            "none. <bookmark mark='b'/> Next come Madison's heavy use of on and by, his fewer uses of to and would, and whilst. "
            "<bookmark mark='c'/> No single word decides it. Dozens of small, unconscious habits all point the same way, and that "
            "agreement is what makes the case."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def joint(self):
        d = load("decided")["joint"]
        rows = fit_rows(VGroup(
            label(r"the three joint papers, \ 18, \ 19 and 20", font_size=24),
            MathTex(r"\log_{10}\text{ odds}: " + ",\\ ".join(f"{v:.0f}" for v in d["log10"]), font_size=28, color=MAD),
            label(r"the words look like Madison's", font_size=22, color=MAD),
            label(r"historians: \ Madison drafted them from notes he and Hamilton shared", font_size=22, color=GREY_A),
            label(r"the classifier agrees with the record where the record exists", font_size=22, color=HIT),
        ), 12.4, 0.45, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A side check: the three joint papers, eighteen to twenty, which both men had a hand in. "
            "<bookmark mark='b'/> The classifier says Madison for all three. <bookmark mark='c'/> Their words look like his. "
            "<bookmark mark='d'/> That fits the historical account that Madison wrote them up from research notes the two "
            "shared. <bookmark mark='e'/> Where the record exists, the classifier agrees with it, which is some reassurance about "
            "where it doesn't."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def robust(self):
        d = load("robust")
        no = d["papers"]
        runs = list(d["runs"].items())
        cols = [MAD, TRAIN, OBS]
        A = axes([-0.6, 11.6], [-4, 21], x_length=10.0, y_length=4.0, xlabel=r"disputed paper",
                 ylabel=r"$\log_{10}$ odds, \ Madison : Hamilton", yticks=[0, 5, 10, 15, 20], center=[0, 0.7, 0])
        ax = A.ax
        A.xlabel.shift(DOWN * 0.3)
        w = ax.c2p(0.26, 0)[0] - ax.c2p(0, 0)[0]
        groups = VGroup()
        for j, (_, r) in enumerate(runs):
            g = VGroup()
            for k, v in enumerate(r["log10"]):
                h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
                rect = Rectangle(width=w, height=max(0.02, abs(h)), stroke_width=0, fill_color=cols[j], fill_opacity=0.9)
                rect.move_to(ax.c2p(k + (j - 1) * 0.28, 0), aligned_edge=DOWN if h >= 0 else UP)
                g.add(rect)
            groups.add(g)
        names = VGroup(*[MathTex(str(n), font_size=22, color=GREY_A).next_to(ax.c2p(k, -4), DOWN, buff=0.1) for k, n in enumerate(no)])
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(11.6, 0), color=GREY_C, stroke_width=1.5)
        k55 = no.index(55)
        keys = VGroup(*[label(rf"{name}: \ {r['n_madison']} of 12 Madison, \ {r['loo_errors']} LOO errors", font_size=20, color=c)
                        for (name, r), c in zip(runs, cols)]).arrange(RIGHT, buff=0.5)
        if keys.width > 13.0:
            keys.width = 13.0
        keys.to_edge(DOWN, buff=0.55)
        msg = label(rf"No. 55 flips without \emph{{upon}}: \ {runs[1][1]['log10'][k55]:.1f}", font_size=24, color=RES)
        msg.to_edge(UP, buff=0.35)
        with self.voiceover(
            "Mosteller and Wallace's most important check was of robustness: does the answer depend on a few words? "
            "<bookmark mark='a'/> In blue, our verdicts with all ninety-one words. <bookmark mark='b'/> Now drop "
            "upon, the single strongest word, in teal. Eleven papers still favour Madison, by a little less. "
            "<bookmark mark='c'/> But number fifty-five flips, to about a hundred and fifty to one for Hamilton, "
            "before chapter five's discount. <bookmark mark='d'/> Drop whilst and there as well, in gold, and the "
            "picture is the same: eleven for Madison, one fragile paper, and just one leave-one-out error in "
            "sixty-five on the known papers. <bookmark mark='e'/> The eleven are robust; number fifty-five rests on "
            "one fact: no upon at all in two thousand words, where Hamilton would average about seven. Their original"
            " analysis also identified fifty-five as its weakest case; sensitivity here is a reason to report the "
            "modelling dependence."
        ) as vo:
            self.play(FadeIn(A), Create(zero), FadeIn(names))
            for j, m_ in enumerate("abd"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] >= ax.c2p(0, 0)[1] else UP)
                                        for b_ in groups[j]], lag_ratio=0.06), FadeIn(keys[j]))
                if m_ == "b":
                    vo.wait_until("c")
                    self.play(Indicate(groups[1][k55], color=RES, scale_factor=1.6), FadeIn(msg))
            vo.wait_until("e")
            self.play(*[Indicate(g[k55], color=RES) for g in groups])
        self.wait(1.0)
        self.clear_scene()

    def conclusion(self):
        rows = fit_rows(VGroup(
            label(r"Mosteller \& Wallace (1964): \ Madison wrote all twelve", font_size=26, color=MAD),
            label(r"their weakest case: \ No. 55, \ still favouring Madison", font_size=22),
            label(r"negative binomial rates, \ priors from other writings, \ sensitivity checks", font_size=22, color=GREY_A),
            label(r"historians now generally agree", font_size=22, color=HIT),
            label(r"one of the first large Bayesian analyses, \ done by hand and early computer", font_size=22, color=OBS),
        ), 12.4, 0.48, [0, 0, 0])
        tag = historical_tag(r"Mosteller \& Wallace, \ \emph{Inference and Disputed Authorship} (1964)", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Mosteller and Wallace's conclusion, in 1964, was that Madison wrote all twelve. "
            "<bookmark mark='b'/> Their weakest case was number fifty-five, as ours is, and even there their odds favoured "
            "Madison. <bookmark mark='c'/> They got there with more realistic negative binomial rates, priors built from other "
            "writings, and extensive checks of how the answer depended on each assumption. <bookmark mark='d'/> Historians now "
            "generally accept the verdict. <bookmark mark='e'/> It was one of the first large Bayesian analyses ever carried "
            "out, and one of the first triumphs of what we'd now call machine learning."
        ) as vo:
            self.add(tag)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
