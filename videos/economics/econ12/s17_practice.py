from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 15, r"In practice: \ the economics of antitrust", r"How do economists help decide whether a merger "
             r"or a cartel harms buyers?", "Chapter fifteen. In practice: the economics of antitrust.",
             lit={1997: r"Staples and Office Depot"}, scale=("firm", "market", "nation"), horizon=("a year",))
        self.market()
        self.staples()
        self.toolkit()

    def market(self):
        b = load("boats")
        P0, c = b["duo_P"], b["c"]
        M = (P0 - c) / P0
        X = 0.05
        crit = X / (X + M)
        Q0 = 100 - P0
        Q1 = 100 - P0 * (1 + X)
        loss = (Q0 - Q1) / Q0
        rows = VGroup(
            label(r"first, \ what is the market? \ boats, \ or all ways of crossing the water?", font_size=24),
            label(r"the hypothetical monopolist test: \ would one owner of all the boats \ gain by raising the price "
                  r"5\%?", font_size=23, color=LEADER),
            MathTex(r"\text{critical loss} = \frac{X}{X + M} = \frac{0.05}{0.05 + " + f"{M:.2f}" + r"} = "
                    + f"{100 * crit:.2f}" + r"\%", font_size=36, color=EQ),
            label(rf"at \${P0:.0f} a boat with margin {100 * M:.0f}\%, \ a 5\% rise loses {100 * loss:.1f}\% of sales: "
                  rf"\ less than {100 * crit:.2f}\%", font_size=23, color=CRUSOE),
            label(r"so the rise pays, \ and boats are a market of their own", font_size=24, color=E.ACCENT),
            label(r"the trap: \ high margins shrink the critical loss, \ but also the actual loss \ (Katz and "
                  r"Shapiro, \ 2003)", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"DOJ and FTC, Merger Guidelines (2023); \ Katz and Shapiro, Antitrust 17(2) (2003); \ Agora", corner=DR,
                            font_size=13)
        with self.voiceover(
            "In practice, a merger case begins with a question that sounds legal and is really economic. "
            "<bookmark mark='a'/> What is the market? Boats, or every way of crossing the water? "
            "<bookmark mark='b'/> The guidelines answer with a thought experiment: would a single owner of all the "
            "boats find it profitable to raise their price by five percent? <bookmark mark='c'/> The rise pays if "
            "the share of sales it loses is smaller than the critical loss: the price rise divided by itself plus "
            "the margin. <bookmark mark='d'/> At Cournot's forty dollars, with a margin of three quarters, the "
            "critical loss is six and a quarter percent. A five percent rise would lose three point three percent "
            "of sales. <bookmark mark='e'/> So the rise pays, and boats are a market of their own. "
            "<bookmark mark='f'/> Notice the trap. High margins make the critical loss small, and merging firms "
            "cite that to argue for a broad market. But Michael Katz and Carl Shapiro pointed out in 2003 that a "
            "firm with a high margin must face few customers ready to leave, so the actual loss is small too. Read "
            "carelessly, the test misleads, which is why economists argue over it in court."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def staples(self):
        hc = history_card(1997, r"FTC v.\ Staples", r"two of the three office-supply superstore chains \ proposed to merge; \\ the "
                          r"court blocked it", color=LEADER, width=11.2, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the firms: \ the market is all office supplies, \ sold everywhere, \ and they hold a small share",
                  font_size=23),
            label(r"the economists: \ compare prices across cities", font_size=24, color=LEADER),
            label(r"Staples charged less where an Office Depot was nearby", font_size=24, color=EQ),
            label(r"so the superstores competed with each other, \ more than with anyone else: \ a market of their "
                  r"own", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"FTC v.\ Staples, 970 F.\ Supp.\ 1066 (D.D.C.\ 1997)", corner=DR, font_size=13)
        with self.voiceover(
            "A famous case shows how the argument is won with data. In 1997 two of America's three office-supply "
            "superstore chains, Staples and Office Depot, agreed to merge. <bookmark mark='a'/> The "
            "firms said their market was all office supplies, sold by every kind of shop, in which they held a "
            "small share. <bookmark mark='b'/> The Federal Trade Commission's economists compared prices across "
            "cities instead. <bookmark mark='c'/> Staples charged less where an Office Depot was nearby. "
            "<bookmark mark='d'/> So the superstores competed with each other more than with anyone else, and the "
            "court accepted that they formed a market of their own, and blocked the merger."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def toolkit(self):
        rows = point_cards([
            (r"market definition", r"the hypothetical \\ monopolist test", LEADER),
            (r"diversion", r"where would a firm's \\ customers go?", CRUSOE),
            (r"merger simulation", r"solve chapters 2 to 4 \\ with estimated demand", EQ),
            (r"overcharges", r"damages for \\ cartel buyers", CARTEL),
            (r"screens", r"prices that look \\ coordinated", PUMP),
            (r"remedies", r"sell a plant, \\ license a patent", COMPETE),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.1)
        head = label(r"the antitrust economist's kit", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"measured markups: \ Part 43; \ platforms and dynamic competition: \ Part 44; \ the expert "
                     r"witness: \ Part 59", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "This is the antitrust economist's kit. <bookmark mark='a'/> Defining the market, with the hypothetical "
            "monopolist. Diversion: if a firm raised its price, where would its customers go? Merger simulation: "
            "solving models like chapters two to four with demand estimated from data, to predict prices after a "
            "merger. Overcharges, which set the damages a cartel's buyers can claim. Screens that look in price "
            "data for signs of coordination. And remedies: selling a plant, or licensing a patent, so that a merger "
            "can go ahead without the harm. <bookmark mark='b'/> Part forty-three measures markups directly, Part "
            "forty-four takes on platforms and dynamic competition, and Part fifty-nine puts you in the witness "
            "box."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in rows.cards], lag_ratio=0.6), run_time=14)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
