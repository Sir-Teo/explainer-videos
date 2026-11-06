from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


def cig_axes(center=(-1.8, 0.2, 0), y=(30, 140)):
    return axes([1970, 2000], list(y), x_length=7.6, y_length=4.4, xlabel=r"year", ylabel=r"cigarette packs per person",
                xticks=[1970, 1980, 1990, 2000], yticks=[40, 80, 120], xfmt=lambda v: f"{v:.0f}", center=list(center))


class Synth(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.average()
        self.recipe()
        self.synthetic()
        self.gap()
        self.placebo()
        self.caveats()

    def card(self):
        card = chapter_card(11, r"Synthetic control", r"One treated state, \ and a weighted mix of the others",
                            lit=(2003, 2010), part=PART)
        with self.voiceover("Chapter eleven. The synthetic control."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def story(self):
        rows = fit_rows(VGroup(
            label(r"November 1988: \ California votes for Proposition 99", font_size=26, color=Y1C),
            label(r"25 cents more tax on every pack from January 1989, \ spent on anti-smoking campaigns", font_size=26),
            label(r"one treated state: \ which state, \ or which mix of states, \ is California without it?", font_size=26, color=TAUC),
            label(r"Abadie \& Gardeazabal (2003), \ the Basque Country; \ Abadie, \ Diamond \& Hainmueller (2010), \ Prop 99", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In November 1988, California's voters passed Proposition 99. <bookmark mark='b'/> From "
            "January 1989, every pack of cigarettes carried twenty-five cents more tax, and the money paid for anti-smoking "
            "campaigns and research. Did it reduce smoking? <bookmark mark='c'/> There is one treated state. "
            "Differences-in-differences needs a comparison group whose trend California would have followed; which state, "
            "or which mixture of states, is California without the law? <bookmark mark='d'/> Alberto Abadie and Javier "
            "Gardeazabal's answer, first used in 2003 for the economic cost of terrorism in the Basque Country, was to build "
            "one. Abadie, Alexis Diamond and Jens Hainmueller applied it to Proposition 99 in 2010."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def average(self):
        d = load("synth")
        yrs = np.asarray(d["years"], float)
        A = cig_axes()
        ax = A.ax
        cal = polyline(ax, yrs, d["cal"], Y1C, 3.5)
        avg = polyline(ax, yrs, d["avg_others"], Y0C, 3.5)
        start = DashedLine(ax.c2p(1988.5, 30), ax.c2p(1988.5, 140), color=GREY_B, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"red: \ California", font_size=22, color=Y1C),
            label(r"blue: \ the average of 38 states \ without large tobacco programmes", font_size=22, color=Y0C),
            label(r"California was already lower, \ and falling faster, \ before 1989", font_size=22, color=MISSC),
            label(r"a DiD against the average would credit the law with that trend", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Cigarette sales per person, 1970 to 2000. California in red. <bookmark mark='b'/> In blue, "
            "the average of the thirty-eight states that did not run large tobacco-control programmes in the period. "
            "<bookmark mark='c'/> California was already lower, and falling faster, long before 1989. <bookmark mark='d'/> A "
            "difference-in-differences against the average would credit the law with California's existing decline."
        ) as vo:
            self.add(prop99_tag())
            self.play(FadeIn(A), Create(start))
            vo.wait_until("a")
            self.play(Create(cal), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(side[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 2]))
        self.clear_scene()

    def recipe(self):
        rows = [
            cmath(r"\hat w", r"=", r"\arg\min_{w \ge 0,\ \sum w_j = 1} \textstyle\sum_{t < T_0} (Y_{1t} - \sum_j w_j Y_{jt})^2", font_size=30),
            cmath(r"\hat Y_{1t}(0)", r"=", r"\textstyle\sum_j \hat w_j Y_{jt}, \quad t \ge T_0", font_size=30),
            cmath(r"\hat\tau_t", r"=", r"Y_{1t} - \hat Y_{1t}(0)", font_size=30),
            cmath(r"\text{convex weights}", r":", r"\text{interpolate, \ never extrapolate}", font_size=30),
        ]
        rows[0][-1].set_color(BANDC)
        whys = [why(r"match the pre-period path"), why(r"the synthetic California"), why(r"the gap, \ year by year"),
                why(r"sparse, \ interpretable, \ transparent")]
        with self.voiceover(
            "<bookmark mark='a'/> The recipe: choose weights on the other states, non-negative and adding to one, so that the "
            "weighted average tracks California's sales as closely as possible before the law. <bookmark mark='b'/> After "
            "the law, the same weighted average is the synthetic California, the estimate of what California would have "
            "done without it. <bookmark mark='c'/> The effect in each year is the gap between the two. <bookmark mark='d'/> "
            "Because the weights are convex, the synthetic control interpolates among real states and never extrapolates "
            "beyond them, and usually only a few states get any weight, so anyone can inspect the comparison. Abadie's "
            "version also matches covariates; ours matches the sales path alone."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def synthetic(self):
        d = load("synth")
        yrs = np.asarray(d["years"], float)
        A = cig_axes()
        ax = A.ax
        cal = polyline(ax, yrs, d["cal"], Y1C, 3.5)
        syn = polyline(ax, yrs, d["synth"], BANDC, 3.5)
        start = DashedLine(ax.c2p(1988.5, 30), ax.c2p(1988.5, 140), color=GREY_B, stroke_width=1.5)
        w = d["weights"][:5]
        wrows = VGroup(label(r"the synthetic California:", font_size=22, color=BANDC),
                       *[label(rf"{n}: \ {v:.2f}", font_size=22, color=GREY_A) for n, v in w],
                       label(rf"pre-1989 RMSPE: \ {d['rmspe_pre']:.2f} packs", font_size=22, color=TAUC))
        side = fit_rows(wrows, 3.8, 0.3, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The weights that track California best: Utah " + say(w[0][1], 2) + ", Montana "
            + say(w[1][1], 2) + ", Nevada " + say(w[2][1], 2) + ", Connecticut " + say(w[3][1], 2) + ", New Hampshire a "
            "little. Abadie and his colleagues found a similar mix. <bookmark mark='b'/> Before 1989, the synthetic "
            "California follows the real one within about one and a half packs a year. <bookmark mark='c'/> After 1989, "
            "they part: real California's sales fall much faster than its synthetic twin's."
        ) as vo:
            self.add(prop99_tag())
            self.play(FadeIn(A), Create(start), Create(cal))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in side[:-1]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(syn), FadeIn(side[-1]))
        self.clear_scene()

    def gap(self):
        d = load("synth")
        yrs = np.asarray(d["years"], float)
        A = axes([1970, 2000], [-35, 15], x_length=7.6, y_length=4.4, xlabel=r"year", ylabel=r"California minus synthetic (packs)",
                 xticks=[1970, 1980, 1990, 2000], yticks=[-30, -20, -10, 0, 10], xfmt=lambda v: f"{v:.0f}", center=[-1.8, 0.2, 0])
        ax = A.ax
        gp = polyline(ax, yrs, d["gap"], Y1C, 3.5)
        zero = DashedLine(ax.c2p(1970, 0), ax.c2p(2000, 0), color=GREY_C, stroke_width=1.5)
        start = DashedLine(ax.c2p(1988.5, -35), ax.c2p(1988.5, 15), color=GREY_B, stroke_width=1.5)
        side = fit_rows(VGroup(
            label(r"the gap: \ the estimated effect, \ year by year", font_size=22),
            label(r"near zero before 1989, \ by construction", font_size=22, color=GREY_A),
            label(rf"2000: \ {d['gap2000']:.1f} packs per person", font_size=22, color=Y1C),
            label(rf"average 1989--2000: \ {d['gap_post_mean']:.1f}", font_size=22, color=TAUC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The gap between them is the estimated effect, year by year. <bookmark mark='b'/> Before "
            "1989 it hovers near zero, as the weights were chosen to make it. <bookmark mark='c'/> After the law it opens "
            "steadily, reaching " + say(-d["gap2000"], 1) + " fewer packs per person by 2000, nearly two fifths of the sales "
            "California would have had. <bookmark mark='d'/> Averaged over the twelve years, " + say(-d["gap_post_mean"], 1)
            + " packs per person per year."
        ) as vo:
            self.add(prop99_tag())
            self.play(FadeIn(A), Create(zero), Create(start))
            vo.wait_until("a")
            self.play(Create(gp), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def placebo(self):
        d = load("synth")
        yrs = np.asarray(d["years"], float)
        A = axes([1970, 2000], [-40, 40], x_length=7.6, y_length=4.4, xlabel=r"year", ylabel=r"gap (packs)",
                 xticks=[1970, 1980, 1990, 2000], yticks=[-40, -20, 0, 20, 40], xfmt=lambda v: f"{v:.0f}", center=[-1.8, 0.2, 0])
        ax = A.ax
        others = VGroup(*[clip_curve(ax, yrs, np.clip(p["gap"], -40, 40), GREY_D, 1.5) for p in d["placebo"] if p["state"] != "California"])
        cal = polyline(ax, yrs, d["gap"], Y1C, 4)
        side = fit_rows(VGroup(
            label(r"placebos: \ pretend each other state passed the law", font_size=22),
            label(rf"post/pre RMSPE ratio: \ California ranks {d['rank']} of {d['n_states']} \ ($p$ = {d['p']:.3f})", font_size=22, color=Y1C),
            label(r"among the 29 states fitted nearly as well before 1989: \ first \ ($p$ = 1/29)", font_size=22, color=BANDC),
            label(r"inference by permutation, \ not by a standard error", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> With one treated state, there is no standard error in the usual sense. Abadie's answer is "
            "a placebo test: pretend, in turn, that each of the other thirty-eight states had passed the law in 1989, build "
            "its synthetic control, and look at its gap. <bookmark mark='b'/> Ranked by how much the fit worsens after 1989 "
            "relative to before, California comes " + ["first", "second", "third", "fourth"][d["rank"] - 1] + " of "
            + str(d["n_states"]) + ", a p-value of " + say(d["p"], 2) + ". Missouri and Virginia, whose synthetic controls "
            "fitted almost perfectly before 1989, edge ahead of it. <bookmark mark='c'/> Keeping only the twenty-nine states, "
            "California included, whose pre-1989 paths could be matched about as well as California's, its gap is the largest "
            "of all. <bookmark mark='d'/> Inference comes from the "
            "permutation, Part sixteen's idea, applied to places."
        ) as vo:
            self.add(prop99_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(o) for o in others], lag_ratio=0.03), FadeIn(side[0]))
            self.play(Create(cal))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def caveats(self):
        rows = fit_rows(VGroup(
            label(r"needs a long pre-period: \ a good fit over a few years can be luck", font_size=26, color=TAUC),
            label(r"needs the treated unit inside the donors' range: \ no extrapolation", font_size=26, color=MISSC),
            label(r"assumes no spillovers: \ smokers buying in Nevada would bias it", font_size=26, color=MISSC),
            label(r"and still an assumption: \ that the mix tracking before would have tracked after", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The method's assumptions. It needs a long pre-period: a close fit over a few years can be "
            "luck, while one over nineteen years, through booms and recessions, is harder to fake. <bookmark mark='b'/> It "
            "needs the treated unit to lie within the range of the donors; a state more extreme than all others cannot be "
            "synthesized. <bookmark mark='c'/> It assumes the law did not spill over: if Californians drove to Nevada for "
            "cigarettes, Nevada's sales, and the synthetic California, would rise. <bookmark mark='d'/> And it still assumes "
            "that a mixture that tracked California before would have kept tracking it, without the law."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
