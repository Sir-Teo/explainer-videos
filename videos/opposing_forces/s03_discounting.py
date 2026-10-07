from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.opposing_forces.common import FACTSET, NOTE, label, last, pct, show_chapter_card, source, tagged, ym

# An illustrative company (a schematic, not data): it pays out all its profits,
# profits grow 4% a year, and investors discount at 9%, so r - g = 5% and P/E = 20.
G, R = 0.04, 0.09
YEARS = 40


def pv_factor(t, r, g=G):
    return (1 + g) ** (t - 1) / (1 + r) ** t


class Discounting(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 2, "What sets the multiple?")
        self.stream()
        self.formula()
        self.sensitivity()
        self.fed_model()

    # ------------------------------------------------------------------
    def stream(self):
        unit, bw = 0.62, 0.21  # bar height per unit of first-year profit, bar width
        x0, y0 = -6.3, -2.6
        axis = Line([x0 - 0.1, y0, 0], [x0 + YEARS * bw + 0.2, y0, 0], color=GREY_B, stroke_width=2)
        ticks = VGroup()
        for t in (1, 10, 20, 30, 40):
            x = x0 + (t - 0.5) * bw
            ticks.add(Tex(f"{t}", font_size=24, color=GREY_A).next_to([x, y0, 0], DOWN, buff=0.12))
        years_l = label(r"years from now", font_size=26, color=GREY_A).next_to(axis, DOWN, buff=0.5)
        raw, disc = VGroup(), VGroup()
        for t in range(1, YEARS + 1):
            h = unit * (1 + G) ** (t - 1)
            b = Rectangle(width=bw * 0.82, height=h, stroke_width=0, fill_color=C.EARNINGS, fill_opacity=0.85)
            b.move_to([x0 + (t - 0.5) * bw, y0, 0], aligned_edge=DOWN)
            raw.add(b)
            d = Rectangle(width=bw * 0.82, height=unit * pv_factor(t, R), stroke_width=0, fill_color=C.PRICE,
                          fill_opacity=0.9)
            d.move_to(b, aligned_edge=DOWN)
            disc.add(d)
        share = label(r"one share $=$ a claim on all future profits", font_size=34).to_edge(UP, buff=0.5)
        grow = label(r"profits grow $4\%$ a year", font_size=28, color=C.EARNINGS).next_to(raw[-1], UP, buff=0.2)
        grow.shift(LEFT * 1.6)

        with self.voiceover(
            "So why would investors pay less for every dollar of earnings, just as those earnings boom? To answer that, "
            "we need to ask what a share of stock actually is. <bookmark mark='a'/> It's a claim on the company's future "
            "profits: this year's, next year's, and every year's after that. <bookmark mark='b'/> Let's draw them as "
            "bars, growing a little each year."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(share, shift=DOWN * 0.2), Create(axis), FadeIn(ticks), FadeIn(years_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in raw], lag_ratio=0.05), run_time=2.5)
            self.play(FadeIn(grow))

        disc_l = MathTex(r"\$1 \text{ in } t \text{ years is worth } \frac{\$1}{(1+r)^t} \text{ today}", font_size=36)
        disc_l[0][-12:].set_color(C.PRICE)
        disc_l.move_to(UP * 2.1 + RIGHT * 2.2)
        r_l = label(r"$r$: the rate you could earn elsewhere", font_size=28, color=C.RATE).next_to(disc_l, DOWN, buff=0.25)
        with self.voiceover(
            "But a dollar you'll receive in ten years isn't worth a dollar today. A dollar today could be invested, "
            "say in a Treasury bond, and grow. <bookmark mark='d'/> So every future dollar has to be discounted: divided "
            "by one plus an interest rate, once for every year you have to wait. <bookmark mark='s'/> Here's what each "
            "bar is worth today."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeOut(grow), Write(disc_l), FadeIn(r_l))
            vo.wait_until("s")
            self.play(LaggedStart(*[ReplacementTransform(raw[i].copy(), disc[i]) for i in range(YEARS)], lag_ratio=0.03),
                      raw.animate.set_fill(opacity=0.18), run_time=2.5)

        # Stack the present values into one column: that's the price.
        col_x = 3.5
        scale = 0.26  # column height per unit of first-year profit
        stack, y = VGroup(), y0
        for t in range(1, YEARS + 1):
            h = scale * pv_factor(t, R)
            seg = Rectangle(width=1.0, height=h, stroke_width=0.5, stroke_color=BACKGROUND, fill_color=C.PRICE,
                            fill_opacity=0.9)
            seg.move_to([col_x, y, 0], aligned_edge=DOWN)
            stack.add(seg)
            y += h
        tail_h = scale * (1 / (R - G)) - (y - y0)
        tail = DashedVMobject(Rectangle(width=1.0, height=tail_h, color=C.PRICE, stroke_width=2), num_dashes=24)
        tail.move_to([col_x, y, 0], aligned_edge=DOWN)
        price_l = label(r"price today", font_size=30, color=C.PRICE).next_to(tail, UP, buff=0.15)
        tail_l = label(r"years 41 to $\infty$", font_size=22, color=GREY_A).next_to(tail, RIGHT, buff=0.15)
        total = label(r"$= 20\times$ the first\\year's profit", font_size=30).next_to(stack, RIGHT, buff=0.25).shift(DOWN * 0.6)
        assert abs(sum(pv_factor(t, R) for t in range(1, 2000)) - 20) < 1e-6
        with self.voiceover(
            "Now stack up what's left. <bookmark mark='s'/> That stack is what the share is worth today: its price. "
            "<bookmark mark='t'/> The far future still counts, but less and less. With these numbers, the whole stack, out "
            "to infinity, comes to twenty times the first year's profit. A P/E of twenty."
        ) as vo:
            self.play(FadeOut(VGroup(disc_l, r_l)))
            vo.wait_until("s")
            self.play(LaggedStart(*[ReplacementTransform(disc[i], stack[i]) for i in range(YEARS)], lag_ratio=0.03),
                      run_time=3)
            vo.wait_until("t")
            self.play(Create(tail), FadeIn(tail_l), FadeIn(price_l))
            self.play(Write(total))
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        rows = VGroup(
            MathTex(r"P", r"=", r"\frac{D}{1+r}", r"+", r"\frac{D(1+g)}{(1+r)^2}", r"+", r"\frac{D(1+g)^2}{(1+r)^3}", r"+",
                    r"\cdots", font_size=46),
            MathTex(r"=", r"\frac{D}{1+r}", r"\Big(1 + q + q^2 + \cdots\Big)", r",\quad q = \frac{1+g}{1+r}", font_size=46),
            MathTex(r"P", r"=", r"\frac{D}{r-g}", font_size=60),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(UP * 0.1 + LEFT * 0.4)
        rows[1].shift(RIGHT * (rows[0][1].get_x() - rows[1][0].get_x()))
        rows[2].shift(RIGHT * (rows[0][1].get_x() - rows[2][1].get_x()))
        rows[0][0].set_color(C.PRICE)
        rows[2][0].set_color(C.PRICE)
        legend = VGroup(
            label(r"$D$: first-year payout to shareholders", font_size=28, color=C.EARNINGS),
            label(r"$g$: how fast it grows", font_size=28, color=C.EARNINGS),
            label(r"$r$: the discount rate", font_size=28, color=C.RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3)
        geo = label(r"geometric series: $1+q+q^2+\cdots = \frac{1}{1-q}$", font_size=28, color=GREY_A)
        geo.next_to(rows[1], DOWN, buff=0.25).align_to(rows[1], LEFT)

        with self.voiceover(
            "We can add up that infinite stack exactly. Call the first year's payout D, its growth rate g, and the "
            "discount rate r. <bookmark mark='a'/> The price is D over one plus r, plus the next year's payout, discounted "
            "twice, and so on forever. <bookmark mark='q'/> Each term is the one before it, times the same ratio, q. "
            "That's a geometric series, <bookmark mark='s'/> and it collapses to something remarkably simple: D divided by "
            "r minus g."
        ) as vo:
            self.play(FadeIn(legend, lag_ratio=0.2))
            vo.wait_until("a")
            self.play(Write(rows[0]), run_time=2.5)
            vo.wait_until("q")
            self.play(FadeIn(rows[1], shift=DOWN * 0.2), FadeIn(geo))
            vo.wait_until("s")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeOut(geo))
            self.play(Circumscribe(rows[2], color=YELLOW))

        pe = MathTex(r"\frac{P}{E}", r"=", r"\frac{D/E}{r-g}", font_size=60).move_to(rows[2]).shift(RIGHT * 4.6)
        pe[0].set_color(C.MULTIPLE)
        payout = label(r"$D/E$: share of profits paid out", font_size=26, color=GREY_A).next_to(pe, DOWN, buff=0.15)
        rdef = MathTex(r"r", r"=", r"\text{risk-free rate}", r"+", r"\text{equity risk premium}", font_size=42)
        rdef[0].set_color(C.RATE)
        rdef[2].set_color(C.RATE)
        rdef.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Divide both sides by earnings, <bookmark mark='p'/> and out comes the P/E ratio itself: the share of profits "
            "paid out, divided by r minus g. <bookmark mark='r'/> And the discount rate r is the risk-free interest rate, "
            "the yield on Treasury bonds, plus an extra return investors demand for the risk of owning stocks: the equity "
            "risk premium."
        ) as vo:
            vo.wait_until("p")
            self.play(TransformFromCopy(rows[2], pe), FadeIn(payout))
            vo.wait_until("r")
            self.play(Write(rdef))
            self.play(Indicate(rdef[2], color=C.RATE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def sensitivity(self):
        from videos.opposing_forces.common import TimeChart

        ch = TimeChart((5.0, 14.0), (0, 50), width=8.0, height=4.6, x_ticks=[6, 8, 10, 12, 14],
                       x_fmt=lambda v: rf"{v:g}\%", y_ticks=[0, 10, 20, 30, 40, 50]).move_to(LEFT * 1.6 + DOWN * 0.3)
        xl = label(r"discount rate $r$ (growth $g = 4\%$)", font_size=28, color=C.RATE).next_to(ch, DOWN, buff=0.15)
        yl = ch.y_title(r"P/E $= 1/(r-g)$", color=C.MULTIPLE)
        rs = np.linspace(0.06, 0.14, 200)
        curve = ch.line(rs * 100, 1 / (rs - G), C.MULTIPLE, 5)
        r = ValueTracker(9.0)
        dot = always_redraw(lambda: ch.dot(r.get_value(), 1 / (r.get_value() / 100 - G), YELLOW, 0.1))
        guide = always_redraw(lambda: DashedLine(ch.c2p(r.get_value(), 0), ch.c2p(r.get_value(), 1 / (r.get_value() / 100 - G)),
                                                 color=GREY_B, stroke_width=2))

        def readout():
            rv = r.get_value()
            pe_v = 1 / (rv / 100 - G)
            g = VGroup(MathTex(rf"r - g = {rv - 4:.1f}\%", font_size=36, color=C.RATE),
                       MathTex(rf"\text{{P/E}} = {pe_v:.1f}", font_size=40, color=C.MULTIPLE),
                       MathTex(rf"{100 * (pe_v / 20 - 1):+.0f}\%", font_size=40,
                               color=WHITE if abs(pe_v - 20) < 0.05 else RED))
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 5.0 + UP * 0.6)
            return g

        box = always_redraw(readout)
        assert abs(1 / (0.095 - G) - 18.18) < 0.01 and abs(1 / (0.10 - G) - 16.67) < 0.01
        with self.voiceover(
            "Here's why this matters so much. Take a company that pays out all its profits, so its P/E is simply one "
            "over r minus g. <bookmark mark='c'/> Plot that against the discount rate. <bookmark mark='d'/> With r minus g "
            "at five percent, the P/E is twenty. <bookmark mark='u'/> Now raise interest rates by just half a point: the "
            "P/E falls to about eighteen, a nine percent drop. <bookmark mark='v'/> A full point: about seventeen, down "
            "seventeen percent. Because r minus g is a small number, small changes in rates make big changes in what "
            "investors will pay."
        ) as vo:
            vo.wait_until("c")
            self.play(Create(ch), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(dot), Create(guide), FadeIn(box))
            vo.wait_until("u")
            self.play(r.animate.set_value(9.5), run_time=1.5)
            vo.wait_until("v")
            self.play(r.animate.set_value(10.0), run_time=1.5)

        # Which future dollars lose the most?
        near = (1.09 / 1.10) ** 1 - 1
        far = (1.09 / 1.10) ** 30 - 1
        assert round(100 * near) == -1 and round(100 * far) == -24
        dur = VGroup(label(r"when $r$ goes from $9\%$ to $10\%$:", font_size=28),
                     label(r"a dollar due next year: $-1\%$", font_size=28, color=C.EARNINGS),
                     label(r"a dollar due in 30 years: $-24\%$", font_size=28, color=C.RATE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                    buff=0.18)
        dur.move_to(RIGHT * 4.85 + DOWN * 1.55)
        dur.add_background_rectangle(color=BACKGROUND, opacity=0.9, buff=0.15)
        with self.voiceover(
            "It also matters which dollars you're discounting. <bookmark mark='a'/> When rates rise from nine to ten "
            "percent, a dollar due next year loses about one percent of its value today. A dollar due in thirty years "
            "loses about a quarter, because it gets discounted thirty times over. Stocks are claims on very distant "
            "profits, so they behave like very long-term bonds."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dur, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def fed_model(self):
        fwd_pe = NOTE["fwd_pe_cap"]
        ey = 100 / fwd_pe
        y10, real10 = last("dgs10_weekly"), last("real10_weekly")
        assert abs(ey - 5.1) < 0.05 and abs(y10 - NOTE["ten_year"]) < 0.1 and abs(real10 - NOTE["real_ten_year"]) < 0.1
        flip = MathTex(r"\frac{P}{E} = 19.7", r"\quad\longrightarrow\quad", r"\frac{E}{P} = \frac{1}{19.7} \approx 5.1\%",
                       font_size=44).to_edge(UP, buff=0.5)
        flip[0].set_color(C.MULTIPLE)
        flip[2].set_color(C.MULTIPLE)
        names = [r"stocks: forward earnings yield", r"10-year Treasury yield", r"10-year inflation-protected (TIPS)"]
        vals = [ey, y10, real10]
        cols = [C.MULTIPLE, C.RATE, C.REAL_RATE]
        texts = [pct(ey), pct(y10, 2), pct(real10, 2) + r"\ + \text{inflation}"]
        bars = VGroup()
        for n, v, c, t in zip(names, vals, cols, texts):
            lab = label(n, font_size=30, color=c)
            bar = Rectangle(width=v * 1.15, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.85)
            val = MathTex(t, font_size=34)
            bars.add(VGroup(lab, bar, val))
        for i, (lab, bar, val) in enumerate(bars):
            y = 0.9 - i * 1.25
            lab.move_to([-6.3, y + 0.5, 0], aligned_edge=LEFT)
            bar.move_to([-6.3, y - 0.05, 0], aligned_edge=LEFT)
            val.next_to(bar, RIGHT, buff=0.25)
        quote = tagged(r"``Ignore the Fed Model at your peril.''", font_size=34, color=YELLOW).to_edge(DOWN, buff=0.85)
        src = source(r"FRED (DGS10, DFII10), " + data_date() + r"; forward P/E: Timmer")
        with self.voiceover(
            "This is the idea behind a shortcut Timmer leans on: the Fed Model, which compares what stocks earn with "
            "what bonds pay. <bookmark mark='f'/> Flip the P/E upside down and you get the earnings yield. At a forward "
            "P/E of 19.7, the stock market earns about 5.1 percent of its price per year. <bookmark mark='b'/> A ten-year "
            "Treasury now pays 5.3 percent, guaranteed. <bookmark mark='t'/> And inflation-protected Treasuries pay 2.9 "
            "percent on top of inflation."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(flip))
            self.play(FadeIn(bars[0][0]), GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1][0]), GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]), FadeIn(src))
            vo.wait_until("t")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]))

        with self.voiceover(
            "That's stiff competition. Why take the risks of owning stocks for a 5.1 percent earnings yield, when the "
            "government will pay you 5.3 with essentially no risk of default? You'd only do it if you expect those earnings to keep "
            "growing fast, and even then you won't pay top dollar for them. <bookmark mark='q'/> In Timmer's words: ignore "
            "the Fed Model at your peril."
        ) as vo:
            vo.wait_until("q")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()

        pe0, pe1 = FACTSET["fwd_pe_june30"], FACTSET["fwd_pe"]
        drop = 100 * (pe1 / pe0 - 1)
        y_jun, y_sep = data_at("dgs10_daily", ym(2026, 6, 30)), data_at("dgs10_daily", ym(2026, 9, 30))
        rise = y_sep - y_jun
        model = 100 * ((R - G) / (R - G + rise / 100) - 1)
        assert -8 < drop < -6 and 0.8 < rise < 0.9 and -15.5 < model < -13.5
        lines = VGroup(
            label(r"June 30 $\to$ Sept 30, 2026:", font_size=34),
            label(rf"10-year yield: ${y_jun:.2f}\% \to {y_sep:.2f}\%$", font_size=34, color=C.RATE),
            label(rf"our simple model predicts a P/E drop of about ${-model:.0f}\%$", font_size=34, color=GREY_A),
            label(rf"actual forward P/E: ${pe0:.1f} \to {pe1:.1f}$, about ${drop:.0f}\%$".replace("-", "-"), font_size=34,
                  color=C.MULTIPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.4)
        src2 = source(r"FRED (DGS10); FactSet Earnings Insight, Oct 2, 2026")
        with self.voiceover(
            "We can even check the size of the effect. <bookmark mark='a'/> Over the third quarter, the ten-year yield "
            "rose by about 0.85 percentage points. <bookmark mark='b'/> Our simple model, with nothing else changing, "
            "says that should knock roughly fifteen percent off the P/E. <bookmark mark='c'/> The market's actual forward "
            "P/E fell about seven. So far, stocks have absorbed only part of the shock: investors may be counting on "
            "faster growth, or accepting a thinner premium for owning stocks. Either way, the real question is: <bookmark "
            "mark='q'/> why are interest rates rising?"
        ) as vo:
            self.play(FadeIn(lines[0]), FadeIn(src2))
            vo.wait_until("a")
            self.play(FadeIn(lines[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(lines[2], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(lines[3], shift=RIGHT * 0.2))
            vo.wait_until("q")
            self.play(Indicate(lines[1], color=C.RATE))
        self.clear_scene()


def data_at(key: str, when: float) -> float:
    from videos.opposing_forces.common import at, ts

    return at(*ts(key), when)


def data_date() -> str:
    from videos.opposing_forces.common import data

    return data()["dgs10_last"]["date"]
