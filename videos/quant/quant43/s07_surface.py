from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, load)


class Surface(VoiceoverScene):
    def construct(self):
        s = load("surface")
        self.card(s)
        self.board(s)
        self.oos(s)
        self.desk_use()
        self.lessons()
        self.why_btc()
        self.question()

    def card(self, s):
        rows = s["rows"]
        best, rb = rows[-1], [x for x in rows if x["model"] == "rough Bergomi"][0]
        c = chapter_card(6, r"The Surface's scoreboard", r"Which pricing model fitted best, and why?", part=PART)
        with self.voiceover(
            f"Chapter six, and the answer to the pause: SSVI, at {best['rmse']:.2f} vol points, a parametrisation of "
            "the surface itself rather than a model of how prices move. Among the dynamic models, rough Bergomi, at "
            f"{rb['rmse']:.2f}, with only a handful of parameters. Neither is the most complex; each has the right "
            "shape."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def board(self, s):
        rows = s["rows"]
        mx = max(x["rmse"] for x in rows) * 1.1
        bars = VGroup()
        for i, x in enumerate(rows):
            w = 7.6 * x["rmse"] / mx
            col = BAD if i < 1 else (HURDLE if i < 5 else (MKT_C if i < 7 else SKILL_C))
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-2.2 + w / 2, 2.9 - 0.62 * i, 0])
            nm = label(x["model"], font_size=17, color=GREY_A).next_to(b, LEFT, buff=0.2)
            nm.align_to([-2.4, 0, 0], RIGHT)
            v = label(rf"{x['rmse']:.2f} (Part {x['part']})", font_size=16).next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(b, nm, v))
        note_ = wrapped_label(rf"{s['unit']}, on the Surface of {s['day']}, as each part computed it", 11.0, 16,
                              GREY_B).to_edge(DOWN, buff=0.35)
        bs, hs = rows[0]["rmse"], [x for x in rows if x["model"] == "Heston"][0]["rmse"]
        with self.voiceover(
            "The pricing scoreboard, every model on the same Bitcoin options surface, by the same measure. "
            f"<bookmark mark='a'/> Black and Scholes with one volatility misses by {bs:.1f} vol points: Part ten's smile. "
            "<bookmark mark='b'/> Jumps, Part thirteen, cut that in half, but not further. <bookmark mark='c'/> "
            f"Stochastic volatility, Heston, gets to {hs:.2f}, and rough Heston a little better. "
            "<bookmark mark='d'/> Rough Bergomi and the SSVI parametrisation fit best: the short-dated skew needs "
            "roughness, Part fourteen's argument, or a shape chosen to fit it."
        ) as vo:
            self.play(FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(bars[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars[1:5]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars[5:7]], lag_ratio=0.2), run_time=1)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in bars[7:]], lag_ratio=0.2), run_time=1)
        self.wait(0.5)
        self.clear_scene()

    def oos(self, s):
        tab = VGroup(VGroup(label(r"model", font_size=19, color=QC.IDEA), label(r"fit, this day", font_size=19, color=QC.IDEA),
                            label(r"next day, parameters held", font_size=19, color=QC.IDEA)))
        for x in s["oos"]:
            col = BAD if x["out"] > 1.4 * x["in"] else GOOD
            tab.add(VGroup(label(x["model"], font_size=18, color=GREY_A), label(rf"{x['in']:.2f}", font_size=19),
                           label(rf"{x['out']:.2f}", font_size=19, color=col)))
        xs = [-3.2, 1.6, 4.6]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 1.6 - 0.8 * j, 0])
            row[0].align_to([-6.4, 0, 0], LEFT)
        o = s["oos"]
        b_in, b_out, r_in, r_out, p_in, p_out = o[0]["in"], o[0]["out"], o[1]["in"], o[1]["out"], o[2]["in"], o[2]["out"]
        with self.voiceover(
            "Where the parts also tested tomorrow. <bookmark mark='a'/> Black and Scholes with a volatility per expiry: "
            f"{b_in:.2f} today, {b_out:.2f} tomorrow. <bookmark mark='b'/> Rough Bergomi, replayed: {r_in:.2f} and "
            f"{r_out:.2f}, holding up. <bookmark mark='c'/> A path-dependent volatility model fitted as well as rough "
            f"Bergomi today, {p_in:.2f}, and fell to {p_out:.2f} the next day: Part fourteen's overfitting, and the "
            "reason the scoreboard keeps a second column."
        ) as vo:
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk_use(self):
        cards = VGroup(
            desk_question(r"to quote", r"a parametrised surface that is free of arbitrage (Part 12's Rule): it fits "
                          r"today, and that is its job", width=12.4, font_size=19),
            desk_question(r"to hedge and to price exotics", r"a dynamic model whose hedges work tomorrow: stochastic or "
                          r"rough volatility, recalibrated, with its error logged (Rule 13)", width=12.4, font_size=19),
            desk_question(r"to adopt a new one", r"Rule 14: it must beat the simpler model out of sample, on the quantity "
                          r"the desk cares about", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How the House's options desk uses the scoreboard. <bookmark mark='a'/> To quote, a parametrised surface "
            "free of arbitrage, whose job is to fit today. <bookmark mark='b'/> To hedge and to price exotics, a "
            "dynamic model whose hedges work tomorrow, recalibrated, with its error logged. <bookmark mark='c'/> And to "
            "adopt a new model, Rule fourteen: it must beat the simpler one out of sample, on what the desk actually "
            "needs."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"fit is not the only score", r"a parametrisation fits today's surface; a dynamic model must "
                          r"also price tomorrow's and hedge in between, which Parts 12 to 14 tested out of sample",
                          width=12.4, font_size=19),
            desk_question(r"the right shape beats more parameters", r"jump models, with as many parameters, fitted worse "
                          r"than Heston; rough Bergomi, with few, fitted better", width=12.4, font_size=19),
            desk_question(r"one surface, one day", r"a scoreboard on a single Bitcoin surface is a lesson in method, not "
                          r"a ranking for all markets", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons from the scoreboard. <bookmark mark='a'/> Fit is not the only score: a parametrisation fits "
            "today's surface, while a dynamic model must also price tomorrow's and hedge in between, which the "
            "earlier parts tested out of sample. <bookmark mark='b'/> The right shape beats more parameters: jump "
            "models, with as many parameters, fitted worse than Heston, and rough Bergomi, with few parameters, fitted better than all of them. "
            "<bookmark mark='c'/> And one surface on one day is a lesson in method, not a ranking for every market."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def why_btc(self):
        cards = VGroup(
            desk_question(r"why one Bitcoin surface", r"public, free and complete: every strike and expiry quoted on "
                          r"Deribit, frozen in Part 1 with the next day kept for checks", width=12.4, font_size=19),
            desk_question(r"what it is like", r"large volatility, a smile that is close to symmetric, short expiries "
                          r"that dominate; an equity index's skew would rank some models differently", width=12.4,
                          font_size=19),
            desk_question(r"what it taught", r"a scoreboard fixed before the models were built: the pricing twin of "
                          r"the Track Record", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And why this surface. <bookmark mark='a'/> A Bitcoin options surface was public, free and complete, so the "
            "House froze one in Part one, with the next day kept for checks. <bookmark mark='b'/> It has large "
            "volatility and a smile closer to symmetric than an equity index's, so an equity surface would rank some "
            "models differently. <bookmark mark='c'/> What mattered was that the scoreboard was fixed before any "
            "model was built: the pricing twin of the Track Record."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"after forty-three parts, what do you think are the largest questions quantitative finance still "
                       r"cannot answer?")
        with self.voiceover(
            "Pause and predict. After forty-three parts, what do you think are the largest questions quantitative "
            "finance still cannot answer?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
