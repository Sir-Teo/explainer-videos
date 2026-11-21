from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403

PROBLEMS = [
    r"The logit: \ if $\varepsilon_{\text{car}}$ and $\varepsilon_{\text{bus}}$ are independent extreme-value draws, "
    r"\ show that $\Pr(\text{bus}) = e^{V_{\text{bus}}}/(e^{V_{\text{car}}} + e^{V_{\text{bus}}})$.",
    r"The value of time: \ with $\beta_{\text{time}} = -0.06$ a minute and $\beta_{\text{cost}} = -0.5$ a dollar, "
    r"\ what is an hour worth? \ Give its standard error by the delta method.",
    r"The red bus and the blue bus: \ car and a red bus are chosen equally often; \ a blue bus identical to the "
    r"red one is added. \ What does the logit predict, \ and what would you expect?",
    r"GMM: \ for $y = x\beta + u$ with instruments $z$, \ show that GMM with $W = (Z'Z)^{-1}$ is two-stage least "
    r"squares.",
    r"Hansen's $J$: \ with eight conditions and two parameters, \ $J = 11.3$. \ Is the model rejected at 5\%? \ "
    r"At 10\%?",
    r"Simulated moments: \ why must the random draws be the same at every guess? \ By how much does $S = 5$ "
    r"inflate the variance?",
    r"Spurious habit: \ with two types and no habit, \ show that $\Pr(y_t = 1 \mid y_{t-1} = 1) > \Pr(y_t = 1 \mid "
    r"y_{t-1} = 0)$.",
    r"$\bigstar$ \ Manski: \ outcomes lie in $[0, 1]$ and shares $p_1$ and $p_0$ of the two arms are missing. \ "
    r"Show that the no-assumption bound on the effect has width $p_1 + p_0$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"By writing down how the choices would follow from the hidden parameters, \ and finding "
                          r"the values under which the model reproduces what people did: \ by likelihood when it "
                          r"gives probabilities, \ by moments when it gives averages, \ by simulation when it gives "
                          r"neither. \ Then by asking what in the data pins each value down, \ how far it leans on "
                          r"assumptions the data cannot check, \ and whether the model predicts what it was never "
                          r"shown.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, DATA, 2.4, smooth=False).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: how is a model's hidden machinery measured from the choices it predicts? <bookmark mark='a'/> By "
            "writing down how the choices would follow from the hidden parameters, and finding the values under "
            "which the model reproduces what people actually did: by likelihood when the model gives "
            "probabilities, by moments when it gives only averages, and by simulation when it gives neither. "
            "Then by asking three more questions, which matter as much as the estimate: what in the data pins each "
            "value down; how far the answer leans on assumptions the data cannot check; and whether the model "
            "predicts what it was never shown."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=12.0, rate_func=linear)
            self.play(Indicate(a, color=E.ACCENT, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def recap(self):
        H, C, Gm, M, L, T, F, S, Sc = (load(x) for x in (
            "history", "commuters", "gmm", "ma1", "lifecycle", "types", "fragile", "sufficient", "school"))
        items = [
            (rf"structural: \ a line through history says {100 * H['charge_line']:.0f}\% drive; \ the logit "
             rf"{100 * H['charge_logit']:.0f}\%".replace("-", "{-}"), MODEL),
            (rf"the logit: \ an hour is worth \${C['vot']:.2f} \ (planted \${C['vot_truth']:.2f})", DATA),
            (r"a new railway: \ the logit draws from car and bus too evenly", RAIL),
            (r"the Play it: \ patience and caution move every fact alike", CAUTION),
            (rf"GMM: \ Euler conditions, \ no solving; \ a mispriced asset, \ $J = {Gm['bad_J']:.0f}$", THEORY),
            (rf"simulation: \ indirect inference, \ error {M['ii']['rmse']:.2f} against {M['naive']['rmse']:.2f}",
             PATIENCE),
            (rf"the life cycle: \ truth recovered; \ the estimates' correlation {L['corr']:.4f}".replace("-", "{-}"),
             EST),
            (rf"hidden types: \ a habit of {T['pooled_lag']:.2f} if ignored, \ {T['mix_lag']:.2f} with them",
             CAUTION),
            (rf"identification: \ 1\% more wealth moves caution "
             rf"{abs(F['efficient']['actual'][1]) / L['se'][1]:.0f} standard errors", ERR),
            (r"calibration: \ the borrowed number sets the estimated one; \ report the fit", PATIENCE),
            (rf"sufficient statistics: \ right nearby; \ {100 * S['b_const']:.0f}\% for {100 * S['bstar']:.0f}\% "
             r"far away", THEORY),
            (rf"validation and bounds: \ {100 * Sc['label']['predicted_effect']:.0f} points predicted, "
             rf"{100 * Sc['label']['experimental_effect']:.0f} found; \ intervals first", GAIN),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 54, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part fifty-four in twelve lines. <bookmark mark='r1'/> A structural model knows why people choose, so "
            "it can be asked about a world nobody has seen; a pattern fitted to history cannot. <bookmark "
            "mark='r2'/> Random utility with extreme-value errors gives the logit, and maximum likelihood reads "
            "the value of time off people's choices. <bookmark mark='r3'/> The logit's independence makes a new "
            "option draw too evenly from the old ones; nests fix it. <bookmark mark='r4'/> Two parameters that move "
            "every fact alike cannot be told apart by those facts. <bookmark mark='r5'/> The generalized method of "
            "moments estimates from conditions alone, and its J-test catches a condition that fails. <bookmark "
            "mark='r6'/> Simulation estimates what has no formula, with fixed draws and a small price in precision. "
            "<bookmark mark='r7'/> The Island's households were estimated, and the truth recovered, along a "
            "very narrow ridge. <bookmark mark='r8'/> Ignore who people are, and a habit appears from nowhere. "
            "<bookmark mark='r9'/> A one-percent error in the data can move an estimate by dozens of standard "
            "errors, and the sensitivity matrix shows where. <bookmark mark='r10'/> Calibration borrows a number, "
            "and the borrowed number decides the rest. <bookmark mark='r11'/> Sufficient statistics answer "
            "nearby questions without a model, and far-away ones wrongly. <bookmark mark='r12'/> And the best tests "
            "are an experiment the model never saw, and the bounds the data allow before we assume anything."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Derive the logit; price an hour and its uncertainty; the red bus and the blue bus; GMM "
            "as two-stage least squares; reading a J statistic; why simulations need fixed draws; a habit made of "
            "types; and a starred problem on the width of Manski's bounds. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Kenneth Train, \emph{Discrete Choice Methods with Simulation} (2nd ed., 2009)",
             r"Fumio Hayashi, \emph{Econometrics} (2000), \ chapters 3, 4 and 7",
             r"Hamish Low and Costas Meghir, \ `The use of structural models in econometrics', \emph{JEP} (2017)",
             r"Charles Manski, \emph{Partial Identification of Probability Distributions} (2003)"],
            [r"Marschak (1953); \ McFadden (1974, 1989); \ Hansen (1982); \ Hansen and Singleton (1982)",
             r"Kydland and Prescott (1982); \ Rust (1987); \ Pakes and Pollard (1989); \ Manski (1990)",
             r"Gouri\'eroux, Monfort and Renault (1993); \ Hotz and Miller (1993); \ Keane and Wolpin (1997)",
             r"Gourinchas and Parker (2002); \ Todd and Wolpin (2006); \ Chetty (2009)",
             r"Andrews, Gentzkow and Shapiro (2017); \ Cranmer, Brehmer and Louppe (2020)"])
        with self.voiceover(
            "The reading: Kenneth Train's book on discrete choice and simulation; Fumio Hayashi's chapters on the "
            "generalized method of moments; Hamish Low and Costas Meghir on what structural models are for; and "
            "Charles Manski on partial identification. Then the papers, from Marschak to the frontier."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1992, r"Christopher Sims and the price puzzle",
                          r"in his vector autoregressions for five countries, \ prices rose after the central bank "
                          r"raised its rate", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 55 \ $\cdot$ \ Act X, \ The Graduate Core", font_size=30, color=GREY_B),
                     label(r"Identifying Macro", font_size=46),
                     label(r"with one history and no control group, \ how can anyone say what a policy did?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from people's choices \ to a whole economy's history", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.5)
        steps = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                 stroke_width=2.0), label(t_, font_size=18, color=c_))
                         for t_, c_ in ((r"vector autoregressions", DATA), (r"narrative shocks", EST),
                                        (r"high-frequency surprises", MODEL), (r"the Island's history", GAIN))])
        for s_ in steps:
            s_[1].move_to(s_[0])
        steps.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, the hardest identification problem in economics. <bookmark mark='a'/> In 1992 Christopher "
            "Sims ran careful vector autoregressions for five countries and found that after a central bank raised "
            "its rate, prices rose. It is called the price puzzle, and it is what identification failing looks "
            "like: the bank raised rates because it saw inflation coming. <bookmark mark='b'/> Part fifty-five is "
            "about identifying macroeconomic effects with one history and no control group: vector "
            "autoregressions, narrative shocks, surprises measured in minutes, <bookmark mark='c'/> and the "
            "Island's own history, where the true effect is known, to grade them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
