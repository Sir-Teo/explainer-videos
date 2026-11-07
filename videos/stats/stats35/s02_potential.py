from __future__ import annotations

import numpy as np

from videos.stats.stats35.common import *  # noqa: F403


class Potential(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.define()
        self.trial()
        self.table()
        self.hide()
        self.histogram()
        self.holland()

    def card(self):
        card = chapter_card(1, r"Potential outcomes", r"Two futures for every unit", lit=(1923, 1974), part=PART)
        with self.voiceover("Chapter one. Potential outcomes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"Jerzy Neyman (1923): \ the yield plot $i$ \emph{would} give under each variety", font_size=26, color=Y0C),
            label(r"written in Polish, \ for agricultural trials; \ translated only in 1990", font_size=26, color=GREY_A),
            label(r"Donald Rubin (1974): \ the same idea for observational studies, \ and for people", font_size=26, color=Y1C),
            label(r"Paul Holland (1986): \ `the Rubin causal model', \ and its fundamental problem", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The language comes from Jerzy Neyman's master's thesis of 1923. Writing about field "
            "trials, he imagined, for each plot of land, the yield it would give under each variety of seed, only one of "
            "which could be sown. <bookmark mark='b'/> The thesis was written in Polish and was not translated into English "
            "until 1990. <bookmark mark='c'/> Donald Rubin reinvented and extended the idea from 1974 onward, for "
            "observational studies and for people, <bookmark mark='d'/> and in 1986 Paul Holland named it the Rubin causal "
            "model and stated its central difficulty."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def define(self):
        rows = [
            cmath(r"Y_i(1), \ Y_i(0)", r":", r"\text{unit } i\text{'s outcome with and without treatment}", font_size=30),
            cmath(r"\tau_i", r"=", r"Y_i(1) - Y_i(0)", font_size=34),
            cmath(r"Y_i", r"=", r"Z_i Y_i(1) + (1 - Z_i)\, Y_i(0)", font_size=34),
            cmath(r"\text{the science}", r":", r"\{Y_i(0), Y_i(1)\}_{i=1}^n \ \text{fixed; \ only } Z \text{ is random}", font_size=28),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"two potential outcomes"), why(r"the unit-level causal effect"), why(r"what we see: \ one of the two"),
                why(r"the design-based view")]
        with self.voiceover(
            "<bookmark mark='a'/> For each unit i, say a patient, there are two potential outcomes: the outcome if treated, "
            "Y i of one, and the outcome if not, Y i of zero. Both are fixed properties of the patient, defined before any "
            "treatment is given. <bookmark mark='b'/> The causal effect of the treatment on this patient is their "
            "difference, tau i. <bookmark mark='c'/> What we observe depends on the assignment Z i: the treated outcome if "
            "Z is one, the untreated outcome if Z is zero. <bookmark mark='d'/> In Neyman's design-based view, the table of "
            "all the potential outcomes, which Rubin calls the science, is fixed. The only randomness is in who gets "
            "treated."
        ) as vo:
            intro=label('A unit-level effect compares two potential outcomes',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def trial(self):
        d = load("science")
        rows = fit_rows(VGroup(
            label(rf"the World's clinic trial: \ {d['n']:,} adults with untreated high blood pressure", font_size=26),
            label(r"outcome: \ systolic pressure after 12 weeks (mm Hg)", font_size=26),
            label(r"$Y(0)$: \ without the drug; \ $Y(1)$: \ with it", font_size=26, color=Y0C),
            label(r"the World knows both for every patient", font_size=26, color=TAUC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This part's patients come from the World. Two thousand adults with untreated high blood "
            "pressure enrol in a trial of a new drug. <bookmark mark='b'/> The outcome is their systolic pressure after twelve "
            "weeks. <bookmark mark='c'/> Each has a pressure they would have without the drug, and a pressure they would "
            "have with it. <bookmark mark='d'/> Because the World is a simulation, we know both, for every patient. No real "
            "trial ever has this table; we will use it to check every method against the truth."
        ) as vo:
            self.add(trial_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("science")
        f = d["first"]
        tab = ScienceTable([r["y0"] for r in f], [r["y1"] for r in f], extra=[(r"age", [r["age"] for r in f])],
                           center=[-2.0, 0.0, 0], font_size=26)
        side = fit_rows(VGroup(
            label(r"eight patients' science", font_size=22),
            label(r"blue: \ $Y(0)$, \ without the drug", font_size=22, color=Y0C),
            label(r"red: \ $Y(1)$, \ with it", font_size=22, color=Y1C),
            label(r"gold: \ their own effects", font_size=22, color=TAUC),
            label(r"from $-4$ to $-15$ mm Hg", font_size=22, color=TAUC),
        ), 4.2, 0.4, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is the science table for the first eight patients, with their ages. <bookmark "
            "mark='b'/> In blue, the pressure each would have at twelve weeks without the drug. <bookmark mark='c'/> In "
            "red, with it. <bookmark mark='d'/> And in gold, each patient's own causal effect: <bookmark mark='e'/> the drug "
            "lowers the pressure of patient two by four points, of patient four by fifteen. The effects differ from person "
            "to person."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(tab.rows[0]), FadeIn(tab.column("unit")[1:]), FadeIn(tab.column("age")[1:]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab.column("y0")[1:]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab.column("y1")[1:]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab.column("tau")[1:]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hide(self):
        d = load("science")
        f = d["first"]
        tab = ScienceTable([r["y0"] for r in f], [r["y1"] for r in f], extra=[(r"age", [r["age"] for r in f])],
                           center=[-2.0, 0.0, 0], font_size=26)
        z = np.array([1, 0, 0, 1, 1, 0, 1, 0], bool)
        m = tab.mask(z)
        side = fit_rows(VGroup(
            label(r"now run the trial: \ a coin for each", font_size=22),
            label(r"treated: \ we see $Y(1)$ only", font_size=22, color=Y1C),
            label(r"control: \ we see $Y(0)$ only", font_size=22, color=Y0C),
            label(r"every $\tau_i$ is hidden", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now run the trial. A coin decides each patient's arm. <bookmark mark='b'/> For the "
            "treated patients we see the pressure with the drug, and the pressure they would have had without it "
            "disappears. <bookmark mark='c'/> For the controls, the reverse. <bookmark mark='d'/> Half of the science table "
            "is now missing, and every single individual effect is gone, because each needs both columns."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[m[2 * i] for i in range(8) if z[i]])), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[m[2 * i] for i in range(8) if not z[i]])), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*[m[2 * i + 1] for i in range(8)])), FadeIn(side[3]))
        self.clear_scene()

    def histogram(self):
        d = load("science")
        h = np.asarray(d["hist"], float)
        e = np.asarray(d["edges"], float)
        A = axes([-28, 8], [0, 0.11], x_length=7.4, y_length=4.2, xlabel=r"$\tau_i$ (mm Hg)", ylabel=r"share",
                 xticks=[-25, -15, -5, 0, 5], yticks=[0, 0.05, 0.1], center=[-2.0, 0.2, 0])
        ax = A.ax
        bars = hist_bars(ax, e, h / h.sum(), color=TAUC, opacity=0.7)
        mean = DashedLine(ax.c2p(d["ate"], 0), ax.c2p(d["ate"], 0.105), color=WHITE, stroke_width=2.5)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.105), color=MISSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"all 2,000 patients' effects", font_size=22),
            label(rf"average: \ {d['ate']:.2f} mm Hg", font_size=22, color=TAUC),
            label(rf"SD across patients: \ {d['sd_tau']:.2f}", font_size=22),
            label(rf"{100 * d['harmed']:.1f}\% would be harmed \ ($\tau_i > 0$)", font_size=22, color=MISSC),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Over all two thousand patients, the individual effects form a distribution. <bookmark "
            "mark='b'/> On average the drug lowers the pressure at twelve weeks by " + say(-d["ate"], 1) + " millimetres of "
            "mercury. <bookmark mark='c'/> But the effects vary, with a standard deviation of nearly five, because the drug "
            "works better at higher pressures and greater ages. <bookmark mark='d'/> And for about four percent of patients, "
            "the drug would make things slightly worse. A real trial can estimate the average; as we will see, it cannot "
            "tell us who those four percent are."
        ) as vo:
            self.add(trial_tag())
            self.play(FadeIn(A), FadeIn(bars), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(zero), FadeIn(side[3]))
        self.clear_scene()

    def holland(self):
        rows = fit_rows(VGroup(
            label(r"\textbf{the fundamental problem of causal inference}: \ we never see both $Y_i(0)$ and $Y_i(1)$", font_size=26, color=MISSC),
            label(r"so causal inference is a missing-data problem: \ half the science is always missing", font_size=26),
            label(r"`no causation without manipulation': \ potential outcomes need a well-defined treatment", font_size=26, color=GREY_A),
            label(r"the way out: \ give up on $\tau_i$, \ aim at averages, \ and let the design do the work", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Holland called this the fundamental problem of causal inference: we never observe both "
            "potential outcomes for the same unit. <bookmark mark='b'/> Causal inference is therefore a missing-data "
            "problem, with half of the science always missing, and Part 41 will treat missing data in general. <bookmark "
            "mark='c'/> Holland also insisted on no causation without manipulation: a potential outcome needs a treatment "
            "that could, at least in principle, be applied; the effect of a person's sex or race is a harder notion. "
            "<bookmark mark='d'/> The way forward is to give up on individual effects, aim at averages over units, and let "
            "the design of the study tell us which missing outcomes look like which observed ones."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
