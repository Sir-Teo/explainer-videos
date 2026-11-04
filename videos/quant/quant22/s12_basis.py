from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, BASIS, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class Basis(VoiceoverScene):
    def construct(self):
        b = load("basis")
        self.card()
        self.futures()
        self.options()
        self.trade(b)
        self.leverage(b)
        self.positions(b)
        self.march()
        self.now()

    def card(self):
        c = chapter_card(11, r"The Treasury basis trade", r"Who stands between the bond and its future?", lit=(2020,),
                         part=PART)
        with self.voiceover("Chapter eleven. The Treasury basis trade: the most leveraged trade in the safest market in "
                            "the world."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def futures(self):
        rows = [cmath(r"\text{invoice}", r"=", r"F \times CF_i + AI_i", font_size=40, colors={r"\text{invoice}": USD}),
                cmath(r"\text{CTD}", r"=", r"\arg\min_i\ \big(P_i - F \times CF_i\big)", font_size=40,
                      colors={r"\text{CTD}": BASIS})]
        whys = [why(r"a Treasury future lets the seller deliver any of a basket of notes; each is converted by a factor "
                    r"$CF_i$ (its price per 1 at a 6\% yield) and paid for with its accrued interest"),
                why(r"the seller delivers whichever is cheapest: the cheapest to deliver. The future tracks that note, "
                    r"adjusted by its conversion factor")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A Treasury future is a promise to deliver a government note in a few months. Not one particular note: "
            "any of a basket, each scaled by a conversion factor, its price per dollar at a six percent yield. "
            "<bookmark mark='a'/> The seller chooses which to deliver, and chooses the cheapest. So the future tracks "
            "one note, the cheapest to deliver, and the gap between that note's price and the future's, scaled, is the "
            "basis."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def options(self):
        cards = VGroup(
            desk_question(r"the quality option", r"the short chooses which note to deliver; if yields move, the cheapest "
                          r"can switch, and the short keeps the better choice", width=12.0, font_size=20),
            desk_question(r"the timing options", r"the short chooses the day within the delivery month, and for a few "
                          r"hours after the futures settle each day can still announce delivery at that price (the "
                          r"'wild card')", width=12.0, font_size=20),
            desk_question(r"what they do to the price", r"options held by the short make the future cheaper than the "
                          r"cheapest note's forward: part of the basis is the value of these options, not free money",
                          width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The seller of a future holds options. <bookmark mark='a'/> It chooses which note to deliver, and if "
            "yields move far enough the cheapest one changes, so it keeps the better of several. "
            "<bookmark mark='b'/> It chooses the day within the delivery month, and for some hours after each day's "
            "settlement it can still announce delivery at that price. <bookmark mark='c'/> Options held by the seller "
            "make the future cheaper than the cheapest note's forward. Part of the basis is the value of those "
            "options, and a basis trader who forgets them has sold them for nothing."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def trade(self, b):
        tr = b["trade"]
        rows = [cmath(r"\text{implied repo}", r"=", r"\Big(\frac{F\,CF + AI_T}{P + AI_0} - 1\Big)\frac{360}{d}",
                      font_size=38, colors={r"\text{implied repo}": GOOD})]
        whys = [why(r"buy the note now at its dirty price, deliver it into the future at the invoice price: the return "
                    r"on that round trip, as a money-market rate. If it beats the repo rate at which the note can be "
                    r"financed, buying cash and selling futures earns the difference")]
        step = ladder(self, rows, whys, keep=1, top=2.6, x=-0.4, buff=0.8, edge=6.9)
        nums = VGroup(
            MathTex(rf"P + AI_0 = {tr['clean']:.2f} + {tr['dirty'] - tr['clean']:.2f} = {tr['dirty']:.2f}", font_size=30),
            MathTex(rf"F\,CF + AI_T = {tr['fut']:.2f}\times{tr['cf']:.4f} + {tr['accrued_T']:.2f} = {tr['invoice']:.2f}",
                    font_size=30),
            MathTex(rf"\text{{implied repo}} = {100 * tr['implied_repo']:.2f}\%\ \text{{over}}\ {tr['days']}\ \text{{days}}",
                    font_size=32, color=GOOD),
            wrapped_label(r"an illustrative note with a 4\% coupon and no coupon paid before delivery; the numbers are "
                          r"made up to show the arithmetic, not taken from a market", 11.0, 17, GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The arbitrage is the same shape as chapter seven's cash and carry. Buy the note, finance it with a repo, "
            "sell the future, and deliver the note at the end. The return on that round trip, written as an interest "
            "rate, is the implied repo rate. <bookmark mark='a'/> With these made-up numbers, buying at "
            f"{tr['dirty']:.2f} and delivering for {tr['invoice']:.2f} three months later earns "
            f"{100 * tr['implied_repo']:.2f} percent a year. If the note can be financed for less than that, the trade "
            "locks in the difference. Futures usually trade a little rich to cash, because asset managers like to hold "
            "their duration in futures, which need little cash; the basis trader is paid to be on the other side."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nums], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def leverage(self, b):
        rows = [cmath(r"\text{return on capital}", r"\approx", r"\frac{\text{implied repo} - \text{repo}}{h}", font_size=40,
                      colors={r"\text{return on capital}": GOOD}),
                cmath(r"\text{loss on margin call}", r"=", r"\Delta(\text{basis})\times\frac{1}{h}", font_size=38,
                      colors={r"\text{loss on margin call}": BAD})]
        whys = [why(r"the spread is a few tens of basis points, so it is levered: repo lends almost the whole price of "
                    r"the note, against a haircut $h$ of a few percent; at $h$ = 2\%, fifty to one"),
                why(r"the trade is riskless only if held to delivery. Before then, the basis can widen, and the futures "
                    r"leg's margin is called in cash, every day")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A few tens of basis points is not worth having unlevered. So the note is financed almost entirely "
            "with repo: the lender keeps a haircut of a percent or two, and the rest is borrowed. At a two percent "
            "haircut the trade is levered fifty to one, and twenty basis points of spread becomes ten percent a year "
            "on capital. <bookmark mark='a'/> It is riskless only if held to delivery. Along the way, the basis can "
            "widen, the futures margin is called in cash every day, and the repo lender can raise the haircut. A "
            "riskless trade levered fifty times is a liquidity trade."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def positions(self, b):
        t, lev, am = np.asarray(b["t"]), np.asarray(b["lev"]), np.asarray(b["am"])
        g = axes([2010, 2026], [-1200, 1200], x_length=8.2, y_length=4.4, xlabel=r"year",
                 ylabel=r"net futures position, \$ billion of face", xticks=[2010, 2014, 2018, 2022, 2026],
                 yticks=[-1000, -500, 0, 500, 1000], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(2010, 0), ax.c2p(2026, 0), color=WHITE, stroke_width=1.2)
        ll = curve(ax, t, lev, BAD, stroke_width=2.4)
        la = curve(ax, t, am, USD, stroke_width=2.4)
        side = VGroup(
            legend([(USD, r"asset managers (long)"), (BAD, r"leveraged funds (short)")], font_size=17),
            MathTex(rf"\text{{end of 2025}}:\ {b['lev_last']:,.0f}".replace(",", "{,}"), font_size=26, color=BAD),
            wrapped_label(r"the CFTC's Traders in Financial Futures report, weekly: 2-, 5-, 10-year and bond futures, "
                          r"at face value. Leveraged funds' shorts overstate the basis trade, which is their short "
                          r"futures matched by long cash; the Fed's estimates use both legs", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "You can watch the trade grow in public data. Every week the futures regulator publishes who holds "
            "Treasury futures. <bookmark mark='a'/> Asset managers are long: they hold duration in futures. Leveraged "
            "funds are short, the mirror image, and most of their shorts are the futures leg of basis trades. "
            f"<bookmark mark='b'/> By the end of 2025 they were short about {abs(b['lev_last']) / 1000:.1f} trillion "
            f"dollars of face value, {abs(b['lev_last'] / b['lev_feb2020']):.1f} times their position on the eve of "
            "March 2020."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(la), Create(ll), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.add(illustration(r"CFTC Traders in Financial Futures: 042601, 044601, 043602, 020601"))
        self.wait(0.4)
        self.clear_scene()

    def march(self):
        cc = crisis_card(r"March 2020", r"The dash for cash",
                         r"as the pandemic hit, foreign central banks, funds and companies sold Treasuries for cash; "
                         r"dealers' balance sheets filled; cash Treasuries cheapened against futures, the basis widened, "
                         r"and leveraged funds faced margin calls on both legs. The Fed's staff later estimated that hedge "
                         r"funds sold about \$173 billion of Treasuries that month, most of it by likely basis traders. "
                         r"On 23 March the Fed promised to buy Treasuries 'in the amounts needed'",
                         stats=[(r"\$173\text{bn}", r"hedge funds' Treasury sales, March 2020 (Fed staff)")], width=8.8,
                         font_size=19).move_to(UP * 0.3)
        with self.voiceover(
            "In March 2020 the safest market in the world seized. Foreign central banks, funds and companies sold "
            "Treasuries to raise cash; dealers' balance sheets filled up, and cash notes cheapened against futures. The "
            "basis widened, margin was called on both legs, and repo lenders raised haircuts. The Federal Reserve's "
            "staff later estimated that hedge funds sold about a hundred and seventy-three billion dollars of "
            "Treasuries that month, mostly the likely basis traders. On the twenty-third of March the Fed promised to "
            "buy Treasuries in whatever amounts were needed, and became, for a while, the basis trader of last resort."
        ) as vo:
            self.play(FadeIn(cc))
        self.add(illustration(r"Glicoes, Iorio, Monin and Petrasek, FEDS Notes (8 March 2024); FOMC statement, 23 March 2020"))
        self.wait(0.4)
        self.clear_scene()

    def now(self):
        cards = VGroup(
            desk_question(r"its size since", r"Fed staff estimates: \$260--574 billion at the end of September 2023; "
                          r"about \$830 billion by September 2025, roughly double the early-2020 peak (Monin, FEDS Notes, "
                          r"June 2026)", width=12.0, font_size=20),
            desk_question(r"why it exists", r"it moves duration from asset managers, who want it in futures, into the "
                          r"cash market, through funds willing to carry balance sheet that dealers no longer will (chapter "
                          r"1's leverage ratio again)", width=12.0, font_size=20),
            desk_question(r"the worry", r"a crowded, levered trade financed overnight: if repo lenders pull back in a "
                          r"stress, the unwind sells Treasuries into a falling market. Central clearing of more Treasury "
                          r"repo, required by the SEC's 2023 rule, is one response", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The trade came back larger. <bookmark mark='a'/> Fed staff estimated it at between two hundred and sixty "
            "and five hundred and seventy-four billion dollars at the end of September 2023, and at about eight hundred "
            "and thirty billion by September 2025, roughly double its early-2020 peak. <bookmark mark='b'/> It is not "
            "a bubble: it does a job, moving duration from asset managers, who want it in futures, into the cash "
            "market, through funds willing to carry balance sheet that dealers, since 2008, will not. "
            "<bookmark mark='c'/> But it is financed overnight, and if the financing goes, the unwind sells "
            "Treasuries into a falling market. The SEC's 2023 rule pushing more Treasury repo into central clearing "
            "is one answer; Part twenty-one's waterfall, applied to the government bond market."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a basis trade earns 20 bp a year on a 2\% repo haircut. Repo lenders raise the haircut to 6\% overnight. "
                r"What happens to the trade's return on capital, and to the trader who cannot raise more capital?")
        with self.voiceover("A basis trade earns twenty basis points on a two percent haircut. Overnight the haircut goes "
                            "to six percent. What happens to its return on capital, and to the trader who cannot raise "
                            "more?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
