from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.price_map()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        deal = history_card(1996, r"Staples agrees to buy Office Depot", r"about \$4 billion: \ the two biggest of "
                            r"America's three office-supply superstore chains", color=GOV, width=11.0,
                            font_size=24).to_edge(UP, buff=0.6)
        sides = VGroup(
            VGroup(label(r"the companies", font_size=26, color=DEF),
                   wrapped_label(r"office supplies are sold by supermarkets, drugstores, warehouse clubs and mail "
                                 r"order: our share of all of it is small", 5.0, 21, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2),
            VGroup(label(r"the Federal Trade Commission", font_size=26, color=GOV),
                   wrapped_label(r"look at your own prices: where you face no other superstore, you charge more",
                                 5.0, 21, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
        ).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(deal, DOWN, buff=0.7)
        verdict = history_card(1997, r"Judge Thomas Hogan, \ 30 June", r"the merger is enjoined; \ the companies "
                               r"abandon it", color=E.ACCENT, width=8.0, font_size=22).next_to(sides, DOWN,
                                                                                               buff=0.6)
        tag = published_tag(r"FTC v. Staples, 970 F. Supp. 1066 (D.D.C. 1997); \ FTC case summary", corner=DL,
                            font_size=12)
        with self.voiceover(
            "In 1996 Staples agreed to buy Office Depot, for about four billion dollars. They were two of "
            "the three office-supply superstore chains in America. <bookmark mark='a'/> The companies said they "
            "competed with everyone who sells a pen: supermarkets, drugstores, warehouse clubs, mail order. Measured "
            "that way, their share was small. <bookmark mark='b'/> The Federal Trade Commission answered with the "
            "companies' own prices. Where Staples faced no other superstore, it charged more, by about thirteen "
            "percent against towns with both rivals, in the comparison as it is usually reported. <bookmark "
            "mark='c'/> In June 1997 Judge Thomas Hogan stopped the merger, and the companies abandoned it. It was "
            "a case in which the econometrics sat at the centre, and both sides brought economists to argue about "
            "it."
        ) as vo:
            self.play(FadeIn(deal, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sides[0], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(sides[1], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()

    def price_map(self):
        T = load("towns")
        G = T["groups"]
        mp = island_map(T, width=6.6, height=4.2).to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
        key = legend_rows([(ALDER, r"Alder alone"), (BIRCH, r"Alder and Birch"), (CEDAR, r"Alder and Cedar"),
                           (WHITE, r"all three")], font_size=17).next_to(mp, DOWN, buff=0.25).align_to(mp, LEFT)
        head = label(r"the Island: \ sixty towns, \ three superstore chains, \ and the corner shops", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        rows = VGroup()
        for i, (name, col) in enumerate((("Alder alone", ALDER), ("Alder and Birch", BIRCH),
                                         ("Alder and Cedar", CEDAR), ("all three", WHITE))):
            g = G[name]
            y = -0.5 * i
            rows.add(VGroup(label(rf"{name}", font_size=20, color=col).next_to([0, y, 0], RIGHT, buff=0),
                            label(rf"{g['n']} towns", font_size=18, color=GREY_B).next_to([2.6, y, 0], RIGHT, buff=0),
                            label(rf"\${g['price']:.2f}", font_size=22, color=col).next_to([5.0, y, 0], LEFT,
                                                                                           buff=0)))
        rh = label(r"Alder's price for a basket of supplies, \ average", font_size=18, color=GREY_A)
        side = VGroup(rh, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        prem = label(rf"alone: \ {T['lone_premium']:.0f}\% above towns with all three", font_size=21,
                     color=GOV).next_to(side, DOWN, buff=0.45).align_to(side, LEFT)
        catch = label(r"but towns with more stores are bigger, \\ with dearer rents", font_size=19,
                      color=HOLD).next_to(prem, DOWN, buff=0.25).align_to(side, LEFT)
        tag = island_tag(r"the Island: \ agora.merger, \ a nested logit with Bertrand pricing", corner=DR,
                         font_size=12)
        with self.voiceover(
            "The Island has its own version of the case. <bookmark mark='a'/> It has sixty towns. Alder, a chain of "
            "office superstores, is in every one; Birch is in some, Cedar in others, and the corner shops are "
            "everywhere. Bigger towns, drawn larger, tend to have more chains. <bookmark mark='b'/> Here is Alder's "
            f"price for a basket of supplies. Where it is alone, it averages {G['Alder alone']['price']:.2f} "
            f"dollars; where all three chains meet, {G['all three']['price']:.2f}. <bookmark mark='c'/> Alder "
            f"charges about {T['lone_premium']:.0f} percent more where it has no superstore rival. <bookmark "
            "mark='d'/> But look again: towns with Birch alone are cheaper than towns with all three. The towns "
            "differ in more than their shops: the big ones have dearer rents. Untangling that is the expert "
            "witness's job, and this part follows a merger of Alder and Birch from the first filing to the "
            "retrospective, with the truth known."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mp.coast), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in mp.dots], lag_ratio=0.03), FadeIn(key), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(rh), LaggedStart(*[FadeIn(r_, shift=LEFT * 0.1) for r_ in rows], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(prem), Indicate(rows[0], color=WHITE, scale_factor=1.05))
            vo.wait_until("d")
            self.play(Indicate(rows[1][2], color=WHITE), Indicate(rows[3][2], color=WHITE), FadeIn(catch))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what does the law ask, \ and who must prove what?", font_size=26, color=GOV),
            label(r"where does a market end?", font_size=26, color=ALDER),
            label(r"how do economists predict what a merger will do to prices, \ and to wages?", font_size=26,
                  color=SIM),
            label(r"what does a regression look like under cross-examination?", font_size=26, color=DEF),
            label(r"and were the predictions right?", font_size=26, color=CARTEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: how is economics used to decide a merger, and what survives cross-examination? "
            "<bookmark mark='a'/> What does the law ask, and who has to prove what? <bookmark mark='b'/> Where does "
            "a market end? <bookmark mark='c'/> How do economists predict what a merger will do to prices, and to "
            "wages? <bookmark mark='d'/> What does a regression look like when the other side's lawyer has it? "
            "<bookmark mark='e'/> And, years later, were the predictions right?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        T = load("towns")
        logo = island_map(T, width=4.2, height=2.3, radius=0.045)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 59 \ $\cdot$ \ The Expert Witness", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-nine: the expert witness."):
            self.play(FadeIn(logo.coast), LaggedStart(*[FadeIn(d) for d in logo.dots], lag_ratio=0.02),
                      run_time=1.8)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XI \ $\cdot$ \ Economics at Work", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the law of mergers: \ the standard, \ the process, \ who must prove what",
            r"market definition: \ the hypothetical monopolist, \ critical loss, \ the cellophane trap",
            r"predicting effects: \ concentration, \ diversion, \ pricing pressure, \ simulation, \ pass-through",
            r"vertical mergers, \ cartels and their damages, \ labour markets, \ regulated prices",
            r"evidence in court: \ regressions under cross-examination, \ and the retrospectives that score them",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part fifty-eight priced a bridge and a bill. This part prices a merger, in front of a judge. By the "
            "end you will know <bookmark mark='a'/> what merger law asks and how a case proceeds; <bookmark "
            "mark='b'/> how a market is drawn, with the hypothetical monopolist and its traps; <bookmark mark='c'/> "
            "how economists predict a merger's effects, from concentration to diversion, pricing pressure, "
            "simulation and pass-through; <bookmark mark='d'/> how vertical mergers, cartels, labour markets and "
            "regulated prices are analysed; <bookmark mark='e'/> and what a regression looks like under "
            "cross-examination, and how retrospectives score the predictions afterwards."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
