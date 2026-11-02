from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, LOSS, MART, P_C, PART, load, real_data

MONTHS = {1994.5: "Jul 94", 1994.75: "Oct 94", 1995.0: "Jan 95", 1995.25: "Apr 95"}


def _date(d: int) -> str:
    """A date as shown on screen (ISO, the same in both languages)."""
    return "%d-%02d-%02d" % (d // 10000, (d // 100) % 100, d % 100)


def _days_after_kobe(d: int) -> int:
    from datetime import date

    return (date(d // 10000, (d // 100) % 100, d % 100) - date(1995, 1, 17)).days


class Barings(VoiceoverScene):
    def construct(self):
        n = load("nikkei")
        nd = load("nikkei_doubling")
        self.card()
        self.file()
        self.chart(n)
        self.replay(nd)
        self.controls()

    def card(self):
        c = chapter_card(8, r"Doubling down: Barings, 1995", r"What happens when the bankroll is someone else's?",
                         lit=(1995,), part=PART)
        with self.voiceover("Chapter eight. Doubling down: Barings, 1995."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self):
        card = crisis_card(r"26 February 1995", r"Barings",
                           r"Britain's oldest merchant bank, founded in 1762, failed after its Singapore derivatives "
                           r"trader, Nick Leeson, lost about \pounds 830 million on Nikkei futures and options, hidden "
                           r"for about two and a half years in error account 88888. ING bought the bank for one pound.",
                           stats=[(r"\pounds 827\text{m}", r"unreported losses by 27 Feb.\ 1995"),
                                  (r"\approx \pounds 350\text{m}", r"the group's capital, Dec.\ 1994"),
                                  (r"88888", r"the error account that hid it")],
                           width=10.6, font_size=27)
        src = note(r"Board of Banking Supervision, report of 18 July 1995, as summarized by the Reserve Bank of "
                   r"Australia, \textit{Bulletin}, November 1995; FIA (2020)", font_size=17)
        VGroup(card, src).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "In February 1995 the doubling system broke a bank. Barings, Britain's oldest merchant bank, founded in "
            "1762, failed after a single trader in Singapore, Nick Leeson, lost about eight hundred and thirty "
            "million pounds, more than twice the bank's capital. For about two and a half years he had hidden his "
            "losses in an error account numbered eight eight eight eight eight. The Dutch bank ING bought what was "
            "left for one pound. Leeson was arrested in Frankfurt and sentenced in Singapore to six and a half years "
            "in prison."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def chart(self, n):
        t, v = np.asarray(n["t"]), np.asarray(n["value"])
        g = axes([1994.5, 1995.25], [15000, 21500], x_length=8.2, y_length=4.6, ylabel=r"Nikkei 225",
                 xticks=[1994.5, 1994.75, 1995.0, 1995.25], xfmt=lambda x: MONTHS[x],
                 yticks=[15000, 17000, 19000, 21000], yfmt=lambda u: f"{int(u):,}".replace(",", "{,}"), font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        tk = ValueTracker(0.0)
        line = tracing(ax, t, v, tk, P_C, stroke_width=3)
        kobe_t = 1995 + 16 / 365
        kobe = DashedLine(ax.c2p(kobe_t, 15000), ax.c2p(kobe_t, 21500), color=LOSS, stroke_width=2)
        kl = label(r"Kobe earthquake, 17 Jan.", font_size=19, color=LOSS).next_to(ax.c2p(kobe_t, 21300), LEFT, buff=0.1)
        bar_t = 1995 + 56 / 365
        fall = DashedLine(ax.c2p(bar_t, 15000), ax.c2p(bar_t, 21500), color=QC.CRISIS, stroke_width=2)
        fl = label(r"Barings fails, 26 Feb.", font_size=19, color=QC.CRISIS).next_to(ax.c2p(bar_t, 15300), LEFT, buff=0.1)
        p = n["pick"]
        week = 100 * (p['19950123'] / p['19950113'] - 1)
        side = VGroup(
            MathTex(rf"\text{{13 Jan.: }} {p['19950113']:,.0f}".replace(",", "{,}"), font_size=28),
            MathTex(rf"\text{{23 Jan.: }} {p['19950123']:,.0f}\ ({week:.0f}\%)".replace(",", "{,}"),
                    font_size=28, color=LOSS),
            MathTex(rf"\text{{27 Feb.: }} {p['19950227']:,.0f}\ ({100 * (p['19950227'] / p['19950113'] - 1):.0f}\%)".replace(",", "{,}"),
                    font_size=28, color=LOSS),
            wrapped_label(r"long Nikkei futures and short options that paid if the index stayed calm (a short "
                          r"volatility position); as it fell he bought more, to win it back", 4.4, 21, GREY_A),
            wrapped_label(r"a doubling system needs an endless bankroll; a hidden account let him borrow the bank's", 4.4,
                          21, LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"FRED: Nikkei 225 daily close (NIKKEI225); facts from the public record")
        i_kobe = int(np.searchsorted(t, kobe_t))
        with self.voiceover(
            "Here is the Nikkei through those months. Leeson was long Nikkei futures, and had sold options that paid "
            "him as long as the index stayed calm. <bookmark mark='a'/> On the seventeenth of January an earthquake "
            f"struck Kobe. Within a week the index had fallen {abs(week):.0f} percent. <bookmark mark='b'/> He did what "
            "the doubling system prescribes: as the market fell, he bought more, to win everything back on the "
            "rebound. The rebound did not come in time. <bookmark mark='c'/> On the twenty-sixth of February Barings "
            "failed, and the next day the Nikkei fell again."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.add(line)
            self.play(tk.animate.set_value(float(i_kobe)), FadeIn(side[0]), run_time=3, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(kobe), FadeIn(kl))
            self.play(tk.animate.set_value(float(i_kobe + 5)), FadeIn(side[1]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(side[3]), tk.animate.set_value(float(len(t) - 1)), run_time=3, rate_func=linear)
            line.clear_updaters()
            vo.wait_until("c")
            self.play(Create(fall), FadeIn(fl), FadeIn(side[2]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, nd):
        t = np.asarray(nd["t"])
        D, C = nd["doubling"], nd["capped"]
        pnl, units = np.asarray(D["pnl"]) / 1000, np.asarray(D["units"])
        pc = np.asarray(C["pnl"]) / 1000
        cap = nd["capital"] / 1000
        lo = float(min(pnl.min(), pc.min(), -cap)) * 1.1
        hi = float(max(pnl.max(), pc.max(), 10)) * 1.05
        g1 = axes([1994.5, 1995.25], [0, 9], x_length=8.0, y_length=1.5, ylabel=r"position, units (log$_2$)",
                  xticks=[], yticks=[0, 4, 8], yfmt=lambda u: f"{2 ** int(u):g}", font_size=15)
        g2 = axes([1994.5, 1995.25], [lo, hi], x_length=8.0, y_length=3.4,
                  ylabel=r"cumulative P\&L, thousands of index points $\times$ units",
                  xticks=[1994.5, 1994.75, 1995.0, 1995.25], xfmt=lambda x: MONTHS[x],
                  yticks=[round(lo / 50) * 50, 0, round(hi / 50) * 50], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        a1, a2 = g1.ax, g2.ax
        tk = ValueTracker(0.0)
        lu = tracing(a1, t, np.log2(units), tk, DRIFT, stroke_width=2.5)
        lp = tracing(a2, t, pnl, tk, LOSS, stroke_width=3)
        lc = curve(a2, t, pc, MART, stroke_width=2.5)
        capl = DashedLine(a2.c2p(1994.5, -cap), a2.c2p(1995.25, -cap), color=QC.CRISIS, stroke_width=2)
        capt = label(rf"capital: {nd['capital'] / 1000:.0f}", font_size=17, color=QC.CRISIS).next_to(
            a2.c2p(1994.5, -cap), UP, buff=0.05).align_to(a2, LEFT).shift(RIGHT * 0.1)
        tag = label(r"schematic: a doubling rule on the real index, not Leeson's book", font_size=20,
                    color=QC.IDEA).to_edge(UP, buff=0.25)
        cross = D["cross"]
        side = VGroup(
            label(r"rule: hold 1 unit; after every down day double it; back to 1 unit when the account is at a new "
                  r"high", font_size=19, color=GREY_A),
            MathTex(rf"\text{{crosses the capital line: }} \text{{{_date(cross)}}}" if cross else
                    r"\text{never crosses the capital line}", font_size=24, color=QC.CRISIS),
            MathTex(rf"\text{{largest position: }} {D['max_units']:.0f}\text{{ units}}", font_size=24, color=DRIFT),
            MathTex(rf"\text{{lowest: }} {D['min'] / 1000:,.0f}\text{{k on }} \text{{{_date(D['min_date'])}}}"
                    .replace(",", "{,}"), font_size=24, color=LOSS),
            MathTex(rf"\text{{unlimited credit, 31 Mar.: }} {D['end'] / 1000:+,.0f}\text{{k}}".replace(",", "{,}"),
                    font_size=24, color=LOSS),
            MathTex(rf"\text{{capped at 16 units, 31 Mar.: }} {C['end'] / 1000:+,.0f}\text{{k}}".replace(",", "{,}"),
                    font_size=24, color=MART),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        side[0] = wrapped_label(r"rule: hold 1 unit; after every down day double it; back to 1 unit when the account "
                                r"is at a new high", 4.4, 19, GREY_A)
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        dd = np.asarray(nd["date"])
        i_low = int(np.argmin(pnl))
        back = np.flatnonzero(pnl[i_low:] >= 0)
        recovered = len(back) > 0
        if recovered:
            k_back = int(back[0])
            story = (f"A doubler with unlimited credit would, in this replay, have been back above zero {k_back} "
                     "trading days after the low, which is exactly what the doubling system promises when no one "
                     "stops it. But the bank's capital line was crossed first.")
        else:
            story = "Even with unlimited credit, the doubler had not won it back by the end of March."
        capped = ("The same rule capped at sixteen units never recovers: bounded bets obey optional stopping, and "
                  "there is no promise of a comeback." if C["end"] < 0 else
                  "The same rule capped at sixteen units also recovered: in this short window, luck sided with it.")
        crossed = (f"the account crosses the capital line {_days_after_kobe(cross)} days after Kobe."
                   if cross else
                   "the account never crosses the capital line.")
        with self.voiceover(
            "We do not have Leeson's book, so here is a schematic instead, labelled as one: a simple doubling "
            "rule run on the real index. Hold one unit of the Nikkei; after every down day, double it; once the "
            "account is back at its high, go back to one unit. Against it, a bank with a stated capital. <bookmark "
            "mark='a'/> Through the autumn the rule wins small amounts, again and again. <bookmark mark='b'/> "
            f"Then Kobe. The position doubles day after day, to {D['max_units']:.0f} units, and {crossed} <bookmark "
            f"mark='c'/> {story} <bookmark mark='d'/> {capped}"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(g1), FadeIn(g2), Create(capl), FadeIn(capt), FadeIn(side[0]))
            self.add(lu, lp)
            vo.wait_until("a")
            i_jan = int(np.searchsorted(t, 1995.0))
            self.play(tk.animate.set_value(float(i_jan)), run_time=4, rate_func=linear)
            vo.wait_until("b")
            i_c = int(np.argmax(pnl <= -cap)) if cross else int(np.searchsorted(t, 1995.1))
            self.play(tk.animate.set_value(float(i_c)), run_time=2.5, rate_func=linear)
            self.play(FadeIn(side[1]), FadeIn(side[2]), Flash(a2.c2p(t[i_c], pnl[i_c]), color=QC.CRISIS))
            vo.wait_until("c")
            self.play(tk.animate.set_value(float(len(t) - 1)), FadeIn(side[3]), run_time=3, rate_func=linear)
            lu.clear_updaters()
            lp.clear_updaters()
            self.play(FadeIn(side[4]))
            self.play(Create(lc), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    def controls(self):
        rows = VGroup(
            label(r"what the theorem needs", font_size=26, color=MART),
            label(r"bounded bets, or a bounded stopped process (chapter 6)", font_size=23, color=GREY_A),
            label(r"what a bank enforces", font_size=26, color=DRIFT),
            label(r"position limits; margin funded only against reported positions", font_size=23, color=GREY_A),
            label(r"segregation of duties: the trader does not settle his own trades", font_size=23, color=GREY_A),
            label(r"what Barings lacked", font_size=26, color=LOSS),
            label(r"Leeson ran both the front office and the back office in Singapore", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(ORIGIN).shift(UP * 0.3)
        src = note(r"``clear segregation of duties is fundamental to any effective control system'': a lesson of the "
                   r"Board of Banking Supervision's report, as summarized by the Reserve Bank of Australia (1995)",
                   font_size=17).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So the lesson is not that optional stopping failed. A bank's controls exist to enforce its hypotheses. "
            "<bookmark mark='a'/> Position limits keep the bets bounded. Funding margin only against positions that "
            "are reported keeps the bankroll bounded. And separating the people who trade from the people who settle "
            "the trades makes the losses visible. <bookmark mark='b'/> In Singapore, Leeson ran both the trading and "
            "the back office. The inquiry's summary put it plainly: clear segregation of duties is fundamental to any "
            "effective control system."
        ) as vo:
            self.play(FadeIn(rows[:2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[2:5]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(rows[5:]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()
