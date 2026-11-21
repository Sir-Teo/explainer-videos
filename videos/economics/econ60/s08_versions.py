from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Versions(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Versions and menus", r"Why sell three versions of nearly the same thing, \ and why damage "
             r"one on purpose?", "Chapter seven. Versions and menus.", lit={1978: r"Mussa and Rosen",
                                                                               1996: r"damaged goods"},
             scale=("firm",), horizon=("a year",))
        self.menu()
        self.damaged()

    def menu(self):
        M = load("menu")["menu"]
        q, p, th, sh, rent = M["q"], M["p"], M["thetas"], M["shares"], M["rents"]
        names = (r"good", r"better", r"best")
        cols = (LEIS, AIR, BUS)
        boxes = VGroup()
        for k in range(3):
            bar = Rectangle(width=0.5, height=1.4 * q[k], fill_color=cols[k], fill_opacity=0.85, stroke_width=0)
            inner = VGroup(
                label(names[k], font_size=24, color=cols[k]),
                bar,
                label(rf"quality {q[k]:.2f}", font_size=17, color=WHITE),
                label(rf"price {p[k]:.2f}", font_size=19, color=WHITE),
                label(rf"bought by type {th[k]:g} \ ({100 * sh[k]:.0f}\%)", font_size=15, color=GREY_A),
                label(rf"their surplus: \ {rent[k]:.2f}", font_size=15, color=GREY_B),
            ).arrange(DOWN, buff=0.14)
            boxes.add(VGroup(SurroundingRectangle(inner, buff=0.22, color=cols[k], corner_radius=0.12,
                                                  stroke_width=1.6), inner))
        boxes.arrange(RIGHT, buff=0.35, aligned_edge=DOWN).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        side = VGroup(
            label(r"types value quality at $\theta q$; \ quality costs $q^2/2$", font_size=19, color=GREY_A),
            label(r"the best version: \ the efficient quality, \ no distortion at the top", font_size=19, color=BUS),
            label(r"the lower versions are made worse on purpose: \\ so that the top type is not tempted down",
                  font_size=19, color=AIR),
            label(rf"profit: \ three versions {M['profit']:.3f}; \ one version {M['profit_one']:.3f}", font_size=20,
                  color=OPT),
            label(rf"if the seller could tell types apart: \ {M['profit_full_info']:.3f}", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 5.8:
            side.width = 5.8
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.revenue.menu, \ Mussa and Rosen with three types", corner=DL,
                        font_size=12)
        with self.voiceover(
            "Part ten derived screening with two types. Here is the practice: good, better, best. <bookmark "
            "mark='a'/> Three kinds of buyer value quality at one, one and a half, and two dollars a unit, and "
            "quality costs its square over two to supply. The seller cannot tell them apart, so it offers a menu. "
            "<bookmark mark='b'/> The best version gets the efficient quality: there is no reason to distort it. "
            "<bookmark mark='c'/> The lower versions are made worse than efficient, on purpose: a better cheap "
            "version would tempt the top buyers down, and the seller would have to cut the top price to keep them. "
            f"<bookmark mark='d'/> The three versions earn {M['profit']:.3f} per buyer, against {M['profit_one']:.3f} "
            "for the best single version. <bookmark mark='e'/> A seller who could tell the types apart would earn "
            f"{M['profit_full_info']:.3f}; the gap is the information rent left to the higher types."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(boxes[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def damaged(self):
        cards = VGroup(
            history_card(1990, r"IBM's LaserPrinter E", r"the same printer as the LaserPrinter, \ with a chip added "
                         r"to slow it down, \ sold for less", color=AIR, width=11.4, font_size=21),
            history_card(1996, r"Raymond Deneckere and Preston McAfee, \ `Damaged Goods'", r"a firm may spend money to "
                         r"make a worse version: \ it lets the firm sell to low-value buyers \ without lowering the "
                         r"price to everyone else; \ when the alternative is not serving them at all, \ even they can "
                         r"gain", color=OPT, width=11.4, font_size=21),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        ex = label(r"also: \ economy fares that forbid changes, \ software with features switched off, \ the "
                   r"slower delivery option", font_size=20, color=GREY_A).next_to(cards, DOWN, buff=0.45)
        tag = published_tag(r"Deneckere and McAfee, \ Journal of Economics and Management Strategy (1996)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Sometimes the worse version costs more to make. <bookmark mark='a'/> IBM's LaserPrinter E was the same "
            "printer as its LaserPrinter, with a chip added to slow it down, sold for less. <bookmark mark='b'/> "
            "Raymond Deneckere and Preston McAfee called such products damaged goods. Damaging the cheap version "
            "lets a firm sell to buyers who value it less without cutting the price to everyone else, and when "
            "the alternative is not selling to them at all, even those buyers can be better off. <bookmark "
            "mark='c'/> Economy fares that forbid changes, software with features switched off and slow delivery "
            "options work the same way. The Ultimate Super Saver's conditions were a damaged ticket."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(ex))
        self.clear_scene()
