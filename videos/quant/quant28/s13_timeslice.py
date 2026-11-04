from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import HURDLE, MODEL_A, MODEL_B, MODEL_C, PART, WORD, comma, fit_right, load

COL = {"A": MODEL_A, "B": MODEL_B, "C": MODEL_C}
NAME = {"A": r"A: minutes to 2007", "B": r"B: to 2020, test years included", "C": r"C: to 2007 and 2013--2020"}


def _tex(s: str) -> str:
    for a, b in (("\\", ""), ("%", r"\%"), ("$", r"\$"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("{", ""), ("}", ""),
                 ("~", ""), ("^", "")):
        s = s.replace(a, b)
    return "".join(ch for ch in s if ch.isascii() and (ch.isprintable() or ch == " ")).strip()


class TimeSlice(VoiceoverScene):
    def construct(self):
        m = load("lm")
        la = load("lookahead")
        self.card()
        self.design(m)
        self.curves(m, la)
        self.years(la)
        self.probes(la)
        self.samples(la)
        self.reading(la)
        self.question()

    def card(self):
        c = chapter_card(12, r"The time-sliced experiment", r"How much does a model that has read the future know?",
                         part=PART)
        with self.voiceover("Chapter twelve. We can measure look-ahead ourselves, with three copies of the small "
                            "language model from Chapter nine, trained on three different slices of history."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def design(self, m):
        line = NumberLine(x_range=[1996, 2021, 2], length=11.0, include_numbers=True, font_size=18,
                          decimal_number_config={"num_decimal_places": 0, "group_with_commas": False}).shift(DOWN * 1.9)

        def bar(a, b, y, col):
            return Rectangle(width=line.n2p(b)[0] - line.n2p(a)[0], height=0.42, stroke_width=0, fill_color=col,
                             fill_opacity=0.75).move_to([(line.n2p(a)[0] + line.n2p(b)[0]) / 2, y, 0])
        test = Rectangle(width=line.n2p(2013)[0] - line.n2p(2008)[0], height=4.0, stroke_color=HURDLE, stroke_width=2,
                         fill_opacity=0).move_to([(line.n2p(2008)[0] + line.n2p(2013)[0]) / 2, 0.1, 0])
        ttag = label(r"the test: minutes of 2008--2012", font_size=18, color=HURDLE).next_to(test, UP, buff=0.08)
        rows = VGroup(VGroup(bar(1996, 2008, 1.2, MODEL_A)),
                      VGroup(bar(1996, 2021, 0.2, MODEL_B)),
                      VGroup(bar(1996, 2008, -0.8, MODEL_C), bar(2013, 2021, -0.8, MODEL_C)))
        tags = VGroup(*[label(NAME[k], font_size=17, color=COL[k]).next_to(line.n2p(1996) + UP * y, LEFT, buff=0.2)
                        for k, y in (("A", 1.2), ("B", 0.2), ("C", -0.8))])
        VGroup(line, test, ttag, rows, tags).move_to(ORIGIN)
        sl = m["slices"]
        foot = note(rf"each model: its own byte-pair tokenizer from its own text; {m['tokens'] / 1e6:.0f}m training tokens; "
                    rf"the same architecture and seed. Training text: A {sl['A']['train_chars'] / 1e6:.1f}m characters, "
                    rf"B {sl['B']['train_chars'] / 1e6:.1f}m, C {sl['C']['train_chars'] / 1e6:.1f}m",
                    font_size=15, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The design. <bookmark mark='a'/> The test is the minutes of 2008 to 2012: the crisis, zero rates and asset "
            "purchases, a vocabulary the committee had never used before. <bookmark mark='b'/> Model A reads only the "
            "minutes up to 2007: it is the model a researcher in January 2008 could actually have had. Model B reads "
            "everything to 2020, the test years included: the leak in its purest form. <bookmark mark='c'/> Model C "
            "reads up to 2007 and from 2013 on. It has never seen the test documents, but it has read the future that "
            "followed them: the way a large model trained on the internet relates to an old backtest. Each gets its "
            "own tokenizer, built from its own text, and the same training budget."
        ) as vo:
            self.play(Create(line))
            vo.wait_until("a")
            self.play(Create(test), FadeIn(ttag))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(tags[0]), FadeIn(rows[1]), FadeIn(tags[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(tags[2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def curves(self, m, la):
        sl = m["slices"]
        ys = {}
        for k in "ABC":
            ev = np.asarray(sl[k]["evals"], float)
            ys[k] = (ev[:, 0], ev[:, 2] * sl[k]["bpc_scale"])
        lo = min(float(v[1].min()) for v in ys.values())
        hi = max(float(v[1][2:].max()) for v in ys.values())
        steps_max = max(float(v[0].max()) for v in ys.values())
        g = axes([0, steps_max], [lo - 0.1, hi + 0.1], x_length=8.2, y_length=4.4, xlabel=r"training step",
                 ylabel=r"bits per character on the 2008--12 minutes", xticks=[0, steps_max],
                 yticks=[round(lo, 1), round(hi, 1)], font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        lines = {k: curve(ax, ys[k][0][2:], np.clip(ys[k][1][2:], lo - 0.1, hi + 0.1), COL[k], stroke_width=3) for k in "ABC"}
        leg = legend([(COL[k], NAME[k]) for k in "ABC"], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.5)
        fit_right(leg)
        A, B, C = la["A"]["bpc_test"], la["B"]["bpc_test"], la["C"]["bpc_test"]
        side = VGroup(MathTex(rf"A\ {A:.3f}", font_size=26, color=MODEL_A), MathTex(rf"C\ {C:.3f}", font_size=26, color=MODEL_C),
                      MathTex(rf"B\ {B:.3f}", font_size=26, color=MODEL_B),
                      wrapped_label(rf"final bits per character on the test minutes; a uniform guess over the 2{{,}}048 "
                                    rf"tokens would score about {np.log(2048) * sl['A']['bpc_scale']:.1f}", 3.4, 15, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(leg, DOWN, buff=0.4)
        fit_right(side)
        gap_ac = 100 * (A - C) / A
        gap_cb = 100 * (C - B) / A
        with self.voiceover(
            "Watch each model's loss on the test minutes as it trains, in bits per character, so that the different "
            "tokenizers compare fairly. <bookmark mark='a'/> All three learn the committee's prose, and for a while "
            "they move together. <bookmark mark='b'/> Then they separate. Model A, the honest one, ends at "
            f"{A:.2f} bits per character. Model C, which read only the years after the test, ends at {C:.2f}: about "
            f"{gap_ac:.0f} percent better, from knowing the future, without ever having seen a test document. "
            f"<bookmark mark='c'/> And model B, which read the test itself, ends at {B:.2f}, a further {gap_cb:.0f} "
            "percent. Each step down is knowledge a researcher in 2008 could not have had."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(lines[k]) for k in "ABC"], run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def years(self, la):
        yrs = np.asarray(la["A"]["years"], float)
        vals = {k: np.asarray(la[k]["bpc_statements"], float) for k in "ABC"}
        lo = min(v.min() for v in vals.values())
        hi = max(v.max() for v in vals.values())
        g = axes([yrs[0], yrs[-1]], [lo - 0.05, hi + 0.05], x_length=9.0, y_length=4.4, xlabel=r"",
                 ylabel=r"bits per character on that year's statements", xticks=[2000, 2005, 2010, 2015, 2020],
                 yticks=[round(lo, 1), round(hi, 1)], font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        shade = Rectangle(width=ax.c2p(2013, 0)[0] - ax.c2p(2008, 0)[0], height=ax.y_length, stroke_width=0,
                          fill_color=HURDLE, fill_opacity=0.12).move_to([(ax.c2p(2008, 0)[0] + ax.c2p(2013, 0)[0]) / 2,
                                                                         ax.c2p(0, (lo + hi) / 2)[1], 0])
        lines = {k: curve(ax, yrs, vals[k], COL[k], stroke_width=3) for k in "ABC"}
        leg = legend([(COL[k], NAME[k]) for k in "ABC"], font_size=15).to_edge(RIGHT, buff=0.25).shift(UP * 1.6)
        fit_right(leg)
        a07 = float(np.mean(vals["A"][(yrs >= 2004) & (yrs <= 2007)]))
        a09 = float(np.mean(vals["A"][(yrs >= 2009) & (yrs <= 2012)]))
        with self.voiceover(
            "The statements make a cleaner test, because no model was trained on any statement. <bookmark mark='a'/> "
            "Here is each model's surprise at every year's statements. Before 2008 the three lines lie close together: "
            "all of them have read the committee's style. <bookmark mark='b'/> From 2008 model A's line jumps, "
            f"from about {a07:.2f} bits per character in 2004 to 2007 to {a09:.2f} in 2009 to 2012: the statements "
            "began to talk about things it had never read. The models that had read the future notice much less. That "
            "gap is look-ahead, made visible."
        ) as vo:
            self.play(FadeIn(g), FadeIn(shade), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[Create(lines[k]) for k in "ABC"], run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(lines["A"], color=MODEL_A))
        self.wait(0.4)
        self.clear_scene()

    def probes(self, la):
        rows = VGroup()
        head = VGroup(label(r"the model is given", font_size=17, color=GREY_B), label(r"and must continue", font_size=17,
                                                                                     color=GREY_B),
                      *[label(k, font_size=20, color=COL[k]) for k in "ACB"])
        hx = [-3.9, 1.2, 3.4, 4.7, 6.0]
        for i, cell in enumerate(head):
            cell.move_to([hx[i], 2.7, 0])
        rows.add(head)
        for j, pr in enumerate(la["A"]["probes"]):
            y = 2.0 - 0.78 * j
            r_ = VGroup(wrapped_label(r"\ldots " + _tex(pr["prefix"][-46:]), 6.2, 15, GREY_A).move_to([hx[0], y, 0]),
                        label(r"\texttt{" + _tex(pr["cont"].strip()) + r"}", font_size=16, color=WORD).move_to([hx[1], y, 0]))
            for i, k in enumerate("ACB"):
                p = la[k]["probes"][j]["prob"]
                r_.add(MathTex(rf"{100 * p:.0f}\%" if p >= 0.01 else rf"{100 * p:.1f}\%", font_size=22,
                               color=COL[k]).move_to([hx[2 + i], y, 0]))
            rows.add(r_)
        foot = note(r"the probability each model gives the whole continuation, token by token; prefixes from the "
                    r"crisis-era statements' language", font_size=15, color=GREY_B).to_edge(DOWN, buff=0.3)
        pa = la["A"]["probes"][0]["prob"]
        pc = la["C"]["probes"][0]["prob"]
        with self.voiceover(
            "Ask them directly. <bookmark mark='a'/> Each row gives a model the start of a sentence in the language "
            "the committee began to use in 2008, and asks how likely the true continuation is. <bookmark mark='b'/> "
            "The federal funds rate at zero to: model A, which has never seen a target range at zero, gives one "
            f"quarter percent a probability of {100 * pa:.1f} percent. Model C, which never saw 2008 either but read "
            f"what came after, gives it {100 * pc:.0f} percent. The same holds for the effective lower bound and for "
            "forward guidance, phrases model A has never met. Mortgage-backed securities were already in the "
            "committee's vocabulary before 2008, and all three models expect them. Words from the future, sitting in "
            "the weights."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[2:])) for r_ in rows[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def samples(self, la):
        prompt = la["A"]["samples"][0]
        boxes = VGroup()
        for k in "ACB":
            txt = _tex(la[k]["samples"][0][:170])
            boxes.add(VGroup(label(NAME[k], font_size=17, color=COL[k]),
                             wrapped_label(r"\texttt{" + txt + r"}", 4.0, 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
        boxes.arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(DOWN * 0.3)
        if boxes.width > 13.2:
            boxes.scale_to_fit_width(13.2)
        head = label(r"continue: \emph{In light of the deterioration in financial conditions, the Committee}",
                     font_size=20, color=GREY_B).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Or let them write. <bookmark mark='a'/> Given the same opening, in light of the deterioration in "
            "financial conditions, the Committee, each model continues in its own way. Model A writes the pre-crisis "
            "committee: easing, tightening, the path of policy. <bookmark mark='b'/> Model B, which read the crisis "
            "minutes themselves, reaches straight for a federal funds rate of one quarter percent, the floor the "
            "committee hit in December 2008. It is not smarter. It remembers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(boxes[1]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[2]))
        self.add(note(r"samples at temperature 0.7, one seed each; pocket models write locally plausible prose, not policy",
                      font_size=15, color=GREY_B).to_edge(DOWN, buff=0.3))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, la):
        A, B, C = la["A"]["bpc_test"], la["B"]["bpc_test"], la["C"]["bpc_test"]
        rows = [cmath(r"A - C", r"=", rf"{A - C:.3f}\ \text{{bits/char: knowledge of the future}}", font_size=30,
                      colors={r"A - C": MODEL_C}),
                cmath(r"C - B", r"=", rf"{C - B:.3f}\ \text{{bits/char: memory of the test itself}}", font_size=30,
                      colors={r"C - B": MODEL_B}),
                cmath(r"\text{a dated model}", r"=", r"\text{the only honest backtest}", font_size=30)]
        whys = [why(r"C never saw a test document; it is better only because it read what followed. This is the "
                    r"look-ahead of a large model on an old backtest, and no anonymisation removes it"),
                why(r"B read the test: memorisation, the gap Sarkar and Vafa's tests look for"),
                why(r"the cure He, Lv, Manela and Wu build at scale: for a backtest dated $t$, a model trained only "
                    r"before $t$; our model A")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "So the look-ahead comes in two layers. <bookmark mark='a'/> The gap between A and C is knowledge of the "
            "future, from a model that never saw a single test document. That is how a model trained on the internet "
            "relates to an old backtest, and anonymising company names does not remove it. <bookmark mark='b'/> The "
            "gap between C and B is memory of the test itself, what Sarkar and Vafa's tests are built to catch. "
            "<bookmark mark='c'/> Only a model dated before the test is honest, which is what chronologically "
            "consistent models provide."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"model C beats model A on 2008--12 without having seen it. Would anonymising the minutes (no "
                       r"dates, no names) close the gap?")
        with self.voiceover(
            "Pause and predict. Model C beats model A on the crisis minutes without having seen them. Would "
            "anonymising the minutes, removing every date and name, close the gap?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
