from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SPIRAL_C, load)


class Cycles(VoiceoverScene):
    def construct(self):
        dk = load("desk")
        self.card(dk)
        self.balance()
        self.haircut()
        self.grid(dk)
        self.minsky()
        self.kindleberger()
        self.geanakoplos()
        self.two_liquidities()
        self.question()

    def card(self, dk):
        b = dk["base"]
        c = chapter_card(1, r"Leverage and its cycle", r"Why does a small loss become a large sale?", part=PART)
        with self.voiceover(
            f"Chapter one, and the answer to the pause: {b['sale']:.1f} of its {b['assets']:.0f}, almost two thirds of "
            f"what it holds. The loss alone takes its equity from twenty to {b['equity']:.0f}; the higher haircut lets "
            f"that equity carry only {b['max_assets']:.1f} of assets. A ten percent loss forces a sixty percent sale. "
            "That arithmetic is the engine of every crisis in this part."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def balance(self):
        rows = [cmath(r"A", r"=", r"E + D", font_size=48),
                cmath(r"\lambda", r"=", r"A/E", font_size=48, colors={r"\lambda": LEV_C}),
                cmath(r"r_E", r"=", r"\lambda\,r_A - (\lambda - 1)\,r_D", font_size=44),
                cmath(r"r_A = -1/\lambda", r"\Rightarrow", r"E = 0", font_size=44, colors={r"E = 0": BAD})]
        whys = [why(r"assets are funded by equity and debt"),
                why(r"leverage: assets per unit of equity, Part 2's margin account"),
                why(r"the return on equity multiplies the return on assets by the leverage, less the cost of the debt"),
                why(r"at 5$\times$ a 20\% fall wipes out the equity; at 30$\times$, as Lehman ran in 2007, about 3\%")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The arithmetic. <bookmark mark='a'/> Assets are funded by equity and debt. <bookmark mark='b'/> Leverage is "
            "assets per unit of equity. <bookmark mark='c'/> So the return on equity is leverage times the return on "
            "assets, less the cost of the debt. <bookmark mark='d'/> And a fall of one over the leverage wipes the equity "
            "out: at five times, twenty percent; at thirty times, as Lehman Brothers ran at the end of twenty oh seven, "
            "as reported, about three."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def haircut(self):
        rows = [cmath(r"\text{loan}", r"=", r"(1 - h) \times \text{collateral}", font_size=42, colors={r"\text{loan}": FUND_C}),
                cmath(r"\lambda_{\max}", r"=", r"1/h", font_size=48, colors={r"\lambda_{\max}": LEV_C}),
                cmath(r"h: 20\% \to 30\%", r"\Rightarrow", r"\lambda_{\max}: 5 \to 3.3", font_size=42)]
        whys = [why(r"a secured lender, in repo or a prime broker's margin account, lends less than the collateral is "
                    r"worth: the difference is the haircut, Part 2's margin"),
                why(r"so the haircut caps leverage: every dollar of assets needs $h$ of the holder's own money"),
                why(r"when lenders grow nervous they raise haircuts, and every leveraged holder must shrink at once")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Where the leverage comes from. <bookmark mark='a'/> A secured lender lends less than the collateral is worth; "
            "the gap is the haircut. <bookmark mark='b'/> So the haircut caps leverage at one over itself. "
            "<bookmark mark='c'/> When lenders grow nervous they raise haircuts, and every leveraged holder of that "
            "collateral must shrink at the same moment."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def grid(self, dk):
        losses = sorted({g["loss"] for g in dk["grid"]})
        hcs = sorted({g["haircut"] for g in dk["grid"]})
        hx = [-4.2] + [-1.6 + 2.0 * j for j in range(len(hcs))]
        head = VGroup(label(r"loss, then haircut", font_size=15, color=GREY_B),
                      *[label(rf"$h = {100 * h:.0f}\%$", font_size=16, color=GREY_B) for h in hcs])
        tab = VGroup(head)
        for lo in losses:
            cells = [label(rf"loss {100 * lo:.0f}\%", font_size=18)]
            for h in hcs:
                g = [x for x in dk["grid"] if x["loss"] == lo and x["haircut"] == h][0]
                cells.append(MathTex(rf"{100 * g['frac']:.0f}\%", font_size=26,
                                     color=BAD if g["frac"] > 0.5 else (HURDLE if g["frac"] > 0 else GOOD)))
            tab.add(VGroup(*cells))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.8 * j, 0])
        foot = wrapped_label(r"share of its remaining assets a fund at 5$\times$ (100 of assets, 20 of equity) must sell", 11.0,
                             17, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The whole table, for a fund at five times. <bookmark mark='a'/> With no loss, a rise in the haircut from twenty "
            "to thirty percent alone forces a third of the book to be sold. <bookmark mark='b'/> With a loss, the two "
            "compound: ten percent down at a forty percent haircut leaves the fund able to hold only a quarter of what "
            "it has. Losses and haircuts move together in a crisis, which is why they must be read together."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def minsky(self):
        cards = VGroup(
            desk_question(r"hedge finance", r"income covers both interest and principal: the borrower is safe whatever "
                          r"the market does", width=12.4, font_size=19),
            desk_question(r"speculative finance", r"income covers the interest only: the principal must be rolled over, so "
                          r"the borrower depends on lenders staying willing", width=12.4, font_size=19),
            desk_question(r"Ponzi finance", r"income covers neither: the borrower depends on rising asset prices to "
                          r"refinance; stability breeds the confidence that moves borrowers down this list", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Hyman Minsky's three kinds of borrower. <bookmark mark='a'/> Hedge finance: income covers interest and "
            "principal. <bookmark mark='b'/> Speculative finance: income covers the interest, and the principal must be "
            "rolled over, so the borrower depends on lenders. <bookmark mark='c'/> Ponzi finance: income covers neither, "
            "and the borrower depends on rising prices. His point was that calm years move borrowers down the list: "
            "stability breeds instability."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def kindleberger(self):
        stages = [(r"displacement", r"a new technology or policy", PRICE_C), (r"boom", r"credit expands", LEV_C),
                  (r"euphoria", r"prices outrun income", HURDLE), (r"distress", r"insiders sell", FUND_C),
                  (r"panic", r"everyone sells", SPIRAL_C)]
        boxes = VGroup()
        for nm, what, col in stages:
            b = RoundedRectangle(width=2.3, height=1.3, corner_radius=0.12, stroke_color=col, fill_color=col,
                                 fill_opacity=0.12)
            t = VGroup(label(nm, font_size=20, color=col), label(what, font_size=14, color=GREY_A)).arrange(DOWN, buff=0.1)
            boxes.add(VGroup(b, t.move_to(b)))
        boxes.arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.03, stroke_width=3, color=GREY_B,
                                tip_length=0.13) for i in range(4)])
        foot = wrapped_label(r"Charles Kindleberger's \textit{Manias, Panics, and Crashes} (1978): the same five stages, from "
                             r"the South Sea Bubble to the crises of this part", 11.4, 17, GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Charles Kindleberger's anatomy of a crisis. <bookmark mark='a'/> A displacement, a new technology or policy, "
            "opens profits; credit expands into a boom; prices outrun income in euphoria. <bookmark mark='b'/> Insiders "
            "sell in distress, and then everyone sells in panic. He found the same five stages from the South Sea "
            "Bubble onward; this part's crises follow them too."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes[:3]], lag_ratio=0.3), Create(arrows[:2]))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Create(arrows[2:]), FadeIn(boxes[3:]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def geanakoplos(self):
        rows = [cmath(r"\text{price}", r"=", r"\text{the marginal buyer's value}", font_size=40),
                cmath(r"\text{low haircuts}", r"\Rightarrow", r"\text{optimists hold everything}", font_size=38,
                      colors={r"\text{low haircuts}": LEV_C}),
                cmath(r"\text{bad news} + \text{higher haircuts}", r"\Rightarrow", r"\text{optimists sell to pessimists}",
                      font_size=34, colors={r"\text{bad news} + \text{higher haircuts}": SPIRAL_C})]
        whys = [why(r"John Geanakoplos's leverage cycle: when buyers differ in their views, the price is set by whoever "
                    r"buys the last unit"),
                why(r"with generous collateral terms, the most optimistic buyers can lever up and own the whole supply: "
                    r"prices sit above the average view"),
                why(r"when news is bad and haircuts rise together, optimists are wiped out and the asset passes to "
                    r"pessimists: the price falls by more than the news")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "John Geanakoplos's leverage cycle. <bookmark mark='a'/> When buyers disagree, the price is set by whoever buys "
            "the last unit. <bookmark mark='b'/> With low haircuts, the most optimistic can borrow enough to own the whole "
            "supply, and the price sits above the average view. <bookmark mark='c'/> When bad news arrives and haircuts "
            "rise together, the optimists are wiped out and the asset passes to pessimists: the price falls by far more "
            "than the news."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def two_liquidities(self):
        cards = VGroup(
            desk_question(r"market liquidity", r"how much a sale moves the price: Part 36's book and Part 37's square "
                          r"root", width=12.4, font_size=19),
            desk_question(r"funding liquidity", r"how easily a position can be financed: haircuts, margins and the "
                          r"willingness of lenders to roll, Parts 2 and 21", width=12.4, font_size=19),
            desk_question(r"they feed each other", r"lower prices raise margins, higher margins force sales, sales lower "
                          r"prices: Brunnermeier and Pedersen's spirals, the next chapter", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two kinds of liquidity. <bookmark mark='a'/> Market liquidity: how much a sale moves the price, Parts "
            "thirty-six and thirty-seven. <bookmark mark='b'/> Funding liquidity: how easily a position can be financed, "
            "Parts two and twenty-one. <bookmark mark='c'/> And they feed each other: lower prices raise margins, higher "
            "margins force sales, and sales lower prices."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a leveraged holder owns a large share of an asset's market. News knocks 3\% off the price. If it must "
                       r"keep its margin, and margins rise as prices fall, how far can the price end up falling?")
        with self.voiceover(
            "Pause and predict. A leveraged holder owns a large share of an asset's market. News knocks three percent off "
            "the price. If it must keep its margin, and margins rise as prices fall, how far can the price end up "
            "falling?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
