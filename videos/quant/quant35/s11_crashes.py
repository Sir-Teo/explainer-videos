from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant35.common import BAD, DEALER_C, FLOW_C, GOOD, HURDLE, PART, PRICE_C, load


class Crashes(VoiceoverScene):
    def construct(self):
        self.card()
        self.flash()
        self.mechanics()
        self.after()
        self.btc_days(load("daily"))
        self.cascades()
        self.treasury()
        self.fba()
        self.fba_math()
        self.question()

    def card(self):
        c = chapter_card(10, r"When liquidity vanishes", r"What happens when the dealers stop quoting at once?", part=PART)
        with self.voiceover("Chapter ten. Every model in this part assumed someone is quoting. Twice in the last fifteen "
                            "years the deepest markets in the world lost their quotes for minutes, and prices went where "
                            "nobody intended."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def flash(self):
        card = crisis_card(r"6 May 2010", r"The flash crash", body=r"a large mutual-fund complex sold 75{,}000 E-mini S\&P "
                           r"500 futures, about \$4.1 billion, by an algorithm set to trade 9\% of volume without regard to "
                           r"price or time, as the CFTC--SEC report described; the E-mini fell about 5\% in minutes and US "
                           r"stocks fell with it, some trading at a cent, before most of the fall reversed within about "
                           r"twenty minutes", width=10.6, font_size=21).move_to(UP * 0.3)
        with self.voiceover(
            "The sixth of May, 2010. <bookmark mark='a'/> On an already nervous afternoon, a large fund complex began "
            "selling seventy-five thousand E-mini futures contracts, about four billion dollars, with an algorithm told to "
            "trade nine percent of the volume, whatever the price, as the regulators' joint report described. The E-mini "
            "fell about five percent in minutes; stocks followed, some trading at a cent; and most of the fall reversed "
            "within about twenty minutes."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def mechanics(self):
        rows = [cmath(r"\text{volume-targeted selling}", r"\Rightarrow", r"\text{more volume} \Rightarrow \text{faster selling}",
                      font_size=30, colors={r"\text{volume-targeted selling}": BAD}),
                cmath(r"\text{HFTs}", r":", r"\text{bought, then sold to each other: hot potato}", font_size=32,
                      colors={r"\text{HFTs}": DEALER_C}),
                cmath(r"\text{liquidity}", r"\to", r"0:\ \text{quotes pulled, stub quotes hit}", font_size=32,
                      colors={r"\text{liquidity}": BAD})]
        whys = [why(r"a rule that trades a share of volume speeds up exactly when its own selling raises the volume"),
                why(r"Kirilenko, Kyle, Samadi and Tuzun (2017): high-frequency traders did not cause the crash, but traded "
                    r"inventory back and forth, raising volume, and then withdrew"),
                why(r"with no one willing to hold inventory, the book emptied down to placeholder quotes far from any value")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What happened inside. <bookmark mark='a'/> An algorithm that trades a fixed share of volume speeds up when "
            "volume rises, and its own selling raised the volume. <bookmark mark='b'/> Andrei Kirilenko, Albert Kyle, "
            "Mehrdad Samadi and Tugkan Tuzun found that high-frequency traders did not cause the fall, but passed "
            "inventory back and forth among themselves, a hot potato that raised the volume further, and then stepped "
            "back. <bookmark mark='c'/> With no one willing to hold inventory, Chapter one's dealer had disappeared, and "
            "orders hit placeholder quotes far from any value."
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

    def after(self):
        cards = VGroup(
            desk_question(r"limit up--limit down", r"single-stock price bands that pause trading when a stock moves too "
                          r"far too fast, in place since 2012", width=12.4, font_size=19),
            desk_question(r"clearly erroneous trades", r"rules to cancel trades far from the market, so a cent trade in a "
                          r"\$40 stock does not stand", width=12.4, font_size=19),
            desk_question(r"the lesson for a dealer", r"liquidity is a choice made every microsecond; it is plentiful when "
                          r"it is least needed and withdrawn when inventory risk spikes", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What changed after. <bookmark mark='a'/> Price bands on single stocks that pause trading when a price moves "
            "too far too fast. <bookmark mark='b'/> Rules to cancel trades far from the market. <bookmark mark='c'/> And "
            "the lesson for anyone relying on liquidity: it is a choice dealers make every microsecond, plentiful when it "
            "is least needed and withdrawn when inventory risk spikes."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def btc_days(self, d):
        import numpy as np
        lam = np.asarray(d["lambda"], float)
        x = np.arange(len(lam))
        ok = np.isfinite(lam)
        top = float(np.ceil(np.nanpercentile(lam, 99.8) / 5) * 5)
        g = axes([0, len(lam)], [0, top], x_length=8.2, y_length=4.0, xlabel=r"BTCUSDT, 2021--2024, by day",
                 ylabel=r"$\hat\lambda$, bp per \$1m", xticks=[0, 365, 730, 1095, 1461], yticks=[0, top / 2, top],
                 xfmt=lambda v: str(2021 + int(round(v / 365.25))), yfmt=lambda v: f"{v:.0f}", font_size=14)
        g.move_to(LEFT * 0.6 + DOWN * 0.3)
        ax = g.ax
        c1 = curve(ax, x[ok], np.clip(lam[ok], 0, top), FLOW_C, stroke_width=1.2)
        med = DashedLine(ax.c2p(0, d["median"]), ax.c2p(len(lam), d["median"]), color=GREY_B, stroke_width=1.5)
        t5 = d["top"]
        st = VGroup(*[label(rf"{t_['date']}: {t_['lambda']:.1f}", font_size=15, color=BAD) for t_ in t5[:4]])
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UR, buff=0.35)
        r1 = d["top"][0]
        ratio = r1["lambda"] / d["median"]
        with self.voiceover(
            "Liquidity that comes and goes, measured on Bitcoin day by day. <bookmark mark='a'/> Kyle's lambda for every "
            f"day from 2021 to 2024: a median of {d['median']:.1f} basis points per million dollars. "
            f"<bookmark mark='b'/> On the worst days it is {ratio:.1f} times that, and the worst days cluster in 2022: the "
            "crypto lenders' failures in June and July, and the week FTX collapsed in November. Its correlation with the "
            f"day's volatility is {d['corr_vol']:.2f}, and with the day's dollar volume essentially zero: depth vanished "
            "on days of stress whether or not trading was heavy."
        ) as vo:
            self.play(FadeIn(g), Create(med))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def cascades(self):
        rows = [cmath(r"\text{leveraged longs}", r"\Rightarrow", r"\text{a fall triggers forced selling}", font_size=32,
                      colors={r"\text{leveraged longs}": BAD}),
                cmath(r"\text{forced selling}", r"\Rightarrow", r"\text{a further fall at } \lambda \text{ per dollar}",
                      font_size=32),
                cmath(r"\text{cascade}", r"\iff", r"\lambda \times \text{liquidations per bp} > 1", font_size=34,
                      colors={r"\text{cascade}": HURDLE})]
        whys = [why(r"perpetual futures let traders hold large leveraged positions; a fall below their margin closes them "
                    r"automatically, at market"),
                why(r"each forced sale is taker flow, and moves the price by Kyle's lambda"),
                why(r"if the selling triggered by a one-basis-point fall moves the price by more than a basis point, the fall "
                    r"feeds itself until the leverage is gone: the mechanics of 19 May 2021")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "In crypto, liquidity can vanish by design. <bookmark mark='a'/> Perpetual futures let traders hold large "
            "leveraged positions, closed automatically, at market, when the price falls through their margin. "
            "<bookmark mark='b'/> Each forced sale is taker flow, and moves the price by lambda. <bookmark mark='c'/> If "
            "the selling triggered by a one-basis-point fall moves the price by more than one basis point, the fall feeds "
            "itself until the leverage is exhausted. A higher lambda on stressed days, as just measured, makes the "
            "cascade more likely exactly when it starts."
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

    def treasury(self):
        card = crisis_card(r"15 October 2014", r"The Treasury flash rally", body=r"in the most liquid bond market in the "
                           r"world, the 10-year yield fell about 16 basis points and rebounded within roughly twelve "
                           r"minutes, with no news to explain it; the official joint staff report found that "
                           r"high-frequency firms dominated the trading and the depth of the order books had thinned before "
                           r"the move", width=10.6, font_size=21).move_to(UP * 0.3)
        with self.voiceover(
            "And bonds. <bookmark mark='a'/> On the fifteenth of October 2014, in the most liquid bond market in the "
            "world, the ten-year Treasury yield fell about sixteen basis points and came back within roughly twelve "
            "minutes, with no news to explain it. The official report found that high-frequency firms dominated the "
            "trading, and that the order books had thinned before the move. A market can be deep in volume and shallow "
            "in commitment."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card))
        self.wait(0.4)
        self.clear_scene()

    def fba(self):
        rows = [cmath(r"\text{continuous}", r":", r"\text{orders matched the instant they arrive}", font_size=32),
                cmath(r"\text{batch}", r":", r"\text{collect orders for, say, 100 ms; clear at one price}", font_size=32,
                      colors={r"\text{batch}": GOOD}),
                cmath(r"\text{speed}", r"\to", r"\text{compete on price, not on being first}", font_size=32,
                      colors={r"\text{speed}": HURDLE})]
        whys = [why(r"today's markets: a tiny speed advantage decides who trades against a stale quote"),
                why(r"Budish, Cramton and Shim's frequent batch auctions: many times a second, a sealed-bid uniform-price "
                    r"auction"),
                why(r"within a batch, arriving first is worth nothing; snipers must outbid each other, so the sniping rent "
                    r"is competed away to the quote's owner")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Chapter nine's remedy. <bookmark mark='a'/> Today, orders are matched the instant they arrive, so a tiny "
            "speed advantage wins every race. <bookmark mark='b'/> Budish, Cramton and Shim propose frequent batch "
            "auctions: collect orders for a fraction of a second, then clear them all at one price. "
            "<bookmark mark='c'/> Within a batch, arriving first is worth nothing, so would-be snipers must compete on "
            "price, and the rent from public news flows back to the quote's owner, and through narrower spreads to "
            "investors."
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

    def fba_math(self):
        lam_j, J, s = 0.02, 3.0, 1.0
        rows = [cmath(r"\text{continuous}", r":", r"\tfrac{s}{2} \ge \Pr(\text{news})\times J", font_size=34),
                cmath(r"\Pr(\text{news}) = 2\%,\ J = 3\ \text{ticks}", r"\Rightarrow", r"s \ge 0.12\ \text{ticks}",
                      font_size=30),
                cmath(r"\text{batch}", r":", r"\text{sniping loss} \to 0\ \Rightarrow\ s\ \text{covers inventory and "
                      r"processing only}", font_size=28, colors={r"\text{batch}": GOOD})]
        whys = [why(r"a market maker breaks even when half the spread earned on each trade covers the expected loss to "
                    r"snipers"),
                why(r"with news on 2\% of trades, each moving the value 3 ticks: the spread must be at least 0.12 ticks "
                    r"wider than it would otherwise be"),
                why(r"in a batch auction the maker can update its order in the same batch as the news, so that component "
                    r"vanishes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The arithmetic, in Chapter nine's example. <bookmark mark='a'/> A market maker breaks even when half the "
            "spread covers the expected loss to snipers. <bookmark mark='b'/> News on two percent of trades, each moving "
            "the value three ticks: the spread must be at least twelve hundredths of a tick wider than it would "
            "otherwise be. <bookmark mark='c'/> In a batch auction the maker can revise its order in the same batch as "
            "the news, and that part of the spread disappears."
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
        q = pause_card(r"a seller must sell 5\% of a market's daily volume, and uses an algorithm that trades 9\% of volume. "
                       r"Volume doubles because of its own selling. What happens to the time it takes?")
        with self.voiceover(
            "Pause and predict. A seller must sell five percent of a market's daily volume, using an algorithm that trades "
            "nine percent of volume. Its own selling doubles the volume. What happens to the time it takes?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
