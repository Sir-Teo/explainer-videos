from __future__ import annotations

import numpy as np

from explainer.stats.board import coverage_board, load_all
from videos.stats.stats30.common import *  # noqa: F403


class World(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_world()
        self.onesided()
        self.widths()
        self.reject()
        self.board()
        self.unseen()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"Contamination on the World", r"Mean vs Hodges--Lehmann intervals", lit=(1960,), part=PART)
        with self.voiceover("Chapter ten. Contamination on the World."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_world(self):
        d = load("board")
        rows = fit_rows(VGroup(
            label(rf"the World's adult women: \ mean height {d['mu']:.2f} cm", font_size=26),
            label(rf"samples of {d['n']}; \ nominal 95\% references, evaluated at the latent mean; \ {d['reps']:,} times", font_size=26),
            label(r"clean: \ heights as measured", font_size=26, color=HIT),
            label(r"gross errors: \ 10\% get a random error, \ $N(0, 40^2)$ cm", font_size=26, color=HUBC),
            label(r"unit errors: \ 10\% recorded in inches, \ not centimetres", font_size=26, color=RES),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Board tests both kinds of interval on the World. The target: the mean height of"
            " its adult women, a hundred and sixty-three centimetres. <bookmark mark='b'/> Draw thirty women, apply "
            "the usual t interval and the continuous-symmetry signed-rank reference, two thousand times. We score "
            "both against the latent population mean; HL targets a pseudo-median under asymmetry, so its mean "
            "coverage here is an empirical diagnostic, not a general guarantee. <bookmark mark='c'/> Clean "
            "measurements. <bookmark mark='d'/> Gross errors: a tenth of the readings get a large random error, "
            "symmetric, standard deviation forty centimetres. <bookmark mark='e'/> And unit errors: a tenth are "
            "written down in inches, a one-sided error of about a hundred centimetres."
        ) as vo:
            self.add(world_tag())
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def widths(self):
        d = load("board")["res"]
        hdr = [r"\textbf{regime}", r"\textbf{$t$: \ cover}", r"\textbf{$t$: \ width}", r"\textbf{HL: \ cover}", r"\textbf{HL: \ width}"]
        spec = (("clean", r"clean"), ("sym", r"10\% gross errors"), ("inch", r"10\% in inches"))
        body = [[t, f"{100 * d[k]['t']['cover']:.1f}\\%", f"{d[k]['t']['width']:.1f}", f"{100 * d[k]['hl']['cover']:.1f}\\%",
                 f"{d[k]['hl']['width']:.1f}"] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, HIT, HUBC, RES])
        for r in tb[1:]:
            r[1].set_color(MEANC)
            r[2].set_color(MEANC)
            r[3].set_color(HLC)
            r[4].set_color(HLC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"widths in cm, \ averaged over the 2,000 intervals", font_size=22),
            label(r"gross errors: \ both cover; \ HL's interval is 40\% shorter", font_size=22, color=HUBC),
            label(r"unit errors: \ neither is safe; \ HL degrades less", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The results. Clean data: both intervals cover ninety-five percent, with almost the same "
            "width, about four point eight centimetres; Hodges–Lehmann's efficiency loss is barely visible. "
            "<bookmark mark='b'/> With symmetric gross errors, the t interval still covers, ninety-six percent, but it is "
            "almost ten centimetres wide; Hodges–Lehmann's covers ninety-five percent and is forty percent shorter. "
            "<bookmark mark='c'/> With unit errors, all pointing one way, the t interval covers only seventy percent, and "
            "Hodges–Lehmann's eighty-seven: better, but not safe. One-sided errors bias every estimator of the centre."
        ) as vo:
            self.add(world_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[2]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(tb[3]), FadeIn(foot[2]))
        self.clear_scene()

    def board(self):
        rows = [r for r in load_all(upto=30) if r.part == 30]
        b = coverage_board(rows, lit_part=30, placeholders=0, font_size=20, row_h=0.56)
        b.scale_to_fit_width(min(b.width, 13.0)).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> On the Board. Clean: both kept. <bookmark mark='b'/> Symmetric gross errors: the t "
            "interval is flagged conservative or kept, wasting width; Hodges–Lehmann kept. <bookmark mark='c'/> Unit errors: "
            "both broken, the t interval badly. The Board's verdicts are only about coverage; the widths say the rest."
        ) as vo:
            self.play(FadeIn(b.head), FadeIn(b.axis), FadeIn(b.legend))
            vo.wait_until("a")
            self.play(FadeIn(b.body[0]), FadeIn(b.body[1]))
            vo.wait_until("b")
            self.play(FadeIn(b.body[2]), FadeIn(b.body[3]))
            vo.wait_until("c")
            self.play(FadeIn(b.body[4]), FadeIn(b.body[5]))
        self.wait(1.0)
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"robust methods cost little when the data are clean", font_size=24, color=HIT),
            label(r"they pay off when errors are symmetric and occasional", font_size=24, color=HUBC),
            label(r"resistant location fitting cannot identify an unknown common shift", font_size=24, color=RES),
            label(r"Newcomb's 33 and the inch-recorded heights: \ the same lesson", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So robust methods cost little when the data are clean, <bookmark mark='b'/> and pay"
            " off when errors are occasional and symmetric. <bookmark mark='c'/> These resistant location estimators "
            "do not identify an unknown common systematic shift; external calibration or an explicit identifiable "
            "error model is needed. <bookmark mark='d'/> The inches written as centimetres and Newcomb's "
            "measurements, all short of thirty-three, teach the same lesson."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def reject(self):
        d = load("board")["reject"]
        r = load("board")["res"]
        hdr = [r"\textbf{regime}", r"\textbf{points dropped}", r"\textbf{reject, \ then $t$: \ cover}", r"\textbf{width}",
               r"\textbf{plain $t$}"]
        spec = (("clean", r"clean"), ("sym", r"10\% gross errors"), ("inch", r"10\% in inches"))
        body = [[t, f"{d[k]['dropped']:.1f}", f"{100 * d[k]['cover']:.1f}\\%", f"{d[k]['width']:.1f}",
                 f"{100 * r[k]['t']['cover']:.1f}\\%"] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, HIT, HUBC, RES])
        for row in tb[1:]:
            row[2].set_color(MEDC)
            row[4].set_color(MEANC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"rule: \ drop points more than 3 MADs from the median, \ then a $t$ interval on the rest", font_size=22),
            label(r"it catches the unit errors, \ but undercovers on clean data: \ the rule is a selection step", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What do practitioners actually do? Often: drop points more than three MADs from the median, "
            "then compute an ordinary t interval on what remains. <bookmark mark='b'/> On the unit errors this works "
            "remarkably well: it drops about three points and covers ninety-four percent, with a narrow interval, because "
            "an error of a hundred centimetres is easy to see. <bookmark mark='c'/> But on clean data it covers only "
            "ninety-three: it trims genuine tails and then pretends nothing was trimmed, a little of Part 28's selection "
            "problem. Rejection rules are a judgement about the kind of error expected, and they should be reported as such."
        ) as vo:
            self.add(world_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[3]), FadeIn(tb[2]))
            vo.wait_until("c")
            self.play(FadeIn(tb[1]), FadeIn(foot[1]))
        self.clear_scene()

    def onesided(self):
        rows = [
            cmath(r"\text{symmetric errors}", r":", r"\text{the centre of symmetry is unchanged}", font_size=30),
            cmath(r"\text{one-sided errors}", r":", r"\text{ordinary location functionals can shift}", font_size=30),
            cmath(r"\text{HL, \ 10\% at } {-100}", r":", r"\text{bias } \approx \text{ a few tenths of } \sigma", font_size=30),
            cmath(r"\text{interval}", r":", r"\text{width } \propto 1/\sqrt n, \ \text{bias fixed: \ coverage falls with } n", font_size=28),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"robust estimates still aim at the truth"), why(r"clean center not identifiable without restrictions"),
                why(r"chapter four's maximal bias"), why(r"more data, \ worse coverage")]
        with self.voiceover(
            "<bookmark mark='a'/> Before the results, a prediction. When errors are symmetric, the centre of symmetry"
            " doesn't move, so robust estimates still aim at the truth. <bookmark mark='b'/> Without restrictions on "
            "one-sided contamination the clean center is not generally identifiable from the observed distribution "
            "alone. These ordinary location functionals can shift. <bookmark mark='c'/> A robust estimate moves less,"
            " chapter four's bounded maximal bias, but it does move. <bookmark mark='d'/> And because an interval "
            "shrinks like one over root n while the bias stays fixed, coverage under one-sided contamination gets "
            "worse as the sample grows."
        ) as vo:
            intro=label('One-sided errors can shift the target of ordinary location fitting',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def unseen(self):
        rows = [
            cmath(r"\text{the Board measures}", r":", r"\text{coverage at a known truth}", font_size=30),
            cmath(r"\text{it cannot see}", r":", r"\text{whether a real data set is contaminated}", font_size=30),
            cmath(r"\text{so}", r":", r"\text{report both: \ classical and robust}", font_size=30),
            cmath(r"\text{if they differ}", r":", r"\text{the difference is the finding}", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"a simulation's privilege"), why(r"with real data, \ only diagnostics"), why(r"Tukey's advice"),
                why(r"investigate, \ don't average them")]
        with self.voiceover(
            "<bookmark mark='a'/> The Board can measure coverage because the World's truth is known. <bookmark mark='b'/> With "
            "real data nobody knows whether contamination is present, or of which kind. <bookmark mark='c'/> So report both "
            "the classical and the robust analysis, as Tukey urged. <bookmark mark='d'/> When they agree, little is lost; when "
            "they differ, the difference is itself the finding, and the data deserve a closer look."
        ) as vo:
            intro=label('Simulation coverage and real-data error diagnosis answer different questions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
