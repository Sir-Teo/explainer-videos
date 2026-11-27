from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Lean(VoiceoverScene):
    def construct(self):
        card(self, 6, "Lean production", "Why did the whole industry copy Toyota, and what did it bet?",
             "Chapter six. Lean production. Why did the whole industry copy Toyota, and what did it bet?",
             lit=("make", "change"))
        self.push_pull()
        self.supply()
        self.chips()

    def _line(self, y, label, col, below=False):
        xs = [-4.5, -1.5, 1.5, 4.5]
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.6, height=0.8, stroke_color=col, stroke_width=2,
                                          fill_color="#141A24", fill_opacity=1).move_to([x, y, 0]) for x in xs])
        names = VGroup(*[tx(n, 14, GREY_A).move_to(b) for n, b in zip(("press", "body", "paint", "assembly"), boxes)])
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=2, color=GREY_B,
                                max_tip_length_to_length_ratio=0.15) for i in range(3)])
        lab = tx(label, 18, col, bold=True).next_to(boxes, DOWN if below else UP, buff=0.25).align_to(boxes, LEFT)
        return VGroup(boxes, names, arrows, lab), xs

    def push_pull(self):
        push, xs = self._line(1.3, "Push: each step makes as much as it can", BAD)
        pull, _ = self._line(-1.6, "Pull: each step makes only what the next one has taken", GOOD, below=True)
        piles = VGroup()
        for k in range(3):
            x = (xs[k] + xs[k + 1]) / 2
            pile = VGroup(*[Square(0.16, stroke_width=0.8, stroke_color="#0E1117", fill_color=SUPPLIER, fill_opacity=0.95)
                            for _ in range(6 + 3 * k)]).arrange_in_grid(cols=3, buff=0.02).move_to([x, 1.3 - 0.75, 0], aligned_edge=UP)
            piles.add(pile)
        cards = VGroup(*[draw.kanban(0.45).move_to([(xs[k] + xs[k + 1]) / 2, -1.6 + 0.65, 0]) for k in range(3)])
        flow = VGroup(*[Square(0.16, stroke_width=0, fill_color=SUPPLIER, fill_opacity=0.95).move_to([(xs[k] + xs[k + 1]) / 2 - 0.6, -1.6 + 0.18, 0]) for k in range(3)])
        quote = VGroup(tx("'we could have a mountain of parts and still not be able to build a car'", 15, WHITE),
                       tx("Kiichiro Toyoda, as quoted by Toyota", 13, GREY_B)).arrange(DOWN, buff=0.05).to_edge(DOWN, buff=0.3)
        tag = estimate_tag("a sketch of the two systems", size=13)
        with self.voiceover(
            "Here is what Toyota changed. <bookmark mark='a'/> In a push system each step works as fast as it can and "
            "hands its output on. When one step is slower, or a part is faulty, the work piles up in front of it: "
            "inventory, which costs money, takes space, and hides mistakes, because a bad batch can sit unnoticed in a "
            "pile. <bookmark mark='b'/> In Toyota's pull system, nothing moves until the step after asks for it. The card, "
            "the kanban, travels backwards: the assembly line uses a box of parts, the card goes back, and only then is "
            "another box made. Almost no piles, and a problem shows itself at once, because the line stops. "
            "<bookmark mark='c'/> Kiichiro Toyoda's warning was that a maker can have a mountain of parts and still not be "
            "able to build a car. Lean production, as it came to be called, set out to have neither "
            "the mountain nor the missing part."
        ) as vo:
            self.play(FadeIn(push[:3]), FadeIn(pull[:3]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(push[3]))
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(s_, shift=DOWN * 0.2) for s_ in p_], lag_ratio=0.1) for p_ in piles], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pull[3]), FadeIn(flow))
            self.play(LaggedStart(*[c.animate.shift(LEFT * 1.2) for c in cards[::-1]], lag_ratio=0.3), FadeIn(cards), run_time=2.0)
            self.play(LaggedStart(*[f.animate.shift(RIGHT * 1.2) for f in flow], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.clear_scene()

    def supply(self):
        L = R["lean"]
        sup = {m: v for m, v in L["supply"].items()}
        months = sorted(sup)
        t = lambda m: int(m[:4]) + (int(m[5:7]) - 0.5) / 12  # noqa: E731
        pa = viz.plot_axes([1993, 2027], [0, 5], x_length=10.4, y_length=4.4, xticks=[1995, 2005, 2015, 2025],
                           yticks=[0, 1, 2, 3, 4, 5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}",
                           ylabel="cars on dealers' lots, in months of sales", size=13).move_to([-0.2, -0.5, 0])
        line = poly(pa, [(t(m), sup[m]) for m in months], DEALER, 2.5)
        low = Dot(pa.ax.c2p(t(L["low_month"]), L["low"]), radius=0.1, color=BAD)
        ll = tx(f"January 2022: {L['low']:.2f} months", 15, BAD, bold=True).next_to(low, UR, buff=0.1).shift(LEFT * 1.8)
        hi = max(months, key=lambda m: sup[m])
        hd = Dot(pa.ax.c2p(t(hi), sup[hi]), radius=0.08, color=PRICE)
        hl = tx(f"January 2009: {sup[hi]:.1f} months", 14, PRICE, bold=True).next_to(hd, RIGHT, buff=0.1)
        lots = VGroup(*[draw.car(0.55, GREY_B) for _ in range(8)]).arrange_in_grid(rows=2, buff=0.08).move_to([4.4, 2.3, 0])
        src = source("US Bureau of Economic Analysis, auto inventory/sales ratio, seasonally adjusted (via FRED, AISRSA)", size=12)
        with self.voiceover(
            "Lean production was a bet that stock is waste. But stock is also a cushion. <bookmark mark='a'/> This line is "
            "the cars sitting on America's dealer lots, measured in months of sales. For years it ran at about two and a "
            f"half months, {L['s2019']:.2f} in 2019. <bookmark mark='b'/> In the crash of 2009 it shot up to "
            f"{sup[hi]:.1f} months: cars nobody was buying. <bookmark mark='c'/> Then 2021. Factories could not get enough "
            f"chips, and by January 2022 the lots held {L['low']:.2f} months of sales, about thirteen days. Dealers had "
            f"almost nothing to sell. <bookmark mark='d'/> In 2025 the lots held about {L['s2025']:.1f} months, still "
            "well below the old level."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(lots), FadeIn(ghost(line, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(hd), FadeIn(hl))
            vo.wait_until("c")
            self.play(GrowFromCenter(low), FadeIn(ll), LaggedStart(*[FadeOut(c) for c in lots[2:]], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(Indicate(line, color=DEALER))
        self.clear_scene()

    def chips(self):
        L = R["lean"]
        D = R["dollar"]
        get("gm.shortage")      # GM's own sentence, quoted on screen
        total = D["materials_total"]
        big = Rectangle(width=10.0, height=0.8, stroke_width=0, fill_color=SUPPLIER, fill_opacity=0.35).move_to([0, 1.2, 0])
        sl = Rectangle(width=10.0 * L["chips_share"], height=0.8, stroke_width=0, fill_color=BAD, fill_opacity=1).move_to(big.get_left(), aligned_edge=LEFT)
        bl = tx(f"everything America's car assemblers bought in 2022: ${total:.0f}bn", 17, WHITE).next_to(big, UP, buff=0.12)
        cl = VGroup(tx(f"semiconductors: ${L['chips']:.1f}bn,", 18, BAD, bold=True),
                    tx(f"{100 * L['chips_share']:.1f}% of it", 18, BAD, bold=True)).arrange(RIGHT, buff=0.15).next_to(big, DOWN, buff=0.2).align_to(big, LEFT)
        chip_ = draw.chip(0.9).move_to([-4.0, -1.4, 0])
        car_ = draw.suv(2.4, GREY_B).move_to([0.6, -1.4, 0])
        cross = VGroup(Line(car_.get_corner(UL), car_.get_corner(DR), stroke_color=BAD, stroke_width=6),
                       Line(car_.get_corner(DL), car_.get_corner(UR), stroke_color=BAD, stroke_width=6))
        quote = VGroup(tx("General Motors, Form 10-K 2021: 'The impact on production in 2021 due to the ongoing semiconductor", 14, WHITE),
                       tx("supply shortage exceeded the impact of production suspensions in 2020 due to the COVID-19 pandemic.'", 14, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_edge(DOWN, buff=0.75)
        src = source("US Census Bureau, 2022 Economic Census, materials consumed, NAICS 336110; GM, Form 10-K 2021", size=12)
        with self.voiceover(
            "Remember the smallest line on the census list? <bookmark mark='a'/> In 2022 America's car assemblers spent "
            f"{L['chips']:.1f} billion dollars on semiconductors, about {100 * L['chips_share']:.0f} per cent of what they "
            "bought. <bookmark mark='b'/> Yet a car cannot leave the line without its chips, any more than without its "
            "wheels. When the chip makers could not supply enough of them in 2021, carmakers had to stop their lines. "
            "<bookmark mark='c'/> General Motors told its investors that the shortage cost it more production in 2021 than "
            "the pandemic's shutdowns had in 2020. That was lean production's hidden bet: a system with no spare parts "
            "works beautifully until the part that is missing is one nobody thought about."
        ) as vo:
            self.play(FadeIn(big), FadeIn(bl), FadeIn(src), FadeIn(ghost(chip_, car_, opacity=0.3)))
            vo.wait_until("a")
            self.play(GrowFromEdge(sl, LEFT), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(chip_), FadeIn(car_))
            self.play(FadeOut(chip_, shift=UP * 0.4), Create(cross))
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.clear_scene()
