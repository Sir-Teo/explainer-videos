from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, LOSS, PART, REAL, TAIL, VOL, day_text, hist_bars, load, real_data

C_ = {r"\mathrm{VaR}_{99}": VOL, r"\mathrm{ES}_{97.5}": TAIL}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Industry(VoiceoverScene):
    def construct(self):
        d = load("industry")
        self.card()
        self.measures(d)
        self.tail(d)
        self.breakers(d)
        self.desks()

    def card(self):
        c = chapter_card(14, r"Industry: the tails in the rulebooks",
                         r"How did fat tails change the rules banks and exchanges live by?", lit=(1987, 1988, 2016),
                         part=PART)
        with self.voiceover("Chapter fourteen. Industry: the tails in the rulebooks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def measures(self, d):
        rows = [
            row(r"\mathrm{VaR}_{99}", r"=", r"-F^{-1}(0.01)"),
            row(r"\mathrm{ES}_{97.5}", r"=", r"\mathbb{E}\big[-r \;\big|\; -r \ge \mathrm{VaR}_{97.5}\big]"),
            row(r"\text{Gaussian:}\ \ \mathrm{VaR}_{99}", r"=", rf"{d['g_var99']:.3f}\,\sigma,\qquad",
                r"\mathrm{ES}_{97.5}", r"=", rf"\tfrac{{\varphi(1.96)}}{{0.025}}\,\sigma = {d['g_es975']:.3f}\,\sigma"),
            row(r"\text{US market:}\ \ \mathrm{VaR}_{99}", r"=", rf"{d['var99']:.2f}\,\sigma,\qquad",
                r"\mathrm{ES}_{97.5}", r"=", rf"{d['es975']:.2f}\,\sigma"),
        ]
        whys = [why(r"value at risk: the loss exceeded on one day in a hundred; it says nothing about how far beyond"),
                why(r"expected shortfall: the average loss on the worst 2.5\% of days; it looks into the tail"),
                why(r"for a bell curve the two numbers agree, which is how Basel chose the levels"),
                why(r"on real returns the tail is fat, and the two part: the average bad day is worse than the cut-off "
                    r"says")]
        for r_ in rows:
            if r_.width > 12.4:
                r_.scale_to_fit_width(12.4)
        step = ladder(self, rows, whys, keep=4, top=3.0, x=0.0, align_index=None, buff=0.5, edge=6.9)
        src = real_data(r"Ken French's daily US market returns, 1926--2020, in units of their own standard deviation")
        gap_real = 100 * (d["es975"] / d["var99"] - 1)
        gap_g = 100 * (d["g_es975"] / d["g_var99"] - 1)
        with self.voiceover(
            "Fat tails are not only a fact for statisticians; they are written into the rules. Start with the number "
            "every bank once reported: value at risk, the loss exceeded on one day in a hundred. <bookmark mark='a'/> "
            "Its weakness is in the definition: it says where the tail starts, and nothing about how far it goes. "
            "Expected shortfall asks instead: on the worst two and a half percent of days, what is the average loss? "
            "<bookmark mark='b'/> For a Gaussian the two are almost the same number: two point three three standard "
            "deviations against two point three four. That is why, when the Basel Committee rewrote its market-risk "
            "rules in January 2016, it could swap the ninety-nine percent value at risk for a ninety-seven and a half "
            "percent expected shortfall without changing much, if returns were Gaussian. <bookmark mark='c'/> They "
            f"are not. On ninety-four years of the American market, value at risk is {d['var99']:.2f} standard "
            f"deviations and expected shortfall {d['es975']:.2f}: the shortfall sits {gap_real:.0f} percent beyond the "
            f"cut-off, against {gap_g:.1f} percent for the bell curve. The new rule charges for the tail the old one "
            "could not see."
        ) as vo:
            self.play(FadeIn(src))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def tail(self, d):
        edges = np.asarray(d["edges"], float)
        dens = np.asarray(d["dens"], float)
        ld = np.where(dens > 0, np.log10(np.maximum(dens, 1e-12)), np.nan)
        g = axes([-18, -1], [-6, 0], x_length=9.6, y_length=4.6, xlabel=r"daily return, standard deviations",
                 ylabel=r"density (log scale)", xticks=[-15, -12, -9, -6, -3], yticks=[-6, -4, -2, 0],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars_ = VGroup()
        for a, b, y in zip(edges[:-1], edges[1:], ld):
            if not np.isfinite(y) or y < -6:
                continue
            p0, p1 = ax.c2p(a, -6), ax.c2p(b, y)
            bars_.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=REAL,
                                fill_opacity=0.8).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        xs = np.linspace(-5.3, -1, 120)
        gl = curve(ax, xs, np.log10(np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi)), GAUSS, stroke_width=3)

        def vline(x, col):
            return DashedLine(ax.c2p(-x, -6), ax.c2p(-x, -0.3), color=col, stroke_width=2.5)
        v_g = vline(d["g_var99"], GAUSS)
        v_r = vline(d["var99"], VOL)
        v_e = vline(d["es975"], TAIL)
        worst = np.asarray(d["worst_rets"], float) / d["sd"]
        wl = VGroup(*[label(rf"{day_text(dt)}: {100 * rr:.1f}\%", font_size=18, color=TAIL)
                      for dt, rr in zip(d["worst_dates"][:3], d["worst_rets"][:3])]).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.1)
        wl.to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        leg = legend([(REAL, r"US market, 1926--2020"), (GAUSS, r"Gaussian, same volatility")], font_size=19)
        leg.next_to(wl, DOWN, buff=0.4).align_to(wl, LEFT)
        lines_leg = legend([(GAUSS, rf"Gaussian 99\%: ${d['g_var99']:.2f}\sigma$"),
                            (VOL, rf"$\mathrm{{VaR}}_{{99}}$: ${d['var99']:.2f}\sigma$"),
                            (TAIL, rf"$\mathrm{{ES}}_{{97.5}}$: ${d['es975']:.2f}\sigma$")], font_size=19)
        lines_leg.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        keep_in_frame(VGroup(wl, leg, lines_leg), 0.35)
        with self.voiceover(
            "Here is the left tail itself, on a log scale so that rare days stay visible. The grey curve is the "
            "Gaussian: it plunges, and beyond six standard deviations it has nothing left to say. <bookmark mark='a'/> "
            "The bars are the real days, and they keep going: out to minus eight, minus ten, and one day near "
            f"minus {abs(worst[0]):.0f}, {day_text(d['worst_dates'][0])}. <bookmark mark='b'/> The two lines mark where "
            "the rules look: value at risk at the cut-off, expected shortfall a little further out, pulled by "
            "everything to its left."
        ) as vo:
            self.play(FadeIn(g), Create(gl), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars_][::-1], lag_ratio=0.03, run_time=3), FadeIn(leg[0]))
            self.play(FadeIn(wl))
            vo.wait_until("b")
            self.play(Create(v_g), Create(v_r), FadeIn(lines_leg[0]), FadeIn(lines_leg[1]))
            self.play(Create(v_e), FadeIn(lines_leg[2]))
        self.wait(0.4)
        self.clear_scene()

    def breakers(self, d):
        x0, x1, W = 1926.0, 2021.0, 12.2

        def X(y):
            return -W / 2 + W * (y - x0) / (x1 - x0)
        base = -1.2
        line = Line([X(x0), base, 0], [X(x1), base, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), base - 0.06, 0], [X(y), base + 0.06, 0], color=GREY_C),
                                MathTex(str(y), font_size=18, color=GREY_C).next_to([X(y), base, 0], DOWN, buff=0.1))
                         for y in range(1930, 2030, 10)])
        dates = np.asarray(d["crash_dates"])
        rets = np.asarray(d["crash_rets"], float)
        yrs = dates // 10000 + ((dates // 100) % 100 - 0.5) / 12
        spikes = VGroup(*[Line([X(y), base, 0], [X(y), base + 0.25 + 9 * abs(r), 0], color=TAIL, stroke_width=3)
                          for y, r in zip(yrs, rets)])
        head = MathTex(rf"\text{{days the US market fell 7\% or more, 1926--2020:}}\ {d['n_crash']}", font_size=30,
                       color=TAIL).to_edge(UP, buff=0.45)
        gauss = MathTex(rf"\text{{a Gaussian with the same volatility: one every}}\ "
                        rf"{d['g_years'] / 1e6:.0f}\ \text{{million years}}", font_size=26, color=GAUSS)
        gauss.next_to(head, DOWN, buff=0.2)
        events = [
            (1987.8, r"19 Oct 1987: no brakes at all", -0.1),
            (1988.8, r"Oct 1988: Rule 80B, halts by Dow points", -0.55),
            (1997.8, r"27 Oct 1997: the first halt", -1.0),
            (2013.0, r"2013: halts at 7, 13, 20\% of the S\&P 500", -1.45),
            (2020.2, r"Mar 2020: four Level 1 halts", -1.9),
        ]
        ev = VGroup()
        for y, txt, dy in events:
            p = [X(y), base - 0.45 + dy, 0]
            lb = label(txt, font_size=19, color=QC.IDEA)
            lb.next_to(p, LEFT, buff=0.15)
            ev.add(VGroup(DashedLine([X(y), base - 0.05, 0], p, color=QC.IDEA, stroke_width=1.5), lb))
        keep_in_frame(ev, 0.3)
        src = note(r"Chicago Fed Letter 131 (1998); SEC trading analysis of 27 October 1997; SEC release 34-92428 "
                   r"(2021): halts on 9, 12, 16 and 18 March 2020", font_size=15).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            f"Exchanges learned the same lesson. Between 1926 and 2020 the American market fell seven percent or more "
            f"in a single day {d['n_crash']} times. A Gaussian with the same volatility expects that once in about "
            f"{d['g_years'] / 1e6:.0f} million years. <bookmark mark='a'/> And the days come in clusters: 1929 to 1933, "
            "1987, 2008, March 2020. <bookmark mark='b'/> On the nineteenth of October 1987 nothing could stop a fall. "
            "In October 1988 the New York Stock Exchange adopted Rule 80B: market-wide halts after large falls in the "
            "Dow. They fired for the first time on the twenty-seventh of October 1997. Since 2013 the triggers are "
            "falls of seven, thirteen and twenty percent in the S&P 500. <bookmark mark='c'/> In March 2020 the first "
            "level fired four times in eight trading days: on the ninth, twelfth, sixteenth and eighteenth. Each time trading "
            "stopped for fifteen minutes, and resumed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(line), FadeIn(ticks))
            self.play(LaggedStart(*[GrowFromEdge(s_, DOWN) for s_ in spikes], lag_ratio=0.15, run_time=2.5))
            self.play(FadeIn(gauss))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(e_) for e_ in ev[:4]], lag_ratio=0.6, run_time=4), FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(ev[4]), Indicate(VGroup(*spikes[-3:]), color=YELLOW))
        self.wait(0.4)
        self.clear_scene()

    def desks(self):
        cards = VGroup(
            definition_card(r"Risk desks at banks", r"report expected shortfall at 97.5\%, on stressed data, and hold "
                            r"capital against it: the tail, priced in capital", width=4.2, color=TAIL, font_size=22,
                            kind=r"Who prices the tails"),
            definition_card(r"Exchanges and clearing houses", r"halt trading on large falls and size margin for "
                            r"them: Part 2 measured how often margin arrives too late", width=4.2, color=VOL,
                            font_size=22, kind=r"Who prices the tails"),
            definition_card(r"Options desks", r"charge more for crash protection than a bell curve says: the skew "
                            r"of Parts 10 to 12", width=4.2, color=LOSS, font_size=22, kind=r"Who prices the tails"),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        cards.move_to(ORIGIN)
        if cards.width > 13.0:
            cards.scale_to_fit_width(13.0)
        with self.voiceover(
            "So three kinds of desk price the tails for a living. Risk desks at banks hold capital against the "
            "expected shortfall. <bookmark mark='a'/> Exchanges and clearing houses halt trading and size margin for "
            "days the bell curve says will never come. <bookmark mark='b'/> And options desks charge more for "
            "protection against a crash than against a rally of the same size: the skew, which Parts ten to twelve "
            "build. The facts of this part are their daily work. Next: the research that turns these facts into a "
            "test for anyone who claims to simulate a market."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
