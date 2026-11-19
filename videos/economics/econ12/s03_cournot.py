from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403


class Cournot(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Cournot: \ competing in quantities", r"If each firm chooses how much to make, \ and the market "
             r"sets the price, \ where do they end up?", "Chapter two. Cournot: competing in quantities.",
             lit={1838: r"Cournot's \emph{Recherches}"}, scale=("firm", "market"), horizon=("a year",))
        self.springs()
        self.reaction()
        self.dilemma()
        self.many()

    def springs(self):
        hc = history_card(1838, r"Antoine Augustin Cournot, \ \emph{Recherches sur les principes math\'ematiques de "
                          r"la th\'eorie des richesses}", r"two owners of mineral springs \ sell the same water; \ "
                          r"each decides how much to bring to market, \\ and the price is whatever sells it all",
                          color=LEADER, width=11.8, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"each owner takes the other's quantity as given, \ and chooses the best reply to it", font_size=24),
            label(r"an equilibrium: \ each quantity is the best reply to the other \ (Nash's idea, \ 112 years early)",
                  font_size=24, color=EQ),
            label(r"the book went almost unread for decades", font_size=23, color=GREY_A),
            label(r"on the Island: \ Crusoe's yard and Dara's \ build boats for the season", font_size=24,
                  color=CRUSOE),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.5)
        glyph = yards(0.8).next_to(rows, DOWN, buff=0.3)
        tag = published_tag(r"Cournot, \emph{Recherches} (1838), ch.\ 7", corner=DR, font_size=13)
        with self.voiceover(
            "The first answer came in 1838, from a French mathematician, Antoine Augustin Cournot, in a book on the "
            "mathematical principles of the theory of wealth. Its seventh chapter imagines two owners of mineral "
            "springs, selling the same water. Each decides how much to bring to market, and the price is whatever "
            "sells it all. <bookmark mark='a'/> Each owner takes the other's quantity as given and chooses the best "
            "reply to it. <bookmark mark='b'/> An equilibrium is a pair of quantities, each the best reply to the "
            "other: Nash's idea, a hundred and twelve years before Nash. <bookmark mark='c'/> For decades, almost "
            "nobody read it. "
            "<bookmark mark='d'/> On the Island, Crusoe's yard and Dara's must each decide in spring how many boats "
            "to build, facing the same demand as before: at a price of p, a hundred minus p boats a season, each "
            "costing ten dollars to build."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(glyph, shift=UP * 0.2))
        self.clear_scene()

    def reaction(self):
        b = load("boats")
        ax = plane([0, 92], [0, 92], center=LEFT * 3.2 + DOWN * 0.3, x_length=5.4, y_length=5.4,
                   xticks=[0, 22.5, 30, 45, 90], yticks=[0, 22.5, 30, 45, 90], xlabel=r"Crusoe's boats",
                   ylabel=r"Dara's boats", font_size=16, xfmt=lambda v: fmt(v), yfmt=lambda v: fmt(v))
        a = ax.ax
        q = np.array(b["q1"])
        rep = np.array(b["reply"])
        rc = path(ax, rep, q, color=CRUSOE, width=3.5, smooth=False)        # Crusoe's reply to Dara's q
        rd = path(ax, q, rep, color=DARA, width=3.5, smooth=False)          # Dara's reply to Crusoe's q
        rcl = label(r"Crusoe's best reply", font_size=16, color=CRUSOE).next_to(a.c2p(12, 78), RIGHT, buff=0.1)
        rdl = label(r"Dara's best reply", font_size=16, color=DARA).next_to(a.c2p(64, 14), UP, buff=0.2)
        pts = b["path"]
        steps = VGroup()
        for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
            if abs(x1 - x0) + abs(y1 - y0) > 1e-9:
                steps.add(Arrow(a.c2p(x0, y0), a.c2p(x1, y1), buff=0, color=WHITE, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.12))
        eq = Dot(a.c2p(b["duo_q"], b["duo_q"]), radius=0.1, color=EQ)
        side = VGroup(
            MathTex(r"q_C = \frac{90 - q_D}{2}", font_size=36, color=CRUSOE),
            label(r"each extra boat lowers the price on all of them: \\ Crusoe stops where that cost meets the "
                  r"margin", font_size=21),
            label(r"start with Crusoe alone at 45; \ Dara replies 22.5; \\ Crusoe cuts to 33.75; \ and so on",
                  font_size=21, color=GREY_A),
            label(rf"they meet at {b['duo_q']:.0f} boats each: \\ price \${b['duo_P']:.0f}, \ \${b['duo_profit']:.0f} "
                  r"profit each", font_size=22, color=EQ),
            label(r"Crusoe's \$40 in Play it \ was Cournot's price", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is the argument as a picture. <bookmark mark='a'/> If Dara builds q D boats, Crusoe faces what is "
            "left of demand, and his best reply is ninety minus q D, halved. <bookmark mark='b'/> Each extra boat he "
            "builds lowers the price on every boat he sells, so he stops where that loss just balances his margin. "
            "Dara's best reply is the mirror image. <bookmark mark='c'/> Start with Crusoe alone, building the "
            "monopoly's forty-five. Dara's best reply is twenty-two and a half. Crusoe's reply to that is "
            "thirty-three and three quarters, and so on, back and forth. <bookmark mark='d'/> The replies close in "
            "on the point where the two curves cross: thirty boats each, sixty in all, selling at forty dollars, "
            "with nine hundred dollars of profit for each yard. <bookmark mark='e'/> Crusoe's forty-dollar sign in "
            "Play it was Cournot's price."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(rc), FadeIn(rcl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(rd), FadeIn(rdl))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), LaggedStart(*[GrowArrow(s_) for s_ in steps], lag_ratio=0.5), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(eq, scale=1.5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dilemma(self):
        b = load("boats")
        rows = VGroup(
            label(rf"together, \ as one monopoly: \ {b['mono_Q']:.0f} boats at \${b['mono_P']:.0f}, \ "
                  rf"\${b['mono_profit']:,.0f} profit".replace(",", "{,}"), font_size=25, color=CARTEL),
            label(rf"split evenly: \ {b['cartel_q_each']:.1f} boats each, \ \${b['cartel_profit_each']:,.1f} each"
                  .replace(",", "{,}"), font_size=25, color=CARTEL),
            label(rf"Cournot: \ {b['duo_q']:.0f} boats each, \ \${b['duo_profit']:.0f} each", font_size=25, color=EQ),
            label(r"from the cartel's 22.5, \ each yard gains by building a few more: \ a prisoner's dilemma",
                  font_size=24),
            label(r"the price lands between monopoly's \$55 and the cost's \$10", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        head = label(r"two yards, \ and the profit they leave on the table", font_size=32, color=E.ACCENT
                     ).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Notice what the two yards leave on the table. <bookmark mark='a'/> Acting as one monopoly, they would "
            "build forty-five boats and sell them at fifty-five dollars, for two thousand and twenty-five dollars "
            "of profit. <bookmark mark='b'/> Split evenly, that is twenty-two and a half boats and a thousand and "
            "twelve dollars and fifty cents each. <bookmark mark='c'/> Cournot's equilibrium gives each only nine "
            "hundred. <bookmark mark='d'/> Yet from the cartel's twenty-two and a half, each yard gains by building "
            "a few more boats, whatever the other does: Part eleven's prisoner's dilemma, with boats. "
            "<bookmark mark='e'/> So the price lands between the monopoly's fifty-five dollars and the cost of "
            "ten."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def many(self):
        b = load("boats")
        ns = np.array(b["ns"])
        P = np.array(b["P"])
        ax = plane([0, 21], [0, 60], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[1, 2, 5, 10, 15, 20], yticks=[0, 10, 20, 40, 55], xlabel=r"number of yards",
                   ylabel=r"price of a boat, \ \$", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        dots = VGroup(*[Dot(a.c2p(n, p), radius=0.07, color=EQ) for n, p in zip(ns, P)])
        cost = DashedLine(a.c2p(0, 10), a.c2p(21, 10), color=COMPETE, stroke_width=2)
        cl = label(r"cost", font_size=16, color=COMPETE).next_to(a.c2p(21, 10), UP, buff=0.08).shift(LEFT * 0.3)
        side = VGroup(
            MathTex(r"P = \frac{a + N c}{N + 1}", font_size=38, color=EQ),
            label(rf"one yard: \ \${P[0]:.0f}; \ two: \ \${P[1]:.0f}; \ three: \ \${P[2]:.1f}", font_size=21),
            label(rf"twenty yards: \ \${b['P20']:.2f}", font_size=22, color=EQ),
            label(r"each new firm takes a smaller bite \\ of the margin it shares: \\ the price slides toward cost",
                  font_size=21, color=GREY_A),
            label(r"from monopoly to perfect competition, \\ in one formula", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Cournot's model has a second gift. Let the number of yards grow. <bookmark mark='a'/> With demand a "
            "minus Q and cost c, N identical firms set a price of a plus N c, over N plus one. "
            "<bookmark mark='b'/> One yard charges fifty-five dollars, two charge forty, three thirty-two fifty. "
            "<bookmark mark='c'/> Twenty yards charge fourteen dollars and twenty-nine cents. "
            "<bookmark mark='d'/> Each new firm cares less about how its extra boat lowers the price, because it "
            "sells a smaller share of the boats at that price, and so the price slides toward cost. "
            "<bookmark mark='e'/> Monopoly and perfect competition turn out to be the two ends of one formula."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cost), FadeIn(cl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots[:3]], lag_ratio=0.4), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots[3:]], lag_ratio=0.1), FadeIn(side[2]),
                      run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
