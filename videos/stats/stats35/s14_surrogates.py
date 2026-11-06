from __future__ import annotations

from explainer.stats import museum
from videos.stats.stats35.common import *  # noqa: F403


class Surrogates(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_()
        self.cast()
        self.prentice_()
        self.world()
        self.table()
        self.lessons()

    def card(self):
        card = chapter_card(13, r"Surrogates", r"When the endpoint you measure is not the one you care about", lit=(1989,), part=PART)
        with self.voiceover("Chapter thirteen. Surrogate endpoints."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def why_(self):
        rows = fit_rows(VGroup(
            label(r"strokes and deaths take years and thousands of patients to count", font_size=26),
            label(r"blood pressure, \ cholesterol, \ tumour size, \ viral load: \ weeks", font_size=26, color=Y0C),
            label(r"a surrogate endpoint: \ measured early, \ standing in for the outcome that matters", font_size=26, color=TAUC),
            label(r"the hope: \ change the surrogate, \ change the outcome", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The outcomes that matter, strokes, heart attacks, deaths, take years and thousands of "
            "patients to count. <bookmark mark='b'/> Blood pressure, cholesterol, tumour size and viral load change within "
            "weeks. <bookmark mark='c'/> A surrogate endpoint is such an early measurement, standing in for the outcome that "
            "matters, so that trials can be smaller and faster. <bookmark mark='d'/> The hope is that a drug that improves "
            "the surrogate improves the outcome."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def cast(self):
        c = museum.CAST
        tl = timeline(lit=(1989,)).to_edge(UP, buff=0.35)
        hc = history_card(1989, r"The Cardiac Arrhythmia Suppression Trial (CAST)",
                          r"After a heart attack, \ irregular heartbeats predict sudden death. \ Encainide and flecainide "
                          r"suppress the irregular beats, \ the surrogate, \ superbly, \ and were widely prescribed. \ CAST "
                          r"randomized patients whose arrhythmias the drugs had suppressed to drug or placebo",
                          color=MISSC, width=11.0, font_size=22).move_to([0, 0.8, 0])
        rows = fit_rows(VGroup(
            label(rf"deaths: \ {c['deaths_drug']} on the drugs \ vs \ {c['deaths_placebo']} on placebo \ ({c['n']:,} patients, \ 10 months)", font_size=24, color=MISSC),
            label(r"the surrogate improved; \ the patients died", font_size=24, color=TAUC),
        ), 12.0, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The cautionary tale is the Cardiac Arrhythmia Suppression Trial. After a heart attack, "
            "patients with frequent irregular heartbeats are more likely to die suddenly. The drugs encainide and flecainide "
            "suppressed those irregular beats superbly, and were widely prescribed on that basis. CAST randomized patients "
            "whose arrhythmias the drugs had suppressed to continue them or to switch to placebo. <bookmark mark='b'/> The "
            "trial was stopped early: after an average of ten months, sixty-three of the patients on the drugs had died, "
            "against twenty-six on placebo. <bookmark mark='c'/> The surrogate improved, and the patients died."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def prentice_(self):
        rows = [
            cmath(r"\text{first}", r":", r"\text{the treatment changes the surrogate } S", font_size=30),
            cmath(r"\text{second}", r":", r"S \text{ predicts the outcome } Y", font_size=30),
            cmath(r"\text{third}", r":", r"\text{given } S, \text{ the treatment tells us nothing more about } Y", font_size=30),
            cmath(r"\text{3 fails}", r"\Rightarrow", r"\text{another path from drug to outcome}", font_size=30),
        ]
        rows[2][-1].set_color(TAUC)
        whys = [why(r"Prentice (1989)"), why(r"the reason it was chosen"), why(r"the whole effect runs through $S$"),
                why(r"CAST's drugs: \ pro-arrhythmic")]
        with self.voiceover(
            "<bookmark mark='a'/> Ross Prentice set out criteria in 1989, the year CAST's first results appeared. First, "
            "the treatment must change the surrogate. <bookmark mark='b'/> Second, the surrogate must predict the outcome. "
            "<bookmark mark='c'/> Third, and crucially, once the surrogate is known, the treatment must tell us nothing more "
            "about the outcome: the whole effect must run through the surrogate. <bookmark mark='d'/> When the third fails, "
            "the drug reaches the outcome by another path. Encainide and flecainide, it turned out, could themselves "
            "provoke fatal arrhythmias."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def world(self):
        rows = fit_rows(VGroup(
            label(r"two drugs for the World's patients, \ each lowering pressure by about 8 points", font_size=26),
            label(r"five-year stroke risk rises with the 12-week pressure", font_size=26, color=Y0C),
            label(r"drug A acts only through pressure", font_size=26, color=BANDC),
            label(r"drug B also has an off-target harm", font_size=26, color=MISSC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two invented drugs for the World's patients, each lowering twelve-week pressure by about "
            "eight points. <bookmark mark='b'/> A patient's five-year risk of stroke rises with their twelve-week pressure. "
            "<bookmark mark='c'/> Drug A acts only through pressure. <bookmark mark='d'/> Drug B has, in addition, an "
            "off-target harm, as CAST's drugs did."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("surrogate")
        A, B = d["A"], d["B"]
        rows = [[r"", r"drug A", r"drug B"],
                [r"pressure change (surrogate)", rf"{A['s_diff']:.1f}", rf"{B['s_diff']:.1f}"],
                [r"stroke: \ drug vs control", rf"{100 * A['risk_t']:.1f}\% \ vs \ {100 * A['risk_c']:.1f}\%", rf"{100 * B['risk_t']:.1f}\% \ vs \ {100 * B['risk_c']:.1f}\%"],
                [r"Prentice 1: \ $t$ for drug on $S$", rf"{A['prentice']['z_on_s'][1]:.1f}", rf"{B['prentice']['z_on_s'][1]:.1f}"],
                [r"Prentice 2: \ $t$ for $S$ on $Y$", rf"{A['prentice']['s_on_y'][1]:.1f}", rf"{B['prentice']['s_on_y'][1]:.1f}"],
                [r"Prentice 3: \ $t$ for drug, \ given $S$", rf"{A['prentice']['z_given_s'][1]:.2f}", rf"{B['prentice']['z_given_s'][1]:.1f}"]]
        tab = table_rows(rows, font_size=26, col_buff=0.8, row_buff=0.28, colors=[GREY_A, Y0C, TAUC, None, None, MISSC]).move_to([0, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A trial of each, with stroke counted. <bookmark mark='b'/> The surrogate cannot tell them "
            "apart: both lower pressure by about eight points. <bookmark mark='c'/> The outcome can: drug A cuts strokes from "
            + say(100 * A["risk_c"], 1) + " to " + say(100 * A["risk_t"], 1) + " percent; drug B raises them, from "
            + say(100 * B["risk_c"], 1) + " to " + say(100 * B["risk_t"], 1) + ". <bookmark mark='d'/> Prentice's first two "
            "criteria hold for both. The third separates them: for drug A, given the pressure, the drug adds nothing; for "
            "drug B, it still predicts stroke strongly, with a t of about five. The surrogate was valid for one drug and "
            "not the other."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(tab[5]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"a surrogate is valid for a mechanism, \ not for every drug", font_size=26, color=TAUC),
            label(r"Fleming \& DeMets (1996): \ `Surrogate end points in clinical trials: \ are we being misled?'", font_size=26, color=GREY_A),
            label(r"modern validation: \ meta-analyses of many trials (Buyse et al. 2000)", font_size=26),
            label(r"Prentice's third criterion is about mediation: \ Part 36's question", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson is that a surrogate is valid for a mechanism, not for every drug that moves it. "
            "<bookmark mark='b'/> Thomas Fleming and David DeMets, in a 1996 paper titled Surrogate end points in clinical "
            "trials: are we being misled?, collected the failures. <bookmark mark='c'/> Modern validation uses meta-analyses "
            "of many trials, asking whether the effects on the surrogate predict the effects on the outcome across drugs, "
            "as in Marc Buyse and colleagues' work of 2000. <bookmark mark='d'/> And Prentice's third criterion is a "
            "statement about mediation, how much of an effect runs through an intermediate variable, which needs the tools "
            "of Part 36, because the surrogate itself is not randomized."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
