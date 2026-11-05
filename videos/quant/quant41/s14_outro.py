from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, NET_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)

DESK = [
    (r"A fund at 5$\times$ leverage loses 10\%. Its lender raises haircuts from 20\% to 30\%. What must it sell?",
     r"assets 100 $\to$ 90, equity 20 $\to$ 10; at a 30\% haircut it may hold $10/0.3 = 33.3$: sell 56.7, or 63\% of "
     r"the book"),
    (r"How can a solvent bank fail?",
     r"a run: if its assets fetch less than their value when sold early, withdrawing is a best response to others "
     r"withdrawing (Diamond--Dybvig); SVB in 2023"),
    (r"What is the difference between a loss spiral and a margin spiral?",
     r"a loss spiral sells to hold leverage constant as equity falls; a margin spiral sells because lenders lower the "
     r"leverage allowed; together they amplify a 3\% shock about sevenfold here"),
    (r"Is a more connected financial system safer?",
     r"for small shocks, yes: losses are shared; past a threshold, no: the complete network fails all at once "
     r"(Acemoglu, Ozdaglar and Tahbaz-Salehi)"),
    (r"How would you measure one bank's contribution to systemic risk?",
     r"CoVaR, the system's VaR when the bank is in distress, less its median; or MES and SRISK, the capital it would "
     r"lack in a crash"),
    (r"Why did Treasury yields rise in March 2020?",
     r"a dash for cash: foreign official holders, funds and basis traders sold, and dealers' balance sheets could not "
     r"absorb it until the Fed bought"),
]

PROBLEMS = [
    r"A fund at 4$\times$ leverage loses 5\% on its assets: its new leverage, and the sale that restores 4$\times$.",
    r"At 8$\times$ with a 10\% haircut, assets fall 3\% and the haircut doubles: the forced sale, as a share of the book.",
    r"A bank targets leverage $\lambda$; each unit sold lowers the price by $\gamma$. Show that a fall $\delta$ becomes "
    r"$\delta / (1 - \gamma(\lambda - 1)A)$.",
    r"A bank with assets 100 and equity 5 holds its leverage constant; its assets fall 1\%: what does it sell?",
    r"A owes B 2, B owes C 2, C owes A 1; outside assets $(0.5, 0, 0.3)$: the clearing vector and each bank's equity.",
    r"A complete network of 20 banks with assets $a = 2$ and senior debt $v = 1.5$: the shock that brings down all.",
    r"System on bank by quantile regression: slope 0.5; the bank's 5\% VaR is $-4\%$, its median $+0.1\%$: "
    r"$\Delta$CoVaR.",
    r"$k = 8\%$, debt 500, equity 20, LRMES 50\%: SRISK.",
    r"Diamond--Dybvig with $\theta = 1.2$, $r = 0.8$: the payoffs of withdrawing and of waiting when half withdraw.",
    r"A bank with deposits 100 and equity 8 holds bonds costing 90 with duration 6: the loss if rates rise 3 points.",
    r"(qual) Prove that a clearing vector exists, that it is unique when the system is regular, and that fictitious "
    r"default reaches it in at most $n$ rounds.",
    r"(qual) In Diamond--Dybvig with fire-sale value $r < 1$, derive the global-games threshold $\theta^*$, show that "
    r"$\theta^* > 1$, and that it falls toward 1 as the insured share rises to one.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("desk"), load("spiral"), load("firesale"), load("network"), load("systemic"), load("ltcm"),
                   load("gfc"), load("dash"), load("china"), load("dd"), load("house"), load("research"))
        self.lessons()
        self.formulas()
        self.connections()
        self.desk()
        self.answers()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, dk, sp, fs, nw, sy, lt, gf, ds, ch, dd, hs, rs):
        k2 = [x for x in sp["rows"] if x["kappa"] == 2.0][0]
        lb = sy["srisk"]
        items = [
            (r"booms build leverage; busts unwind it: Minsky's instability, Kindleberger's stages", LEV_C),
            (rf"a 5$\times$ fund that loses 10\% and faces a 30\% haircut sells {100 * dk['base']['sale_frac']:.0f}\% of "
             r"its book", FUND_C),
            (rf"loss and margin spirals together turn a 3\% shock into {100 * k2['fall']:.0f}\%", SPIRAL_C),
            (rf"fire sales through common holdings: the first round costs {100 * fs['first_share']:.0f}\% of the banks' "
             r"equity", SPIRAL_C),
            (r"clearing in a network: links share small losses and spread large ones", NET_C),
            (rf"systemic risk measured: Lehman's 2007 SRISK \${lb['srisk']:.0f}bn at {lb['leverage']:.0f}$\times$", BAD),
            (rf"LTCM at {lt['lev']:.0f}$\times$: one bet on liquidity, ended by a 4\% move", LEV_C),
        ]
        items2 = [
            (rf"2008: the TED spread from {gf['ted']['pre']:.2f} to {gf['ted']['max']:.2f}; a run on the shadow banks",
             FUND_C),
            (rf"March 2020: the ten-year yield rose {ds['y10']['m9']:.2f} $\to$ {ds['y10']['m18']:.2f} as stocks fell",
             PRICE_C),
            (rf"China 2015: margin-financed, {100 * -ch['fall']:.0f}\% down in eleven weeks; a breaker gone in four days",
             BAD),
            (rf"2023: a run on a solvent-looking bank; run threshold {dd['thr85']:.2f} at a fire-sale value of 0.85",
             FUND_C),
            (rf"Rule 41: at most {hs['lev_max']:.0f}$\times$, term funding, a cash buffer, no single door", QC.HOUSE),
            (rf"research: a unique clearing vector, {rs['agree']} of {rs['trials']} checks; the threshold $n(a - v)$",
             GOOD),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 41 in thirteen lines")
        with self.voiceover(
            "Part forty-one in thirteen lines. Booms build leverage and busts unwind it. A five-times fund that loses ten "
            "percent and faces a higher haircut must sell most of its book. Loss and margin spirals together turn a small "
            "shock into a large fall. Fire sales spread losses through common holdings. Links between banks share small "
            "losses and spread large ones. Systemic risk can be measured, and Lehman's was large. And LTCM showed what "
            "one crowded bet on liquidity can do."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 41 in thirteen lines")
        with self.voiceover(
            "In twenty oh eight the run was on the shadow banks. In March twenty twenty it was on the safest asset of all. "
            "In China in twenty fifteen it was margin debt, and a circuit breaker that pulled prices toward it. In "
            "twenty twenty-three it was a bank whose losses were in a footnote. The House's rule caps its leverage and "
            "secures its funding. And the research chapter proved that the clearing vector exists, is unique, and has a "
            "threshold in closed form."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"solvency is not enough", r"most of the firms in this part that failed looked solvent on paper; "
                          r"they could not fund themselves for a week", width=12.4, font_size=19),
            desk_question(r"the crowd is the risk", r"what one holder can sell, all holders cannot: common positions, "
                          r"common lenders and common models make a fall self-feeding", width=12.4, font_size=19),
            desk_question(r"backstops work, and cost", r"lenders of last resort, guarantees and purchases ended every "
                          r"panic here; each one changed what the next boom would expect", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Solvency is not enough: most of the firms in this part looked solvent on "
            "paper, and failed because they could not fund themselves for a week. <bookmark mark='b'/> The crowd is the risk: what one holder can sell, "
            "all holders cannot. <bookmark mark='c'/> And backstops work, and cost: each rescue ended a panic and "
            "changed what the next boom would expect."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"\text{sale} = A(1 - \ell) - \frac{E - A\ell}{h},\qquad \delta_{\text{total}} = "
                    r"\frac{\delta}{1 - \gamma(\lambda - 1)A}", font_size=30, color=FUND_C),
            MathTex(r"p^* = \min\bigl(\bar p,\ e + \Pi^\top p^*\bigr),\qquad \text{all default} \iff \varepsilon > n(a - v)",
                    font_size=30, color=NET_C),
            MathTex(r"\Delta\text{CoVaR}_i = \beta_i\bigl(\text{VaR}_{i,q} - \text{median}_i\bigr),\quad "
                    r"\text{SRISK} = kD - (1 - k)(1 - \text{LRMES})E", font_size=28, color=BAD),
            MathTex(r"\text{wait}(f) = \theta\,\frac{1 - f/r}{1 - f},\qquad \int_0^1 \bigl(\text{wait} - \text{early}\bigr)"
                    r"(f)\,df = 0 \Rightarrow \theta^*", font_size=30, color=SAFE_C),
        ).arrange(DOWN, buff=0.4)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "The part on one card. The forced sale, and the spiral's multiplier. The clearing vector, and the contagion "
            "threshold. CoVaR and SRISK. And the run: the payoff of waiting, and the integral that fixes the threshold."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4, run_time=5))
            self.wait(2)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 2's margin, Part 10's LTCM, Part 20's credit, Part 21's clearing, Part "
                          r"37's impact, Part 39's stablecoin runs and Part 40's risk numbers all meet in a crisis",
                          width=12.4, font_size=19),
            desk_question(r"sideways", r"the fire sale is Part 37's market impact, paid by everyone at once; the run is "
                          r"Part 39's depeg, with deposits instead of tokens", width=12.4, font_size=19),
            desk_question(r"forwards", r"Part 42 asks what happens when the crowd is made of machines sharing one model; "
                          r"Part 43, whether anyone is paid for bearing this risk", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: margin, LTCM, credit, clearing, impact, stablecoin "
            "runs and risk numbers all meet in a crisis. <bookmark mark='b'/> Sideways: a fire sale is market impact paid "
            "by everyone at once, and a bank run is a depeg with deposits. <bookmark mark='c'/> Forwards: Part forty-two "
            "asks what happens when the crowd is machines sharing one model, and Part forty-three whether anyone is paid "
            "for bearing this risk."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. The hook's: at five times, down ten percent, with a thirty percent haircut, sell "
            "fifty-six point seven of ninety. <bookmark mark='a'/> How can a solvent bank fail? A run, when assets sold "
            "early fetch less than they are worth. <bookmark mark='b'/> Loss spirals keep leverage constant; margin "
            "spirals lower the leverage allowed."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "Is a connected system safer? For small shocks, and not past the threshold. <bookmark mark='a'/> One bank's "
            "contribution to systemic risk? CoVaR, or SRISK. <bookmark mark='b'/> And why did Treasury yields rise in "
            "March twenty twenty? A dash for cash that dealers could not absorb. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self):
        cards = VGroup(
            desk_question(r"Research: the ring of three", r"regular, since every bank holds 0.5 outside, so the clearing "
                          r"vector is unique", width=12.4, font_size=20),
            desk_question(r"and it is full payment", r"$p = (1, 1, 1)$: each receives 1 and holds 0.5, so it can pay its "
                          r"1 and keeps 0.5 of equity; $\Phi(1, 1, 1) = (1, 1, 1)$", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The research chapter's pause, answered. <bookmark mark='a'/> Every bank holds a half outside, so the system "
            "is regular and the clearing vector unique. <bookmark mark='b'/> And it is full payment: each bank receives "
            "one, holds a half, pays its one and keeps a half. Plugging in confirms the fixed point."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: leverage after a loss; a forced sale; the spiral's multiplier; leverage targeting; a "
            "clearing vector by hand; a contagion threshold; CoVaR; SRISK; a run's payoffs; and a bank's rate loss. Then "
            "two qualifying-exam problems: the clearing theorem in full, and the global-games run threshold. Solutions, "
            "in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"machines in the market: herding when everyone shares a model, and flash crashes", [42]),
            (r"whether anyone is paid for bearing crash and liquidity risk", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part forty-two puts machines in the market, and asks whether a crowd sharing one "
            "model herds into the same spirals. And Part forty-three asks whether anyone is paid for bearing crash and "
            "liquidity risk."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Brunnermeier and Oehmke, ``Bubbles, Financial Crises, and Systemic Risk'' (2013); Gorton, \textit{Slapped "
             r"by the Invisible Hand} (2010); Kindleberger and Aliber, \textit{Manias, Panics, and Crashes} (2015); "
             r"Lowenstein, \textit{When Genius Failed} (2000)"],
            [r"Diamond and Dybvig (1983); Shleifer and Vishny (1992); Morris and Shin (1998); Allen and Gale (2000); "
             r"Eisenberg and Noe (2001); Goldstein and Pauzner (2005); Cifuentes, Shin and Rochet (2005); Brunnermeier and "
             r"Pedersen (2009); Adrian and Shin (2010); Geanakoplos (2010); Gorton and Metrick (2012)",
             r"Greenwood, Landier and Thesmar (2015); Acemoglu, Ozdaglar and Tahbaz-Salehi (2015); Glasserman and Young "
             r"(2015); Adrian and Brunnermeier (2016); Acharya, Pedersen, Philippon and Richardson (2017); Brownlees and "
             r"Engle (2017); Rogers and Veraart (2013). Data: FRED, Kenneth French's library, Yahoo Finance, SVB's 2022 "
             r"annual report"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Diamond and Dybvig to SRISK. Every number "
            "on screen was computed by the House's code from FRED, Kenneth French's daily returns through twenty twenty, "
            "public index data and public filings, or from simulation."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("treasury",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 42, Machines in the Market", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now knows how much leverage it can carry through a crisis, and why it must not count on anyone "
            "else's. <bookmark mark='a'/> Next, Part forty-two: machines in the market. Simulated markets, learning "
            "traders, algorithms that collude without speaking, and what happens when everyone shares a model."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
