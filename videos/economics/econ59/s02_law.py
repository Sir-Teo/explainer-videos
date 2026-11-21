from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class Law(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What the law asks", r"When may a merger be stopped, \ and who must prove what?",
             "Chapter one. What the law asks.", lit={1914: r"Clayton Act", 1963: r"Philadelphia National Bank",
                                                    1976: r"Hart-Scott-Rodino"},
             scale=("firm", "market", "nation"), horizon=("a year", "a decade"))
        self.statute()
        self.process()
        self.burden()

    def statute(self):
        text = history_card(1914, r"the Clayton Act, \ section 7 \ (as amended in 1950)", r"no person shall acquire "
                            r"\ldots\ the stock or \ldots\ the assets of another \ldots\ where in any line of "
                            r"commerce \ldots\ in any section of the country, \ the effect of such acquisition "
                            r"\textbf{may be substantially to lessen competition, \ or to tend to create a "
                            r"monopoly}", color=GOV, width=11.8, font_size=23).to_edge(UP, buff=0.5)
        words = VGroup(
            label(r"`may be': \ a prediction, \ made before the harm", font_size=23, color=SIM),
            label(r"`line of commerce': \ a product market", font_size=23, color=ALDER),
            label(r"`section of the country': \ a geographic market", font_size=23, color=CEDAR),
            label(r"`substantially to lessen competition': \ higher prices, \ worse quality, \ less innovation",
                  font_size=23, color=CARTEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(text, DOWN, buff=0.55)
        tag = published_tag(r"15 U.S.C. \S\ 18", corner=DL, font_size=12)
        with self.voiceover(
            "American merger law rests on one sentence, section seven of the Clayton Act of 1914, amended in 1950 to "
            "reach purchases of assets as well as shares. No one may acquire another firm where, in any line of "
            "commerce in any section of the country, the effect may be substantially to lessen competition, or to "
            "tend to create a monopoly. <bookmark mark='a'/> May be: the law asks for a prediction, made before "
            "any harm is done, which is why economists are needed at all. <bookmark mark='b'/> Line of commerce: a "
            "product market. <bookmark mark='c'/> Section of the country: a geographic one. <bookmark mark='d'/> "
            "And substantially to lessen competition: in practice, to raise prices, or to lower quality or "
            "innovation, for the buyers in that market. That last reading is the consumer-welfare standard of Part "
            "forty-four, and most of the arguments in this part are about how to measure it."
        ) as vo:
            self.play(FadeIn(text, shift=UP * 0.1), FadeIn(tag))
            for mk, r_ in zip("abcd", words):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def process(self):
        steps = flow_chain([(r"the deal \\ is signed", WHITE), (r"filing; \\ 30 days' wait", GOV),
                            (r"a second \\ request", GOV), (r"clear, settle \\ or sue", E.ACCENT),
                            (r"a federal \\ judge decides", DEF)], box_w=2.1, box_h=1.1, buff=0.45, font_size=20,
                           notes=[r"most deals \\ are small", r"Hart-Scott-Rodino \\ (1976)",
                                  r"documents, \\ data, \\ months", r"settle: \\ sell stores \\ or plants",
                                  r"an injunction, \\ or not"], note_size=16).scale(0.98).move_to(UP * 0.6)
        eu = label(r"in the European Union the Commission decides itself, \ subject to appeal; \ in Britain the "
                   r"Competition and Markets Authority", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"how an American merger is reviewed", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = published_tag(r"Hart-Scott-Rodino Antitrust Improvements Act of 1976", corner=DL, font_size=12)
        with self.voiceover(
            "How does a case proceed? <bookmark mark='a'/> Two firms sign a deal. <bookmark mark='b'/> If it is "
            "large enough, the Hart-Scott-Rodino Act of 1976 requires them to tell the Federal Trade Commission "
            "and the Justice Department, and to wait thirty days before closing. <bookmark mark='c'/> Most deals "
            "are cleared. For the few that worry the agency, it issues a second request: documents, data, and "
            "months of economists' work on both sides. <bookmark mark='d'/> Then the agency clears the deal, "
            "settles, usually by making the firms sell stores or plants where they overlap, or sues. <bookmark "
            "mark='e'/> A suit goes to a federal judge, who decides whether to block it; many firms give up rather "
            "than wait. <bookmark mark='f'/> In the European Union the Commission decides for itself, subject to "
            "appeal to the courts, and Britain's Competition and Markets Authority does the same. Either way, "
            "the economics is argued before someone who is not an economist."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k], shift=RIGHT * 0.1), FadeIn(steps.notes[k])]
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(eu))
        self.clear_scene()

    def burden(self):
        cards = point_cards([
            (r"1. \ the plaintiff's case", r"a market, \ shares in it, \ and a big enough rise in concentration: "
             r"\ harm is presumed", GOV),
            (r"2. \ the defence's rebuttal", r"entry is easy, \ the shares mislead, \ the savings are real, \ the "
             r"target was failing", DEF),
            (r"3. \ the ultimate burden", r"stays with the plaintiff: \ will this merger, \ more likely than not, "
             r"\ lessen competition substantially?", E.ACCENT),
        ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.1)
        head = label(r"who must prove what", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        pnb = history_card(1963, r"United States v. Philadelphia National Bank", r"a merger giving one firm "
                           r"\textbf{30\%} of a market, \ with a significant rise in concentration, \ is presumed "
                           r"unlawful", color=GOV, width=9.6, font_size=20).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"374 U.S. 321 (1963); \ United States v. Baker Hughes, 908 F.2d 981 (D.C. Cir. 1990)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "In court the burden moves in three steps. <bookmark mark='a'/> The plaintiff, the agency, defines a "
            "market and shows the merging firms' shares in it. If concentration is high and rises enough, harm is "
            "presumed. <bookmark mark='b'/> The defence then rebuts: entry is easy, shares mislead in this market, "
            "the cost savings are real, or the firm being bought was failing. <bookmark mark='c'/> And the final "
            "burden stays with the plaintiff: will this merger, more likely than not, substantially lessen "
            "competition? <bookmark mark='d'/> The presumption is old. In 1963, in the Philadelphia National Bank "
            "case, the Supreme Court held that a merger giving one firm thirty percent of a market, with a "
            "significant rise in concentration, is presumed unlawful. Every step of that ladder needs a market, "
            "which is where the economics starts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(cards.animate.shift(UP * 0.7), FadeIn(pnb, shift=UP * 0.1))
        self.clear_scene()
