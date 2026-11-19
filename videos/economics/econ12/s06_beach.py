from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

SAND = "#E9D8A6"
ANA = island.CAST["ana"].color
BO = island.CAST["bo"].color


def beach(width=11.0):
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=SAND, stroke_width=10)
    ends = VGroup(label(r"0", font_size=20, color=GREY_B).next_to(line.get_left(), DOWN, buff=0.25),
                  label(r"1", font_size=20, color=GREY_B).next_to(line.get_right(), DOWN, buff=0.25),
                  label(r"$\tfrac12$", font_size=22, color=GREY_B).next_to(line.get_center(), DOWN, buff=0.25))
    return VGroup(line, ends)


def at(line, x):
    return line.point_from_proportion(float(np.clip(x, 0, 1)))


class Beach(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Hotelling's line \ and Salop's circle", r"Where do sellers choose to stand, \ and how many "
             r"of them does a market get?", "Chapter five. Hotelling's line and Salop's circle.",
             lit={1929: r"Hotelling's ``Stability in Competition''"}, scale=("firm", "market"),
             horizon=("a season",))
        self.drift()
        self.sameness()
        self.apart()
        self.circle()

    def drift(self):
        be = load("beach")
        bch = beach().move_to(UP * 0.6)
        line = bch[0]
        path_ = be["path"]
        a = VGroup(islander("ana", 0.7), label(r"Ana", font_size=18, color=ANA)).arrange(DOWN, buff=0.08)
        b = VGroup(islander("bo", 0.7), label(r"Bo", font_size=18, color=BO)).arrange(DOWN, buff=0.08)
        a.next_to(at(line, path_[0][0]), UP, buff=0.12)
        b.next_to(at(line, path_[0][1]), UP, buff=0.12)
        split = DashedLine(at(line, 0.5) + UP * 0.25, at(line, 0.5) + DOWN * 0.25, color=WHITE, stroke_width=2)
        rows = VGroup(
            label(r"bathers spread evenly along a beach; \ ice creams at one fixed price; \ each walks to the "
                  r"nearer seller", font_size=23),
            label(r"each seller gains by stepping toward the other: \ she keeps her side and wins some of his",
                  font_size=23, color=GREY_A),
            label(r"until both stand back to back in the middle", font_size=24, color=EQ),
            label(r"average walk: \ a quarter of the beach; \ at the quarter-points it would be an eighth",
                  font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Hotelling, Economic Journal 39(153) (1929)", corner=DR, font_size=13)
        with self.voiceover(
            "In 1929 the American statistician Harold Hotelling turned competition into geography. Picture Ana and "
            "Bo selling ice creams on the Island's beach. <bookmark mark='a'/> Bathers are spread evenly along the "
            "sand, both sellers charge the same fixed price, and every bather walks to the nearer of the two. "
            "<bookmark mark='b'/> Each seller gains by stepping toward the other: she keeps every bather on her side "
            "and wins some of his. <bookmark mark='c'/> They keep stepping until they stand back to back in the "
            "middle. <bookmark mark='d'/> Bathers then walk a quarter of the beach on average. If the sellers stood "
            "at the quarter-points, the same split of customers would need only an eighth."
        ) as vo:
            self.play(FadeIn(bch), FadeIn(a), FadeIn(b), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            for x1, x2 in path_[1:4]:
                self.play(a.animate.next_to(at(line, x1), UP, buff=0.12).shift(LEFT * 0.35 if x1 == 0.5 else 0),
                          b.animate.next_to(at(line, x2), UP, buff=0.12).shift(RIGHT * 0.35 if x2 == 0.5 else 0),
                          run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(split))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sameness(self):
        q = quote_card(r"Buyers are confronted everywhere with an excessive sameness.", r"Harold Hotelling, "
                       r"\ ``Stability in Competition'' (1929)", width=10.6, font_size=30).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"Hotelling's own example: \ in a two-party election, \ each party makes its platform \\ as "
                  r"much like the other's as it can", font_size=23),
            label(r"Anthony Downs's theory of party competition \ (1957; \ Part 47) \ starts here", font_size=24,
                  color=LEADER),
            label(r"radio stations playing the same hits; \ shops on one street; \ films released the same week",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(q, DOWN, buff=0.55)
        tag = published_tag(r"Hotelling (1929), p.\ 54; \ Downs, \emph{An Economic Theory of Democracy} (1957)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Hotelling thought the result explained a great deal. Buyers, he wrote, are confronted everywhere with an "
            "excessive sameness. <bookmark mark='a'/> His own example was politics: in a two-party election, each "
            "party strives to make its platform as much like the other's as possible. <bookmark mark='b'/> In 1957 "
            "Anthony Downs built a theory of party competition on the idea, which Part forty-seven takes up. "
            "<bookmark mark='c'/> Radio stations playing the same hits, shops crowding one street, films released "
            "in the same week: all are sellers moving toward the middle of their customers."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.1), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def apart(self):
        be = load("beach")
        bch = beach().move_to(UP * 1.2)
        line = bch[0]
        a = VGroup(islander("ana", 0.7), label(r"Ana", font_size=18, color=ANA)).arrange(DOWN, buff=0.08)
        b = VGroup(islander("bo", 0.7), label(r"Bo", font_size=18, color=BO)).arrange(DOWN, buff=0.08)
        a.next_to(at(line, 0.5), UP, buff=0.12).shift(LEFT * 0.35)
        b.next_to(at(line, 0.5), UP, buff=0.12).shift(RIGHT * 0.35)
        rows = VGroup(
            label(r"but if the sellers also choose prices, \ standing together is Bertrand's war: \ prices fall to "
                  r"cost", font_size=23),
            label(r"d'Aspremont, \ Gabszewicz and Thisse (1979): \ with walking costs that rise with the square of "
                  r"distance, \\ they move to opposite ends", font_size=23, color=LEADER),
            label(rf"at the ends: \ each charges cost plus the walking cost, \ \${be['end_p']:.0f} with $t = 1$, \ "
                  rf"and earns {be['end_profit']:.1f}", font_size=23, color=EQ),
            label(r"close together for customers, \ far apart for prices: \ which force wins depends on the market",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"d'Aspremont, Gabszewicz and Thisse, Econometrica 47(5) (1979)", corner=DR, font_size=13)
        with self.voiceover(
            "Hotelling's sellers did not choose their prices. <bookmark mark='a'/> If they did, standing back to "
            "back would be Bertrand's war: identical sellers in the same spot would cut their prices to cost. "
            "<bookmark mark='b'/> In 1979 Claude d'Aspremont, Jean Gabszewicz and Jacques Thisse showed that when "
            "walking costs rise with the square of the distance, sellers who choose both place and price move to "
            "opposite ends of the beach. <bookmark mark='c'/> There each charges its cost plus the walking cost "
            "across the whole beach, and earns half of it. <bookmark mark='d'/> Moving together wins customers; "
            "moving apart protects prices. Which force wins depends on the market, which is why some products are "
            "copies of each other and others are deliberately unlike."
        ) as vo:
            self.play(FadeIn(bch), FadeIn(a), FadeIn(b), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(a.animate.next_to(at(line, 0.0), UP, buff=0.12), b.animate.next_to(at(line, 1.0), UP, buff=0.12),
                      FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def circle(self):
        be = load("beach")
        ns = np.array(be["ns"])
        total = np.array(be["total"])
        ring = Circle(radius=1.45, color=SAND, stroke_width=8).move_to(LEFT * 4.9 + DOWN * 0.2)
        n_free = int(round(be["n_free"]))
        shops = VGroup(*[Dot(ring.point_at_angle(TAU * k / n_free + PI / 2), radius=0.1, color=ENTRANT)
                         for k in range(n_free)])
        rl = label(rf"free entry: \ {n_free} sellers", font_size=19, color=ENTRANT).next_to(ring, DOWN, buff=0.3)
        ax = plane([1.5, 20.5], [0, 0.25], center=LEFT * 0.3 + DOWN * 0.4, x_length=4.4, y_length=3.8,
                   xticks=[2, 5, 10, 15, 20], yticks=[0, 0.1, 0.2], xlabel=r"number of sellers",
                   ylabel=r"entry plus walking costs", font_size=15, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}")
        a = ax.ax
        curve = path(ax, ns, total, color=WHITE, width=3, yr=(0, 0.25))
        po = Dot(a.c2p(be["n_opt"], be["cost_opt"]), radius=0.09, color=COMPETE)
        pf = Dot(a.c2p(be["n_free"], be["cost_free"]), radius=0.09, color=ENTRANT)
        side = VGroup(
            label(r"Steven Salop (1979): \\ the coast as a circle, \\ a cost to set up a stall", font_size=20),
            MathTex(r"n_{\text{free}} = \sqrt{t/F}, \quad n_{\text{best}} = \tfrac12 \sqrt{t/F}", font_size=30,
                    color=EQ),
            label(rf"free entry: \ {n_free}; \\ the planner's best: \ {be['n_opt']:.0f}", font_size=21,
                  color=ENTRANT),
            label(r"each newcomer mostly steals \\ customers, \ which is private gain, \\ not social gain: \ "
                  r"too many sellers", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Salop, Bell Journal 10(1) (1979); \ the numbers: \ Agora", corner=DR, font_size=13)
        with self.voiceover(
            "How many sellers does a market get? <bookmark mark='a'/> In 1979 Steven Salop bent Hotelling's line "
            "into a circle, like the Island's coast, so that there are no ends, and made every new seller pay a cost "
            "to set up. <bookmark mark='b'/> Sellers enter until profit is gone, at the square root of the walking "
            "cost over the setup cost. A planner, adding setup costs to walking costs, would want only half as many. "
            "<bookmark mark='c'/> With the Island's numbers, free entry brings ten stalls, and the planner would "
            "choose five. <bookmark mark='d'/> The reason is that each newcomer mostly steals customers from its "
            "neighbours. That is gain to the newcomer, but not to the island, which only saves a little walking. So "
            "free entry can give too many sellers, as well as too few."
        ) as vo:
            self.play(Create(ring), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(side[1]), FadeIn(ax), Create(curve))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_, scale=1.5) for s_ in shops], lag_ratio=0.15), FadeIn(rl),
                      FadeIn(po), FadeIn(pf), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
