from __future__ import annotations

import numpy as np

from explainer.stats.kit import bootstrap as Bt
from videos.stats.stats16.common import *  # noqa: F403


class Jackknife(VoiceoverScene):
    def construct(self):
        self.card()
        self.leave_out()
        self.formulas()
        self.variance_check()
        self.influence()
        self.median_fail()

    def card(self):
        card = chapter_card(6, r"The jackknife", r"Leave one out, \ and watch what moves", part=PART)
        with self.voiceover("Chapter six. The jackknife."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def leave_out(self):
        d = load("law")
        L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
        loo = np.asarray(d["jack"]["loo"])
        A = axes([530, 680], [2.6, 3.6], x_length=6.0, y_length=4.0, xlabel=r"LSAT", ylabel=r"GPA", xticks=[550, 600, 650],
                 yticks=[2.8, 3.2, 3.6], center=[-3.3, 0.6, 0])
        ax = A.ax
        dots = scatter(ax, L, G, radius=0.08)
        B = axes([0.7, 0.9], [0, 1], x_length=5.0, y_length=0.6, xlabel=r"$r_{(i)}$: \ $r$ without school $i$",
                 xticks=[0.7, 0.75, 0.8, 0.85, 0.9], center=[3.6, -1.0, 0], font_size=18)
        bx = B.ax
        full = Line(bx.c2p(d["r"], 0), bx.c2p(d["r"], 1.6), color=OBS, stroke_width=3)
        fl = MathTex(rf"r = {d['r']:.3f}", font_size=24, color=OBS).next_to(full, UP, buff=0.1)
        rd = MathTex(r"r_{(i)} = ", font_size=34).move_to([2.8, 1.8, 0])
        val = DecimalNumber(d["r"], num_decimal_places=3, font_size=34, color=BOOT).next_to(rd, RIGHT, buff=0.15)
        marks = VGroup()
        hist = historical_tag(r"Quenouille (1949, \ 1956); \ Tukey (1958)", corner=DR)
        with self.voiceover(
            "Before the bootstrap there was the jackknife. <bookmark mark='a'/> Maurice Quenouille, in 1949, proposed it to "
            "reduce bias; John Tukey, in 1958, saw it could estimate a standard error, and gave it its name, for a rough "
            "all-purpose tool you keep in your pocket. <bookmark mark='b'/> The recipe: leave out one school, recompute the "
            "correlation from the other fourteen, put the school back, and leave out the next. Fifteen recomputations, "
            "fifteen values. <bookmark mark='c'/> They scatter around point seven seven six. How much they move tells us how "
            "sensitive the correlation is to the data."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), FadeIn(hist))
            vo.wait_until("a")
            self.play(FadeIn(B), Create(full), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(rd), FadeIn(val))
            for i in range(15):
                rt = 0.5 if i < 3 else 0.22
                self.play(dots[i].animate.set_opacity(0.12), val.animate.set_value(loo[i]), run_time=rt)
                m = Dot(bx.c2p(loo[i], 0.3), radius=0.07, color=BOOT)
                marks.add(m)
                self.play(FadeIn(m, scale=1.6), dots[i].animate.set_opacity(1), run_time=rt)
            vo.wait_until("c")
            self.play(Indicate(marks, color=BOOT))
        self.clear_scene()

    def formulas(self):
        d = load("law")
        j = d["jack"]
        rows = [
            cmath(r"\bar r_{(\cdot)}", r"=", r"\tfrac1n \textstyle\sum_i r_{(i)}", font_size=32),
            cmath(r"\widehat{\text{bias}}", r"=", rf"(n-1)\big(\bar r_{{(\cdot)}} - r\big) = {j['bias']:.4f}", font_size=32),
            cmath(r"\widehat{\mathrm{SE}}_{\text{jack}}", r"=", r"\sqrt{\tfrac{n-1}{n} \textstyle\sum_i \big(r_{(i)} - \bar r_{(\cdot)}\big)^2}", font_size=32),
            cmath(r"\ ", r"=", rf"{j['se']:.3f}\quad (\text{{formula}}\ {d['se_normal']:.3f})", font_size=32),
        ]
        rows[3][2].set_color(BOOT)
        whys = [why(r"the average of the leave-one-out values"), why(r"Quenouille: \ removes the $1/n$ term of the bias"),
                why(r"the $n - 1$: \ the $r_{(i)}$ share 13 of 14 schools"), why(r"no model; \ larger than the normal formula")]
        with self.voiceover(
            "<bookmark mark='a'/> Average the leave-one-out values. <bookmark mark='b'/> Quenouille's bias estimate is n minus "
            "one times the difference between that average and the full-sample correlation: minus point oh oh six five, tiny "
            "here. It removes the part of an estimator's bias that shrinks like one over n. <bookmark mark='c'/> Tukey's standard "
            "error looks like an ordinary standard deviation of the fifteen values, but multiplied by n minus one. That's "
            "because the leave-one-out values are far too alike: any two share thirteen of their fourteen schools, so their "
            "spread must be scaled up. <bookmark mark='d'/> The result is point one four three, with no model at all: larger "
            "than the normal-theory formula's point one one five, and close to the bootstrap's point one three five."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def variance_check(self):
        L = np.asarray(museum.LAW_LSAT, float)
        jv = Bt.jackknife(L, lambda v: v.var())
        rows = [
            cmath(r"\hat\sigma^2", r"=", rf"\tfrac1n \textstyle\sum (x_i - \bar x)^2 = {L.var():.1f}", font_size=32),
            cmath(r"\text{bias}", r"=", r"-\sigma^2/n\ \ \text{(exactly order } 1/n)", font_size=32),
            cmath(r"\hat\sigma^2 - \widehat{\text{bias}}", r"=", rf"{L.var():.1f} + {-jv['bias']:.1f} = {L.var() - jv['bias']:.1f}", font_size=32),
            cmath(r"\ ", r"=", rf"s^2 = \tfrac{{1}}{{n-1}} \textstyle\sum (x_i - \bar x)^2 = {L.var(ddof=1):.1f}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the LSAT scores: \ dividing by $n$"), why(r"Part 9"), why(r"the jackknife's correction"),
                why(r"exactly the unbiased variance")]
        with self.voiceover(
            "A check that the bias correction does what it claims. <bookmark mark='a'/> Take the plug-in variance of the fifteen "
            "LSAT scores, dividing by n. <bookmark mark='b'/> Part 9 showed its bias is exactly minus sigma squared over n, "
            "a pure one-over-n term. <bookmark mark='c'/> Subtract the jackknife's estimate of the bias: <bookmark mark='d'/> "
            "the result is exactly s squared, the variance with n minus one. The jackknife rediscovers Bessel's correction by "
            "itself, from the data, with no algebra."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def influence(self):
        d = load("law")
        L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
        loo = np.asarray(d["jack"]["loo"])
        infl = (len(L) - 1) * (d["r"] - loo)
        A = axes([530, 680], [2.6, 3.6], x_length=6.4, y_length=4.4, xlabel=r"LSAT", ylabel=r"GPA", xticks=[550, 600, 650],
                 yticks=[2.8, 3.2, 3.6], center=[-3.0, 0.2, 0])
        ax = A.ax
        sz = np.abs(infl) / np.abs(infl).max()
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06 + 0.16 * s, color=RES if v < 0 else S.CTRL, fill_opacity=0.8)
                        for a, b, s, v in zip(L, G, sz, infl)])
        i0 = int(np.argmax(np.abs(infl)))
        rows = fit_rows(VGroup(
            MathTex(r"(n-1)\big(r - r_{(i)}\big)", font_size=30),
            label(r"each school's pull on $r$: \ a finite-sample influence", font_size=22),
            label(r"red: \ lowers $r$; \ blue: \ raises it", font_size=22, color=GREY_A),
            MathTex(rf"\text{{without school }}{i0 + 1}:\ r = {loo[i0]:.3f}", font_size=28, color=RES),
            label(r"Part 12's influence probe, \ for any statistic", font_size=22, color=BOOT),
        ), 4.8, 0.38, [4.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The jackknife has a second use. Scale each school's change by n minus one, and you have a "
            "measure of how hard that school pulls on the estimate: a finite-sample version of what Part 30 will call the "
            "influence function. <bookmark mark='b'/> Draw each school with its size proportional to its pull. "
            "<bookmark mark='c'/> Red schools lower the correlation, blue ones raise it. <bookmark mark='d'/> One school dominates: "
            "LSAT five seven six, GPA three point three nine, far above the trend. Without it the correlation is point eight nine "
            "three. <bookmark mark='e'/> It's Part 12's influence probe, extended to any statistic: not only regression "
            "coefficients but correlations, ratios, medians."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(d_) for d_ in dots], lag_ratio=0.06))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Circumscribe(dots[i0], color=RES, shape=Circle), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def median_fail(self):
        L = np.asarray(museum.LAW_LSAT, float)
        j = Bt.jackknife(L, np.median)
        loo = np.asarray(j["loo"])
        g = np.random.Generator(np.random.PCG64(7))
        bse = float(np.std(Bt.bootstrap(L, np.median, 2000, g), ddof=1))
        A = axes([570, 595], [0, 9], x_length=7.0, y_length=3.0, xlabel=r"leave-one-out medians of the 15 LSATs",
                 ylabel=r"count", xticks=[575, 580, 585, 590], yticks=[0, 4, 8], center=[-2.2, 0.6, 0])
        ax = A.ax
        vals, cnt = np.unique(loo, return_counts=True)
        bars = bars_at(ax, vals, cnt, 0.9, BOOT)
        rows = fit_rows(VGroup(
            label(rf"15 leave-one-outs, \ only {len(vals)} distinct values", font_size=22),
            MathTex(rf"\widehat{{\mathrm{{SE}}}}_{{\text{{jack}}}} = {j['se']:.1f}", font_size=28, color=BOOT),
            MathTex(rf"\widehat{{\mathrm{{SE}}}}_{{\text{{boot}}}} = {bse:.1f}", font_size=28),
            label(r"the median isn't smooth: \ removing one point barely moves it, \ or jumps it", font_size=20, color=RES),
            label(r"Efron (1982): \ the jackknife SE of a median doesn't even converge", font_size=20, color=RES),
        ), 4.6, 0.36, [4.4, 0.4, 0])
        with self.voiceover(
            "But the jackknife has a blind spot. <bookmark mark='a'/> Leave one LSAT out at a time and take the median of the "
            "other fourteen: there are only three distinct answers. The median of fourteen is the average of the middle two, "
            "and leaving out one point can only shift which two those are. <bookmark mark='b'/> The jackknife standard error "
            "is fourteen point seven; <bookmark mark='c'/> the bootstrap, which we're about to build, gives eighteen point four. "
            "<bookmark mark='d'/> The jackknife works by small perturbations, so it needs a statistic that changes smoothly "
            "with the data, and the median jumps. <bookmark mark='e'/> Efron showed in 1982 that for the median the jackknife "
            "standard error isn't even consistent: it stays noisy however large the sample. Something that perturbs the data "
            "more boldly is needed."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.3), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()
