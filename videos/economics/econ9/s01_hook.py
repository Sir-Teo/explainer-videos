from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

R = tables.RADFORD_1945.data


def bungalow(width=1.5, color="#6B5B45"):
    body = Rectangle(width=width, height=width * 0.5, stroke_color="#A89276", stroke_width=2, fill_color=color,
                     fill_opacity=0.8)
    roof = Polygon(body.get_corner(UL) + LEFT * 0.12, body.get_corner(UR) + RIGHT * 0.12,
                   body.get_top() + UP * width * 0.28, stroke_color="#A89276", stroke_width=2, fill_color="#4F4334",
                   fill_opacity=0.9)
    door = Rectangle(width=width * 0.14, height=width * 0.26, stroke_width=0, fill_color="#2E271E",
                     fill_opacity=1).move_to(body.get_bottom(), aligned_edge=DOWN)
    return VGroup(body, roof, door)


class Hook(VoiceoverScene):
    def construct(self):
        self.parcel()
        self.padre()
        self.currency()
        self.liberation()
        self.arrow_debreu()
        self.question()
        self.title()
        self.objectives()

    def parcel(self):
        camp = VGroup(*[bungalow() for _ in range(6)]).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.8)
        wire = DashedLine(camp.get_corner(DL) + DOWN * 0.35 + LEFT * 0.3, camp.get_corner(DR) + DOWN * 0.35 +
                          RIGHT * 0.3, color=GREY_C, stroke_width=2, dash_length=0.12)
        where = label(r"an Oflag, \ a camp for captured officers: \ 1{,}200 to 2{,}500 prisoners, \\ "
                      r"about 200 to a bungalow", font_size=22, color=GREY_A).next_to(wire, DOWN, buff=0.3)
        box = parcel(2.0).move_to(DOWN * 0.35 + LEFT * 4.2)
        items = VGroup(*[tin(t, c) for t, c in (("milk", "#DCE6F0"), ("jam", "#D96C6C"), ("butter", "#F2D98B"),
                                                 ("biscuits", "#D9B98B"), ("bully", "#B5655B"),
                                                 ("chocolate", "#7A4E3A"), ("sugar", "#EDEDED"))])
        items.add(VGroup(*[cigarette(0.5) for _ in range(5)]).arrange(DOWN, buff=0.06))
        items.arrange(RIGHT, buff=0.22).next_to(box, RIGHT, buff=0.5)
        q = quote_card(tex_safe(R["equal"]), r"R.\ A.\ Radford, \emph{Economica} (1945), p.\ 190", width=11.4,
                       font_size=25, color=E.ACCENT).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"Radford, Economica 12(48) (1945)", corner=DR, font_size=14)
        with self.voiceover(
            "In 1945 an economist named R. A. Radford published an account of an economy he had just left, a "
            "prisoner-of-war camp. <bookmark mark='a'/> He had spent the last part of the war in camps for captured "
            "officers, in "
            "Italy and then Germany: between twelve hundred and twenty-five hundred men, two hundred or so to a "
            "bungalow. <bookmark mark='b'/> Almost everything they had came in Red Cross parcels: tinned milk, jam, "
            "butter, biscuits, bully beef, chocolate, sugar, and cigarettes. <bookmark mark='c'/> And every man got "
            "the same parcel. There was almost nothing to produce, and nobody set the prices. "
            "<bookmark mark='d'/> Yet, Radford wrote, everyone receives a roughly equal share of essentials; it is "
            "by trade that individual preferences are given expression and comfort increased."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in camp], lag_ratio=0.15), Create(wire),
                      FadeIn(tag), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(where))
            vo.wait_until("b")
            self.play(FadeIn(box, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.15), run_time=2.2)
            vo.wait_until("c")
            self.play(Indicate(box, color=E.ACCENT, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeOut(where), FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def padre(self):
        camp = VGroup(*[bungalow(1.3) for _ in range(8)]).arrange_in_grid(2, 4, buff=(0.9, 0.7)).move_to(
            LEFT * 2.6 + UP * 0.3)
        street = 0.5 * (camp[0].get_bottom()[1] + camp[4].get_top()[1])
        pts = []
        for k in range(4):
            x = camp[k].get_center()[0]
            pts += [np.array([x, street + 0.15, 0]), np.array([x, camp[k].get_bottom()[1] - 0.05, 0]),
                    np.array([x, street + 0.15, 0]), np.array([x, street - 0.15, 0]),
                    np.array([x, camp[4 + k].get_top()[1] + 0.05, 0]), np.array([x, street - 0.15, 0])]
        pts.append(pts[0])
        stops = pts
        route = VMobject(stroke_color=E.ACCENT, stroke_width=2.5).set_points_as_corners(pts)
        walker = Dot(stops[0], radius=0.11, color=E.ACCENT)
        hand = VGroup(tin("cheese", "#F2C14E", 0.6, 12), VGroup(*[cigarette(0.35) for _ in range(5)]).arrange(
            DOWN, buff=0.04)).arrange(RIGHT, buff=0.12)
        start = VGroup(label(r"he sets out with:", font_size=22), hand.copy()).arrange(DOWN, buff=0.18)
        end = VGroup(label(r"he comes back with:", font_size=22),
                     VGroup(hand.copy(), label(r"+", font_size=30), parcel(1.0)).arrange(RIGHT, buff=0.2)
                     ).arrange(DOWN, buff=0.18)
        side = VGroup(start, end).arrange(DOWN, buff=0.7, aligned_edge=LEFT).to_edge(RIGHT, buff=0.7).shift(UP * 0.6)
        moral = label(r"prices varied from bungalow to bungalow: \\ ``the market was not yet perfect''", font_size=24,
                      color=E.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Trade started at once, as simple swaps: a non-smoker's cigarettes for a friend's chocolate. "
            "<bookmark mark='a'/> And a story went round the first camp, in Italy. A padre set off round the camp "
            "with a tin of cheese and five cigarettes, <bookmark mark='b'/> and came back to his bed with a "
            "complete parcel, as well as the cheese and cigarettes he had started with. <bookmark mark='c'/> Nobody "
            "had been robbed. In that camp men rarely visited other bungalows, so the same goods fetched different "
            "prices in different huts, and the padre carried them from where they were cheap to where they were dear. "
            "The market, Radford noted, was not yet perfect."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in camp], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(walker), FadeIn(start))
            vo.wait_until("b")
            self.play(MoveAlongPath(walker, route), Create(route), run_time=4.5, rate_func=linear)
            self.play(FadeIn(end, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(moral, shift=UP * 0.2))
        self.clear_scene()

    def currency(self):
        board = RoundedRectangle(width=6.2, height=4.4, corner_radius=0.12, stroke_color="#A89276", stroke_width=3,
                                 fill_color="#2B241B", fill_opacity=0.9).move_to(LEFT * 3.4 + DOWN * 0.2)
        head = label(r"Exchange and Mart", font_size=26, color="#F2E3C6").next_to(board.get_top(), DOWN, buff=0.25)
        cols = VGroup(*[label(t, font_size=19, color="#C8B79A") for t in (r"name", r"room", r"wanted",
                                                                           r"offered")]).arrange(RIGHT, buff=0.55)
        cols.next_to(head, DOWN, buff=0.3)
        ads = VGroup(*[label(t, font_size=18, color="#F2E3C6") for t in (
            r"B. \quad 12 \quad cheese \quad 7 cigs",
            r"H. \quad 4 \quad 4 cigs \quad treacle",
            r"R. \quad 9 \quad 8 cigs \quad bread",
            r"D. \quad 3 \quad 80 cigs \quad shirt")]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        ads.next_to(cols, DOWN, buff=0.3)
        note = label(r"a board drawn with prices from Radford's article", font_size=15, color=GREY_B).next_to(
            board, DOWN, buff=0.15)
        side = VGroup(
            label(r"``cheese for seven'' \ (cigarettes)", font_size=25, color=E.ACCENT),
            label(r"``The cigarette became the standard of value.''", font_size=24),
            label(r"posted prices: \ one price, \ nearly, \ across the camp", font_size=23, color=GREY_A),
            label(r"a transit camp, \ with no board: \\ a tin of salmon varied by two cigarettes in 20 \\ "
                  r"from one end of a hut to the other", font_size=22, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "By the time they reached their permanent camps, every price was quoted in one good. "
            "<bookmark mark='a'/> Men walked the bungalows calling their offers: cheese for seven, meaning seven "
            "cigarettes. <bookmark mark='b'/> The cigarette became the standard of value, and even non-smokers sold "
            "for cigarettes, to buy something else later. <bookmark mark='c'/> Soon each bungalow had an Exchange "
            "and Mart board, with columns for name, room, wanted and offered. Because the offers were public, prices "
            "tended to equality throughout the camp. <bookmark mark='d'/> Where there was no board, as in the "
            "chaotic transit camps, the price of a tin of salmon could vary by two cigarettes in twenty from one end "
            "of a hut to the other."
        ) as vo:
            self.play(FadeIn(board), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cols), LaggedStart(*[FadeIn(a, shift=RIGHT * 0.1) for a in ads], lag_ratio=0.3),
                      FadeIn(side[2]), FadeIn(note), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def liberation(self):
        rows = VGroup(
            history_card(r"1944", r"August: \ parcels and cigarettes halved", r"prices fall; \ a paper money backed "
                         r"by food, \ the Bully Mark, \ slides to four-fifths of a cigarette; \ fixed prices give way "
                         r"to a black market", color=HOLD, width=11.6, font_size=23),
            history_card(r"1945", r"February: \ the food parcels run out", r"``the depression became a blizzard''",
                         color=HOLD, width=11.6, font_size=23),
            history_card(r"1945", r"12 April: \ the 30th U.S.\ Infantry Division arrives",
                         r"``the ushering in of an age of plenty demonstrated the hypothesis that with infinite "
                         r"means economic organisation and activity would be redundant''", color=E.TRUTH, width=11.6,
                         font_size=23),
        ).arrange(DOWN, buff=0.35)
        head = label(r"booms and slumps, \ set off by the deliveries of cigarettes", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.4)
        tag = published_tag(r"Radford, Economica 12(48) (1945), pp.\ 195--201", corner=DR, font_size=14)
        with self.voiceover(
            "The camp economy had booms and slumps, set off by the deliveries of cigarettes. <bookmark mark='a'/> "
            "In August 1944 parcels and cigarettes were both halved. Prices fell. A paper currency backed by food, "
            "the Bully Mark, slipped below its value in cigarettes, and an attempt to fix fair prices gave way to a "
            "black market. <bookmark mark='b'/> In February 1945 the food parcels ran out, and in Radford's words "
            "the depression became a blizzard. <bookmark mark='c'/> Then, on the twelfth of April, the American "
            "thirtieth infantry division arrived, and with it, he wrote, an age of plenty, which demonstrated that "
            "with infinite means economic organisation would be redundant."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=UP * 0.2))
        self.clear_scene()

    def arrow_debreu(self):
        hc = history_card(1954, r"Kenneth Arrow and G\'erard Debreu", r"``Existence of an Equilibrium for a "
                          r"Competitive Economy'', \emph{Econometrica}: \ in any economy that meets their conditions, "
                          r"there are prices at which every market clears at once", color=E.ACCENT, width=11.4,
                          font_size=25).move_to(UP * 1.6)
        rows = VGroup(
            label(r"Radford saw it happen: \ order that nobody designed", font_size=27),
            label(r"Arrow and Debreu proved it can exist, \ in any economy of that kind", font_size=27,
                  color=E.ACCENT),
            label(r"nobody has proved that an economy gets there", font_size=27, color=HOLD),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.6)
        tag = published_tag(r"Arrow and Debreu, Econometrica 22(3) (1954) 265--290", corner=DR, font_size=14)
        with self.voiceover(
            "Radford had watched prices appear, settle and spread, with nobody in charge of them. "
            "<bookmark mark='a'/> Nine years later two economists, Kenneth Arrow and Gerard Debreu, proved that "
            "order of that kind can exist in any economy that meets their conditions: there is a set of prices at "
            "which every market clears at once. <bookmark mark='b'/> It was one of the oldest claims in economics, "
            "Adam Smith's invisible hand, turned into a theorem. <bookmark mark='c'/> What they could not prove, and what "
            "nobody has proved since, is that an economy gets there."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.7)
        rows = VGroup(
            label(r"when can trade go no further, \ and who gets what?", font_size=30, color=CC),
            label(r"are there prices that clear every market at once?", font_size=30, color=PRICE),
            label(r"is the result good, \ and will a market find it?", font_size=30, color=CORE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "So this part asks: can a whole economy of selfish traders reach a state that nobody could improve on, "
            "and will it? <bookmark mark='a'/> When can trade go no further, and who ends up with what? "
            "<bookmark mark='b'/> Are there prices that clear every market at the same time? "
            "<bookmark mark='c'/> And is the result any good, and will a market find it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = VGroup(cigarette(1.4), cigarette(1.4), cigarette(1.4)).arrange(DOWN, buff=0.1)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 9 \ $\cdot$ \ The Invisible Hand, Proved", font_size=34, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part nine: the invisible hand, proved."):
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in logo], lag_ratio=0.3), run_time=1.2)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()
        del g

    def objectives(self):
        head = label(r"Act III \ $\cdot$ \ Markets", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"trade in a box: \ gains from trade, \ efficiency, \ the contract curve",
            r"prices that clear every market, \ and the core of a large economy",
            r"the two welfare theorems, \ proved, \ and what they assume",
            r"existence by a colouring game; \ stability, \ and a market that circles for ever",
            r"production, \ uncertainty, \ planning, \ and what the theorems cannot promise",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part opens Act Three, on markets: not one market, as in Act One, but all of them at once. "
            "<bookmark mark='a'/> We'll start with two traders in a box, and see what trade can achieve. "
            "<bookmark mark='b'/> Then prices that clear every market, and why a large economy leaves almost no room "
            "for bargaining. <bookmark mark='c'/> We'll prove the two welfare theorems, and list what they assume. "
            "<bookmark mark='d'/> We'll prove that equilibrium exists with a colouring game, and watch a market that "
            "circles for ever without finding it. <bookmark mark='e'/> And then production, uncertainty, the old "
            "argument over central planning, and what the theory cannot promise."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
