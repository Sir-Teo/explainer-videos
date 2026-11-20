from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Space(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Demand for differentiated products", r"How do you estimate demand for hundreds of goods?",
             "Chapter four. Demand for differentiated products.", lit={1966: r"Lancaster"},
             scale=("market",), horizon=("a year",))
        self.count()
        self.space()
        self.utility()

    def count(self):
        n = 12
        cells = VGroup(*[Square(side_length=0.3, stroke_width=0.6, stroke_color=GREY_D, fill_color=DEMAND,
                                fill_opacity=0.15) for _ in range(n * n)])
        cells.arrange_in_grid(rows=n, cols=n, buff=0.03).move_to(LEFT * 2.6 + DOWN * 0.3)
        diag = VGroup(*[cells[i * n + i] for i in range(n)])
        side = VGroup(
            label(r"one row per product, \\ one column per price", font_size=19, color=GREY_A),
            label(r"the diagonal: \ own-price \\ elasticities", font_size=19, color=PRICE),
            label(r"everything else: \\ cross-price elasticities", font_size=19, color=DEMAND),
            label(r"200 cereals: \ 40,000 numbers; \\ 2,217 car models: \\ far more than the data \\ can pin down",
                  font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "To measure market power, or to predict a merger, we need demand: how each product's sales respond to "
            "its own price and to every rival's. <bookmark mark='a'/> Write it as a table with one row for each "
            "product and one column for each price. <bookmark mark='b'/> On the diagonal sit the own-price "
            "elasticities. <bookmark mark='c'/> Everywhere else sit the cross-price elasticities, which say where "
            "lost shoppers go. <bookmark mark='d'/> With twelve products that is a hundred and forty-four numbers. "
            "With two hundred cereals it is forty thousand, and no market ever offers enough independent changes "
            "in prices to estimate them one by one."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[c.animate.set_fill(PRICE, opacity=0.8) for c in diag], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[c.animate.set_fill(DEMAND, opacity=0.55) for k, c in enumerate(cells) if k % (n + 1)],
                      FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(cells, color=LOSS, scale_factor=1.02))
        self.clear_scene()

    def space(self):
        B = load("blpdata")
        Y = B["y1990"]
        hp, sp, pr, sh, air = (np.array(Y[c]) for c in ("hpwt", "space", "price", "share", "air"))
        ax = plane([0.25, 0.85], [0.8, 1.8], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8], yticks=[0.8, 1.0, 1.2, 1.4, 1.6, 1.8],
                   xlabel=r"horsepower per unit of weight", ylabel=r"size \ (length times width)",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        lo, hi = np.log(pr.min()), np.log(pr.max())
        pts = VGroup()
        for x, y, p, s in zip(hp, sp, pr, sh):
            f = (np.log(p) - lo) / (hi - lo)
            col = interpolate_color(ManimColor(DEMAND), ManimColor(PRICE), f)
            pts.add(Dot(ax.ax.c2p(x, y), radius=0.04 + 6.0 * s, color=col, fill_opacity=0.8))
        side = VGroup(
            label(rf"1990: \ {B['n1990']} car models", font_size=19, color=WHITE),
            label(r"each a point in the \\ space of what it offers", font_size=18, color=GREY_A),
            label(r"blue cheap, \ gold dear; \\ bigger dots sell more", font_size=18, color=PRICE),
            label(r"neighbours are \\ close substitutes", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Berry, \ Levinsohn and Pakes's data \ (BLPestimatoR); \ "
                       + tables.LANCASTER_1966.tag.split(";")[0], corner=DR, font_size=11)
        with self.voiceover(
            "The way out came from Kelvin Lancaster in 1966: people do not want goods for themselves, they want "
            "what goods offer. <bookmark mark='a'/> Here are the car models sold in the United States in 1990, from "
            "the data Berry, Levinsohn and Pakes used. <bookmark mark='b'/> Each is a point in the space of what it "
            "offers: power for its weight across, size up. <bookmark mark='c'/> Colour shows price, from cheap in "
            "blue to dear in gold, and the size of a dot shows its sales. <bookmark mark='d'/> In this space, "
            "neighbours are close substitutes. A small, weak car competes with other small, weak cars, not with a "
            "large, powerful one. Demand for hundreds of products can then be described by how much people value "
            "a few characteristics, a handful of numbers instead of forty thousand."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), run_time=2.0)
            for mk, k in zip("bcd", (1, 2, 3)):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def utility(self):
        eq = MathTex(r"u_{ij} \;=\;", r"x_j\,\beta", r"\;-\;", r"\alpha\, p_j", r"\;+\;", r"\xi_j", r"\;+\;",
                     r"\varepsilon_{ij}", font_size=52).move_to(UP * 1.6)
        parts = [(1, r"what the product \\ offers, \ valued", DEMAND), (3, r"its price", PRICE),
                 (5, r"quality buyers see \\ and we do not", LOSS), (7, r"buyer $i$'s own \\ taste for it", GREY_A)]
        notes = VGroup()
        for k, txt, col in parts:
            eq[k].set_color(col)
            notes.add(label(txt, font_size=17, color=col).next_to(eq[k], DOWN, buff=0.45))
        foot = VGroup(
            label(r"each buyer picks the product with the highest utility, \ or buys nothing", font_size=21,
                  color=WHITE),
            label(r"the trouble: \ firms price their best products high, \ so price is correlated with $\xi$",
                  font_size=21, color=LOSS),
            label(r"the fix, \ as in Part 4: \ instruments, \ things that move price but not quality", font_size=21,
                  color=GAIN),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.LANCASTER_1966.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Write it down. Buyer i's utility from product j is the value of what j offers, minus alpha times its "
            "price, plus two more terms. <bookmark mark='a'/> Characteristics, valued at weights beta. "
            "<bookmark mark='b'/> The price. <bookmark mark='c'/> Xi: quality that buyers see and the economist "
            "does not, such as style, reputation or how the seats feel. <bookmark mark='d'/> And epsilon, buyer i's "
            "own idiosyncratic taste. <bookmark mark='e'/> Each buyer picks the product with the highest utility, or "
            "buys nothing. <bookmark mark='f'/> The trouble is xi. Firms know their products, and they price the "
            "better ones higher, so price is correlated with the quality the economist cannot see. A regression "
            "that ignores this will find that high prices hardly deter buyers, because the expensive products are "
            "also the good ones. <bookmark mark='g'/> The fix, as in Part four, is instruments: things that move a "
            "product's price but not its unseen quality."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), run_time=2.0)
            for mk, nt in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(nt, shift=UP * 0.1))
            for mk, f in zip("efg", foot):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.clear_scene()
