from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


def cabin(rows: int = 10, cols: int = 10, w: float = 0.32, h: float = 0.26):
    """A hundred seats as a grid, front at the top."""
    g = VGroup()
    for r in range(rows):
        for c in range(cols):
            x = (c - (cols - 1) / 2) * (w + 0.06) + (0.18 if c >= cols // 2 else -0.18)
            g.add(RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=GREY_C, stroke_width=1.2,
                                   fill_color=GREY_E, fill_opacity=0.6).move_to([x, -r * (h + 0.06), 0]))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.seats()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        cards = VGroup(
            history_card(1981, r"People Express", r"a no-frills airline out of Newark: \ fares far below the big "
                         r"carriers', \ bags and snacks extra", color=LEIS, width=11.2, font_size=21),
            history_card(1985, r"American Airlines, \ January", r"Ultimate Super Saver fares as low as People's, \ on "
                         r"a limited number of seats per flight, \ with conditions business travellers would not "
                         r"accept",
                         color=AIR, width=11.2, font_size=21),
            history_card(1986, r"People Express is sold", r"to Texas Air, \ after its traffic fell for the first time",
                         color=COST, width=11.2, font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        quote = label(r"`We had been profitable from the day we started \\ until American came at us with Ultimate "
                      r"Super Savers.' \ --- Donald Burr, \ as he later told it", font_size=20, color=GREY_A).next_to(
            cards, DOWN, buff=0.4)
        tag = published_tag(r"Smith, \ Leimkuhler and Darrow, \ Interfaces 22(1) (1992); \ company histories",
                            corner=DL, font_size=12)
        with self.voiceover(
            "In 1981 Donald Burr started People Express, a no-frills airline flying out of Newark at fares far below "
            "the big carriers', with bags and snacks extra. By 1985 it was one of the fastest-growing companies in "
            "America. <bookmark mark='a'/> American Airlines could not match those fares on every seat without "
            "giving away money its business travellers were happy to pay. So in January 1985 it announced Ultimate "
            "Super Saver fares, as low as People's, but only on a limited number of seats on each flight, and with "
            "conditions, booking well ahead and no refunds, that business travellers would not accept. Software "
            "decided how many seats to sell that way: the ones it forecast would otherwise fly empty. <bookmark "
            "mark='b'/> People Express's traffic fell for the first time, and in 1986 it was sold to Texas Air. "
            "<bookmark mark='c'/> As Burr later told it, the company had been profitable from the day it started "
            "until American came at it with Ultimate Super Savers. American later put the benefit of the technique, "
            "which it called yield management, at 1.4 billion dollars over three years."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.clear_scene()

    def seats(self):
        P = load("playit")
        g = cabin().scale(1.05).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        head = label(r"the Island's flight: \ a hundred seats, \ sixty days of sales", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"early buyers: \ leisure travellers, \ price-sensitive", font_size=21, color=LEIS),
            label(r"late buyers: \ business travellers, \ who will pay more", font_size=21, color=BUS),
            label(r"sell too many seats cheap, \ and the late buyers find the plane full", font_size=20,
                  color=GREY_A),
            label(r"hold too many back, \ and they fly empty", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.6).shift(UP * 0.4)
        tag = island_tag(r"the Island: \ agora.revenue.flight", corner=DR, font_size=12)
        cheap = list(range(40, 100))
        late = list(range(10, 40))
        with self.voiceover(
            "The Island has an airline too. <bookmark mark='a'/> One flight, a hundred seats, sixty days of sales. "
            "<bookmark mark='b'/> Early in the sale come leisure travellers, who will fly if the price is right. "
            "<bookmark mark='c'/> Late come business travellers, who will pay much more but book at the last "
            "minute. <bookmark mark='d'/> Sell too many seats cheap, and the late buyers find the plane full. Hold "
            "too many back, and they fly empty. How should the price move over sixty days? That is the problem "
            "this part follows, from what firms say they do to what the mathematics says they should."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in g], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("b")
            self.play(*[g[k].animate.set_fill(LEIS, opacity=0.9) for k in cheap], FadeIn(rows[0]), run_time=1.2)
            vo.wait_until("c")
            self.play(*[g[k].animate.set_fill(BUS, opacity=0.9) for k in late], FadeIn(rows[1]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        del P
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what do firms say they do, \ and why?", font_size=26, color=FIRM),
            label(r"how do you learn what buyers will pay?", font_size=26, color=TEST),
            label(r"how should a price move as seats sell and the date nears?", font_size=26, color=AIR),
            label(r"versions, \ bundles, \ promotions, \ and one price for every store", font_size=26, color=SHOP),
            label(r"and when costs jump, \ how much reaches the shelf?", font_size=26, color=PPI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: how do firms actually set prices, and how much of the theory do they use? <bookmark "
            "mark='a'/> What do firms say they do, and why? <bookmark mark='b'/> How do you learn what buyers "
            "will pay? <bookmark mark='c'/> How should a price move as seats sell and the date nears? <bookmark "
            "mark='d'/> Why sell versions and bundles, run promotions, and charge one price in every store? "
            "<bookmark mark='e'/> And when costs jump, how much reaches the shelf?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        g = cabin(rows=5, cols=10, w=0.2, h=0.16)
        for k, s in enumerate(g):
            s.set_fill(LEIS if k >= 20 else BUS, opacity=0.85)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 60 \ $\cdot$ \ The Price", font_size=34, color=E.ACCENT)
        VGroup(g, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty: the price."):
            self.play(LaggedStart(*[FadeIn(s) for s in g], lag_ratio=0.01), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XI \ $\cdot$ \ Economics at Work", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"what firms say about pricing, \ and why a fixed markup survives",
            r"measuring willingness to pay: \ surveys, \ conjoint analysis, \ experiments and their traps",
            r"revenue management: \ Littlewood's rule, \ protection levels, \ overbooking, \ dynamic programming",
            r"versions, \ bundles, \ promotions and reference prices, \ uniform prices across a chain",
            r"cost pass-through in 2021--22, \ algorithms, \ business-to-business prices, \ pricing that learns",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part fifty-nine judged prices in court. This part sets them. By the end you will know <bookmark "
            "mark='a'/> what firms say about pricing, and why a fixed markup survives; <bookmark mark='b'/> how "
            "willingness to pay is measured, and the traps in surveys and experiments; <bookmark mark='c'/> how "
            "revenue management works, from Littlewood's rule to dynamic programming; <bookmark mark='d'/> why "
            "firms sell versions and bundles, run promotions, and charge one price across a chain; <bookmark "
            "mark='e'/> and how much of the cost jump of 2021 and 2022 reached the shelf, what algorithms change, "
            "how business prices are made, and how prices can be learned while they are set."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
