from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.ioannidis()
        self.genes()
        self.question()
        self.history()
        self.window()
        self.upgrade()
        self.objectives()

    def ioannidis(self):
        tl = timeline(lit=(2008,)).to_edge(UP, buff=0.35)
        hc = history_card(2008, r"John Ioannidis, \ \emph{Why most discovered true associations are inflated}",
                          r"in \emph{Epidemiology}: \ the effect a study reports for the association it found is, \ on "
                          r"average, \ larger than the truth, \ because it was found by being large",
                          color=SELC, width=11.4, font_size=23).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"a field tests many associations; \ the ones that cross a threshold are reported", font_size=26, color=GREY_A),
            label(r"crossing the threshold selects the lucky draws, \ the ones with noise pushing up", font_size=26, color=NAIVEC),
            label(r"so replications come in smaller: \ the winner's curse", font_size=28, color=SELC),
        ), 12.4, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "This is the first part of the research stage. Each part from here centres on a few recent papers, proves their "
            "main results, reproduces their central experiment, and ends with open problems. <bookmark mark='a'/> In 2008 "
            "John Ioannidis published a paper with a blunt title: why most discovered true associations are inflated. "
            "<bookmark mark='b'/> A field tests many associations, and reports the ones whose estimates cross a threshold. "
            "<bookmark mark='c'/> But crossing the threshold selects the lucky draws, the ones whose noise happened to push "
            "them up. <bookmark mark='d'/> So when the findings are replicated, the effects come in smaller. Auction "
            "theorists call it the winner's curse: the winning bid is the one that overestimated the most."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def genes(self):
        d = load("hook")
        k = len(d["est"])
        xs = np.arange(k)
        A = axes([-0.8, k - 0.2], [0, 2.4], x_length=8.0, y_length=4.2, xlabel=r"the 20 genes with the largest $|t|$, \ ranked",
                 ylabel=r"effect, \ SD units", xticks=[0, 4, 9, 14, 19], xfmt=lambda v: f"{int(v) + 1}", yticks=[0, 1, 2], center=[-2.3, 0.0, 0])
        ax = A.ax
        est = VGroup(*[Dot(ax.c2p(x, v), radius=0.09, color=NAIVEC) for x, v in zip(xs, d["est"])])
        tru = VGroup(*[Dot(ax.c2p(x, v), radius=0.09, color=TRUEC6) for x, v in zip(xs, d["true"])])
        rep = VGroup(*[Dot(ax.c2p(x, min(max(v, 0), 2.35)), radius=0.08, color=SPLITC) for x, v in zip(xs, d["rep"])])
        links = VGroup(*[Line(ax.c2p(x, a), ax.c2p(x, b), color=GREY_D, stroke_width=1.5) for x, a, b in zip(xs, d["est"], d["true"])])
        side = fit_rows(VGroup(
            label(rf"the World's gene study: \ {d['m']:,} genes, \ 25 + 25 people", font_size=22),
            label(rf"red: \ the discovery estimates, \ mean {d['mean_est']:.2f}", font_size=22, color=NAIVEC),
            label(rf"white: \ the true effects, \ mean {d['mean_true']:.2f}", font_size=22, color=TRUEC6),
            label(rf"teal: \ a replication study, \ mean {d['mean_rep']:.2f}", font_size=22, color=SPLITC),
            label(rf"inflated by {100 * (d['mean_est'] / d['mean_true'] - 1):.0f}\%, \ though every one of the 20 is real", font_size=22, color=SELC),
        ), 4.2, 0.4, [4.6, 0.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The World can show it, because in the World we know the truth. Its gene study measures five "
            f"thousand genes on twenty-five patients and twenty-five controls. Take the twenty genes with the largest test "
            f"statistics. <bookmark mark='b'/> Their estimated effects, in red, average {say(d['mean_est'], 2)} standard "
            f"deviations. <bookmark mark='c'/> Their true effects, in white, average {say(d['mean_true'], 2)}. <bookmark "
            f"mark='d'/> And a replication study, a fresh twenty-five and twenty-five, finds {say(d['mean_rep'], 2)}: the "
            f"truth, not the discovery. <bookmark mark='e'/> The discoveries were inflated by about "
            f"{100 * (d['mean_est'] / d['mean_true'] - 1):.0f} percent, even though every one of these twenty genes is "
            f"genuinely involved. Selection, not error, did it."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"the World; \ truth known")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in est], lag_ratio=0.05), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(links), LaggedStart(*[FadeIn(p) for p in tru], lag_ratio=0.05), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in rep], lag_ratio=0.05), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"this part's question:", font_size=28, color=GREY_A),
            label(r"how do you give honest uncertainty about a question chosen by looking at the data?", font_size=28, color=SELC),
            label(r"five answers, \ at five prices:", font_size=26, color=GREY_A),
            label(r"cover every question you might have asked \ (PoSI)", font_size=24, color=SIMC),
            label(r"condition on having asked this one \ (selective inference)", font_size=24, color=CONDC),
            label(r"pay a little noise or data for freedom \ (randomization, \ splitting, \ fission)", font_size=24, color=SPLITC),
            label(r"control an error rate over the selected set \ (knockoffs, \ conformal selection)", font_size=24, color=HYBC),
        ), 12.4, 0.36, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This part's question: <bookmark mark='b'/> how do you give honest uncertainty about a "
            "question that was chosen by looking at the data? <bookmark mark='c'/> There are five kinds of answer, each with "
            "its own price. <bookmark mark='d'/> You can cover every question you might have asked, which is the idea of "
            "post-selection inference, PoSI. <bookmark mark='e'/> You can condition on having asked this particular "
            "question, which is selective inference. <bookmark mark='f'/> You can pay a little noise, or a little data, "
            "for the freedom to select as you like: randomization, splitting and fission. <bookmark mark='g'/> Or you can "
            "control an error rate over the whole selected set, as knockoffs and conformal selection do."
        ) as vo:
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def history(self):
        rows = [
            cmath(r"\text{Cox (1975)}", r":", r"\text{split the sample: \ select on one half, \ test on the other}", font_size=34),
            cmath(r"\text{Leeb \& P\"otscher (2006)}", r":", r"\text{no uniform fix for naive intervals}", font_size=32),
            cmath(r"\text{Berk et al. (2013)}", r":", r"\text{cover every model: \ PoSI}", font_size=34),
            cmath(r"\text{Lee et al. (2016)}", r":", r"\text{condition on selection, \ exactly}", font_size=34),
        ]
        rows[1][-1].set_color(NAIVEC)
        rows[3][-1].set_color(CONDC)
        whys = [why(r"the oldest fix"), why(r"an impossibility theorem"), why(r"simultaneity"), why(r"the polyhedral lemma")]
        with self.voiceover(
            "<bookmark mark='a'/> A short history. In 1975 David Cox analysed sample splitting: select on one half of "
            "the data and test on the other. <bookmark mark='b'/> In 2006 Hannes Leeb and Benedikt Pötscher proved a "
            "sobering impossibility: the distribution of an estimator after model selection depends on unknown "
            "parameters in a way that cannot be estimated uniformly, so no bootstrap or plug-in can fix the naive "
            "intervals. <bookmark mark='c'/> The response came in two forms. Berk and colleagues in 2013 covered every "
            "model at once. <bookmark mark='d'/> Lee, Sun, Sun and Taylor in 2016 conditioned on the selection, "
            "exactly and computably, and the field of selective inference grew from there."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def window(self):
        A = axes([-3, 5], [0, 2.6], x_length=8.4, y_length=4.0, xlabel=r"the statistic", ylabel=r"density",
                 xticks=[-2, 0, 2, 4], yticks=[0, 1, 2], center=[-2.0, -0.1, 0])
        ax = A.ax
        sw = SelectionWindow(ax, a=1.96, b=np.inf, y=2.3, x_range=(-3, 5), full_color=GREY_B, trunc_color=CONDC, obs_color=SELC, region_color=SELC)
        pic0 = sw.at(0.0)
        side = fit_rows(VGroup(
            label(r"this part's instrument: \ the selection window", font_size=22),
            label(r"grey: \ the statistic's law, \ $N(\mu, 1)$", font_size=22, color=GREY_B),
            label(r"gold band: \ where it must fall to be reported, \ $> 1.96$", font_size=22, color=SELC),
            label(r"blue: \ the same law given selection: \ truncated, \ rescaled", font_size=22, color=CONDC),
            label(rf"shaded: \ $P_\mu(Y > y \mid$ selected$)$: \ {sw.pivot(0.0):.2f} at $\mu = 0$", font_size=22, color=CONDC),
        ), 4.4, 0.38, [4.5, 0.1, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> This part's instrument is the selection window. <bookmark mark='b'/> In grey, the law of a "
            f"statistic, normal with mean mu. <bookmark mark='c'/> The gold band is where it must fall to be reported: "
            f"above one point nine six, significant. <bookmark mark='d'/> In blue, the same law given that it was reported: "
            f"cut at the threshold and rescaled to have total mass one. That is the law a reader of the published finding "
            f"should use. <bookmark mark='e'/> The observed value here is two point three. Under the selected law with mu "
            f"zero, the chance of a value at least this large is not one percent but {say(sw.pivot(0.0), 2)}: a finding "
            f"that looked significant is not, once you account for how it was found."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pic0[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(sw.region), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(pic0[1]), FadeIn(sw.obs), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(pic0[2]), FadeIn(side[4]))
        self.clear_scene()

    def upgrade(self):
        cards = [
            upgrade_card(33, r"control the false discovery rate over thousands of questions", r"the discoveries' estimates and intervals can be read at face value",
                         r"chapters 1--8: \ honest intervals for what was selected"),
            upgrade_card(52, r"the lasso selects, \ and the debiased lasso gives intervals", r"the question was fixed before the lasso chose",
                         r"chapter 3: \ inference on the lasso's own model"),
        ]
        VGroup(*cards).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises come due. Part thirty-three controlled the false discovery rate over thousands "
            "of questions, and quietly let us read the discoveries' estimates at face value. Chapters one to eight give "
            "honest intervals for what was selected. <bookmark mark='b'/> And Part fifty-two's lasso selected variables, "
            "while its intervals assumed the question had been fixed in advance. Chapter three gives inference on the "
            "lasso's own model."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 56", font_size=34, color=GREY_B), label(r"Inference After Selection", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the problem; \ PoSI's simultaneous constant",
            r"the polyhedral lemma, \ proved; \ the lasso's selective intervals on Stamey's data",
            r"randomization, \ splitting and fission; \ knockoffs and conformal selection",
            r"inference on winners; \ inference after clustering; \ open problems",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 33, \ 46, \ 52").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.selective}, \ the selection window").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-six: inference after selection. <bookmark mark='b'/> The problem, and PoSI's "
            "simultaneous answer; the polyhedral lemma, proved, and the lasso's selective intervals on Stamey's prostate "
            "data; randomization, splitting and fission; knockoffs and conformal selection; inference on winners, with the "
            "prostate microarray's top gene; inference after clustering, with Old Faithful; and the open problems."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
