from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load, real_data


def _t(d):
    d = int(d)
    x = date(d // 10000, (d // 100) % 100, d % 100)
    return x.year + (x.timetuple().tm_yday - 1) / 365


class Volmageddon(VoiceoverScene):
    def construct(self):
        v = load("volmageddon")
        x = load("vx_etp")
        c = load("vixcomp")
        self.card()
        self.file(v, x)
        self.mechanics(v, c)
        self.firms()
        self.lessons()

    def card(self):
        c = chapter_card(15, r"Volmageddon, 5 February 2018", r"What happens when everyone is short volatility?",
                         lit=(2018,), part=PART)
        with self.voiceover("Chapter fifteen. Volmageddon: the fifth of February, 2018."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def file(self, v, x):
        card = crisis_card(
            r"5 February 2018", r"Volmageddon",
            r"After a year of record calm, the VIX more than doubled in a day. XIV, Credit Suisse's exchange-traded note "
            r"paying the inverse of each day's move in short-term VIX futures, collapsed after the close. On 6 February "
            r"the bank announced an ``acceleration event'': the note's intraday indicative value on 5 February had fallen "
            r"to 20\% or less of the previous close, \$108.37. The notes were redeemed later that month.",
            stats=[(rf"{v['before']:.2f} \to {v['after']:.2f}", r"the VIX, 2 to 5 February"),
                   (rf"+{100 * v['jump']:.0f}\%", r"its largest one-day rise on record"),
                   (rf"{100 * x['note_feb5']:.0f}\%", r"a $-1\times$ note on the rebuilt index, that day")],
            width=11.6, font_size=24)
        card.move_to(ORIGIN)
        src = note(r"FRED (VIXCLS); Credit Suisse release of 6 February 2018 (SEC Form 6-K); Cboe settlements",
                   font_size=17, color=GREY_B).to_corner(DR, buff=0.25)
        b, a, n = v["before"], v["after"], abs(100 * x["note_feb5"])
        with self.voiceover(
            "On Monday the fifth of February 2018, after the calmest year in the VIX's history, the index went from "
            f"{b:.2f} to {a:.2f} in one day, the largest one-day rise on record. That evening XIV, a note issued by "
            "Credit Suisse that paid the inverse of each day's move in short-term VIX futures, collapsed. The next "
            "morning the bank announced what its prospectus called an acceleration event: during the fifth, the note's "
            "indicative value had fallen to a fifth or less of the previous close of a hundred and eight dollars. Our "
            f"own rebuild of the index, from Cboe's settlement prices, has a minus-one note losing {n:.0f} percent that "
            "day."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(src))
        self.wait(0.5)
        self.clear_scene()

    def mechanics(self, v, c):
        t = np.array([_t(d) for d in v["date"]])
        xv = np.asarray(v["vix"])
        g = axes([2017.4, 2018.5], [5, 40], x_length=6.0, y_length=3.4, ylabel=r"the VIX", xticks=[2017.5, 2018.0, 2018.5],
                 xfmt=lambda u: {2017.5: "Jul 2017", 2018.0: "Jan 2018", 2018.5: "Jul 2018"}[round(u * 2) / 2],
                 yticks=[10, 20, 30, 40], font_size=16).to_edge(LEFT, buff=0.6).to_edge(UP, buff=0.6)
        line = curve(g.ax, t, xv, IV, stroke_width=2.5)
        snap = c["ts_snap"]
        steps = VGroup(
            label(r"how a short-volatility note amplifies a shock", font_size=22, color=GREY_A),
            wrapped_label(r"1. the VIX jumps in the afternoon; front futures follow", 5.6, 19, GREY_A),
            wrapped_label(r"2. each inverse or leveraged note must buy futures near the close, in proportion to the "
                          r"day's move (Chapter 14: $+2rN$)", 5.6, 19, OPT),
            wrapped_label(r"3. all of them buy the same contracts in the same minutes; the buying lifts the futures "
                          r"further, which raises tomorrow's required buying", 5.6, 19, BAD),
            wrapped_label(r"4. VIX futures traded until 4:15 pm New York time, a quarter of an hour after stocks closed: "
                          r"the notes' index moved in a thin market", 5.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        ts = MathTex(rf"\text{{VIX / VIX3M: }}\ {snap['20180202']:.3f}\ (2\ \text{{Feb}})\ \to\ {snap['20180205']:.3f}"
                     rf"\ (5\ \text{{Feb}})", font_size=30, color=LV).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        tsl = wrapped_label(r"the term structure inverted in a day: short-dated fear above long", 6.0, 19, GREY_B
                            ).next_to(ts, DOWN, buff=0.15).align_to(ts, LEFT)
        src = real_data(r"FRED: VIXCLS, VXVCLS")
        r1, r2 = snap["20180202"], snap["20180205"]
        with self.voiceover(
            "The VIX through that year: long and low, then the spike. <bookmark mark='a'/> VIX over its three-month "
            f"version went from {r1:.3f} on the Friday to {r2:.3f} on the Monday. <bookmark mark='b'/> The mechanism: "
            "the front futures jumped in the afternoon; every inverse and leveraged note had to buy futures near the "
            "close, Chapter fourteen's two r N; all needed the same contracts in the same minutes, and their buying "
            "pushed prices higher, in futures that traded on for a quarter of an hour after stocks closed. The hedge "
            "was the amplifier."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(ts), FadeIn(tsl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.6, run_time=6))
        self.wait(0.4)
        self.clear_scene()

    def firms(self):
        cs = firm_card(r"Credit Suisse: XIV",
                       r"Issuer of the note. Investors later \emph{alleged} that the bank's own hedge trading in the "
                       r"minutes after the close helped drive the collapse; in 2021 the Second Circuit held the "
                       r"manipulation claims adequately pleaded and returned the case to the district court (Set Capital v. "
                       r"Credit Suisse, 996 F.3d 64). The bank contested the claims. Allegations, not findings.",
                       source=r"Credit Suisse 6-K, 6 Feb 2018; 2d Cir. opinion, 27 Apr 2021", width=6.3, font_size=20)
        ps = firm_card(r"ProShares: SVXY",
                       r"The surviving inverse VIX fund. Effective at the close of 27 February 2018 it cut its target from "
                       r"$-1\times$ to $-0.5\times$ the daily return of the same index (and UVXY from $2\times$ to "
                       r"$1.5\times$), halving the close-of-day hedge a spike forces.",
                       source=r"ProShare Capital Management announcement, February 2018", width=6.3, font_size=20)
        gs = firm_card(r"Research: Griffin and Shams (2018)",
                       r"``Manipulation in the VIX?'' (\emph{Review of Financial Studies}): volume spikes in out-of-the-money "
                       r"S\&P 500 options at the VIX settlement auction, consistent with attempts to move the settlement. "
                       r"Cboe disputed the paper's conclusions. A research finding and an allegation, not a ruling.",
                       source=r"Griffin and Shams, RFS 31(4), 2018", width=6.3, font_size=20)
        tv = firm_card(r"Earlier: TVIX, 2012",
                       r"When Credit Suisse suspended new issuance of its $2\times$ VIX note in February 2012, the note's "
                       r"price detached from its indicative value; buyers at the premium lost it when issuance resumed. "
                       r"The option-writing funds of the same era (LJM in 2018, Allianz's Structured Alpha in 2020) are "
                       r"Part 11's crisis file.", source=r"as reported by Bloomberg, March 2012", width=6.3, font_size=20)
        grid = VGroup(VGroup(cs, ps).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(gs, tv).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 7.4:
            grid.scale_to_fit_height(7.4)
        grid.move_to(ORIGIN)
        with self.voiceover(
            "The firm files, from the public record. Investors later alleged that Credit Suisse's own hedge trading "
            "after the close helped drive XIV's collapse; in 2021 the Second Circuit held the manipulation claims "
            "adequately pleaded and sent the case back; the bank contested them. Allegations, not findings. "
            "<bookmark mark='a'/> ProShares' SVXY, which survived, cut its leverage to minus one half on the "
            "twenty-seventh of February. <bookmark mark='b'/> John Griffin and Amin Shams found volume spikes in S&P "
            "options exactly at the VIX settlement auction, consistent with attempts to move it; Cboe disputed their "
            "conclusions. <bookmark mark='c'/> In 2012 Credit Suisse had suspended issuance of TVIX, whose price then "
            "drifted far above its value. The option-writing funds of those years, LJM and Allianz's Structured "
            "Alpha, are Part eleven's crisis file."
        ) as vo:
            self.play(FadeIn(cs))
            vo.wait_until("a")
            self.play(FadeIn(ps))
            vo.wait_until("b")
            self.play(FadeIn(gs))
            vo.wait_until("c")
            self.play(FadeIn(tv))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        rows = [cmath(r"\text{loss of a } -1\times \text{ note}", r"=", r"-\,r_{\text{index}}\ \ \text{(one day, unbounded "
                      r"relative to its gains)}", font_size=34, colors={r"\text{loss of a } -1\times \text{ note}": BAD})]
        whys = [why(r"a year of roll yield is a few percent a month; one day's index return can exceed 100\%")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        notes = VGroup(
            wrapped_label(r"the variance premium of Chapter 12 and the roll of Chapter 14 are the same trade: paid a little "
                          r"every month, for bearing the crash", 11.6, 21, GREY_A),
            wrapped_label(r"the product's own hedging made the crash worse: a promise on the daily close-to-close return "
                          r"forces trades at the close, whatever the price", 11.6, 21, BAD),
            wrapped_label(r"pause and predict: why did the issuer have to buy at the close, not earlier?", 11.6, 21, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The arithmetic of the loss is one line: an inverse note loses the index's daily return, and nothing caps "
            "that return. A year of roll yield is a few percent a month; one day erased it. <bookmark mark='a'/> This "
            "is Chapter twelve's premium again, seen from the seller: paid a little every month, for bearing the crash. "
            "And the product's design made the crash worse. Pause and predict: why did the issuer have to buy at the "
            "close, not earlier in the day? Because the note promised the close-to-close return, and the hedge is only "
            "exact at the close: buying earlier is a bet that the move will hold."
            " Today a feedback of this kind runs through dealers' option hedges. Next."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()
