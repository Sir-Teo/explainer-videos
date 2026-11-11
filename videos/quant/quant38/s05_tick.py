from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, FAST_C, GOOD, HURDLE, PART, SPREAD_C, load)


class Tick(VoiceoverScene):
    def construct(self):
        b = load("bcs")
        self.card()
        self.pinned()
        self.rent(b)
        self.queue_race()
        self.pro_rata()
        self.waiting()
        self.optimal_tick()
        self.subtick()
        self.who_gains()
        self.rules()
        self.question()

    def card(self):
        c = chapter_card(4, r"Tick size and queue position", r"What happens when the tick, not competition, sets the spread?",
                         part=PART)
        with self.voiceover("Chapter four, and the answer to the pause: no. On a book pinned at one tick, a smaller tick "
                            "lets the spread narrow only to where competition would put it, and it moves the contest from "
                            "queue position to price. Takers gain from the narrower spread; makers who held the front of "
                            "long queues lose their rent."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pinned(self):
        rows = [cmath(r"s_{\text{natural}}", r"<", r"\text{tick}", font_size=40),
                cmath(r"\Rightarrow", r"\ ", r"s = 1\ \text{tick, long queues}", font_size=38),
                cmath(r"\text{competition}", r"\to", r"\text{for priority, not price}", font_size=36,
                      colors={r"\text{for priority, not price}": FAST_C})]
        whys = [why(r"the spread makers would accept, if they could quote any price, is smaller than the minimum "
                    r"increment"),
                why(r"so the spread sits at one tick, and the makers who would undercut each other cannot: they queue"),
                why(r"the only way to get more of the flow is to be earlier in the line, which is a race in speed")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A pinned spread. <bookmark mark='a'/> When the spread makers would accept is smaller than the tick, "
            "<bookmark mark='b'/> the spread sits at one tick and the queues grow long: makers who would undercut each "
            "other cannot. <bookmark mark='c'/> So they compete for priority instead of price, and priority goes to "
            "whoever arrives first: a race in speed."
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

    def rent(self, b):
        bt = b["btc"]
        rows = [cmath(r"\lambda_I", r"\approx", rf"{bt['lam_i']:.0f}\ \text{{trades a second}}", font_size=36),
                cmath(r"\lambda_J,\ J", r"\approx", rf"{bt['lam_j']:.2f}\ \text{{a second}},\ {bt['J']:.0f}\ \text{{ticks}}",
                      font_size=36),
                cmath(r"\tfrac{s^*}{2}", r"=", rf"\frac{{\lambda_J J}}{{\lambda_I + \lambda_J}} \approx {bt['half']:.2f}\ "
                      r"\text{tick}", font_size=36, colors={r"\tfrac{s^*}{2}": HURDLE}),
                cmath(r"\tfrac{s}{2}", r"=", r"0.5\ \text{tick (pinned)}", font_size=38, colors={r"\tfrac{s}{2}": SPREAD_C})]
        whys = [why(r"takers' trades on Bitcoin's perpetual, 16--17 May, as a rough rate of uninformed arrivals"),
                why(r"proxy jumps: net mid moves of five ticks or more in a tenth of a second, and their mean size"),
                why(r"the sniping model of Chapter 6 and the research chapter: the half-spread that compensates for being "
                    r"picked off"),
                why(r"this substitution lies below the quoted half-tick floor; actual natural spread and rent are not identified by "
                    r"these proxies")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"A rough model substitution. <bookmark mark='a'/> Treat the aggregate trade count, about {bt['lam_i']:.0f} per second, as a proxy investor rate. <bookmark mark='b'/> Net mid changes of at least five ticks occur about {bt['lam_j']:.2f} per second, with mean size {bt['J']:.0f}. These are not identified public-news events or unit uninformed arrivals. <bookmark mark='c'/> The formula then gives {bt['half']:.2f} tick. <bookmark mark='d'/> That is below the quoted half-tick floor in this illustrative model. It does not establish the actual natural spread, rent, or the source of the replay losses."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def queue_race(self):
        cards = VGroup(
            desk_question(r"different replay fill sets", r"Part 36 compared front and back gross functionals per "
                          r"submission; selected fill sets differ, so their gap is not causal priority value", width=12.4, font_size=19),
            desk_question(r"how to be first", r"post at a price before it becomes the best, keep orders resting through "
                          r"small moves, and be the fastest to rejoin after a level clears", width=12.4, font_size=19),
            desk_question(r"queue-jumping", r"some venues sell priority by other means: size pro rata in some futures, "
                          r"or order types that rest in the book in ways others cannot", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Queue priority changes who can execute. <bookmark mark='a'/> Part thirty-six compared front and back replay functionals on different filled sets. Their gap was not a causal price for moving one order forward. <bookmark mark='b'/> Posting earlier can obtain priority, subject to cancellation and queue rules. <bookmark mark='c'/> Some futures use pro-rata size allocation or hybrid rules. Those designs change incentives, but their welfare cannot be inferred from one replay."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def pro_rata(self):
        rows = [cmath(r"\text{time priority}", r":", r"\text{first in, first filled}", font_size=36, colors={r"\text{time priority}": FAST_C}),
                cmath(r"\text{pro rata}", r":", r"\text{fill} \propto \text{size resting at the price}", font_size=36),
                cmath(r"\text{pro rata}", r"\Rightarrow", r"\text{oversize orders, size races}", font_size=36,
                      colors={r"\text{oversize orders, size races}": BAD})]
        whys = [why(r"the rule of most stock and crypto books: speed buys position"),
                why(r"used in some interest-rate futures: an incoming order is split across resting orders in proportion to "
                    r"their size, often with a top-of-book allocation first"),
                why(r"makers post far more than they want, since fills scale with size; the race moves from time to "
                    r"size, and the displayed depth overstates what anyone intends to trade")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Another way to share a pinned spread. <bookmark mark='a'/> Time priority, the rule of most stock and crypto "
            "books, makes speed buy position. <bookmark mark='b'/> Pro-rata matching, used in some interest-rate futures, "
            "splits each incoming order across the resting orders in proportion to their size. <bookmark mark='c'/> Then "
            "makers post far more than they want, because fills scale with size: the race moves from speed to size, and "
            "displayed depth overstates what anyone intends to trade."
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

    def waiting(self):
        rows = [cmath(r"\text{back of the queue}", r":", r"\text{median wait } 3.2\ \text{s},\ 82\%\ \text{filled in a minute}",
                      font_size=32),
                cmath(r"\text{front}", r":", r"\text{median wait } 0.2\ \text{s},\ 94\%", font_size=34),
                cmath(r"\text{priority}", r"=", r"\text{different conditional fills}", font_size=38, colors={r"\text{priority}": FAST_C})]
        whys = [why(r"Part 36's replay of a passive order on Bitcoin's perpetual"),
                why(r"the same order at the head of the line"),
                why(r"the replay front fills sooner on a different selected set; informed identities and causal rent are not "
                    r"identified here")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Recall the chosen queue reconstruction. <bookmark mark='a'/> Its back-of-queue filled orders have a median wait around three seconds, with roughly four in five submissions filled within a minute. <bookmark mark='b'/> Front placement has a median around a fifth of a second. <bookmark mark='c'/> These conditional waiting summaries and fill probabilities have different censoring and selected sets. Smaller adverse marks do not identify less informed trader identities or a causal gain from priority."
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

    def optimal_tick(self):
        rows = [cmath(r"\text{tick too large}", r":", r"\text{spreads too wide, queues, speed races}", font_size=34,
                      colors={r"\text{tick too large}": BAD}),
                cmath(r"\text{tick too small}", r":", r"\text{flickering quotes, pennying, thin best levels}", font_size=32,
                      colors={r"\text{tick too small}": BAD}),
                cmath(r"\text{optimum}", r":", r"\text{a spread of a little more than one tick}", font_size=34,
                      colors={r"\text{optimum}": GOOD})]
        whys = [why(r"takers pay a spread set by the rule, not by competition, and makers spend on speed to hold their "
                    r"place"),
                why(r"anyone can step ahead of a queue by a trivial amount, so displayed liquidity is fleeting"),
                why(r"Dayri and Rosenbaum (2015): choose the tick so that the average spread is somewhat above one tick, "
                    r"where price competition works but quotes are worth posting")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "So what is the right tick? <bookmark mark='a'/> Too large, and spreads are set by the rule, queues are long, "
            "and makers spend on speed. <bookmark mark='b'/> Too small, and anyone can step ahead of a queue by a "
            "trivial amount, so quotes flicker and the best levels thin out. <bookmark mark='c'/> Khalil Dayri and "
            "Mathieu Rosenbaum proposed choosing the tick so the average spread sits a little above one tick, where "
            "competition on price works and quotes are still worth posting."
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

    def subtick(self):
        rows = [cmath(r"\text{quoted}", r":", r"1\ \text{tick}", font_size=40),
                cmath(r"\text{effective for a taker}", r"=", r"1\ \text{tick} + 2 \times \text{take fee}", font_size=34,
                      colors={r"\text{effective for a taker}": BAD}),
                cmath(r"\text{effective for a maker}", r"=", r"1\ \text{tick} + 2 \times \text{rebate}", font_size=34,
                      colors={r"\text{effective for a maker}": GOOD})]
        whys = [why(r"the price grid stops at one tick"),
                why(r"fixed-mid round-trip illustration, matching price units and equal per-side fees; other costs omitted"),
                why(r"the opposite completed round trip earns spread and rebates before adverse marks and other costs; this "
                    r"is an accounting illustration, not unconditional maker profit (Part 35)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A static fee illustration with a common price benchmark. <bookmark mark='a'/> Hold the mid fixed, with one tick between bid and ask. <bookmark mark='b'/> A taker round trip pays that spread plus two equal per-unit taker fees. <bookmark mark='c'/> A maker completing the opposite round trip earns it plus two equal rebates, before adverse marks and other costs. Fees must use matching price units; changing prices and inventory prevent interpreting this as unconditional profit."
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

    def who_gains(self):
        rows = [cmath(r"\text{tick} \downarrow", r"\Rightarrow", r"\text{spread} \to s_{\text{natural}}", font_size=38),
                cmath(r"\text{takers}", r":", r"\text{pay less per trade}", font_size=36, colors={r"\text{takers}": GOOD}),
                cmath(r"\text{front-of-queue makers}", r":", r"\text{lose their rent}", font_size=34,
                      colors={r"\text{front-of-queue makers}": BAD})]
        whys = [why(r"once the tick no longer binds, competition sets the spread"),
                why(r"the investors and executors of Part 37"),
                why(r"the firms that won the queue race; displayed depth at the best also thins, since the queue's value "
                    r"is gone, which can raise the cost of large orders")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "So who gains when the tick shrinks? <bookmark mark='a'/> Once it no longer binds, competition sets the "
            "spread. <bookmark mark='b'/> Takers pay less per trade. <bookmark mark='c'/> The makers who won the queue "
            "race lose their rent. And the displayed depth at the best thins out, which can make large orders costlier "
            "even as small ones get cheaper."
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

    def rules(self):
        cards = VGroup(
            desk_question(r"the US tick pilot", r"from 2016 to 2018 the SEC widened the tick for a sample of small stocks "
                          r"to five cents; spreads widened and depth rose, and the results were mixed for investors",
                          width=12.4, font_size=19),
            desk_question(r"the historical 2024 adoption", r"the half-cent tick for liquid stocks pinned at a cent, and lower "
                          r"access-fee caps (Part 35)", width=12.4, font_size=19),
            desk_question(r"crypto", r"exchanges set their own ticks and change them, sometimes for one pair at a time; "
                          r"each change moves rents between takers and makers", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Historical rule changes. <bookmark mark='a'/> The United States tick-size pilot ran from twenty sixteen to twenty eighteen for selected small stocks. Published evaluations found wider spreads and changed displayed depth, with mixed investor effects. <bookmark mark='b'/> The SEC adopted half-cent increments for qualifying stocks in twenty twenty-four. Adoption and compliance are separate dates; this is a historical example, not a statement of the rule currently in force. <bookmark mark='c'/> Crypto venues also revise increments, changing queue and price incentives."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label('an ETF that holds corporate bonds trades at \\$80 while the published value of its bonds is \\$84. Who could profit, how, and why might they not?', 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. An ETF holding corporate bonds trades at eighty dollars, while the published value of "
            "its bonds is eighty-four. Who could profit, how, and why might they not?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
