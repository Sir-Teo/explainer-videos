from __future__ import annotations

from videos.stats.stats35.common import *  # noqa: F403


class Noncompliance(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.types()
        self.estimates()
        self.late()
        self.assumptions()
        self.board()
        self.meaning()

    def card(self):
        card = chapter_card(9, r"Noncompliance", r"Assigned is not treated", lit=(1994,), part=PART)
        with self.voiceover("Chapter nine. Noncompliance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"$Z$: \ the coin's assignment; \ $D$: \ the treatment actually taken", font_size=26),
            label(r"some assigned the drug never take it; \ some controls get it elsewhere", font_size=26, color=MISSC),
            label(r"$Z$ is random; \ $D$ is not: \ it is chosen, \ by patients", font_size=26, color=TAUC),
            label(r"ITT targets assignment; \ LATE targets compliers under extra assumptions", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In a real trial, the coin's assignment Z and the treatment actually taken, D, can "
            "differ. <bookmark mark='b'/> Some patients assigned the drug never take it; some assigned to control "
            "obtain it elsewhere. <bookmark mark='c'/> Z is random; D is not. It is chosen, by the patients, for "
            "reasons that may be related to their health. <bookmark mark='d'/> Different analyses target different "
            "effects. Intention to treat preserves randomization; a complier effect needs further assumptions."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def types(self):
        d = load("noncomp")
        sh, ag, y0, ta = d["shares"], d["age_by_type"], d["y0_by_type"], d["tau_by_type"]
        rows = [[r"type", r"$D$ if $Z = 0$", r"$D$ if $Z = 1$", r"share", r"mean $Y(0)$", r"mean $\tau$"],
                [r"complier", r"0", r"1", rf"{100 * sh[0]:.1f}\%", rf"{y0[0]:.1f}", rf"{ta[0]:.1f}"],
                [r"never-taker", r"0", r"0", rf"{100 * sh[1]:.1f}\%", rf"{y0[1]:.1f}", rf"{ta[1]:.1f}"],
                [r"always-taker", r"1", r"1", rf"{100 * sh[2]:.1f}\%", rf"{y0[2]:.1f}", rf"{ta[2]:.1f}"],
                [r"defier", r"1", r"0", r"0\% \ (assumed)", r"", r""]]
        tab = table_rows(rows, font_size=24, col_buff=0.6, row_buff=0.3, colors=[GREY_A, BANDC, Y0C, Y1C, GREY_C]).move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"principal strata: \ how each patient \emph{would} respond to each assignment", font_size=24, color=TAUC),
            label(r"never-takers feel well \ (lower $Y(0)$); \ always-takers are the sickest", font_size=24, color=MISSC),
        ), 12.4, 0.35, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Potential outcomes handle this by giving each patient two potential treatments too: what "
            "they would take if assigned to control, and if assigned to the drug. That sorts patients into principal "
            "strata. <bookmark mark='b'/> Compliers take the drug exactly when assigned it: " + f"{100 * sh[0]:.0f}" + " "
            "percent of the World's patients. Never-takers never take it: " + f"{100 * sh[1]:.0f}" + " percent. "
            "Always-takers get it regardless: " + f"{100 * sh[2]:.0f}" + " percent. Defiers would do the opposite of their assignment; we assume there are none. <bookmark "
            "mark='c'/> The strata are different people. The never-takers tend to feel well, with lower pressure even"
            " untreated; the always-takers are the sickest. Individual stratum membership is only partly observed. "
            "Under monotonicity, a treated control is an always-taker and an untreated assigned patient is a "
            "never-taker; the other two observed groups mix strata."
        ) as vo:
            self.add(trial_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def estimates(self):
        d = load("noncomp")
        rows = [[r"analysis", r"compares", r"estimate"],
                [r"intention to treat", r"by $Z$", rf"{d['itt']['est']:.2f}"],
                [r"as treated", r"by $D$", rf"{d['as_treated']['est']:.2f}"],
                [r"per protocol", r"observed adherers only", rf"{d['per_protocol']['est']:.2f}"],
                [r"IV (Wald)", r"ITT / estimated first stage", rf"{d['iv']['est']:.2f}"],
                [r"truth", r"compliers' average effect", rf"{d['cace']:.2f}"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.28, colors=[GREY_A, Y0C, MISSC, MISSC, BANDC, TRUEC]).move_to([0, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One randomization of the World's trial, with real compliance. The intention-to-treat "
            "analysis compares the arms as randomized: minus " + say(-d["itt"]["est"], 1) + ". It is unbiased, but for the "
            "effect of being assigned the drug, diluted by everyone who did not take it. <bookmark mark='b'/> The "
            "as-treated analysis compares those who took the drug with those who did not: minus " + say(-d["as_treated"]["est"], 1)
            + ". The naive per-protocol analysis keeps observed adherers, a mixture of principal strata: minus " + say(-d["per_protocol"]["est"], 1) + ". Both compare groups formed by the patients' choices, and both are biased. <bookmark mark='c'/> The "
            "instrumental variable estimate divides the intention-to-treat effect by the estimated first-stage "
            "treatment contrast: minus "
            + say(-d["iv"]["est"], 1) + ", <bookmark mark='d'/> against the compliers' true average effect of minus "
            + say(-d["cace"], 1) + "."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(tab[5]))
        self.clear_scene()

    def late(self):
        rows = [
            cmath(r"\text{ITT}_Y", r"=", r"\pi_c\, \text{CACE} + \pi_n \cdot 0 + \pi_a \cdot 0", font_size=32),
            cmath(r"\text{ITT}_D", r"=", r"E[D \mid Z = 1] - E[D \mid Z = 0] = \pi_c", font_size=32),
            cmath(r"\text{CACE}", r"=", r"\dfrac{\text{ITT}_Y}{\text{ITT}_D}", font_size=34),
            cmath(r"\text{here}", r":", r"-5.62 / 0.649 = -8.66", font_size=32),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"assignment changes nothing for never- and always-takers"), why(r"the share of compliers"),
                why(r"Imbens \& Angrist (1994); \ Angrist, \ Imbens \& Rubin (1996)"), why(r"the World's trial")]
        with self.voiceover(
            "<bookmark mark='a'/> Why the ratio works. The intention-to-treat effect on the outcome averages over the "
            "strata. For never-takers and always-takers, the assignment does not change what they take, so, if the "
            "assignment has no effect except through the drug, their contribution is zero. Only compliers contribute, with "
            "their average effect, weighted by their share. <bookmark mark='b'/> The intention-to-treat effect on the "
            "treatment taken is exactly that share. <bookmark mark='c'/> So the ratio is the compliers' average causal "
            "effect, which Guido Imbens and Joshua Angrist called in 1994 the local average treatment effect. <bookmark "
            "mark='d'/> For the World's trial, minus five point six two over point six four nine, which is minus eight "
            "point six six."
        ) as vo:
            intro=label('Randomization and exclusion isolate the complier contribution',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def assumptions(self):
        rows = fit_rows(VGroup(
            label(r"1. \ $Z$ randomized", font_size=26, color=BANDC),
            label(r"2. \ exclusion: \ $Z$ affects $Y$ only through $D$ \ (blinding helps)", font_size=26, color=TAUC),
            label(r"3. \ monotonicity: \ no defiers", font_size=26, color=TAUC),
            label(r"4. \ a first stage: \ $\pi_c > 0$; \ weak if small (Part 37)", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The derivation used four assumptions. The assignment is randomized, which the trial "
            "guarantees. <bookmark mark='b'/> Exclusion: being assigned the drug changes the outcome only through taking "
            "it, which a placebo and blinding make plausible. <bookmark mark='c'/> Monotonicity: no one does the opposite of "
            "their assignment. <bookmark mark='d'/> And there must be some compliers; when there are few, the ratio becomes "
            "unstable, the weak-instrument problem of Part 37."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("as-treated", "IV (Wald)")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Board, as intervals for the compliers' average effect over a thousand "
                   "randomizations. The as-treated comparison: broken, never covering it. <bookmark mark='b'/> The IV "
                   "estimate with its delta-method interval: kept.",
                   [("a", [0]), ("b", [1])])

    def meaning(self):
        rows = fit_rows(VGroup(
            label(r"the LATE is the effect for compliers, \ whose full membership is not observed", font_size=26),
            label(r"intention to treat answers the policy question: \ what happens if we offer the drug?", font_size=26, color=Y0C),
            label(r"the LATE answers a scientific one: \ what does the drug do to those who take it only when offered?", font_size=26, color=BANDC),
            label(r"report both; \ never as-treated alone", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The local average treatment effect is the effect for compliers, a group whose full "
            "membership we cannot list from one assignment. <bookmark mark='b'/> The intention-to-treat effect "
            "answers the policy question: what happens if we offer this drug to such patients? <bookmark mark='c'/> "
            "The local effect answers a scientific one: what does the drug do for those who take it only when it is "
            "offered? <bookmark mark='d'/> Report both; and never report the as-treated comparison alone."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
