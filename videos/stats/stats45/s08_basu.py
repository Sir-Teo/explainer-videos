from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class Ancillarity(VoiceoverScene):
    def construct(self):
        self.card()
        self.basu()
        self.scatter()
        self.cox()
        self.uniform()
        self.principle()
        self.board()

    def card(self):
        card = chapter_card(7, r"Ancillarity and Basu", r"Statistics that say nothing about $\theta$, \ yet matter", lit=(1955, 1958), part=PART)
        with self.voiceover("Chapter seven. Ancillarity and Basu's theorem: statistics that say nothing about theta, yet matter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def basu(self):
        rows = [
            cmath(r"V \text{ ancillary}", r":", r"\text{its law is the same for every } \theta", font_size=34),
            cmath(r"T \text{ complete sufficient}", r":", r"\phi(T) = P(V \in B \mid T) - P(V \in B) \ \text{is free of } \theta", font_size=30),
            cmath(r"E_\theta\, \phi(T) = 0 \ \forall\theta", r"\Rightarrow", r"\phi = 0: \ P(V \in B \mid T) = P(V \in B)", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"T \perp V \ \text{for every } \theta", font_size=36),
        ]
        rows[3][-1].set_color(ADMC)
        whys = [why(r"Fisher's term"), why(r"sufficiency makes it a statistic"), why(r"completeness"), why(r"Basu (1955)")]
        with self.voiceover(
            "<bookmark mark='a'/> A statistic is ancillary if its distribution does not depend on the parameter at all, "
            "like the uniform range of chapter five. <bookmark mark='b'/> Debabrata Basu proved in 1955 that such a "
            "statistic is independent of any complete sufficient statistic. Take the conditional probability of an event "
            "for V given T, minus its unconditional probability; sufficiency makes this a function of T alone, and "
            "ancillarity makes the second term a constant. <bookmark mark='c'/> Its mean is zero for every theta, so "
            "completeness forces it to be zero: <bookmark mark='d'/> the conditional law of V given T equals its "
            "unconditional law. T and V are independent, at every theta."
        ) as vo:
            heading=label('Complete sufficiency is independent of an ancillary statistic',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scatter(self):
        d = load("basu")
        A = axes([-1.2, 1.2], [0, 3.2], x_length=7.4, y_length=4.4, xlabel=r"$\bar x$", ylabel=r"$s^2$",
                 xticks=[-1, 0, 1], yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        xb, s2 = np.asarray(d["xbar"]), np.asarray(d["s2"])
        keep = s2 < 3.2
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=MLEC, fill_opacity=0.6) for a, b in zip(xb[keep], s2[keep])])
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$ normal observations, \ $\sigma$ known", font_size=22),
            label(r"$\bar x$: \ complete sufficient for $\mu$", font_size=22, color=MLEC),
            label(r"$s^2$: \ its law does not involve $\mu$: \ ancillary", font_size=22, color=MMC),
            label(rf"independent by Basu; 4,000-run correlation ${d['r']:.2f}$", font_size=22, color=ADMC),
            label(rf"exponential data: \ correlation {d['r_exp']:.2f}", font_size=22, color=INADC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The classic application. Take {d['n']} normal observations and, for the moment, treat sigma as known. <bookmark mark='b'/> Then the sample mean is complete and sufficient for the mean. <bookmark mark='c'/> The sample variance is computed from deviations about the mean, so shifting mu leaves its distribution unchanged: it is ancillary. <bookmark mark='d'/> Basu's theorem says they are independent for every mu, and since sigma was arbitrary, for every sigma too. Eight hundred pairs are displayed; the reported correlation uses all four thousand simulated samples: {say(d['r'], 2)}. That is the independence of x-bar and s squared behind Student's t, in three lines. <bookmark mark='e'/> It is special to the normal: for exponential data the two are strongly correlated."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 800 samples")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.002), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cox(self):
        d = load("basu")["cox"]
        rows = [
            cmath(r"\text{a fair coin picks an instrument}", r":", r"\text{SD } 1 \text{ or SD } 10; \ \text{we see which}", font_size=32),
            cmath(r"x \pm c, \ \ c = " + f"{d['c']:.2f}", r":", r"\text{covers } 90\% \text{ on average}", font_size=32),
            cmath(r"\text{given the instrument}", r":", rf"{100 * d['cover_precise']:.2f}\% \ \text{{(precise)}}, \ \ {100 * d['cover_rough']:.1f}\% \ \text{{(rough)}}", font_size=32),
            cmath(r"\text{conditional interval}", r":", rf"x \pm {d['half_precise']:.2f} \ \text{{or}} \ x \pm {d['half_rough']:.1f}: \ 90\% \text{{ each}}", font_size=30),
        ]
        rows[2][-1].set_color(INADC)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"the instrument is ancillary"), why(r"the unconditional answer"), why(r"conditional coverage differs from nominal"), why(r"Cox (1958)")]
        with self.voiceover(
            f"<bookmark mark='a'/> But ancillary statistics can matter enormously, as David Cox showed in 1958. A fair coin decides whether a quantity is measured with a precise instrument, standard deviation one, or a rough one, standard deviation ten, and we know which was used. Which instrument is ancillary: its probability does not depend on the quantity. <bookmark mark='b'/> An interval of plus or minus {say(d['c'], 1)} covers the truth ninety percent of the time over repetitions of the whole experiment. <bookmark mark='c'/> But given the instrument, it covers essentially always with the precise one, and only eighty percent of the time with the rough one. Its conditional coverage misses the nominal ninety percent for each instrument, although its unconditional coverage is valid. <bookmark mark='d'/> The sensible interval conditions on the instrument: plus or minus {say(d['half_precise'], 2)}, or plus or minus {say(d['half_rough'], 1)}, each covering ninety percent of the time."
        ) as vo:
            heading=label('Marginal coverage can conceal conditional miscalibration',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uniform(self):
        d = load("basu")
        mids = (np.asarray(d["bins"][:-1]) + np.asarray(d["bins"][1:])) / 2
        A = axes([0, 1], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"the range $R = \max - \min$", ylabel=r"coverage given $R$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 0.9, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ok = np.asarray(d["share"]) > 0.005
        unc = VGroup(polyline(ax, mids[ok], np.asarray(d["cover_unc"])[ok], INADC, 4),
                     *[Dot(ax.c2p(a, b), radius=0.07, color=INADC) for a, b in zip(mids[ok], np.asarray(d["cover_unc"])[ok])])
        con = VGroup(polyline(ax, mids[ok], np.asarray(d["cover_cond"])[ok], ADMC, 4),
                     *[Dot(ax.c2p(a, b), radius=0.07, color=ADMC) for a, b in zip(mids[ok], np.asarray(d["cover_cond"])[ok])])
        nom = DashedLine(ax.c2p(0, 0.9), ax.c2p(1, 0.9), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"$n = {d['m']}$ from $U(\theta - \tfrac12, \theta + \tfrac12)$", font_size=22),
            label(rf"red: \ midrange $\pm {d['c_unc']:.3f}$, \ 90\% overall", font_size=22, color=INADC),
            label(r"given a small range: \ 42\%; \ a large one: \ 100\%", font_size=22, color=INADC),
            label(r"given $R$: midrange error uniform on $[-(1-R)/2,(1-R)/2]$", font_size=22, color=ADMC),
            label(r"its central 90\%: \ 90\% at every $R$", font_size=22, color=ADMC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same thing happens without any coin. Take {d['m']} observations uniform on theta minus a half to theta plus a half, and estimate theta by the midrange. <bookmark mark='b'/> The interval midrange plus or minus {say(d['c_unc'], 3)} covers ninety percent of the time overall. <bookmark mark='c'/> But sort the samples by their range, which is ancillary. When the range is small, the sample says little, and the interval covers less than half the time; when it is large, the data pin theta down and the interval always covers. <bookmark mark='d'/> Conditioning on the range, theta must lie between the maximum minus a half and the minimum plus a half, The frequentist parameter is fixed. Conditional on the range R, the midrange error is uniform between minus and plus one minus R over two. Equivalently, a flat-prior posterior is uniform on the observed compatible interval; that is a separate Bayesian interpretation. <bookmark mark='e'/> The central ninety percent of that interval covers ninety percent of the time at every range: honest for the sample at hand."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(exact_tag(r"simulated: 200,000 samples")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(unc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(con), FadeIn(side[4]))
        self.clear_scene()

    def principle(self):
        rows = fit_rows(VGroup(
            label(r"the conditionality principle \ (Cox 1958): \ condition on ancillaries", font_size=28, color=ADMC),
            label(r"Birnbaum (1962): \ conditionality + sufficiency \ $\Rightarrow$ \ the likelihood principle", font_size=26, color=BAYESC),
            label(r"which most frequentist methods violate \ (Part 22's stopping rules)", font_size=26, color=INADC),
            label(r"observed information can approximate conditional precision; it need not be ancillary", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Cox's conclusion became the conditionality principle: inference should be "
            "conditional on ancillary features of the experiment that was actually performed. <bookmark mark='b'/> In"
            " 1962 Allan Birnbaum derived the likelihood principle from particular formulations of sufficiency and "
            "mixture conditionality. The exact formulation of conditionality matters; <bookmark mark='c'/> which much"
            " of frequentist practice violates, as Part twenty-two's stopping-rule example showed; the argument is "
            "still debated. <bookmark mark='d'/> A useful practical lesson is to report the precision of the "
            "experiment you ran, Efron and Hinkley studied observed information as an approximation to conditional "
            "precision in regular models. Observed information is not generally ancillary or uniformly preferable to "
            "expected information."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def board(self):
        rows = board_rows("instrument", "uniform location")
        show_board(self, rows,
                   "<bookmark mark='a'/> On the Coverage Board. Cox's unconditional interval, given the precise instrument: "
            "rounding to one hundred percent in this simulation, conservative. <bookmark mark='b'/> Given the rough "
            "one: eighty percent, broken. <bookmark mark='c'/> The conditional intervals, and the uniform location "
            "interval given its range: ninety percent, kept.",
                   [("a", [0]), ("b", [1]), ("c", [2, 3])])
