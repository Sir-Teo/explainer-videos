from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.planning()
        self.cohen()
        self.type_sm()
        self.sm_table()
        self.lesson()

    def card(self):
        card = chapter_card(9, r"Power and sample size", r"Could the study have found it?", part=PART)
        with self.voiceover("Chapter nine. Power and sample size."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def curves(self):
        d = load("power")
        dl = np.asarray(d["deltas"])
        A = axes([-1.2, 1.2], [0, 1], x_length=7.6, y_length=4.4, xlabel=r"true effect $\delta/\sigma$", ylabel=r"power, \ two-sided, \ $\alpha = 0.05$",
                 xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.05, 0.5, 0.8, 1], center=[-2.0, -0.3, 0])
        ax = A.ax
        cols = {"10": S.PRIOR, "30": S.POST, "100": ALTC}
        cvs = VGroup(*[polyline(ax, dl, d["curves"][n], cols[n], 3.5) for n in ("10", "30", "100")])
        floor = DashedLine(ax.c2p(-1.2, 0.05), ax.c2p(1.2, 0.05), color=REJ, stroke_width=1.5)
        leg = legend([(cols[n], rf"$n = {n}$") for n in ("10", "30", "100")], font_size=22).move_to([4.6, 2.0, 0])
        rows = fit_rows(VGroup(
            label(r"at $\delta = 0$ every curve touches $\alpha$: \ power there is the false-alarm rate", font_size=24),
            label(r"more data: \ a narrower valley, \ more power at every $\delta \ne 0$", font_size=24, color=OBS),
            label(r"a test is a detector with a sensitivity curve", font_size=24, color=GREY_A),
        ), 5.0, 0.34, [4.4, -0.6, 0])
        with self.voiceover(
            "Power isn't one number; it's a curve. <bookmark mark='a'/> For the two-sided z-test, here's the chance of "
            "rejecting as a function of the true effect, for ten observations. <bookmark mark='b'/> At zero effect, the "
            "curve touches five percent: there, the power is just the false-alarm rate. Far from zero, it climbs toward "
            "one. <bookmark mark='c'/> With thirty observations the valley narrows, and with a hundred it narrows again. "
            "A test is a detector, and this is its sensitivity curve: small effects need large samples to see."
        ) as vo:
            self.play(FadeIn(A), Create(floor))
            vo.wait_until("a")
            self.play(Create(cvs[0]), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(cvs[1]), FadeIn(leg[1]))
            self.play(Create(cvs[2]), FadeIn(leg[2]), FadeIn(rows[1:]))
        self.clear_scene()

    def planning(self):
        d = load("power")["n80"]
        hdr = VGroup(*[label(t, font_size=26, color=GREY_B) for t in (r"effect $\delta/\sigma$", r"Cohen's label", r"$n$ for 80\% power")])
        xs = [-3.8, 0.0, 3.8]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.0, 0])
        cells = VGroup()
        for i, (dl, nm) in enumerate((("0.2", r"small"), ("0.5", r"medium"), ("0.8", r"large"))):
            y = 1.2 - 0.7 * i
            cells.add(VGroup(MathTex(dl, font_size=34).move_to([xs[0], y, 0]), label(nm, font_size=28, color=GREY_A).move_to([xs[1], y, 0]),
                             MathTex(str(d[dl]), font_size=34, color=OBS).move_to([xs[2], y, 0])))
        rows = fit_rows(VGroup(
            MathTex(r"n \propto 1/\delta^2:\ \ \text{halve the effect, \ quadruple the sample}", font_size=30, color=OBS),
            label(r"a power analysis needs an effect size chosen \emph{before} the data: \ the smallest effect worth detecting",
                  font_size=24),
            label(r"Jacob Cohen, \ \emph{Statistical Power Analysis for the Behavioral Sciences} (1969, 1988)", font_size=22, color=GREY_A),
        ), 12.6, 0.32, [0, -1.7, 0])
        with self.voiceover(
            "Planning a study means turning that around. <bookmark mark='a'/> For a one-sample z-test at five percent, "
            "eighty percent power against an effect of point two standard deviations, which the psychologist Jacob Cohen "
            "called small, needs a hundred and ninety-seven observations. A medium effect, half a standard deviation, "
            "needs thirty-two. A large one, point eight, needs thirteen. <bookmark mark='b'/> The sample size grows like "
            "one over the effect squared: halve the effect and you need four times the data. <bookmark mark='c'/> A power "
            "analysis needs an effect size chosen before the data are seen, ideally the smallest effect that would "
            "matter. <bookmark mark='d'/> Cohen's book on power analysis made this standard practice, at least on paper."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in cells], lag_ratio=0.5))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def cohen(self):
        hc = history_card(1962, r"Jacob Cohen, \ \emph{J.\ Abnormal and Social Psychology} 65", r"surveyed a year of a leading journal: \ "
                          r"the typical study had only about an even chance of detecting a medium-sized effect", color=GREY_B, width=9.0,
                          font_size=24).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"repeated surveys decades later \ (Sedlmeier \& Gigerenzer, 1989) \ found little change", font_size=24, color=GREY_A),
            label(r"low power does more than miss effects: \ it distorts the ones it finds", font_size=28, color=OBS),
        ), 12.6, 0.34, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1962 Cohen surveyed a year of papers in a leading psychology journal and estimated "
            "that the typical study had only about an even chance of detecting an effect of medium size. "
            "<bookmark mark='b'/> When Peter Sedlmeier and Gerd Gigerenzer repeated the survey a quarter of a century "
            "later, little had changed. <bookmark mark='c'/> You might think low power only means missing real effects. "
            "It does something worse: it distorts the effects that do get found."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def type_sm(self):
        d = load("power")
        est = np.asarray(d["sm_draws"])
        sm = d["sm"]["0.1_50"]
        se = sm["se"]
        nl = NumberLine(x_range=[-0.8, 0.9, 0.1], length=12.0, include_numbers=False, color=GREY_C).move_to([0, 0.2, 0])
        ticks = VGroup(*[MathTex(f"{v:g}", font_size=20, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.15) for v in (-0.6, -0.39, 0, 0.1, 0.39, 0.6)])
        zone_r = Rectangle(width=nl.n2p(0.9)[0] - nl.n2p(1.96 * se)[0], height=3.2, stroke_width=0, fill_color=REJ, fill_opacity=0.12)
        zone_r.move_to([(nl.n2p(0.9)[0] + nl.n2p(1.96 * se)[0]) / 2, 1.5, 0])
        zone_l = Rectangle(width=nl.n2p(-1.96 * se)[0] - nl.n2p(-0.8)[0], height=3.2, stroke_width=0, fill_color=REJ, fill_opacity=0.12)
        zone_l.move_to([(nl.n2p(-1.96 * se)[0] + nl.n2p(-0.8)[0]) / 2, 1.5, 0])
        truth = DashedLine(nl.n2p(0.1) + DOWN * 0.1, nl.n2p(0.1) + UP * 3.1, color=EXACT, stroke_width=2.5)
        g = np.random.Generator(np.random.PCG64(7))
        ys = 0.45 + g.random(len(est)) * 2.5
        dots = VGroup(*[Dot([nl.n2p(float(np.clip(e, -0.79, 0.89)))[0], y, 0], radius=0.04, color=SIM) for e, y in zip(est, ys)])
        sig = [i for i, e in enumerate(est) if abs(e) > 1.96 * se]
        rows = fit_rows(VGroup(
            label(rf"true effect $0.1$, \ standard error $0.2$ \ (two groups of 50): \ power {100 * sm['power']:.0f}\%", font_size=24),
            label(rf"the significant estimates exaggerate the effect {sm['exaggeration']:.1f}-fold \ (type M)", font_size=26, color=OBS),
            label(rf"and {100 * sm['type_s']:.0f}\% of them have the wrong sign \ (type S)", font_size=26, color=REJ),
            label(r"Gelman \& Carlin (2014): \ ``Beyond power calculations''", font_size=22, color=GREY_A),
        ), 12.6, 0.28, [0, -2.3, 0])
        tag = simulated_tag(r"simulated: \ 400 studies (of 200,000)", corner=UR)
        with self.voiceover(
            "Andrew Gelman and John Carlin made this vivid in 2014. <bookmark mark='a'/> Suppose the true effect is "
            "small, point one, and the study's standard error is point two, as with two groups of fifty. "
            "<bookmark mark='b'/> Here are four hundred replications of the study: each dot is one study's estimate. "
            "They scatter widely around the truth. <bookmark mark='c'/> A study is significant only if its estimate "
            "lands in a red zone, more than one point nine six standard errors from zero. That happens eight percent of "
            "the time. <bookmark mark='d'/> Now look at the studies that made it. To be significant, an estimate had to "
            "be at least point three nine, nearly four times the truth. On average, the significant estimates are "
            "almost five times too big. Gelman and Carlin call this a type M error, for magnitude. "
            "<bookmark mark='e'/> And nearly one in ten of them is significant in the wrong direction: a type S error, "
            "for sign. If only significant results get published, the published record is exaggerated, and sometimes "
            "backwards."
        ) as vo:
            self.play(Create(nl), FadeIn(ticks), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.003), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(zone_l), FadeIn(zone_r))
            vo.wait_until("d")
            self.play(*[dots[i].animate.set_color(OBS).scale(1.6) for i in sig],
                      *[dots[i].animate.set_opacity(0.25) for i in range(len(dots)) if i not in set(sig)], FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(*[dots[i].animate.set_color(REJ) for i in sig if est[i] < 0], FadeIn(rows[2:]))
        self.clear_scene()

    def sm_table(self):
        sm = load("power")["sm"]
        hdr = VGroup(*[label(t, font_size=24, color=GREY_B) for t in (r"true effect, \ $n$ per group", r"power", r"exaggeration", r"wrong sign")])
        xs = [-4.0, -0.6, 2.2, 4.8]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 1.6, 0])
        cells = VGroup()
        for i, (k, lab) in enumerate((("0.1_50", r"0.1,\ 50"), ("0.3_50", r"0.3,\ 50"), ("0.5_64", r"0.5,\ 64"))):
            r = sm[k]
            y = 0.9 - 0.6 * i
            cells.add(VGroup(MathTex(lab, font_size=30).move_to([xs[0], y, 0]), MathTex(rf"{100 * r['power']:.0f}\%", font_size=30).move_to([xs[1], y, 0]),
                             MathTex(rf"{r['exaggeration']:.2f}\times", font_size=30, color=OBS).move_to([xs[2], y, 0]),
                             MathTex(rf"{100 * r['type_s']:.1f}\%", font_size=30, color=REJ).move_to([xs[3], y, 0])))
        foot = label(r"at 80\% power the significant estimates are only 12\% too big; \ at 8\%, \ almost fivefold", font_size=26,
                     color=OBS).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "How bad it is depends on the power. <bookmark mark='a'/> At eight percent power, significant estimates are "
            "nearly five times too large. At thirty-two percent, about one and three quarter times. "
            "<bookmark mark='b'/> At eighty-one percent, only twelve percent too large, and the wrong sign essentially "
            "never. A well-powered study isn't just more likely to find an effect; what it finds can be believed."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(FadeIn(cells[0]), FadeIn(cells[1]))
            vo.wait_until("b")
            self.play(FadeIn(cells[2]), FadeIn(foot))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"the winner's curse", font_size=32, color=OBS),
            label(r"filter noisy estimates by significance and you select the lucky ones", font_size=26),
            label(r"replication then disappoints: \ large replication projects in psychology (2015) found effects about half as large",
                  font_size=24, color=GREY_A),
            label(r"remedies: \ adequate power, \ preregistration, \ reporting estimates with intervals (Part 11), \ shrinkage (Part 25)",
                  font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Economists call it the winner's curse. <bookmark mark='b'/> If you filter noisy "
            "estimates by whether they're significant, you select the lucky ones. <bookmark mark='c'/> So when the "
            "studies are repeated, the effects shrink: the large replication project in psychology published in 2015 "
            "found effects about half the size of the originals, on average. <bookmark mark='d'/> The remedies are "
            "adequate power, deciding the analysis in advance, reporting estimates with honest intervals, the subject of "
            "Part 11, and the shrinkage estimators of Part 25, which correct for the selection directly."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
