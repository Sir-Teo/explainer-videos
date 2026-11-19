from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.purdue()
        self.question()
        self.title()
        self.pipes()
        self.objectives()

    # ------------------------------------------------------------------
    def purdue(self):
        call = calls.CALLS["smith_1956"]
        when = history_card(r"autumn 1955", r"Vernon Smith, 28, Purdue University",
                            r"teaching his first course in the principles of economics", color=E.DEMAND, width=6.6,
                            font_size=26).to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.6)
        ask = quote_card(r"Why/how could any market approximate a competitive equilibrium?",
                         r"Vernon Smith, looking back (Nobel autobiography, 2002)", width=6.2, font_size=28,
                         color=E.DEMAND).next_to(when, DOWN, buff=0.4).align_to(when, LEFT)
        plan = quote_card(r"\dots if you were going to show that the competitive model did not work, then you "
                          r"should choose a more competitive trading procedure, so that when the competitive model "
                          r"failed to predict the outcomes, you would have a stronger case than had been made by "
                          r"Chamberlin.", r"Smith (2002)", width=6.3, font_size=24, color=E.PRED)
        plan.to_edge(UP, buff=0.45).to_edge(RIGHT, buff=0.5)
        src = published_tag(r"V. L. Smith, autobiography, Nobel Prize in Economic Sciences 2002", corner=DR,
                            font_size=17)
        with self.voiceover(
            "In the autumn of 1955, a young economist named Vernon Smith began teaching his first course, the "
            "principles of economics, at Purdue University in Indiana. <bookmark mark='a'/> He found it hard to "
            "convey the theory to his students, and he had a doubt of his own. Why, he asked himself, or how, could "
            "any market approximate a competitive equilibrium? <bookmark mark='b'/> He decided to run an "
            "experiment on the first day of the next semester. He knew Edward Chamberlin's classroom market from "
            "Harvard, where the prices had come out scattered and wrong. And he planned to give the textbook theory "
            "its fairest chance, so that when it failed, as he expected it to, the case against it would be "
            "stronger than Chamberlin's."
        ) as vo:
            self.play(FadeIn(when, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(ask, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(plan, shift=LEFT * 0.2))
        self.wait(0.4)
        jan = history_card(r"January 1956", r"the first session", r"22 students, each with one private card",
                           color=E.ACCENT, width=5.6, font_size=26)
        amazed = quote_card(r"To my amazement the experimental market converged `quickly' to near the predicted "
                            r"equilibrium price and exchange volume \dots", r"Smith (2002)", width=7.4,
                            font_size=28, color=E.ACCENT)
        VGroup(jan, amazed).arrange(RIGHT, buff=0.5, aligned_edge=UP).to_edge(UP, buff=0.6)
        cc = call_card(r"Vernon Smith", call.when, r"the competitive model will fail to predict the price",
                       r"\dots", r"too early to say", width=10.6, font_size=24).to_edge(DOWN, buff=0.55)
        later = label(r"scored in chapter 5", font_size=24, color=E.PRED).move_to(cc.stamp)
        with self.voiceover(
            "In January 1956 he carried out his plan, with twenty-two students who knew nothing but their own "
            "cards. <bookmark mark='a'/> To his amazement, he wrote, the market converged quickly, to near the "
            "price and the quantity the theory predicted. <bookmark mark='b'/> He had made a prediction, and the "
            "series keeps score of predictions. We'll score this one when we've seen why it came out the way it "
            "did, and whether it was a fluke."
        ) as vo:
            self.play(FadeOut(when), FadeOut(ask), FadeOut(plan), FadeIn(jan, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(amazed, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(later))
        self.clear_scene()

    def question(self):
        q = label(r"What sets a price?", font_size=76, color=E.ACCENT).to_edge(UP, buff=0.8)
        drop = drop_glyph(1.5).move_to(LEFT * 3.4 + DOWN * 0.4)
        gem = gem_glyph(1.9).move_to(RIGHT * 3.4 + DOWN * 0.4)
        wl = label(r"water: \ nothing more useful, \ nearly free", font_size=28, color=WATER).next_to(drop, DOWN,
                                                                                                     buff=0.45)
        gl = label(r"diamonds: \ nearly useless, \ dear", font_size=28, color=DIAMOND).next_to(gem, DOWN, buff=0.45)
        cost = label(r"cost of making it?", font_size=30, color=E.SUPPLY)
        use = label(r"how useful it is?", font_size=30, color=E.DEMAND)
        VGroup(cost, use).arrange(RIGHT, buff=2.6).move_to(DOWN * 0.4)
        logo = scissors_logo(1.3).move_to(DOWN * 0.4)
        with self.voiceover(
            "This part is about one question: what sets a price? <bookmark mark='a'/> For a century it was a "
            "puzzle. Nothing is more useful than water, and it's nearly free. A diamond is nearly useless, and it's "
            "dear. <bookmark mark='b'/> Is a price set by what a thing costs to make, or by how useful it is? "
            "Economists argued about that for a hundred years. <bookmark mark='c'/> The answer, when it came, was "
            "both, at the margin, and an English economist named Alfred Marshall drew it as a pair of scissors."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(drop), FadeIn(wl))
            self.play(FadeIn(gem), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeOut(drop), FadeOut(gem), FadeOut(wl), FadeOut(gl), FadeIn(cost, shift=RIGHT * 0.2),
                      FadeIn(use, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(cost.animate.next_to(logo, LEFT, buff=0.8), use.animate.next_to(logo, RIGHT, buff=0.8))
            self.play(Create(logo.demand), Create(logo.supply), run_time=1.2)
            self.play(FadeIn(logo.price, scale=0.3))
        self.clear_scene()

    def title(self):
        logo = scissors_logo(1.5)
        t = label(SERIES_EN, font_size=72)
        sub = label(r"Part 2 \ \textperiodcentered\ \ The Scissors", font_size=40, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part two: the scissors."):
            self.play(Create(logo.demand), Create(logo.supply), run_time=1.2)
            self.play(FadeIn(logo.price, scale=0.3), Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(0.8)
        self.clear_scene()

    def pipes(self):
        sealed = tableau_map(open_pipes=(), width=12.6, font_size=21).move_to(DOWN * 0.2)
        opened = tableau_map(open_pipes=("spending", "goods"), lit=("households", "firms"), width=12.6,
                             font_size=21).move_to(DOWN * 0.2)
        head = heading(r"The Tableau: \ the first pipes open")
        flows = VGroup(*[flowing(opened.paths[k], c, n=6, period=3.0) for k, c in (("spending", E.HOUSEHOLDS),
                                                                                    ("goods", E.FIRMS))])
        with self.voiceover(
            "Part one drew the economy as plumbing, with every pipe sealed. <bookmark mark='a'/> This part opens "
            "the first two: money flowing from households to firms, and goods and services flowing back. Where the "
            "two flows meet is a market, and in every market there is a price. <bookmark mark='b'/> By the end of "
            "the part you'll know what sets it, what moves it, and what happens when someone tries to hold it "
            "still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sealed))
            vo.wait_until("a")
            self.play(FadeTransform(sealed, opened), run_time=1.5)
            self.add(flows)
            vo.wait_until("b")
            self.wait(1.0)
        for f in flows:
            f.clear_updaters()
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 2", font_size=34, color=GREY_B), label(r"The Scissors", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why water is cheap and diamonds dear: \ value at the margin",
            r"demand built from buyers' cards, \ supply from sellers' costs, \ and the price where they cross",
            r"play a lopsided market, \ and test whether traders with no intelligence find its price",
            r"elasticity, \ and a frost in Brazil that moved the price of coffee fivefold",
            r"who really pays a tax, \ and what a price control costs, \ in the pit and in the data",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Part two: the scissors. <bookmark mark='a'/> We'll start with the puzzle of water and diamonds, and "
            "the idea that solved it: value at the margin. <bookmark mark='b'/> Then we'll build demand from "
            "buyers' cards and supply from sellers' costs, and find where they cross. <bookmark mark='c'/> You'll "
            "play a lopsided market, and we'll test whether traders with no intelligence at all can find its "
            "price. <bookmark mark='d'/> We'll measure how much people respond to a price, and follow a frost in "
            "Brazil that moved the price of coffee fivefold. <bookmark mark='e'/> And we'll work out who really "
            "pays a tax, and what a price control costs, in the pit and in the data."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
