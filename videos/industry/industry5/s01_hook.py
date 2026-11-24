from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.siege()
        self.three()
        self.title()

    def siege(self):
        place = tx("Omaha, Nebraska  ·  February 2008", 26, GREY_B).to_edge(UP, buff=0.35)
        keep = draw.castle(2.6, moat=0.9).move_to([-1.6, -0.6, 0])
        quote = VGroup(tx("“A truly great business must have an enduring ‘moat’", 26, WHITE),
                       tx("that protects excellent returns on invested capital.”", 26, WHITE),
                       tx("Warren Buffett, letter to Berkshire Hathaway shareholders, 2007", 18, GREY_B)).arrange(
            DOWN, buff=0.1).move_to([0, 2.5, 0])
        raiders = VGroup(*[draw.person(0.45, color=ENTRANT) for _ in range(5)]).arrange(RIGHT, buff=0.25)
        raiders.move_to([6.8, -0.9, 0])
        coins = VGroup(*[draw.coin(0.11) for _ in range(6)])
        for c in coins:
            c.move_to(keep.get_top())
        src = source("Berkshire Hathaway, letter to shareholders for 2007, pp. 6-8")
        with self.voiceover(
            "In February 2008 Warren Buffett wrote to Berkshire Hathaway's shareholders about the kind of business he "
            "most wanted to own. <bookmark mark='a'/> A truly great business, he wrote, must have an enduring moat "
            "that protects excellent returns on invested capital. <bookmark mark='b'/> The returns are the treasure "
            "inside the castle. <bookmark mark='c'/> And capitalism, he went on, guarantees that competitors will "
            "keep attacking any castle that earns them. <bookmark mark='d'/> The moat is whatever stops them."
        ) as vo:
            self.play(FadeIn(place), FadeIn(src), FadeIn(keep, shift=UP * 0.3))
            vo.wait_until("a")
            self.play(FadeIn(quote, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.add(coins)
            self.play(LaggedStart(*[c.animate.move_to(keep.get_top() + np.array([0.3 * (k - 2.5), 0.5 + 0.1 * (k % 2), 0]))
                                    for k, c in enumerate(coins)], lag_ratio=0.1), run_time=1.2)
            vo.wait_until("c")
            self.play(raiders.animate.move_to([2.4, -0.9, 0]), run_time=2.2, rate_func=rate_functions.ease_out_quad)
            vo.wait_until("d")
            self.play(LaggedStart(*[r_.animate.shift(DOWN * 0.5 + LEFT * 0.3).set_opacity(0) for r_ in raiders],
                                  lag_ratio=0.15), Indicate(keep.moat, color="#7EC8F5", scale_factor=1.04),
                      run_time=1.8)
        self.clear_scene()

    def three(self):
        T3 = R["three"]
        s, f = T3["sees"], T3["fsi"]
        xs = (-4.6, 0.0, 4.6)
        candy = draw.castle(1.7, moat=0.7, color="#E9C9A6").move_to([xs[0], 1.6, 0])
        sims = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.5, height=0.36, stroke_width=0,
                                         fill_color="#7EC8F5", fill_opacity=0.9) for _ in range(6)])
        sims.arrange_in_grid(rows=2, cols=3, buff=0.08)
        flight = VGroup(draw.castle(1.7, color=STONE), sims.next_to(ORIGIN, RIGHT, buff=0)).move_to([xs[1], 1.6, 0])
        sims.next_to(flight[0], RIGHT, buff=0.12).align_to(flight[0], DOWN)
        flight = VGroup(flight[0], sims).move_to([xs[1], 1.6, 0])
        jet = draw.plane(2.4).move_to([xs[2], 1.7, 0])
        names = VGroup(tx("See's Candies", 24, "#E9C9A6", bold=True), tx("FlightSafety", 24, "#7EC8F5", bold=True),
                       tx("Airlines", 24, ENTRANT, bold=True))
        for n_, x in zip(names, xs):
            n_.move_to([x, 0.35, 0])
        subs = VGroup(tx("boxed chocolates, sold for cash", 16, GREY_B), tx("pilots trained on simulators", 16, GREY_B),
                      tx("in Buffett's words, 'the worst sort'", 16, GREY_B))
        for t_, x in zip(subs, xs):
            t_.move_to([x, 0.0, 0])

        base = -3.05
        u = 0.014  # inches per $m

        def bars(x, cap, pre, cap_t, pre_t):
            b1 = Rectangle(width=0.8, height=max(cap * u, 0.03), stroke_width=0, fill_color=MOAT, fill_opacity=0.85)
            b2 = Rectangle(width=0.8, height=max(pre * u, 0.03), stroke_width=0, fill_color=RET, fill_opacity=0.9)
            b1.move_to([x - 0.5, base, 0], aligned_edge=DOWN)
            b2.move_to([x + 0.5, base, 0], aligned_edge=DOWN)
            return VGroup(b1, b2, tx(cap_t, 15, MOAT).next_to(b1, UP, buff=0.06),
                          tx(pre_t, 15, RET).next_to(b2, UP, buff=0.06))
        sees0 = bars(xs[0], s["cap0"], s["pre0"], "$8m", "$5m")
        sees1 = bars(xs[0], s["cap1"], s["pre1"], "$40m", "$82m")
        fsi1 = bars(xs[1], 570 + 509, f["pre1"], "+$509m", "$270m")
        fsi0 = bars(xs[1], 570, f["pre0"], "$570m", "$111m")
        for b in (fsi0, fsi1):
            b[0].stretch_to_fit_height(min(b[0].height, 1.6), about_edge=DOWN)
            b[2].next_to(b[0], UP, buff=0.06)
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=MOAT, fill_opacity=1),
                            tx("capital tied up", 16, MOAT)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.2, stroke_width=0, fill_color=RET, fill_opacity=1),
                            tx("profit a year, before tax", 16, RET)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.15)
        yr0 = tx("1972", 20, GREY_A).move_to([xs[0], -0.55, 0])
        yr1 = tx("2007", 20, GREY_A).move_to([xs[0], -0.55, 0])
        fy0 = tx("1996", 20, GREY_A).move_to([xs[1], -0.55, 0])
        fy1 = tx("2007", 20, GREY_A).move_to([xs[1], -0.55, 0])
        sink = VGroup(*[draw.coin(0.1) for _ in range(8)])
        per = VGroup(tx(f"${s['incr']:.2f}", 30, RET, bold=True), tx(f"${f['incr']:.2f}", 30, "#7EC8F5", bold=True),
                     tx("little or nothing", 22, ENTRANT, bold=True))
        for p_, x in zip(per, xs):
            p_.move_to([x, -1.45, 0])
        per_t = tx("extra profit a year for each extra dollar put in", 18, GREY_B).move_to([0, -0.9, 0])
        src = source("Berkshire Hathaway, letter to shareholders for 2007, pp. 6-8", corner=DR)
        with self.voiceover(
            "Then he described three businesses. <bookmark mark='a'/> See's Candies, a chocolate maker from "
            "California. In 1972 Blue Chip Stamps, a company Buffett and Charlie Munger controlled, bought it for "
            f"{s['price']:.0f} million dollars, when running it took "
            f"{s['cap0']:.0f} million of capital and it earned under {s['pre0']:.0f} million before tax. "
            "<bookmark mark='b'/> By 2007 it earned 82 million before tax, on only 40 million of capital. It sold "
            "31 million pounds of candy that year, against 16 million in 1972: growth of two percent a year, nothing "
            "special. What was special was how little money the business needed. Its chocolates sell for cash and "
            "leave the shop within weeks, so almost nothing is tied up in debts or stock. "
            "<bookmark mark='c'/> FlightSafety, which trains pilots: a fine business, with an advantage Buffett "
            "thought durable. But every new aircraft needs new simulators, at over twelve million dollars each. From "
            "1996 to 2007 it put in 509 million dollars more, and its profit rose by 159 million. "
            "<bookmark mark='d'/> And airlines, which he called the worst sort of business: growing fast, hungry for "
            "capital, earning little or nothing. If a farsighted capitalist had been present at Kitty Hawk, he wrote, "
            "he would have done his successors a huge favour by shooting Orville down. <bookmark mark='e'/> Put it as "
            "one number: what each extra dollar put into the business brought back every year. See's, about two "
            "dollars forty. FlightSafety, about thirty cents. Airlines, little or nothing."
        ) as vo:
            ghosts = VGroup(candy.copy(), flight.copy(), jet.copy()).set_opacity(0.18)
            self.play(FadeIn(src), FadeIn(key), LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in ghosts],
                                                            lag_ratio=0.3), run_time=1.6)
            vo.wait_until("a")
            self.remove(ghosts[0])
            self.play(FadeIn(candy, shift=UP * 0.2), FadeIn(names[0]), FadeIn(subs[0]), FadeIn(yr0))
            self.play(*[GrowFromEdge(b, DOWN) for b in sees0[:2]], FadeIn(sees0[2:]))
            vo.wait_until("b")
            self.play(Transform(sees0, sees1), Transform(yr0, yr1), run_time=2.0)
            vo.wait_until("c")
            self.remove(ghosts[1])
            self.play(FadeIn(flight, shift=UP * 0.2), FadeIn(names[1]), FadeIn(subs[1]), FadeIn(fy0))
            self.play(*[GrowFromEdge(b, DOWN) for b in fsi0[:2]], FadeIn(fsi0[2:]))
            self.play(Transform(fsi0, fsi1), Transform(fy0, fy1),
                      LaggedStart(*[Indicate(x_, color=WHITE) for x_ in sims], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("d")
            self.remove(ghosts[2])
            self.play(FadeIn(jet, shift=RIGHT * 0.4), FadeIn(names[2]), FadeIn(subs[2]))
            for c in sink:
                c.move_to([xs[2] + 2.0, -1.4, 0])
            self.add(sink)
            self.play(LaggedStart(*[c.animate.move_to(jet.get_center()).scale(0.3).set_opacity(0) for c in sink],
                                  lag_ratio=0.15), run_time=2.2)
            self.remove(sink)
            vo.wait_until("e")
            self.play(FadeOut(VGroup(sees0, fsi0, yr0, fy0)), FadeIn(per_t))
            self.play(LaggedStart(*[FadeIn(p_, scale=1.2) for p_ in per], lag_ratio=0.4), run_time=1.8)
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "The same country, the same years: one business made money almost out of nothing, one made a fair return, "
            "one devoured capital. Industry, Built. Part five: the moat. Why do some industries earn high returns for "
            "decades, while others never do?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
