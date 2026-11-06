from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Immortal(VoiceoverScene):
    def construct(self):
        self.card()
        self.oscars()
        self.mechanism()
        self.stanford_curves()
        self.stanford_table()
        self.statins()
        self.board()
        self.target()

    def card(self):
        card = chapter_card(11, r"Immortal time", r"Time in which the outcome could not happen", lit=(1977, 2001, 2008), part=PART)
        with self.voiceover("Chapter eleven. Immortal time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def oscars(self):
        rows = fit_rows(VGroup(
            label(r"Redelmeier \& Singh (2001): \ Oscar winners live 3.9 years longer than other nominees", font_size=26, color=TAUC),
            label(r"but to win, \ an actor must survive to the ceremony", font_size=26),
            label(r"counting the years before winning as a winner's years: \ immortal time", font_size=26, color=MISSC),
            label(r"Sylvestre, \ Huszti \& Hanley (2006): \ analysed properly, \ about a year, \ not significant", font_size=26, color=SURVC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2001 Donald Redelmeier and Sheldon Singh reported that actors who won an Academy "
            "Award lived almost four years longer than nominees who did not. Fame, they suggested, was good for health. "
            "<bookmark mark='b'/> But to win an Oscar, an actor has to be alive on the night. <bookmark mark='c'/> Counting "
            "each winner's life before their first win as winner's time credits the winners with years in which they "
            "could not have died as winners: immortal time. <bookmark mark='d'/> When Marie-Pierre Sylvestre, Ella Huszti "
            "and James Hanley re-analysed the data in 2006, treating winning as something that happens during follow-up, "
            "the advantage shrank to about a year and was no longer statistically significant."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def mechanism(self):
        rows = [
            cmath(r"\text{ever-treated}", r":", r"\text{classified by what happens later}", font_size=30),
            cmath(r"\text{those treated}", r":", r"\text{survived at least until treatment}", font_size=30),
            cmath(r"\text{fix}", r":", r"x(t) = 1\{\text{treated by } t\}: \ \text{a time-varying covariate}", font_size=30),
            cmath(r"\text{or}", r":", r"\text{landmark: \ classify at a fixed time, \ follow from there}", font_size=30),
        ]
        rows[2][-1].set_color(SURVC)
        whys = [why(r"looking into the future"), why(r"guaranteed survival"), why(r"start-stop rows"), why(r"Anderson et al.\ (1983)")]
        with self.voiceover(
            "<bookmark mark='a'/> The general mistake: classifying people at the start of follow-up by something that "
            "happens to them later. <bookmark mark='b'/> Whoever ends up treated must have survived until treatment, so "
            "the treated group is guaranteed a stretch of survival. <bookmark mark='c'/> The fix is to let treatment be a "
            "covariate that switches on when it starts: each person contributes untreated time until then, and treated "
            "time after, using chapter nine's start-stop rows. <bookmark mark='d'/> Or classify everyone at a fixed "
            "landmark time and follow from there."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def _stair(self, ax, k, col, end):
        t, s = np.asarray(k["t"], float), np.asarray(k["surv"], float)
        pts = [(0, 1.0)]
        prev = 1.0
        for a, b in zip(t, s):
            if a > end:
                break
            pts += [(a, prev), (a, b)]
            prev = b
        pts.append((min(end, float(t[-1])), prev))
        m = VMobject(stroke_color=col, stroke_width=3)
        m.set_points_as_corners([ax.c2p(a, b) for a, b in pts])
        return m

    def stanford_curves(self):
        d = load("immortal")["stanford"]
        A = axes([0, 1500], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"days from acceptance", ylabel=r"survival",
                 xticks=[0, 500, 1000, 1500], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = self._stair(ax, d["km_ever"], MPC, 1500)
        c0 = self._stair(ax, d["km_never"], PLC, 1500)
        side = fit_rows(VGroup(
            label(rf"Stanford, \ 1967--74: \ {d['n']} patients accepted for a new heart", font_size=22),
            label(rf"{d['transplanted']} received one, \ after a median wait of {d['median_wait']:.0f} days", font_size=22, color=MPC),
            label(rf"{d['died_waiting']} died waiting \ (red)", font_size=22, color=PLC),
            label(r"green: \ the transplanted, \ from acceptance", font_size=22, color=MPC),
            label(r"a huge gap \ ... \ partly built in", font_size=22, color=MISSC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic case. Stanford's heart transplant programme accepted " + str(d["n"]) + " "
            "patients between 1967 and 1974. <bookmark mark='b'/> " + str(d["transplanted"]) + " received a heart, after a "
            "median wait of " + str(round(d["median_wait"])) + " days. <bookmark mark='c'/> " + str(d["died_waiting"])
            + " died while waiting. <bookmark mark='d'/> Compare survival from acceptance of those who were ever "
            "transplanted with those who never were, <bookmark mark='e'/> and the gap is enormous. But part of it is built "
            "in: to receive a heart you had to survive the wait, and those who died early never could."
        ) as vo:
            self.add(stanford_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def stanford_table(self):
        d = load("immortal")["stanford"]
        rows = [[r"Stanford: \ transplant vs not", r"HR", r"95\% CI"],
                [r"ever transplanted \ (naive)", f"{d['naive_hr']:.2f}", f"{d['naive_ci'][0]:.2f}--{d['naive_ci'][1]:.2f}"],
                [r"transplant as time-varying", f"{d['tv_hr']:.2f}", f"{d['tv_ci'][0]:.2f}--{d['tv_ci'][1]:.2f}"],
                [r"time-varying, \ adjusted for age", f"{d['tva_hr']:.2f}", f"{d['tva_ci'][0]:.2f}--{d['tva_ci'][1]:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.2, row_buff=0.36, colors=[GREY_A, MISSC, SURVC, SURVC]).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"a 73\% reduction in the hazard becomes \ no detectable difference", font_size=24, color=TAUC),
            label(r"Crowley \& Hu (1977): \ the analysis that made time-varying covariates standard", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The numbers. <bookmark mark='b'/> The naive comparison gives a hazard ratio of "
            + say(d["naive_hr"], 2) + ": transplantation would cut the hazard of death by nearly three quarters. "
            "<bookmark mark='c'/> With transplant as a time-varying covariate, the ratio is " + say(d["tv_hr"], 2) + ", "
            "<bookmark mark='d'/> and adjusting for age, " + say(d["tva_hr"], 2) + ", with wide intervals around one. In "
            "these early years, with the drugs of the time, there was no clear survival benefit at all. John Crowley and "
            "Marie Hu's analysis of 1977 made time-varying covariates a standard tool."
        ) as vo:
            self.add(stanford_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(foot))
        self.clear_scene()

    def statins(self):
        d = load("immortal")["statin"]
        rows = [[r"the World's statins \ (no effect at all)", r"HR", r"95\% CI"],
                [r"ever-users vs never \ (immortal time)", f"{d['naive_hr']:.2f}", f"{d['naive_ci'][0]:.2f}--{d['naive_ci'][1]:.2f}"],
                [r"time-varying, \ unadjusted", f"{d['tv_hr']:.2f}", f"{d['tv_ci'][0]:.2f}--{d['tv_ci'][1]:.2f}"],
                [r"time-varying, \ adjusted for pressure and age", f"{d['tva_hr']:.2f}", f"{d['tva_ci'][0]:.2f}--{d['tva_ci'][1]:.2f}"]]
        tab = table_rows(rows, font_size=28, col_buff=1.0, row_buff=0.36, colors=[GREY_A, MISSC, AREAC, SURVC]).move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"two biases in opposite directions: \ immortal time, \ then confounding by indication", font_size=24, color=TAUC),
            label(rf"{d['users']} of 4,000 start a statin, \ sooner if their pressure is high; \ the truth is HR = 1", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World's cohort has a statin that does nothing at all; doctors start it sooner in "
            "people with high blood pressure. <bookmark mark='b'/> Comparing ever-users with never-users gives a hazard "
            "ratio of " + say(d["naive_hr"], 2) + ", a protective effect, with an interval excluding one: immortal time "
            "again. <bookmark mark='c'/> Treating use as time-varying removes that, and reveals the next bias: "
            + say(d["tv_hr"], 2) + ", harmful, because those given statins had higher pressure, confounding by indication. "
            "<bookmark mark='d'/> Adjusting for pressure and age as well gives " + say(d["tva_hr"], 2) + ", the truth."
        ) as vo:
            self.add(cohort_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]), FadeIn(foot[0]))
        self.clear_scene()

    def board(self):
        rows = board_rows("immortal", "time-varying")
        text = (
            "<bookmark mark='a'/> On the Coverage Board, a null treatment started at random times during follow-up, with "
            "four hundred patients. The ever-treated Cox interval for the hazard ratio covers the truth, one, essentially "
            "never. <bookmark mark='b'/> The time-varying analysis keeps its ninety percent promise."
        )
        show_board(self, rows, text, [("a", [0]), ("b", [1])])

    def target(self):
        rows = fit_rows(VGroup(
            label(r"Suissa (2008): \ immortal time in dozens of published drug studies", font_size=26, color=MISSC),
            label(r"the cure: \ align time zero, \ eligibility and treatment assignment", font_size=26, color=TAUC),
            label(r"emulate the target trial \ (Hern\'an \& Robins 2016, \ Part 36)", font_size=26, color=SURVC),
            label(r"in a trial they align by design; \ in data, \ only by care", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Samy Suissa found immortal time in dozens of published studies of drugs, often "
            "producing impressive, and spurious, benefits. <bookmark mark='b'/> The cure is to line up three things: the "
            "time zero of follow-up, the moment of eligibility, and the moment treatment is assigned. <bookmark mark='c'/> "
            "That is what emulating a target trial, Part thirty-six's discipline, enforces. <bookmark mark='d'/> In a "
            "randomized trial the three coincide by design; in observational data, only by care."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
