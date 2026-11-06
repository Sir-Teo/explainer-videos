from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403

RULES = [("brier", r"Brier", r"(q - o)^2", "#6FB7FF"),
         ("log", r"logarithmic", r"-\ln q_o", "#5EE6D0"),
         ("spherical", r"spherical", r"-q_o / \lVert q \rVert", "#C3A6FF"),
         ("linear", r"linear \ (absolute error)", r"-q_o", "#F28EC2")]
FC = {"calibrated": "#5EE6D0", "overconfident": "#F28EC2", "timid": "#FFD166", "always 1/2": "#9AA4B2"}


class Scoring(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Keeping score", r"How do you reward an honest forecast?", lit=(1950,), part=PART)
        with self.voiceover("Chapter four. Keeping score."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.setup_()
        self.curves()
        self.absolute()
        self.forecasters()
        self.calibration()
        self.uses()

    def setup_(self):
        head = label(r"A forecaster, \ a report, \ a penalty", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"your credence that it rains: \ $p$", font_size=26, color=CRED),
            label(r"what you report: \ $q$ \ \ (it need not be $p$)", font_size=26, color=BET),
            label(r"tomorrow you are penalized $S(q, o)$, \ where $o = 1$ if it rains, \ $0$ if not", font_size=26),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        exp = MathTex(r"\mathbb{E}_p\,[S(q)] \;=\; p\,S(q, 1) + (1 - p)\,S(q, 0)", font_size=40).next_to(
            rows, DOWN, buff=0.5)
        proper = label(r"$S$ is \textit{proper} \ if reporting $q = p$ minimizes your expected penalty", font_size=27,
                       color=GOAL).next_to(exp, DOWN, buff=0.45)
        sub = label(r"strictly proper: \ $q = p$ is the \textit{only} minimizer \ \ (honesty is the unique best policy)",
                    font_size=22, color=GREY_A).next_to(proper, DOWN, buff=0.25)
        with self.voiceover(
            "The Brier score raises a practical question. How should we score forecasters so that they tell us what "
            "they really think? <bookmark mark='a'/>Say your credence in rain is p. You report a number q, which "
            "need not be p, and tomorrow you are penalized by a scoring rule, S, according to whether it rained. "
            "<bookmark mark='b'/>By your own lights, your expected penalty is p times the penalty if it rains, plus "
            "one minus p times the penalty if not. <bookmark mark='c'/>The rule is called proper if your expected "
            "penalty is smallest when you report your true credence, <bookmark mark='d'/>and strictly proper if that "
            "is the only best report. Under a strictly proper rule, honesty is the unique best policy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(exp))
            vo.wait_until("c")
            self.play(FadeIn(proper))
            vo.wait_until("d")
            self.play(FadeIn(sub))
        self.clear_scene()

    def curves(self):
        d = load("scoring")
        p = d["p"]
        head = label(rf"Expected penalty when your credence is ${p}$", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        panels = VGroup()
        for i, (key, name, formula, col) in enumerate(RULES):
            pts = d["curves"][key]
            raw = [y for _, y in pts]
            lo, hi = min(raw), max(raw)
            pad = (hi - lo) * 0.12
            ys = [y - lo + pad for y in raw]          # shifted so the axis sits at the bottom; only the shape matters
            top = hi - lo + 2 * pad
            ax = Axes(x_range=[0, 1, 0.5], y_range=[0, top, top / 2], x_length=4.6, y_length=2.0, tips=False,
                      axis_config={"color": GREY_C, "include_numbers": False, "include_ticks": False})
            curve = ax.plot_line_graph([q for q, _ in pts], ys, line_color=col, add_vertex_dots=False,
                                       stroke_width=3)
            best = d["best"][key]
            bx = min(pts, key=lambda t: t[1])[0]
            vline = DashedLine(ax.c2p(bx, 0), ax.c2p(bx, top), color=col, stroke_width=2)
            pline = DashedLine(ax.c2p(p, 0), ax.c2p(p, top), color=GREY_B, stroke_width=1.5, dash_length=0.05)
            dot = Dot(ax.c2p(bx, pad), color=col, radius=0.07)
            title = VGroup(label(name, font_size=21, color=col), MathTex(formula, font_size=24, color=col)).arrange(
                RIGHT, buff=0.25).next_to(ax, UP, buff=0.12)
            ticks = VGroup(MathTex(r"0", font_size=18).next_to(ax.c2p(0, 0), DOWN, buff=0.08),
                           MathTex(r"1", font_size=18).next_to(ax.c2p(1, 0), DOWN, buff=0.08),
                           MathTex(r"q", font_size=20).next_to(ax.c2p(1, 0), RIGHT, buff=0.12))
            bl = MathTex(rf"q^* = {best:.2f}" if best < 0.99 else r"q^* = 1", font_size=22,
                         color=OK if abs(best - p) < 0.01 else BAD)
            if best < 0.99:
                bl.next_to(dot, DOWN, buff=0.12)
            else:
                bl.next_to(dot, UL, buff=0.08)
            panel = VGroup(ax, ticks, pline, curve, vline, dot, title, bl)
            panel.ax, panel.curve, panel.extras = ax, curve, VGroup(vline, dot, bl)
            panels.add(panel)
        panels.arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.7)).next_to(head, DOWN, buff=0.35)
        foot = label(r"$q_o$: \ the probability you gave to what happened; \ grey line: \ your credence $p = 0.7$",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The Reasoner plots the expected penalty for every report, when your credence is point seven, under four "
            "rules. <bookmark mark='a'/>The Brier score: the minimum is at point seven. <bookmark mark='b'/>The "
            "logarithmic score, minus the log of the probability you gave to what actually happened: again the "
            "minimum is at point seven. <bookmark mark='c'/>The spherical score: point seven. "
            "<bookmark mark='d'/>But the linear score, minus the probability you gave to what happened, which is the "
            "same as absolute error: its expected penalty falls all the way to the edge. Under the linear rule, a "
            "forecaster who thinks rain is seventy percent likely does best by announcing that rain is certain. It "
            "rewards exaggeration."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            for mk, pn in zip("abcd", panels):
                vo.wait_until(mk)
                self.play(FadeIn(pn[0]), FadeIn(pn[1]), FadeIn(pn[2]), FadeIn(pn[6]), run_time=0.6)
                self.play(Create(pn[3]), run_time=1.2)
                self.play(FadeIn(pn.extras))
        self.clear_scene()

    def absolute(self):
        head = label(r"Why the accuracy argument needs a proper measure", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        hd = [r"\text{credences over three worlds}", r"\text{absolute error in each world}", r"\text{coherent?}"]
        rows = [[r"(\tfrac13,\ \tfrac13,\ \tfrac13)", r"\tfrac23 + \tfrac13 + \tfrac13 = \tfrac43", mark(True, 26)],
                [r"(0,\ 0,\ 0)", r"1 + 0 + 0 = 1", mark(False, 26)]]
        grid = ValueGrid(hd, rows, col_w=[4.0, 4.6, 2.2], cell_h=0.7, font_size=28).next_to(head, DOWN, buff=0.6)
        grid.cell[1][1].set_color(BAD)
        notes = stack([(r"under absolute error, \ the incoherent $(0,0,0)$ beats the coherent uniform credence "
                        r"in \textit{every} world", BAD),
                       (r"an improper measure rewards extreme or incoherent credences", WHITE),
                       (r"strictly proper measures are exactly the ones for which Joyce's theorem holds", GOAL)],
                      font_size=24, width=12.4).next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            "This is why the accuracy argument of the last chapter must use a proper measure. "
            "<bookmark mark='a'/>Take three worlds, and the coherent uniform credence, one third each. Measured by "
            "absolute error, its inaccuracy in any world is two thirds plus a third plus a third: four thirds. "
            "<bookmark mark='b'/>Now take the incoherent credence that gives zero to everything. In any world, its "
            "absolute error is one. <bookmark mark='c'/>So by absolute error, the incoherent credence beats the "
            "coherent one in every world. <bookmark mark='d'/>An improper measure rewards extreme, even incoherent, "
            "credences. <bookmark mark='e'/>With strictly proper measures, dominance always favours coherence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("ab", range(2)):
                vo.wait_until(mk)
                self.play(*[FadeIn(m) for m in grid.cell[r]])
            for mk, n in zip("cde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.clear_scene()

    def forecasters(self):
        f = load("forecast")
        head = label(r"Four forecasters, \ 2{,}000 events", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        desc = stack([(r"each event has a true chance; \ the outcomes are drawn from it", GREY_A),
                      (r"calibrated: \ reports the chance", FC["calibrated"]),
                      (r"overconfident: \ pushes it towards 0 or 1", FC["overconfident"]),
                      (r"timid: \ pulls it towards $\tfrac12$", FC["timid"]),
                      (r"always $\tfrac12$", FC["always 1/2"])], font_size=22, aligned_edge=LEFT).move_to(
            [-3.8, 0.6, 0])
        names = list(FC)
        brier = bar_row([f[k]["brier"] for k in names], [k for k in names], [FC[k] for k in names], width=3.0,
                        font_size=20, vmax=0.26, fmt=lambda v: f"{v:.3f}").move_to([3.2, 1.0, 0])
        logs = bar_row([f[k]["log"] for k in names], [k for k in names], [FC[k] for k in names], width=3.0,
                       font_size=20, vmax=0.72, fmt=lambda v: f"{v:.3f}").move_to([3.2, -1.7, 0])
        bt = label(r"mean Brier penalty", font_size=22, color=GREY_B).next_to(brier, UP, buff=0.2)
        lt = label(r"mean log penalty", font_size=22, color=GREY_B).next_to(logs, UP, buff=0.2)
        note = label(r"both rules put the honest forecaster first, \ but they order the others differently",
                     font_size=22, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now a simulation. <bookmark mark='a'/>Two thousand events, each with a true chance, and outcomes drawn "
            "from those chances. Four forecasters. One reports the true chance. One is overconfident, pushing every "
            "number towards zero or one. One is timid, pulling every number towards a half. And one always says one "
            "half. <bookmark mark='b'/>Their mean Brier penalties: the honest forecaster wins, at point one six six; "
            "the overconfident one is second, the timid one third, and always-a-half is worst, at a quarter. "
            "<bookmark mark='c'/>Under the log score the honest forecaster wins again, but now the overconfident one "
            "falls behind the timid one, because the log score punishes confident mistakes without limit. "
            "<bookmark mark='d'/>Every strictly proper rule ranks honesty first; they disagree about how to rank "
            "the different ways of being wrong."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in desc], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bt), LaggedStart(*[FadeIn(r) for r in brier], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(lt), LaggedStart(*[FadeIn(r) for r in logs], lag_ratio=0.25))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def calibration(self):
        f = load("forecast")
        head = label(r"Calibration: \ of the days you said 70\%, \ did it rain on 70\%?", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.6, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-3.3, -0.6, 0])
        xl = label(r"forecast", font_size=20, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"how often it happened", font_size=20, color=GREY_B).rotate(PI / 2).next_to(ax.y_axis, LEFT,
                                                                                               buff=0.4)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        series = VGroup()
        for k, col in FC.items():
            bins = f[k]["bins"]
            dots = VGroup(*[Dot(ax.c2p(b[1], b[2]), radius=0.05 + 0.06 * (b[3] / 540) ** 0.5, color=col)
                            for b in bins])
            line = VMobject(stroke_color=col, stroke_width=2.5).set_points_as_corners(
                [ax.c2p(b[1], b[2]) for b in bins]) if len(bins) > 1 else VGroup()
            series.add(VGroup(line, dots))
        notes = stack([
            (r"calibrated: \ on the diagonal", FC["calibrated"]),
            (r"overconfident: \ an S, \ flatter than the diagonal", FC["overconfident"]),
            (r"timid: \ steeper than the diagonal", FC["timid"]),
            (r"always $\tfrac12$: \ one point, \ and it is calibrated!", FC["always 1/2"]),
            (r"calibration is not enough: \ you must also \textit{discriminate}", GOAL),
            (r"Murphy (1973): \ Brier $=$ miscalibration $-$ resolution $+$ uncertainty", WHITE),
        ], font_size=22, aligned_edge=LEFT, width=6.6).move_to([3.3, -0.5, 0])
        with self.voiceover(
            "There is a second way to judge forecasters: calibration. <bookmark mark='a'/>Group the days by forecast. "
            "Of the days on which you said seventy percent, did it rain on about seventy percent? Plot forecast "
            "against frequency. <bookmark mark='b'/>The honest forecaster lies on the diagonal. "
            "<bookmark mark='c'/>The overconfident one makes an S-shape, flatter than the diagonal: when she says ninety "
            "eight percent, it happens only eighty eight percent of the time. <bookmark mark='d'/>The timid one is "
            "steeper than the diagonal. <bookmark mark='e'/>And the forecaster who always says a half is a single "
            "point, on the diagonal: it happened about half the time. She is perfectly calibrated, and useless. "
            "<bookmark mark='f'/>Calibration is not enough; a good forecaster must also separate the days that will "
            "be rainy from the days that won't. <bookmark mark='g'/>Allan Murphy's decomposition makes this exact: the "
            "Brier score equals miscalibration, minus resolution, plus the uncertainty in the weather itself."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(diag))
            for mk, s, n in zip("bcde", series, notes):
                vo.wait_until(mk)
                anims = [FadeIn(s[1]), FadeIn(n)]
                if s[0].has_points():
                    anims.append(Create(s[0]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(notes[4]))
            vo.wait_until("g")
            self.play(FadeIn(notes[5]))
        self.clear_scene()

    def uses(self):
        head = label(r"Proper scores everywhere", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        items = [
            (1950, r"weather forecasts", r"Brier's score, \ still used by meteorologists"),
            (1952, r"information", r"I.\ J.\ Good: \ the log score counts bits of surprise"),
            (1971, r"the general form", r"Savage; \ Schervish: \ every proper rule comes from a convex function"),
            (2003, r"markets", r"Hanson's market scoring rules: \ a prediction market as a sequence of forecasts"),
            (2015, r"superforecasters", r"Tetlock: \ amateurs scored by Brier beat the professionals; \ Metaculus"),
            (2017, r"machine learning", r"cross-entropy loss \textit{is} the log score; \ and deep nets are "
                                        r"overconfident (Guo et al.)"),
        ]
        g = VGroup()
        for i, (y, a, b) in enumerate(items):
            yr = label(str(y), font_size=22, color=HIST)
            x = label(a, font_size=23, color=BET)
            z = label(b, font_size=21, color=GREY_A)
            if z.width > 7.8:
                z.width = 7.8
            yr.move_to([-6.2, 2.0 - i * 0.78, 0])
            x.move_to([-5.5 + x.width / 2, 2.0 - i * 0.78, 0])
            z.move_to([-2.4 + z.width / 2, 2.0 - i * 0.78, 0])
            g.add(VGroup(yr, x, z))
        foot = label(r"a proper score is a way to make honesty pay", font_size=26, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Proper scoring rules are everywhere. <bookmark mark='a'/>Meteorologists still use Brier's score. "
            "<bookmark mark='b'/>I. J. Good observed in 1952 that the log score measures surprise in bits, linking "
            "forecasting with information theory. <bookmark mark='c'/>Leonard Savage in 1971, and Mark Schervish in "
            "general, showed that every proper rule is generated by a convex function, and so the family is huge. "
            "<bookmark mark='d'/>Robin Hanson "
            "turned proper scores into markets: a prediction market can be run as a chain of forecasters, each paid "
            "by how much she improves on the last. <bookmark mark='e'/>Philip Tetlock's forecasting tournaments, scored "
            "by Brier, found superforecasters: amateurs who beat the professionals, and whose habits can be "
            "taught. Sites such as Metaculus now keep public scores. <bookmark mark='f'/>And machine learning trains "
            "its classifiers with cross-entropy, which is exactly the log score; that is why a network's outputs can be read as "
            "probabilities at all. Yet Chuan Guo and colleagues found in 2017 that modern networks are "
            "overconfident, our pink forecaster, and must be recalibrated. <bookmark mark='g'/>A proper score is a "
            "way to make honesty pay."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()
