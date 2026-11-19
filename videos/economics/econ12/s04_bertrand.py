from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

YOU = "#7BD88F"


class Bertrand(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Bertrand's reply: \ competing in prices", r"If each firm names a price instead, \ how many "
             r"firms does it take to compete the profit away?", "Chapter three. Bertrand's reply: competing in "
             "prices.", lit={1883: r"Bertrand's review"}, scale=("firm", "market"), horizon=("a season",))
        self.review()
        self.spiral()
        self.costs()
        self.which()

    def review(self):
        hc = history_card(1883, r"Joseph Bertrand, \ in the \emph{Journal des Savants}", r"a review of Cournot's book, "
                          r"\ 45 years on: \\ the owners would not choose quantities; \ they would name prices",
                          color=CRUSOE, width=11.6, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"whatever price the two share, \ either can cut it slightly \ and take every buyer", font_size=24),
            label(r"the other replies in kind, \ and there is no stopping point above cost", font_size=24,
                  color=GREY_A),
            label(r"that is what you did in Play it: \ \$39 against \$40", font_size=24, color=YOU),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Bertrand, Journal des Savants (September 1883), \ paraphrased", corner=DR, font_size=13)
        with self.voiceover(
            "In 1883, forty-five years after Cournot's book appeared, another French mathematician, Joseph Bertrand, "
            "reviewed it. He objected that the spring owners would not choose quantities and "
            "wait for the market. They would name prices. <bookmark mark='a'/> Whatever price the two share, either "
            "can cut it slightly and take every buyer. <bookmark mark='b'/> The other replies in kind, and there is "
            "no stopping point above cost. <bookmark mark='c'/> That is exactly what you did in Play it, when you "
            "undercut Crusoe's forty dollars with thirty-nine."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def spiral(self):
        bt = load("bertrand")
        sp = bt["spiral"]
        line = NumberLine(x_range=[0, 50, 10], length=11.4, include_numbers=True, font_size=22, color=GREY_B
                          ).move_to(UP * 0.9)
        lab = label(r"price of a repair, \ dollars", font_size=18, color=GREY_B).next_to(line, DOWN, buff=0.45)
        cost = Dot(line.n2p(10), radius=0.11, color=COMPETE)
        cl = label(r"cost", font_size=18, color=COMPETE).next_to(cost, UP, buff=0.2)
        marker = Triangle(color=WHITE, fill_opacity=1).scale(0.12).rotate(PI).next_to(line.n2p(sp[0]), UP, buff=0.1)
        who = label(r"Crusoe", font_size=20, color=CRUSOE).next_to(marker, UP, buff=0.1)
        price = DecimalNumber(sp[0], num_decimal_places=0, font_size=44, color=WHITE).move_to(DOWN * 0.7 + LEFT * 3.5)
        dollar = label(r"\$", font_size=44).next_to(price, LEFT, buff=0.08)
        rows = VGroup(
            label(r"each cut takes the whole island \ until the price reaches cost", font_size=24),
            label(r"at \$10: \ cutting loses money on every repair, \ raising loses every customer", font_size=24,
                  color=COMPETE),
            label(r"the only equilibrium: \ both at cost, \ zero profit", font_size=26, color=EQ),
            label(r"two firms are enough for the competitive price: \ the Bertrand paradox", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Follow the war through. Crusoe answers your thirty-nine with thirty-eight; you answer with "
            "thirty-seven, and so on down. <bookmark mark='a'/> Each cut takes the whole island, so each is worth "
            "making, until the price reaches the cost of a repair. <bookmark mark='b'/> At ten dollars, cutting "
            "again would lose money on every repair, and raising the price would lose every customer. "
            "<bookmark mark='c'/> So the only equilibrium has both yards at cost, earning nothing. "
            "<bookmark mark='d'/> Two firms are enough to give the competitive price of Part nine. This is the "
            "Bertrand paradox: Cournot's answer with two firms was forty dollars, Bertrand's is ten."
        ) as vo:
            self.play(Create(line), FadeIn(lab), FadeIn(cost), FadeIn(cl), FadeIn(marker), FadeIn(who),
                      FadeIn(price), FadeIn(dollar), FadeIn(tag))
            for k, p in enumerate(sp[1:] + [10.0]):
                col = YOU if k % 2 == 0 else CRUSOE
                name = r"you" if k % 2 == 0 else r"Crusoe"
                new_who = label(name, font_size=20, color=col)
                self.play(marker.animate.next_to(line.n2p(p), UP, buff=0.1),
                          who.animate.become(new_who.next_to(line.n2p(p) + UP * 0.3, UP, buff=0.1)),
                          price.animate.set_value(p), run_time=0.22)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(cost))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def costs(self):
        bt = load("bertrand")
        line = NumberLine(x_range=[0, 50, 10], length=11.4, include_numbers=True, font_size=22, color=GREY_B
                          ).move_to(UP * 1.3)
        c1 = VGroup(Dot(line.n2p(bt["low_cost"]), radius=0.1, color=YOU),
                    label(r"your cost: \ \$10", font_size=19, color=YOU).next_to(line.n2p(bt["low_cost"]), UP,
                                                                                buff=0.25))
        c2 = VGroup(Dot(line.n2p(bt["high_cost"]), radius=0.1, color=CRUSOE),
                    label(r"Crusoe's cost: \ \$20", font_size=19, color=CRUSOE).next_to(line.n2p(bt["high_cost"]),
                                                                                       UP, buff=0.65))
        tri = Triangle(color=E.ACCENT, fill_opacity=1).scale(0.12).next_to(line.n2p(bt["unequal_P"]), DOWN, buff=0.5)
        pr = VGroup(tri, label(rf"your price: \ \${bt['unequal_P']:.2f}", font_size=19, color=E.ACCENT).next_to(
            tri, DOWN, buff=0.1))
        rows = VGroup(
            label(r"if your yard is cheaper to run, \ Crusoe cannot follow you below \$20", font_size=24),
            label(rf"you price a cent under his cost \ and serve everyone: \ \${bt['unequal_profit']:,.0f} a season"
                  .replace(",", "{,}"), font_size=24, color=E.ACCENT),
            label(r"the efficient firm earns its cost advantage, \ and no more", font_size=24, color=EQ),
            label(r"in Bertrand's world, \ profit comes only from being better", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The paradox softens a little when costs differ. Suppose your yard is cheaper to run: ten dollars a "
            "repair against Crusoe's twenty. <bookmark mark='a'/> Crusoe cannot follow you below twenty without "
            "losing money. <bookmark mark='b'/> So you price a cent under his cost, nineteen ninety-nine, serve the "
            "whole island, and earn about eight hundred dollars a season. <bookmark mark='c'/> The efficient firm "
            "earns its cost advantage, and nothing more. <bookmark mark='d'/> In Bertrand's world, the only way to "
            "make a profit is to be better than your rival."
        ) as vo:
            self.play(Create(line), FadeIn(c1), FadeIn(c2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def which(self):
        left = VGroup(
            label(r"Cournot", font_size=34, color=LEADER),
            label(r"firms commit to quantities: \\ capacity, \ a harvest, \ a fleet", font_size=23),
            label(r"two firms: \ \$40", font_size=28, color=LEADER),
            label(r"price falls gradually \\ as firms are added", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        right = VGroup(
            label(r"Bertrand", font_size=34, color=CRUSOE),
            label(r"firms commit to prices: \\ a catalogue, \ a posted sign", font_size=23),
            label(r"two firms: \ \$10", font_size=28, color=CRUSOE),
            label(r"price hits cost \\ with the second firm", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3)
        cols = VGroup(left, right).arrange(RIGHT, buff=2.0).move_to(UP * 0.5)
        bar = Line(UP * 2.3, DOWN * 1.4, color=GREY_C).move_to(cols.get_center())
        foot = label(r"which is right? \ it depends on what firms can't easily change", font_size=28,
                     color=E.ACCENT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "So which is right? <bookmark mark='a'/> In Cournot's world firms commit to quantities, a harvest, a "
            "factory's capacity, a fleet of ships, and the price falls gradually as firms are added. "
            "<bookmark mark='b'/> In Bertrand's they commit to prices, in a catalogue or on a sign, and the second "
            "firm is enough to drive the price to cost. <bookmark mark='c'/> The answer depends on what firms "
            "cannot easily change, and the next chapter shows how each of the paradox's assumptions can fail."
        ) as vo:
            self.play(FadeIn(left[0]), FadeIn(right[0]), Create(bar))
            vo.wait_until("a")
            self.play(FadeIn(left[1:]))
            vo.wait_until("b")
            self.play(FadeIn(right[1:]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
