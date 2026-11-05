from __future__ import annotations

import numpy as np
from scipy import special, stats

from videos.stats.stats24.common import *  # noqa: F403

GINV = {"logit": special.expit, "probit": stats.norm.cdf, "cloglog": lambda e: -np.expm1(-np.exp(e))}
LCOL = {"logit": LOGIT, "probit": PROBIT, "cloglog": CLOGLOG}


def beetle_panel(d, center=(-1.6, 0.2, 0)):
    return DoseResponse(d["x"], d["n"], d["k"], (1.65, 1.92), xlabel=r"$\log_{10}$ dose of carbon disulphide, \ mg/l",
                        xticks=[1.7, 1.75, 1.8, 1.85, 1.9], center=list(center))


class Hook(VoiceoverScene):
    def construct(self):
        self.bliss()
        self.data()
        self.probits()
        self.curves()
        self.ld50()
        self.objectives()

    def bliss(self):
        tl = timeline(lit=(1935,)).to_edge(UP, buff=0.35)
        hc = history_card(1935, r"Chester Bliss, \ \emph{Annals of Applied Biology}",
                          r"``The calculation of the dosage-mortality curve'': \ flour beetles exposed for five hours to "
                          r"carbon disulphide gas at eight concentrations. \ How lethal is each dose, \ and what dose kills "
                          r"half the beetles? \ His answer, \ the probit, \ was the first generalized linear model in all but name",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"each beetle: \ dead or alive, \ a yes-or-no outcome", font_size=24),
            label(r"a straight line cannot be a probability", font_size=24, color=RES),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1935 the entomologist Chester Bliss published a paper on the calculation of the "
            "dosage-mortality curve. He had exposed flour beetles for five hours to carbon disulphide gas at eight "
            "concentrations and counted the dead. How lethal is each dose, and what dose kills half the beetles? "
            "<bookmark mark='b'/> Each beetle's outcome is yes or no, <bookmark mark='c'/> and a straight line through such "
            "data would predict probabilities below zero and above one."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def data(self):
        d = load("bliss")
        P = beetle_panel(d)
        hdr = [r"$\log_{10}$ dose", r"exposed", r"killed"]
        body = [[f"{a:.4f}", f"{b:.0f}", f"{c:.0f}"] for a, b, c in zip(d["x"], d["n"], d["k"])]
        t = table_rows([hdr] + body, font_size=20, col_buff=0.4, row_buff=0.12, colors=[GREY_A] + [None] * 8)
        t.move_to([5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are Bliss's data as they appear in Annette Dobson's textbook: eight doses, about sixty "
            "beetles at each, four hundred and eighty-one in all. <bookmark mark='b'/> At the lowest dose six of fifty-nine "
            "died; at the highest, all sixty. <bookmark mark='c'/> Each dot is a proportion killed, with a bar for its "
            "binomial uncertainty. The proportions climb in an S."
        ) as vo:
            self.add(bliss_tag())
            vo.wait_until("a")
            self.play(FadeIn(P.A), LaggedStart(*[FadeIn(r) for r in t], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(VGroup(t[1], t[8]), color=PATH))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(b) for b in P.bars], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(x, scale=0.5) for x in P.dots], lag_ratio=0.1))
        self.clear_scene()

    def probits(self):
        rows = [
            cmath(r"P(\text{dead} \mid x)", r"=", r"\Phi(\alpha + \beta x)", font_size=30),
            cmath(r"\text{probit}", r"=", r"\Phi^{-1}(p) + 5", font_size=30),
            cmath(r"\text{Bliss's method}", r":", r"\text{straight lines through probits, \ refitted with weights}", font_size=28),
            cmath(r"\text{Fisher's appendix}", r":", r"\text{the iterations converge to the maximum likelihood}", font_size=28),
        ]
        rows[0][2].set_color(PROBIT)
        whys = [why(r"a tolerance distribution: \ each beetle dies above its own threshold"), why(r"the $+5$ avoided negative numbers by hand"),
                why(r"working probits and weights, \ by hand"), why(r"IRLS, \ 37 years early: \ chapter three")]
        with self.voiceover(
            "<bookmark mark='a'/> Bliss's idea: each beetle has its own tolerance, normally distributed on the log-dose scale, "
            "and dies if the dose exceeds it. Then the death rate is the normal distribution function of a straight line in "
            "the log dose. <bookmark mark='b'/> He called the normal deviate plus five a probit, the five keeping hand "
            "calculations free of minus signs. <bookmark mark='c'/> He fitted straight lines through the probits, weighted "
            "them, recalculated, and fitted again. <bookmark mark='d'/> In an appendix to the paper, Ronald Fisher showed "
            "that the procedure converges to the maximum likelihood estimate. It was iteratively reweighted least squares, "
            "thirty-seven years before it had that name."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curves(self):
        d = load("bliss")
        P = beetle_panel(d)
        cs = {l: P.curve(GINV[l], d["fits"][l]["coef"], LCOL[l]) for l in ("logit", "probit", "cloglog")}
        f = d["fits"]
        rows = fit_rows(VGroup(
            label(r"three links, \ three S-shapes", font_size=22),
            label(rf"blue: \ logit, \ deviance {f['logit']['deviance']:.2f}", font_size=22, color=LOGIT),
            label(rf"teal: \ probit, \ deviance {f['probit']['deviance']:.2f}", font_size=22, color=PROBIT),
            label(rf"gold: \ cloglog, \ deviance {f['cloglog']['deviance']:.2f}", font_size=22, color=CLOGLOG),
            label(r"6 degrees of freedom: \ cloglog fits best", font_size=22, color=HIT),
        ), 3.45, 0.42, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit three S-shaped curves by maximum likelihood. <bookmark mark='b'/> The logistic, "
            "Part 14's model, has deviance eleven point two three. <bookmark mark='c'/> Bliss's probit is barely different, "
            "ten point one two. <bookmark mark='d'/> The complementary log-log, which is not symmetric, rising slowly and then "
            "steeply, has deviance three point four five. <bookmark mark='e'/> With six residual degrees of freedom, the "
            "symmetric curves are marginal and the asymmetric one fits well: the beetles at the top die faster than a "
            "symmetric curve allows. Chapter four makes the deviance precise."
        ) as vo:
            self.add(bliss_tag())
            self.play(FadeIn(P))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k, (m_, l) in enumerate(zip("bcd", ("logit", "probit", "cloglog"))):
                vo.wait_until(m_)
                self.play(Create(cs[l]), FadeIn(rows[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def ld50(self):
        d = load("bliss")
        P = beetle_panel(d)
        f = d["fits"]["cloglog"]
        cv = P.curve(GINV["cloglog"], f["coef"], CLOGLOG)
        L = f["ld50"]
        mk = P.mark(L["x"], 0.5)
        lg = d["fits"]["logit"]["ld50"]
        rows = fit_rows(VGroup(
            label(r"LD50: \ the dose that kills half", font_size=22, color=PATH),
            label(rf"cloglog: \ {L['x']:.4f}, \ i.e. {10 ** L['x']:.1f} mg/l", font_size=22, color=CLOGLOG),
            label(rf"Fieller 95\%: \ [{L['fieller'][0]:.4f}, {L['fieller'][1]:.4f}]", font_size=22),
            label(rf"logit: \ {lg['x']:.4f}: \ the link moves it", font_size=22, color=LOGIT),
            label(r"a ratio of coefficients: \ Part 11's Fieller", font_size=22, color=GREY_A),
        ), 3.45, 0.42, [5.1, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The quantity of interest is the dose that kills half, the LD fifty. <bookmark mark='b'/> "
            "Under the complementary log-log fit it is a log dose of one point seven seven nine, about sixty milligrams per "
            "litre. <bookmark mark='c'/> It's a ratio of coefficients, so Part 11's Fieller interval applies: one point "
            "seven seven oh to one point seven eight six. <bookmark mark='d'/> The logistic fit puts it at one point seven "
            "seven two, near the bottom of that interval: the choice of link moves the answer by about as much as the "
            "sampling error does. "
            "<bookmark mark='e'/> That's the question of this part: how to choose among models for outcomes that aren't "
            "normal, fit them all with one algorithm, and judge them."
        ) as vo:
            self.add(bliss_tag())
            self.play(FadeIn(P), Create(cv))
            vo.wait_until("a")
            self.play(Create(mk), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 24", font_size=34, color=GREY_B), label(r"Generalized Linear Models", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the exponential dispersion family; \ links and variance functions",
            r"IRLS derived; \ deviance, \ residuals and analysis of deviance",
            r"separation and Firth; \ quasi-likelihood and overdispersion",
            r"counts with too many zeros; \ log-linear, \ multinomial and ordinal models",
            r"GEE for clustered outcomes; \ proper scoring rules",
        ], color=MODEL, font_size=26)
        prereq = note(r"prerequisites: \ Parts 14, \ 21 and 22").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.glm} II; \ the dose--response panel").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-four: generalized linear models. <bookmark mark='b'/> We'll meet the "
            "exponential dispersion family that unifies them; derive iteratively reweighted least squares; read deviances "
            "and residuals; see what goes wrong under separation and how Firth fixes it; handle overdispersion with "
            "quasi-likelihood; model counts with too many zeros; fit log-linear, multinomial and ordinal models; extend "
            "the whole thing to clustered outcomes with generalized estimating equations; and finish with how to score a "
            "probability forecast."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
