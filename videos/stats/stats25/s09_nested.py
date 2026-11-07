from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class Nested(VoiceoverScene):
    def construct(self):
        self.card()
        self.nested_model()
        self.nested_fit()
        self.radon()
        self.crossed_model()
        self.raters()
        self.crossed_fit()
        self.syntax()

    def card(self):
        card = chapter_card(8, r"Nested and crossed", r"Schools in towns; \ essays and raters", lit=(2007,), part=PART)
        with self.voiceover("Chapter eight. Nested and crossed random effects."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def nested_model(self):
        rows = [
            cmath(r"y_{tgi}", r"=", r"\mu + v_t + u_{tg} + \varepsilon_{tgi}", font_size=32),
            cmath(r"v_t \sim N(0, \tau_v^2)", r",", r"\ u_{tg} \sim N(0, \tau_u^2)", font_size=30),
            cmath(r"\mathrm{corr}", r":", r"\tfrac{\tau_v^2}{\text{total}} \text{ same town}; \ \tfrac{\tau_v^2 + \tau_u^2}{\text{total}} \text{ same school}", font_size=28),
            cmath(r"\text{nested}", r":", r"\text{each school lies in exactly one town}", font_size=30),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"towns, \ schools within towns, \ pupils within schools"), why(r"a variance at each level"),
                why(r"two pupils share more the closer they sit"), why(r"school 7 of town 3 is not school 7 of town 4")]
        intro = label('Nested random effects create covariance at multiple levels', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Clusters can sit inside clusters. The World's schools are in towns, so a pupil's score can "
            "have a town effect, a school-within-town effect, and the pupil's own. <bookmark mark='b'/> Each level has its "
            "own variance. <bookmark mark='c'/> Two pupils in the same town share the town variance; two in the same school "
            "share both. <bookmark mark='d'/> The design is nested: every school belongs to exactly one town, so a school's "
            "label only means something within its town."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nested_fit(self):
        d = load("nested")
        tot = d["school_var"] + d["pupil_var"]
        vals = [(r"towns", d["town_var"], PATH), (r"school-mean residuals", d["school_resid_var"], SHRUNK), (r"pupils", d["pupil_var"], RAW)]
        bar_w = 9.0
        y0 = 0.6
        segs = VGroup()
        names = VGroup()
        x = -bar_w / 2
        tot3 = sum(v for _, v, _ in vals)
        for nm, v, c in vals:
            w = max(bar_w * v / max(vv for _, vv, _ in vals), 0.04)
            r = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x + w / 2, y0 - len(segs) * 0.65, 0])
            segs.add(r)
            # Independent estimate bars, not an additive variance decomposition.
        for (nm, v, c), r in zip(vals, segs):
            names.add(label(rf"{nm}: \ {v:,.0f}", font_size=22, color=c))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.9, 0])
        head = label(rf"{d['n_schools']} schools in {d['n_towns']} towns: \ separate two-stage estimates", font_size=26).move_to([0, 2.4, 0])
        foot = label(r"no explicit town effect generated; \ no calibrated test computed", font_size=22, color=GREY_A).move_to([0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This display compares two separate working fits: a pupil-level school-intercept "
            "model, and an unweighted model of school means grouped by town. It is a two-stage approximation, not a "
            "joint three-level likelihood. <bookmark mark='b'/> The pupil-model residual variance is large. <bookmark"
            " mark='c'/> The school-mean model also has substantial residual variation, including pupil-mean noise. "
            "<bookmark mark='d'/> Its town component is about forty-nine. <bookmark mark='e'/> No explicit town "
            "effect was generated, but a positive fitted component can occur. We have not computed a calibrated "
            "town-variance test, so these estimates alone do not establish significance."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(head))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                j = 2 - k
                self.play(GrowFromEdge(segs[j], LEFT), FadeIn(names[j]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def radon(self):
        rows = fit_rows(VGroup(
            label(r"Gelman \& Hill (2007): \ radon in 919 Minnesota homes, \ 85 counties", font_size=24, color=PATH),
            label(r"house level: \ measured in the basement or on the first floor", font_size=24),
            label(r"county level: \ the soil's uranium, \ a predictor for the county effects", font_size=24),
            label(r"a county with 2 homes is pulled to the line its uranium predicts", font_size=24, color=SHRUNK),
            label(r"group-level predictors make the shrinkage target smarter", font_size=24, color=HIT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The classic teaching example, from Andrew Gelman and Jennifer Hill's book: radon gas "
            "measured in nine hundred and nineteen Minnesota homes in eighty-five counties. <bookmark mark='b'/> Each house "
            "was measured in the basement or on the first floor, a predictor at the house level. <bookmark mark='c'/> Each "
            "county has a soil uranium reading, a predictor at the county level, which models the county effects themselves. "
            "<bookmark mark='d'/> A county with two homes is then pulled not to the state average but to the radon level its "
            "uranium predicts. <bookmark mark='e'/> Group-level predictors make the target of shrinkage smarter, as "
            "chapter eleven will use for towns."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def crossed_model(self):
        rows = [
            cmath(r"y_{er}", r"=", r"\mu + a_e - s_r + \varepsilon_{er}", font_size=32),
            cmath(r"a_e \sim N(0, \tau_a^2)", r",", r"\ s_r \sim N(0, \tau_s^2)", font_size=30),
            cmath(r"\text{crossed}", r":", r"\text{every rater could read every essay}", font_size=30),
            cmath(r"V", r"=", r"\tau_a^2 Z_a Z_a^\top + \tau_s^2 Z_s Z_s^\top + \sigma^2 I", font_size=30),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"essay quality, \ rater severity"), why(r"both are samples from populations"),
                why(r"no nesting: \ the factors cut across"), why(r"no block structure: \ dense algebra, \ or sparse")]
        intro = label('Crossed effects separate essay quality from rater severity', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Other factors cross instead of nesting. An exam essay's grade depends on the essay's "
            "quality and on the severity of whoever reads it. <bookmark mark='b'/> Both essays and raters are samples from "
            "larger populations, so both effects are random. <bookmark mark='c'/> The factors are crossed: any rater could "
            "read any essay. <bookmark mark='d'/> The covariance no longer splits into blocks, one per group, so the fit "
            "needs general sparse algebra, which is what lme4 does; statkit's version is dense, for a few thousand rows."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def raters(self):
        d = load("crossed")
        sev, sh = np.asarray(d["severity"]), np.asarray(d["sev_hat"])
        A = axes([-1, 1], [-1, 1], x_length=4.8, y_length=4.8, xlabel=r"true severity", ylabel=r"estimated",
                 xticks=[-1, 0, 1], yticks=[-1, 0, 1], center=[-3.0, 0.1, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(-1, -1), ax.c2p(1, 1), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=PATH) for a, b in zip(sev, sh)])
        rows = fit_rows(VGroup(
            label(r"60 essays, \ 8 raters; \ each essay read by 2 raters at random", font_size=22),
            label(r"an essay's raw mean depends on whom it drew", font_size=22, color=RES),
            label(r"gold: \ the 8 raters' severities, \ recovered", font_size=22, color=PATH),
            label(rf"$\hat\tau_s^2 = {d['var']['rater']:.2f}$, \ $\hat\tau_a^2 = {d['var']['essay']:.2f}$, \ $\hat\sigma^2 = {d['sigma2']:.2f}$", font_size=22),
        ), 5.8, 0.42, [3.6, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulation: sixty essays and eight raters, each essay read by two raters chosen at "
            "random. <bookmark mark='b'/> An essay that draws two harsh raters gets a low mean for reasons that have nothing "
            "to do with the essay. <bookmark mark='c'/> Because the raters overlap across essays, the crossed model can "
            "separate the two, and it recovers each rater's severity. <bookmark mark='d'/> The variances: one point five "
            "seven for essays, point one seven for raters, point two two for the noise."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.15), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def crossed_fit(self):
        d = load("crossed")
        hdr = [r"\textbf{essay quality from}", r"\textbf{mean squared error}", r"\textbf{rank correlation}"]
        body = [[r"the raw mean of its 2 grades", f"{d['mse']['raw']:.3f}", f"{d['rank']['raw']:.3f}"],
                [r"essays random, \ raters ignored", f"{d['mse']['essay_only']:.3f}", f"{d['rank']['essay_only']:.3f}"],
                [r"essays and raters crossed", f"{d['mse']['crossed']:.3f}", f"{d['rank']['crossed']:.3f}"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, RAW, POOLED, SHRUNK])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"shrinking alone helps a little; \ adjusting for the raters helps more", font_size=22, color=HIT),
            label(r"the same idea ranks hospitals, \ referees and judges", font_size=22, color=GREY_A),
        ), 12.0, 0.25, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How well does each method recover the essays' true quality? <bookmark mark='b'/> The raw "
            "mean of two grades has a mean squared error of point two oh. <bookmark mark='c'/> Shrinking the means, with "
            "essays random but raters ignored, brings it to point one seven, though the ranking cannot change. "
            "<bookmark mark='d'/> The crossed model, which also corrects for who did the reading, brings it to point one two "
            "and improves the ranking. <bookmark mark='e'/> The same model adjusts for referees in peer review and for "
            "judges in competitions."
        ) as vo:
            self.add(simulated_tag(r"simulated: \ a seeded example"))
            vo.wait_until("a")
            self.play(FadeIn(tb[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tb[k + 1]))
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def syntax(self):
        rows = fit_rows(VGroup(
            label(r"\texttt{score $\sim$ ses + (1 | school)}: \ \ random intercepts, \ chapter four", font_size=24, color=SHRUNK),
            label(r"\texttt{height $\sim$ age + (age | child)}: \ \ random slopes, \ chapter seven", font_size=24, color=SHRUNK),
            label(r"\texttt{score $\sim$ 1 + (1 | town/school)}: \ \ nested", font_size=24, color=PATH),
            label(r"\texttt{grade $\sim$ 1 + (1 | essay) + (1 | rater)}: \ \ crossed", font_size=24, color=PATH),
            label(r"the notation of R's lme4 \ (Bates, M\"achler, Bolker \& Walker 2015)", font_size=22, color=GREY_A),
        ), 12.6, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In practice these models are written in a compact formula language. A random intercept for "
            "each school is one plus bar school, in brackets. <bookmark mark='b'/> A random intercept and slope in age for "
            "each child puts age before the bar. <bookmark mark='c'/> Schools nested in towns are written town slash school, "
            "<bookmark mark='d'/> and crossed essays and raters are simply two separate terms. <bookmark mark='e'/> This is "
            "the notation of Douglas Bates's lme4 package for R, now copied by most other software."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
