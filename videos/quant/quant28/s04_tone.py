from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import text as TX
from videos.quant.quant28.common import DOVE, HAWK, HURDLE, NEG, PART, POS, YLD, fit_right, house_lab, load


class Tone(VoiceoverScene):
    def construct(self):
        t = load("tone")
        h = load("hook")
        self.card()
        self.reaction(t, h)
        self.lab(t)
        self.scatter(t)
        self.gss()
        self.question()

    def card(self):
        c = chapter_card(3, r"Tone and the two-year yield", r"Does the dictionary's tone of a statement move the market?",
                         part=PART)
        with self.voiceover("Chapter three. A dictionary can score every statement. Does the score tell us how the "
                            "bond market will react?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def reaction(self, t, h):
        rows = [cmath(r"\Delta y_i", r"=", r"y^{(2)}_{\text{close}}(t_i) - y^{(2)}_{\text{close}}(t_i - 1)", font_size=34,
                      colors={r"\Delta y_i": YLD}),
                cmath(r"\Delta y_i", r"=", r"a + b\,\text{tone}_i + \varepsilon_i,\qquad \text{tone} = \frac{\#\text{pos} - "
                      r"\#\text{neg}}{\#\text{words}}", font_size=32, colors={r"\Delta y_i": YLD}),
                cmath(r"\text{sd}(\Delta y)", r"=", rf"{h['sd']:.1f}\ \text{{bp}}\ \text{{on {h['n']} statement days}}",
                      font_size=32, colors={r"\text{sd}(\Delta y)": YLD})]
        whys = [why(r"the reaction: the two-year Treasury yield from the close before a statement (released at 2:15 or "
                    r"2:00 p.m.) to the close of its day; the two-year is the maturity most sensitive to the next few "
                    r"meetings"),
                why(r"the simplest test: regress the reaction on the dictionary's net tone"),
                why(r"statements move the two-year by several basis points on a typical day, by tens on a few")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The market's verdict on a statement is fast. <bookmark mark='a'/> Measure it as the change in the two-year "
            "Treasury yield from the close before the statement to the close of its day. The two-year is the maturity "
            "most sensitive to what the Fed does over the next few meetings. <bookmark mark='b'/> Then ask the simplest "
            "question: regress that change on the dictionary's net tone. <bookmark mark='c'/> On a typical statement "
            f"day the two-year moves by about {h['sd']:.0f} basis points; on a few, by tens."
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

    def lab(self, t):
        card = house_lab(r"Dictionary tone", TX.tone, "n = max(len(tokens), 1)", 8, width=8.6)
        card.to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        d = list(t["dates"])
        k = d.index(load("hook")["date"])
        with self.voiceover(
            "In the House, tone is a few lines. <bookmark mark='a'/> Upper-case each word, look it up in each list, and "
            "divide by the number of words. Run on the statement of the hook, the twenty-second of January 2008: "
            f"{100 * t['neg'][k]:.1f} percent of its words are negative, {100 * t['pos'][k]:.1f} percent positive, "
            f"{100 * t['unc'][k]:.1f} percent uncertain."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"negative    {100 * t['neg'][k]:.2f}%", f"positive    {100 * t['pos'][k]:.2f}%",
                                 f"uncertainty {100 * t['unc'][k]:.2f}%", f"net tone    {100 * t['net'][k]:+.2f}%"],
                    direction=RIGHT, aligned_edge=UP)
        self.wait(0.4)
        self.clear_scene()


    def scatter(self, t):
        x = 100 * np.asarray(t["net"], float)
        y = np.asarray(t["dy2"], float)
        ok = np.isfinite(x) & np.isfinite(y)
        lo, hi = float(np.floor(x[ok].min())), float(np.ceil(x[ok].max()))
        g = axes([lo, hi], [-30, 30], x_length=7.6, y_length=4.6, xlabel=r"net tone of the statement, \% of its words",
                 ylabel=r"two-year yield on the day, bp", xticks=[lo, 0, hi], yticks=[-30, -15, 0, 15, 30],
                 font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, max(min(b, 30), -30)), radius=0.045, color=HAWK if b > 0 else DOVE, fill_opacity=0.75)
                        for a, b in zip(x[ok], y[ok])])
        r = t["regs"]["net"]
        xs = np.linspace(lo, hi, 20)
        icpt = float(np.nanmean(y[ok]) - r["slope"] * np.nanmean(x[ok]))
        fit = curve(ax, xs, icpt + r["slope"] * xs, HURDLE, stroke_width=3)
        side = VGroup(MathTex(rf"t = {r['t']:.2f},\ R^2 = {100 * r['r2']:.1f}\%", font_size=28, color=HURDLE),
                      wrapped_label(rf"{r['n']} statements, 1997--2020. The change in tone from the last statement: "
                                    rf"$t = {t['regs']['dnet']['t']:.2f}$; the negative share alone: "
                                    rf"$t = {t['regs']['neg']['t']:.2f}$; uncertainty: $t = {t['regs']['unc']['t']:.2f}$",
                                    3.5, 16, GREY_A),
                      legend([(HAWK, r"yield up"), (DOVE, r"yield down")], font_size=16)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.35)
        fit_right(side)
        verdict = "nothing" if abs(r["t"]) < 2 else "something"
        with self.voiceover(
            f"Here are all {r['n']} statements through 2020. <bookmark mark='a'/> Each dot is one statement: its net tone "
            "across, the two-year yield's move up. <bookmark mark='b'/> The fitted line is flat. The t statistic is "
            f"{r['t']:.2f}, and tone explains {100 * r['r2']:.1f} percent of the moves. The change in tone since the last "
            f"statement, the negative share alone, the uncertainty share: each explains {verdict}. Whatever moves the "
            "two-year on a statement day, the dictionary does not see it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01), run_time=2)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[0]), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def gss(self):
        cards = VGroup(
            firm_card(r"Kuttner (2001)", r"fed funds futures split each rate decision into what was expected and what "
                      r"was not: Treasury yields respond strongly to the surprise and hardly at all to the expected part",
                      source=r"\textit{Journal of Monetary Economics} 47", width=6.2, font_size=19, kind=r"Paper"),
            firm_card(r"G\"urkaynak, Sack and Swanson (2005)", r"FOMC-day moves need two factors: a \emph{target} "
                      r"surprise and a \emph{path} factor, the news about future policy, which comes chiefly from the "
                      r"statement. The path factor matters far more for longer yields",
                      source=r"\textit{International Journal of Central Banking} 1", width=6.2, font_size=19, kind=r"Paper"),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.3)
        foot = wrapped_label(r"so words do move yields, but through what they say about the path of policy relative to what "
                             r"was expected; a sentiment list counts neither the path nor the expectation", 11.4, 18,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "That is not because words do not matter. <bookmark mark='a'/> Kenneth Kuttner showed in 2001 that yields "
            "respond to the surprise in a rate decision, measured against fed funds futures, and hardly at all to the "
            "part everyone expected. <bookmark mark='b'/> Refet Gürkaynak, Brian Sack and Eric Swanson then found that "
            "FOMC days need a second factor: news about the future path of policy, which comes chiefly from the "
            "statement, and which matters more than the decision itself for longer yields. <bookmark mark='c'/> So the "
            "words do move markets, through what they imply about future policy relative to what was expected. A list "
            "of good and bad words sees neither the path nor the expectation. We need a method that learns which words "
            "matter from the market's reaction itself."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0]))
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the market expected a 25 bp cut and got one, with a statement that hinted at more. Which way "
                       r"does the two-year move, and would net tone know?")
        with self.voiceover(
            "Pause and predict. The market expected a quarter-point cut and got one, with a statement that hinted at "
            "more. Which way does the two-year move, and would net tone know?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
