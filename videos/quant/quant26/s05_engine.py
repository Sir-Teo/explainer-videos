"""Execution clocks and accounting with fixed quotes; no replacement historical strategy."""
from __future__ import annotations
from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT
from videos.quant.quant26.common import BAD, GOOD, PART, ask, house_lab

class Engine(VoiceoverScene):
    def construct(self):
        self.card()
        self.clock()
        self.ledger()
        self.frictions()
        self.split()
        self.dividends()
        self.lab()
        self.provenance()
        self.question()

    def card(self):
        c=chapter_card(4,r"Execution clocks and the event-driven engine",r"What price is available after the signal?",part=PART)
        with self.voiceover("Chapter four. Execution clocks and the event-driven engine. The original Yahoo-based calculation is unavailable because its recorded data hash does not match. We use fixed invented quotes and accounting identities to explain the mechanism, without generating another historical backtest."):
            self.play(FadeIn(c[0],shift=UP*.2),FadeIn(c[1]))
        self.play(FadeOut(c))

    def clock(self):
        head=label(r"One share; three explicitly invented quotes",font_size=32).to_edge(UP,buff=.5)
        boxes=VGroup(*[VGroup(RoundedRectangle(width=3.7,height=1.9,corner_radius=.12,stroke_color=QC.HOUSE),VGroup(label(t,font_size=23),MathTex(p,font_size=39),label(role,font_size=18,color=GREY_A)).arrange(DOWN,buff=.2)) for t,p,role in [(r'day 0 close',r'100',r'observe; then decide'),(r'day 1 open',r'102',r'assumed next-open fill'),(r'day 1 close',r'101',r'mark the position')]])
        for box in boxes:box[1].move_to(box[0])
        boxes.arrange(RIGHT,buff=.5).shift(UP*.3)
        arrows=VGroup(*[Arrow(boxes[i].get_right(),boxes[i+1].get_left(),buff=.07,color=QC.HOUSE) for i in range(2)])
        foot=wrapped_label(r"An observed close is information. Filling after observing it at that same price requires an explicit executable-order assumption. Next-open fills also remain a model, with market impact and order availability to assess.",12,22,GREY_A).to_edge(DOWN,buff=.7)
        with self.voiceover("Three invented quotes make the timing issue visible. The first close is one hundred, and the signal is computed after observing it. <bookmark mark='a'/> Suppose the next available modelled fill is the following open at one hundred and two. <bookmark mark='b'/> The next close is one hundred and one. Buying one share at the assumed open loses one dollar before costs. A calculation that instead fills at the already observed close would show a one-dollar gain. Neither path is a historical strategy result. The difference illustrates why the order clock and fill assumption must be stated.") as vo:
            self.play(FadeIn(head),FadeIn(boxes[0]));vo.wait_until('a');self.play(GrowArrow(arrows[0]),FadeIn(boxes[1]));vo.wait_until('b');self.play(GrowArrow(arrows[1]),FadeIn(boxes[2]),FadeIn(foot))
        self.clear_scene()

    def ledger(self):
        rows=[cmath(r"C_0,q",r"=",r"1000,1\quad\text{fixed illustration}",font_size=35),
              cmath(r"\Delta C",r"=",r"-qP_{\rm fill}-\text{fee}=-102-0.20",font_size=34),
              cmath(r"V_1",r"=",r"C_0+\Delta C+qP_{\rm mark}=998.80",font_size=35),
              cmath(r"r_1",r"=",r"V_1/C_0-1=-0.12\%",font_size=38)]
        whys=[why(r"One share on an explicit capital base; no leverage or rebalancing series is inferred"),why(r"The 20-cent fee is a declared illustration, not an estimated spread, impact or commission for any security"),why(r"Keep cash, inventory, marks and fees on the same clock"),why(r"Return depends on the capital denominator; a per-share price change is a different quantity")]
        step=ladder(self,rows,whys,keep=4,top=3.0,x=-.4,buff=.35,edge=6.8)
        with self.voiceover("Keep a ledger on a stated capital base. <bookmark mark='a'/> Start with one thousand dollars and buy one share at one hundred and two, with an illustrative fee of twenty cents. Cash falls by one hundred and two dollars and twenty cents. <bookmark mark='b'/> Marking that share at one hundred and one leaves portfolio value nine hundred and ninety-eight dollars and eighty cents. <bookmark mark='c'/> The return on the stated starting capital is minus point one two percent. The fee is a declared arithmetic assumption, not a calibrated market cost. Changing the capital denominator changes the reported return.") as vo:
            step(0);vo.wait_until('a');step(1);vo.wait_until('b');step(2);vo.wait_until('c');step(3)
        self.clear_scene()

    def frictions(self):
        cards=VGroup(
            desk_question(r"order the events",r"available observation; decision; submitted order; assumed fill; corporate actions; mark and financing. Match each input to its availability timestamp.",width=12,font_size=21),
            desk_question(r"declare the execution model",r"spread, commissions, borrow, financing, impact, participation, capacity and order availability need explicit assumptions; open/close bars do not identify queue priority.",width=12,font_size=21),
            desk_question(r"audit information outside the callback",r"A view restricted to past bars does not prevent revised inputs, leaked preprocessing, future-tuned parameters or hard-coded future information elsewhere.",width=12,font_size=21),
        ).arrange(DOWN,buff=.28)
        with self.voiceover("Event ordering reduces one class of mistakes. <bookmark mark='a'/> Match observations, decisions, orders, fills, corporate actions and marks to their own timestamps. Cost inputs must also be available at the fill time. <bookmark mark='b'/> An open-or-close fill model is not an order-book replay. Spread, commissions, impact, borrow, funding and capacity require assumptions or measurements; a touched price does not reveal queue priority or a guaranteed fill. <bookmark mark='c'/> Restricting the callback to past bars is useful, but it cannot stop future information embedded in revised data, leaked preprocessing, selected parameters or external code.") as vo:
            for i,mk in enumerate(('a','b','c')):
                if i:vo.wait_until(mk)
                self.play(FadeIn(cards[i],shift=UP*.2))
        self.clear_scene()

    def split(self):
        head=label(r"Fixed 4-for-1 split arithmetic",font_size=32).to_edge(UP,buff=.6)
        before=MathTex(r"1\ \text{share}\times100=100",font_size=40).shift(UP*.8)
        after=MathTex(r"4\ \text{shares}\times25=100",font_size=40,color=GOOD).shift(DOWN*.3)
        foot=wrapped_label(r"Ignoring the share-count change would create an artificial 75\% loss from the price change alone. Adjust positions, outstanding orders and per-share fields consistently; provider adjustment conventions differ.",12,23,GREY_A).to_edge(DOWN,buff=.7)
        with self.voiceover("Corporate actions must preserve the accounting. In a fixed four-for-one split, one share priced at one hundred becomes four shares priced at twenty-five. <bookmark mark='a'/> Value stays one hundred. Treating the price reduction alone as a return would create an artificial seventy-five-percent loss. <bookmark mark='b'/> Share counts, pending orders and per-share fields must use consistent conventions. This is fabricated split arithmetic, not an Apple event study or a new market calculation.") as vo:
            self.play(FadeIn(head),FadeIn(before));vo.wait_until('a');self.play(FadeIn(after));vo.wait_until('b');self.play(FadeIn(foot))
        self.clear_scene()

    def dividends(self):
        eq=MathTex(r"r_{\rm total}={P_1+D-P_0\over P_0}",font_size=42).to_edge(UP,buff=.8)
        fixed=MathTex(r"(98+2-100)/100=0",font_size=42,color=GOOD).next_to(eq,DOWN,buff=.65)
        foot=wrapped_label(r"Fixed one-share illustration before tax, fees, borrow and financing. An actual ex-dividend price can move for many reasons. Longs receive the payment; a short may owe an equivalent payment under its borrowing terms.",12,23,GREY_A).to_edge(DOWN,buff=.65)
        with self.voiceover("A dividend creates a cash flow as well as a price observation. <bookmark mark='a'/> In a fixed example, a share starts at one hundred, ends at ninety-eight and pays two in cash. Total return is zero before fees and taxes. Real ex-dividend prices can move for many other reasons. <bookmark mark='b'/> Account for payments to a long and equivalent-payment obligations on a short, using the provider's price-adjustment convention. No SPY dividend history or historical return is substituted here.") as vo:
            self.play(FadeIn(eq));vo.wait_until('a');self.play(FadeIn(fixed));vo.wait_until('b');self.play(FadeIn(foot))
        self.clear_scene()

    def lab(self):
        card=house_lab(r"The preserved event loop",BT.Backtester.run,"for t in range(n)",8,extra=((BT.Backtester._fill,"vol = lr",3),),width=11.8).move_to(ORIGIN)
        with self.voiceover("The House source remains unchanged. These exact excerpts show the original event loop and the lagged volatility and participation inputs used by its fill-cost routine. They are code excerpts, not empirical evidence that a fill was executable or a cost model calibrated. The existing pure numerical tests check the library on synthetic inputs; this review does not change the algorithm or run another historical strategy."):
            self.play(FadeIn(card))
        self.clear_scene()

    def provenance(self):
        card=desk_question(r"original Yahoo example unavailable",r"The EEM reader failed its protected recorded-source hash check before the original engine calculation could finish. Its code, raw public input and failure log are retained; no force, refresh or replacement historical result is used.",width=12,font_size=23)
        with self.voiceover("The original Yahoo calculation remains blocked at its EEM data-integrity check. Its algorithm, public input and failure evidence are preserved. We have not refreshed the manifest, displayed unavailable Sharpe ratios, or generated a replacement historical strategy. The fixed quotes and corporate-action examples explain the accounting separately."):
            self.play(FadeIn(card))
        self.clear_scene()

    def question(self):
        q=ask(r"After observing the fixed close 100, one share fills next open 102, is marked 101 and incurs a 0.20 fee. On capital 1000, explain both the cash ledger and the -0.12\% return.")
        with self.voiceover("Pause and predict. After the invented close of one hundred is observed, one share fills next open at one hundred and two, is marked at one hundred and one, and incurs the illustrative twenty-cent fee. On one thousand dollars of starting capital, explain the cash ledger and the minus point one two percent return. Which fill assumption would change the sign before costs?"):
            self.play(FadeIn(q))
        self.clear_scene()
