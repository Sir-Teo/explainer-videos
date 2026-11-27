from __future__ import annotations

from videos.industry.industry23.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.two()
        self.seesaw()
        self.rules()
        self.title()

    def two(self):
        H, L = R["hook"], R["luxury"]
        rail = draw.rail(4.4, n=6).move_to([-3.4, 1.5, 0])
        bag = draw.handbag(1.9, color=LEATHER).move_to([3.4, 1.4, 0])
        left = stat_cards([(eur(H["sales"]), "Inditex's sales, the year to January 2026", FAST),
                           (f"{H['stores']:,}", f"stores, in {H['markets']} markets", FAST)], y=-1.4, size=34, span=5.6)
        left.shift(LEFT * 3.4)
        right = stat_cards([(eur(H["rms_rev"] / 1e3), "Hermès's revenue, 2025", LUX),
                            (f"{H['rms_margin']:.0f}%", "of it kept as operating profit", LUX)], y=-1.4, size=34, span=5.6)
        right.shift(RIGHT * 3.4)
        src = source("Inditex, FY2025 results; Hermès International, 2025 full-year results", size=12)
        beat(self,
             "Two companies that sell clothes and leather. <bookmark mark='a'/> One is Inditex, the Spanish group behind "
             f"Zara. In the year to January 2026 it sold {H['sales']:.1f} billion euros of clothes, <bookmark mark='b'/> "
             f"through {H['stores']:,} shops in {H['markets']} markets and online, and its own report calls the trade it "
             "is in 'highly fragmented'. <bookmark mark='c'/> The other is Hermès, the Paris house, which made "
             f"{H['rms_rev'] / 1e3:.1f} billion euros of revenue in 2025, less than half as much, <bookmark mark='d'/> "
             f"and kept {H['rms_margin']:.0f} cents of every euro as operating profit. Inditex kept about "
             f"{R['fast']['ebit_margin']:.0f}.",
             base=[src], steps=[[rail, left[0]], left[1], [bag, right[0]], right[1]])

    def seesaw(self):
        H = R["hook"]
        cols = [GOOD, BAD, GOOD, BAD]
        items = [(f"Q{q}", H["q"][q][1] - 50, cols[q - 1], f"{H['q'][q][1]:.1f}%") for q in (1, 2, 3, 4)]
        bars_ = vbars(items, base_y=-2.2, height=3.6, width=1.3, gap=0.6, size=18, max_value=14)
        floor = tx("bars start at 50%", 12, GREY_B).move_to([-4.6, -2.0, 0])
        months = VGroup(*[tx(m, 13, GREY_B).next_to(b, DOWN, buff=0.45) for b, m in
                          zip(bars_, ("Feb-Apr", "May-Jul", "Aug-Oct", "Nov-Jan"))])
        lab = tx("Inditex's gross margin, each quarter of the year to January 2026", 16, GREY_A).to_edge(UP, buff=0.75)
        tags = VGroup(draw.price_tag("$40", 0.9).move_to([5.6, 1.8, 0]),
                      Arrow([5.6, 1.5, 0], [5.6, 0.7, 0], buff=0, stroke_color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.25),
                      draw.price_tag("$8", 0.9, color=BAD).move_to([5.6, 0.4, 0]),
                      tx("the sale", 14, BAD).move_to([5.6, -0.05, 0]))
        src = source("Inditex, FY2025 results, Annex I: quarterly income statement", size=12)
        beat(self,
             "Now watch Inditex's year, quarter by quarter. <bookmark mark='a'/> From February to April, the first quarter, "
             f"it kept {H['q'][1][1]:.1f} per cent of its sales after the cost of the clothes. <bookmark mark='b'/> From May to "
             f"July, {H['q'][2][1]:.1f}. <bookmark mark='c'/> From August to October, {H['q'][3][1]:.1f}. <bookmark mark='d'/> "
             f"And from November to January, {H['q'][4][1]:.1f}. Up, down, up, down. The low quarters are the ones that close "
             "a season, summer and then winter, when what did not sell is sold off at a lower price. Inditex does not break "
             "its margin down that way, but the saw-tooth is there in its own table: <bookmark mark='e'/> every season, "
             "somebody guessed how many of each thing people would buy, and every season, part of the guess was wrong.",
             base=[lab, src, floor], steps=[[bars_[0], months[0]], [bars_[1], months[1]], [bars_[2], months[2]], [bars_[3], months[3]],
                                     tags])

    def rules(self):
        fast = VGroup(draw.rail(3.6, n=5).scale(0.8), tx("Fast fashion", 26, FAST, bold=True),
                      tx("make what people want now,", 18, WHITE), tx("and stop the moment they stop", 18, WHITE)
                      ).arrange(DOWN, buff=0.22).move_to([-3.5, 0.2, 0])
        lux = VGroup(draw.handbag(1.6, color=LEATHER), tx("Luxury", 26, LUX, bold=True),
                     tx("make fewer than people want,", 18, WHITE), tx("and never sell them off", 18, WHITE)
                     ).arrange(DOWN, buff=0.22).move_to([3.5, 0.2, 0])
        line = DashedLine([0, 2.6, 0], [0, -2.2, 0], stroke_color=GREY_B, stroke_width=2)
        beat(self,
             "This film is about that guess, and the two opposite ways the industry has found to live with it. "
             "<bookmark mark='a'/> One way is speed: make less up front, watch what sells, and make more of that, fast, "
             "so that less is left over to sell off. <bookmark mark='b'/> The other way is the wait: make fewer of a thing "
             "than people want, so there is never anything left to sell off, and let customers wait. Between them sit "
             "the sports brands, the department stores and the shops that sell everybody else's mistakes.",
             base=[line], steps=[fast, lux])

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover("Industry, Built. Part twenty-three: fashion and luxury. How do two industries that sell clothes "
                            "run on opposite rules?"):
            self.play(FadeIn(card_[0]), FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.0)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
