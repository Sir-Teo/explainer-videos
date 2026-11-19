from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


class Models(VoiceoverScene):
    def construct(self):
        card(self, 8, r"What a model is", r"What is a model for, if it is wrong on purpose?",
             "Chapter eight. What a model is.", scale=("market",), horizon=("a year",))
        self.maps()
        self.pit_model()
        self.judging()
        self.is_ought()

    # ------------------------------------------------------------------
    def maps(self):
        big = island_shape(13.6, 7.4, seed=9).set_opacity(0.9)
        mid = island_shape(3.6, 1.9, seed=9)
        small = Dot(radius=0.06, color="#C9B38A")
        labels = VGroup(label(r"1 : 1", font_size=30, color=WHITE), label(r"1 : 100{,}000", font_size=30, color=WHITE),
                        label(r"1 : 100{,}000{,}000", font_size=30, color=WHITE))
        mid_g = VGroup(mid, palm(0.6).move_to(mid.get_center() + RIGHT * 0.5),
                       islander("crusoe", 0.35).move_to(mid.get_center() + LEFT * 0.3)).move_to(ORIGIN)
        trio = VGroup(VGroup(big.copy().scale(0.25), labels[0].copy()).arrange(DOWN, buff=0.25),
                      VGroup(mid_g.copy(), labels[1].copy()).arrange(DOWN, buff=0.25),
                      VGroup(small.copy(), labels[2].copy()).arrange(DOWN, buff=0.25)).arrange(RIGHT, buff=1.4)
        quote = label(r"Borges, 1946: \ a map of the Empire ``whose size was that of the Empire''", font_size=28,
                      color=E.ACCENT).to_edge(DOWN, buff=0.6)
        quote.add_background_rectangle(color=BACKGROUND, opacity=0.88, buff=0.18)  # readable over the map's sand
        with self.voiceover(
            "We've used a lot of models already: a pit market, an island, a tin market. Every one of them was "
            "wrong. That's on purpose. <bookmark mark='a'/> In a story of 1946, Jorge Luis Borges described an "
            "empire whose map makers grew so exact that they drew a map of the Empire whose size was that of the "
            "Empire, and coincided with it point for point. The generations that followed saw that the vast map was "
            "useless, and abandoned it to the sun and the winters. <bookmark mark='b'/> A map is useful because of what it leaves out. At the scale "
            "of one to one you learn nothing. At a scale too small you see only a dot. <bookmark mark='c'/> The "
            "right scale depends on the question. A model in economics is a map in exactly this sense: it is "
            "wrong on purpose, and the skill is choosing what to leave out."
        ) as vo:
            self.play(FadeIn(big), FadeIn(quote))
            vo.wait_until("b")
            self.play(FadeOut(big), FadeIn(trio, lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(trio[1], color=E.ACCENT, scale_factor=1.05))
        self.clear_scene()

    def pit_model(self):
        kept = point_cards([
            (r"kept", r"each person trades one unit; \ each knows only their own card; \ deals are called out to "
             r"everyone; \ the same cards each period", E.ACCENT),
            (r"left out", r"names and faces; \ haggling, trust, fatigue; \ what the thing is; \ the weather", GREY_B),
            (r"which mattered?", r"the rules: \ calling out to everyone made prices converge (Chamberlin and Smith); "
             r"\ intelligence: \ random traders still captured most of the gains (Gode and Sunder)", E.AGORA),
        ], width=12.6, cols=3, font_size=23).move_to(UP * 0.2)
        head = heading(r"The pit, as a model")
        bottom = label(r"you find out which assumptions matter \ by changing them, \ one at a time", font_size=28,
                       color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Take the model we began with. <bookmark mark='a'/> It kept a handful of things: one unit each, private "
            "cards, bids and offers called out to everyone, the same cards each period. <bookmark mark='b'/> It "
            "left out almost everything else: who the people were, whether they trusted each other, what the thing "
            "being traded even was. <bookmark mark='c'/> Which assumptions mattered? We found out by changing "
            "them. When the deals were made in private pairs, as in Chamberlin's room, the prices scattered. When "
            "the traders were replaced by random number generators, the prices never settled, but most of the "
            "gains were still made. <bookmark mark='d'/> That is the method of this series: build the smallest "
            "model that produces the thing you see, then change one assumption at a time and watch what breaks."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abc", kept.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(bottom, shift=UP * 0.1))
        self.clear_scene()

    def judging(self):
        fr = history_card(1953, r"Milton Friedman, \ ``The Methodology of Positive Economics''",
                          r"judge a model by its predictions: \ an expert billiard player shoots as if he knew the "
                          r"equations of mechanics, \ though he has never seen them", color=E.DEMAND, width=6.1,
                          font_size=23)
        ro = history_card(2015, r"Dani Rodrik, \ \emph{Economics Rules}",
                          r"economics is a collection of models, \ each true of some situations and false of others; "
                          r"\ the skill is knowing which one applies", color=E.SUPPLY, width=6.1, font_size=23)
        VGroup(fr, ro).arrange(RIGHT, buff=0.5, aligned_edge=UP).to_edge(UP, buff=0.6)
        mid = label(r"and a model that predicts well can still mislead \ when the world it describes changes "
                    r"(Part 4)", font_size=26, color=GREY_A).next_to(VGroup(fr, ro), DOWN, buff=0.7)
        with self.voiceover(
            "How should a model be judged, if its assumptions are false by design? <bookmark mark='a'/> In 1953 "
            "Milton Friedman argued: by its predictions, and by nothing else. An expert billiard player makes his "
            "shots as if he knew the complicated formulas of mechanics, though he has never seen them, and a "
            "theory that assumes he knows them predicts his shots very well. <bookmark mark='b'/> Dani Rodrik, "
            "sixty years later, put it differently. Economics is not one model but a library of them, each true "
            "of some situations and false of others, and the skill of an economist is knowing which one fits the "
            "case in front of them. <bookmark mark='c'/> Both are right, with a warning attached: a model that "
            "predicts well in one world can mislead when the world changes, and sometimes the model's own use "
            "is what changes it. That's a story for Part four."
        ) as vo:
            self.play(FadeIn(fr, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ro, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(mid))
        self.clear_scene()

    def is_ought(self):
        hume = history_card(1740, r"David Hume, \ \emph{A Treatise of Human Nature}, Book III",
                            r"no ``ought'' follows from ``is'' alone", color=E.OUGHT, width=7.2, font_size=24)
        hume.to_edge(UP, buff=0.4)
        io = is_ought_card(r"in the standard model, a ceiling on rents below the market price lowers rents for "
                           r"those who keep their homes, \ and fewer homes are offered to rent (checked against "
                           r"evidence in Part 37)",
                           r"cap rents in this city",
                           r"how much weight to give sitting tenants against people still looking for a home, \ "
                           r"and against landlords", width=12.0, font_size=24).next_to(hume, DOWN, buff=0.4)
        rule = label(r"the series marks this step with this card, \ every time", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One more distinction, and the series will be strict about it. <bookmark mark='a'/> In 1740 David Hume "
            "pointed out that no statement about what ought to be done follows from statements about what is, on "
            "their own. You always need a value judgment in between. <bookmark mark='b'/> Economists call the first "
            "kind of claim positive and the second normative. Here is an example. Is: in the standard model, a "
            "ceiling on rents below the market price lowers the rent for people who keep their homes, and fewer "
            "homes are offered to rent; Part thirty-seven checks that against the evidence. "
            "<bookmark mark='c'/> Ought: cap rents in this city. <bookmark mark='d'/> To get from one to the "
            "other you need a judgment that no model supplies: how much weight to give the sitting tenants, against "
            "the people still looking for a home, and against the landlords. <bookmark mark='e'/> Whenever this "
            "series makes that step, it will show this card, and name the judgment."
        ) as vo:
            self.play(FadeIn(hume, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(io.card), FadeIn(io.is_row))
            vo.wait_until("c")
            self.play(FadeIn(io.ought), FadeIn(io[1][3]))
            vo.wait_until("d")
            self.play(FadeIn(io.judgment), FadeIn(io[1][1]))
            vo.wait_until("e")
            self.play(FadeIn(rule))
        self.clear_scene()
