from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class Regimes(VoiceoverScene):
    def construct(self):
        e = load("erm")
        self.card()
        self.model()
        self.plot(e["attack"])
        self.erm(e)
        self.second()
        self.franc(load("snb"))

    def card(self):
        c = chapter_card(6, r"Pegs and attacks", r"When does a fixed exchange rate break?", lit=(1992, 2015), part=PART)
        with self.voiceover("Chapter six. Fixed exchange rates, and the attacks that break them."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"m_t - s_t", r"=", r"-\alpha\,\dot s_t", font_size=40, colors={r"m_t - s_t": FOR}),
                cmath(r"m_t", r"=", r"d_t + R_t,\qquad \dot d_t = \mu > 0", font_size=40),
                cmath(r"\tilde s_t", r"=", r"d_t + \alpha\mu", font_size=40, colors={r"\tilde s_t": BAD})]
        whys = [why(r"money demand (in logs, prices proportional to the exchange rate): people hold less money when "
                    r"they expect the currency to depreciate"),
                why(r"money is backed by domestic credit $d$, which the government keeps expanding, and foreign "
                    r"reserves $R$; under the peg, every new unit of credit drains a unit of reserves"),
                why(r"the shadow exchange rate: where the currency would float if reserves were gone, depreciating at "
                    r"$\mu$. Krugman (1979); Flood and Garber (1984)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Paul Krugman's 1979 model of a currency attack fits in three lines. People hold less money when they "
            "expect it to lose value. <bookmark mark='a'/> The money supply is the government's domestic credit plus "
            "the central bank's foreign reserves, and the government keeps expanding credit; to hold the peg, the "
            "central bank sells a unit of reserves for every unit of new credit. <bookmark mark='b'/> Now ask where "
            "the currency would trade if the reserves were gone and it floated: the shadow rate, which rises with "
            "credit, and sits above credit by alpha times mu, because a floating currency would be expected to fall."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def plot(self, a):
        t, sh, R, s = np.asarray(a["t"]), np.asarray(a["shadow"]), np.asarray(a["R"]), np.asarray(a["s"])
        ts = a["t_star"]
        g = axes([0, 14], [0, 1.4], x_length=8.0, y_length=4.4, xlabel=r"time", ylabel=r"log exchange rate, reserves",
                 xticks=[0, 4, 8, 12], yticks=[0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        peg = DashedLine(ax.c2p(0, 1.0), ax.c2p(14, 1.0), color=USD, stroke_width=2)
        lsh = curve(ax, t, sh, BAD, stroke_width=3)
        lR = curve(ax, t, R, GOOD, stroke_width=3)
        ls = curve(ax, t, s, FOR, stroke_width=4)
        v = DashedLine(ax.c2p(ts, 0), ax.c2p(ts, 1.3), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            legend([(USD, r"the peg"), (BAD, r"the shadow rate"), (GOOD, r"reserves"), (FOR, r"the exchange rate")],
                   font_size=17),
            MathTex(rf"T^* = \frac{{\bar s - \alpha\mu - d_0}}{{\mu}} = {ts:.0f}", font_size=26, color=BAD),
            wrapped_label(rf"reserves would last until $t$ = {a['reserves_if_no_attack_run_out']:.0f}; the attack comes "
                          rf"earlier, at {ts:.0f}, when the shadow rate meets the peg, and takes the last "
                          rf"{a['reserves_at_attack']:.2f} in one day. Illustrative parameters", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Watch it run. <bookmark mark='a'/> Reserves drain steadily as credit grows; the shadow rate climbs toward "
            "the peg. <bookmark mark='b'/> Speculators know the peg must eventually go. If they wait until reserves "
            "run out, the currency jumps and they would have profited by selling earlier; so they move earlier. The "
            "attack comes exactly when the shadow rate reaches the peg, at time "
            f"{ts:.0f}, while reserves would have lasted until {a['reserves_if_no_attack_run_out']:.0f}. "
            "<bookmark mark='c'/> On that day they buy every remaining reserve in one stroke, the peg ends, and the "
            "currency floats, without a jump. The crisis is sudden, and entirely predictable."
        ) as vo:
            self.play(FadeIn(g), Create(peg), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lR), Create(lsh), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(v), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ls), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def erm(self, e):
        t, v = np.asarray(e["t"]), np.asarray(e["dmgbp"])
        g = axes([1990, 1994], [2.2, 3.3], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"Deutsche marks per pound",
                 xticks=[1990, 1991, 1992, 1993], yticks=[2.4, 2.6, 2.8, 3.0, 3.2], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        t0, t1 = 1990.77, 1992.71
        band = VGroup(DashedLine(ax.c2p(t0, e["floor"]), ax.c2p(t1, e["floor"]), color=BAD, stroke_width=2),
                      DashedLine(ax.c2p(t0, e["ceiling"]), ax.c2p(t1, e["ceiling"]), color=GREY_B, stroke_width=1.5),
                      DashedLine(ax.c2p(t0, e["central"]), ax.c2p(t1, e["central"]), color=USD, stroke_width=1.5))
        bl = label(rf"ERM: central rate {e['central']:.2f}, floor {e['floor']:.3f}", font_size=16, color=GREY_A).next_to(
            ax.c2p(t0, e["ceiling"]), UP, buff=0.1).shift(RIGHT * 1.6)
        line = curve(ax, t, v, FOR, stroke_width=2.4)
        side = VGroup(
            MathTex(rf"15\ \text{{Sep}}:\ {e['sep15']:.4f}", font_size=24),
            MathTex(rf"16\ \text{{Sep}}:\ {e['sep16']:.4f}", font_size=24, color=BAD),
            MathTex(rf"17\ \text{{Sep}}:\ {e['sep17']:.4f}", font_size=24, color=BAD),
            MathTex(rf"\text{{low after}}:\ {e['min_after']:.4f}", font_size=24, color=BAD),
            wrapped_label(r"Bank of England, London late afternoon. On the 16th the base rate went from 10\% to 12\% in "
                          r"the morning, 15\% was promised in the afternoon; in the evening Britain left the mechanism",
                          3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "In October 1990 Britain joined Europe's exchange-rate mechanism at two point nine five marks to the pound, "
            "promising to keep sterling above two point seven seven eight. <bookmark mark='a'/> Two years later, with "
            "German rates high after reunification and Britain in recession, the pound sat on its floor. "
            "<bookmark mark='b'/> On Wednesday the sixteenth of September 1992 the Bank of England bought pounds all "
            "morning, raised its rate from ten to twelve percent, and promised fifteen. The selling continued. That "
            f"evening Britain left the mechanism, and the pound fell through the floor, "
            f"{100 * (1 - e['oct30'] / e['sep15']):.0f} percent within six weeks. "
            "George Soros's fund was reported to have made about a billion dollars; the Treasury later put the cost of "
            "the defence at about three point three billion pounds."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(band), FadeIn(bl), Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.3))
        self.add(illustration(r"Bank of England XUDLDMS; HM Treasury papers released 2005 (the cost)"))
        self.wait(0.4)
        self.clear_scene()

    def second(self):
        rows = [cmath(r"\text{defend}", r"\iff", r"\text{cost of high rates} < \text{cost of devaluing}", font_size=36,
                      colors={r"\text{defend}": USD})]
        whys = [why(r"second-generation models (Obstfeld, 1994): the government chooses. Defending the peg needs high "
                    r"interest rates, which hurt; if speculators expect a devaluation, defending costs more, which makes "
                    r"giving up rational: an attack can be self-fulfilling")]
        step = ladder(self, rows, whys, keep=1, top=2.0, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Britain in 1992 does not fit Krugman's model: its reserves were not being drained by reckless credit. "
            "Maurice Obstfeld's second-generation models fit better. The government chooses whether to defend, "
            "weighing the pain of high interest rates against the cost of devaluing. If markets expect a devaluation, "
            "the defence needs even higher rates, which makes giving up the sensible choice. An attack can succeed "
            "because it is expected to succeed. A fifteen percent interest rate in a recession was a promise no one "
            "believed."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def franc(self, s):
        cards = VGroup(
            desk_question(r"defending a floor", r"the Swiss franc's problem was the opposite of sterling's: the market "
                          r"wanted to buy it. The SNB could print francs without limit to sell them, so it could never run "
                          r"out", width=12.0, font_size=21),
            desk_question(r"the cost", r"every franc printed bought a euro asset: the SNB's balance sheet swelled with "
                          r"foreign currency, and a later appreciation would become a loss on it. The limit was its "
                          r"willingness, not its means", width=12.0, font_size=21),
            desk_question(r"the market's mistake", r"options priced the floor as almost certain; three years without "
                          r"volatility made selling protection against its end look free (chapter 3's steamroller)",
                          width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "And the franc, from the start of this part. <bookmark mark='a'/> Its problem was the opposite of "
            "sterling's: everyone wanted to buy it. The Swiss National Bank could print francs without limit to sell "
            "them, so it could never run out. <bookmark mark='b'/> But every franc it printed bought a euro asset, and "
            "its balance sheet swelled with foreign currency that would lose value the day the franc rose. The limit "
            "was its willingness, not its means. <bookmark mark='c'/> When it let go, the market had priced the floor "
            "as nearly certain. Three calm years had made protection against its end look free."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a central bank defends a weak peg with \$30 billion of reserves and loses \$2 billion a month. In "
                r"Krugman's model, when does the attack come: when reserves hit zero, or before?")
        with self.voiceover("A central bank defends a weak peg with thirty billion dollars of reserves, losing two "
                            "billion a month. In Krugman's model, does the attack come when reserves hit zero, or "
                            "before?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
