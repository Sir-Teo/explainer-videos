from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class Censoring(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.assumption()
        self.cohort()
        self.naive()
        self.truncation()
        self.entry_plot()

    def card(self):
        card = chapter_card(2, r"Censoring and truncation", r"What a study cannot see", lit=(1958,), part=PART)
        with self.voiceover("Chapter two. Censoring and truncation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def kinds(self):
        rows = [[r"kind", r"what we know", r"example"],
                [r"right censoring", r"$T > c$", r"the study ends; \ the patient moves away"],
                [r"left censoring", r"$T < c$", r"the tumour was already there at the first scan"],
                [r"interval censoring", r"$a < T \le b$", r"infection found between two visits"],
                [r"left truncation", r"seen only if $T > a$", r"a cohort recruited at age 60 never meets the dead"]]
        tab = table_rows(rows, font_size=26, col_buff=0.7, row_buff=0.36, colors=[GREY_A, CENSC, AREAC, TAUC, MISSC]).move_to([0, 0.4, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> Four ways a lifetime can be partly hidden. <bookmark mark='b'/> Right censoring, the "
            "common one: we know only that the event had not happened by some time, because the study ended or the "
            "patient was lost. <bookmark mark='c'/> Left censoring: it had already happened before we looked. <bookmark "
            "mark='d'/> Interval censoring: it happened between two visits. <bookmark mark='e'/> And truncation, which is "
            "different: people whose event came too early never enter the study at all, so we do not even know they "
            "existed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
        self.clear_scene()

    def assumption(self):
        rows = [
            cmath(r"\text{observe}", r":", r"X = \min(T, C), \ \ \delta = 1\{T \le C\}", font_size=32),
            cmath(r"\text{assume}", r":", r"T \perp C \ \ (\text{given covariates})", font_size=32),
            cmath(r"\text{then}", r":", r"L = \textstyle\prod_i f(x_i)^{\delta_i}\, S(x_i)^{1 - \delta_i}", font_size=32),
            cmath(r"\text{fails if}", r":", r"\text{the sickest drop out, \ or the well stop coming}", font_size=30),
        ]
        rows[2][-1].set_color(SURVC)
        whys = [why(r"the time and the indicator"), why(r"non-informative censoring"), why(r"a censored case contributes $S$"),
                why(r"untestable from the data")]
        with self.voiceover(
            "<bookmark mark='a'/> With right censoring we see the smaller of the lifetime T and a censoring time C, "
            "and an indicator of which came first. <bookmark mark='b'/> The likelihood and regression analyses "
            "require censoring to be independent of the lifetime conditional on the covariates used, with adequate "
            "follow-up support. Unadjusted Kaplan-Meier needs independence at the population level being pooled; "
            "conditional independence alone is insufficient. <bookmark mark='c'/> Then the likelihood multiplies the "
            "density for each observed event and the survival function for each censored case, exactly the at least "
            "this long of the open rings. <bookmark mark='d'/> The assumption fails if the sickest patients drop out,"
            " or the healthiest stop coming to clinic, and the data alone cannot tell: it is the missing at random of"
            " Part forty-one, in disguise."
        ) as vo:
            heading = label('Independent censoring assumptions determine the likelihood', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def cohort(self):
        d = load("life")
        rows = fit_rows(VGroup(
            label(rf"the World's cohort: \ {d['n']:,} adults aged 40--79, \ followed for 15 years", font_size=28, color=SURVC),
            label(rf"{d['deaths']:,} deaths seen; \ {d['censored']:,} censored", font_size=28),
            label(rf"{d['admin']:,} reached the end of the study alive; \ {d['lost']:,} were lost to follow-up", font_size=28, color=CENSC),
            label(r"and the World knows every latent lifetime: \ the truth to check against", font_size=28, color=TRUEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World runs a cohort study: " + f"{d['n']:,}" + " adults aged forty to seventy-nine, "
            "followed for fifteen years. <bookmark mark='b'/> " + f"{d['deaths']:,}" + " deaths are seen, and the other "
            + f"{d['censored']:,}" + " are censored: <bookmark mark='c'/> most reached the end of the study alive, and the "
            "rest moved away or stopped answering. <bookmark mark='d'/> Unlike any real study, the World also knows every "
            "lifetime, including those it did not see, so we can check each method against the truth."
        ) as vo:
            self.add(cohort_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def naive(self):
        d = load("censor")
        grid = np.asarray(d["grid"], float)
        A = axes([0, 15], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"years of follow-up", ylabel=r"share still alive",
                 xticks=[0, 5, 10, 15], yticks=[0, 0.25, 0.5, 0.75, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        cs = {k: polyline(ax, grid, np.asarray(d[k], float), c, 3) for k, c in
              (("truth", TRUEC), ("as_dead", MISSC), ("drop", AREAC), ("as_alive", GREY_B), ("km", SURVC))}
        a = d["at10"]
        side = fit_rows(VGroup(
            label(rf"gold: \ the truth \ (at 10 years: \ {a['truth']:.3f})", font_size=22, color=TRUEC),
            label(rf"censored counted as deaths: \ {a['as_dead']:.3f}", font_size=22, color=MISSC),
            label(rf"censored dropped: \ {a['drop']:.3f}", font_size=22, color=AREAC),
            label(rf"censored as alive to the end: \ {a['as_alive']:.3f}", font_size=22, color=GREY_B),
            label(rf"Kaplan--Meier: \ {a['km']:.3f}", font_size=22, color=SURVC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What share of the cohort survives ten years? The truth, in gold, is " + say(a["truth"], 3)
            + ". <bookmark mark='b'/> Counting the censored as deaths gives " + say(a["as_dead"], 2) + ", far too low. "
            "<bookmark mark='c'/> Dropping them, and using only people whose fate is known, is worse: " + say(a["drop"], 2)
            + ", because the dropped are mostly survivors. <bookmark mark='d'/> Counting them as alive to the end gives "
            + say(a["as_alive"], 2) + ", too high. <bookmark mark='e'/> The Kaplan-Meier curve, in blue, closely follows the truth: " + say(a["km"], 3) + ". This agreement is empirical, under the simulator’s independent dropout; Kaplan-Meier is not exact in "
            "one finite sample."
        ) as vo:
            self.add(cohort_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(cs["truth"]), FadeIn(side[0]))
            for k, (m_, key) in enumerate(zip("bcde", ("as_dead", "drop", "as_alive", "km"))):
                vo.wait_until(m_)
                self.play(Create(cs[key]), FadeIn(side[k + 1]))
        self.clear_scene()

    def truncation(self):
        rows = [
            cmath(r"\text{entry at age } a_i", r":", r"\text{only those alive at } a_i \text{ are ever seen}", font_size=30),
            cmath(r"\text{risk set at age } u", r":", r"R(u) = \{i: a_i < u \le x_i\}", font_size=32),
            cmath(r"\text{ignore it}", r":", r"\text{count everyone as at risk from 40: \ immortal years}", font_size=30),
            cmath(r"\text{the age scale}", r":", r"\text{the natural clock for a cohort \ (Korn et al.\ 1997)}", font_size=30),
        ]
        rows[1][-1].set_color(SURVC)
        whys = [why(r"delayed entry"), why(r"enter late, \ leave at the event"), why(r"survival overstated"),
                why(r"age, \ not time on study")]
        with self.voiceover(
            "<bookmark mark='a'/> Truncation appears as soon as we measure time by age. Someone enrolled at "
            "sixty-five is seen only because they survived to sixty-five. <bookmark mark='b'/> So the risk set at "
            "each age must contain only those who have entered and not yet left: delayed entry. <bookmark mark='c'/> "
            "Ignoring it treats everyone as at risk from forty, crediting them with years in which they could not "
            "have died in our data. <bookmark mark='d'/> Age can be a useful clock. Estimating survival from forty "
            "additionally requires entry to be independent of lifetime, possibly after appropriate adjustment."
        ) as vo:
            heading = label('Delayed-entry risk sets exclude the years before recruitment', font_size=36).move_to([0,3.3,0])
            if heading.width > 12.5: heading.width = 12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def entry_plot(self):
        d = load("censor")
        ag = np.asarray(d["ages"], float)
        A = axes([40, 95], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"age", ylabel=r"survival from 40",
                 xticks=[40, 50, 60, 70, 80, 90], yticks=[0, 0.5, 1], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 center=[-2.5, 0.2, 0])
        ax = A.ax
        ct = polyline(ax, ag, np.asarray(d["age_truth"], float), TRUEC, 3)
        cn = polyline(ax, ag, np.asarray(d["age_naive"], float), MISSC, 3)
        ce = polyline(ax, ag, np.asarray(d["age_entry"], float), SURVC, 3)
        m = d["age_med"]
        side = fit_rows(VGroup(
            label(rf"gold: \ the truth \ (median {m['truth']:.0f})", font_size=22, color=TRUEC),
            label(rf"entry ignored: \ median {m['naive']:.0f}", font_size=22, color=MISSC),
            label(rf"delayed entry: \ median {m['entry']:.0f}", font_size=22, color=SURVC),
            label(r"separate age-40 simulation; independent scheduled entry", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A separate seeded demonstration generates lifetimes from forty and independent "
            "scheduled entry ages from forty to eighty. Only people alive at entry are observed, followed for at most"
            " fifteen years. The true survival from forty, in gold, has a median of "
            + str(round(m["truth"])) + ". <bookmark mark='b'/> Ignoring delayed entry gives a curve that is far too "
            "optimistic, with a median of " + str(round(m["naive"])) + ". <bookmark mark='c'/> Starting each person’s risk at entry closely follows the reference curve here. "
            "Frailty is generated at forty and survivor selection is retained; this is not the original World cohort,"
            " whose frailty is reset at recruitment."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), Create(ct), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cn), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ce), FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()
