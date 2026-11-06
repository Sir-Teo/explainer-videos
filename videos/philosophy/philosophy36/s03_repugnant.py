from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Repugnant(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The repugnant conclusion", r"Can numbers make up for quality?", lit=(1984,),
                            part=PART)
        with self.voiceover("Chapter two. The repugnant conclusion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bars()
        self.statement()
        self.scope()
        self.responses()

    def bars(self):
        d = load("sequence")
        rows = d["rows"]
        head = label(r"From A to Z", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert [r["name"] for r in rows[:5]] == list("ABCDE") and rows[-1]["name"] == "Z"
        base = -2.3
        blocks, names = VGroup(), VGroup()
        x = -6.6
        for r in rows[:5]:
            b = parfit_bars([(r["n"], r["w"])], x, base, unit_w=0.17, unit_h=0.042, color=WELL)
            blocks.add(b)
            names.add(label(r["name"], font_size=20, color=GOAL).next_to(b, DOWN, buff=0.15))
            x += b.width + 0.35
        dots = label(r"$\dots$", font_size=30, color=GREY_A).move_to([x + 0.3, base + 0.3, 0])
        z_left = x + 0.9
        z = Rectangle(width=6.6 - z_left, height=0.042 * rows[-1]["w"] + 0.02, stroke_width=1, stroke_color=POP,
                      fill_color=POP, fill_opacity=0.85)
        z.move_to([(z_left + 6.6) / 2, base + z.height / 2, 0])
        zl = label(r"Z: \ 1024 times the people, \ each at 0.25: \ off the edge of the screen", font_size=17,
                   color=POP).next_to(z, UP, buff=0.2)
        totals = VGroup(*[label(f"{r['total']:.0f}", font_size=15, color=GREY_A).next_to(b, UP, buff=0.08)
                          for r, b in zip(rows[:5], blocks)])
        tz = label(f"total {rows[-1]['total']:.0f}", font_size=15, color=GREY_A).next_to(zl, UP, buff=0.1)
        side = stack([(r"each block's area is its total welfare", GREY_A),
                      (r"every step: \ twice as wide, \ 55\% as tall, \ 10\% more area", WELL),
                      (r"by the total view, \ each step is an improvement", WELL)],
                     font_size=19, aligned_edge=LEFT, width=5.6, buff=0.25).move_to([3.4, 2.3, 0])
        with self.voiceover(
            "Parfit followed the sequence to its end. <bookmark mark='a'/>Draw each world as a block, width the "
            "number of people, height their welfare, so that the area is the total. A is ten billion people, all "
            "with a very high quality of life. <bookmark mark='b'/>B is twice as wide and a little more than half as "
            "tall; C twice as wide again; each step adds ten percent to the area. <bookmark mark='c'/>By the total "
            "view each step is an improvement. <bookmark mark='d'/>So after enough steps we reach Z: a population "
            "so large that its block runs off the screen, a thousand and twenty four times as wide as A, and so low "
            "that its lives are barely worth living. Parfit pictured them as lives with nothing in them but muzak and "
            "potatoes. By the total view, Z is better than A."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(blocks[0], DOWN), FadeIn(names[0]), FadeIn(totals[0]), FadeIn(side[0]))
            vo.wait_until("b")
            for b, n, t in zip(blocks[1:], names[1:], totals[1:]):
                self.play(GrowFromEdge(b, DOWN), FadeIn(n), FadeIn(t), run_time=0.7)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dots), GrowFromEdge(z, LEFT), run_time=1.5)
            self.play(FadeIn(zl), FadeIn(tz))
        self.clear_scene()

    def statement(self):
        q = quote_card(r"For any possible population of at least ten billion people, \ all with a very high quality of "
                       r"life, \ there must be some much larger imaginable population whose existence, \ if other "
                       r"things are equal, \ would be better even though its members have lives that are barely worth "
                       r"living.", r"Derek Parfit", r"\textit{Reasons and Persons} \ (1984), \ \S 131", width=10.4,
                       font_size=27).move_to([0, 0.4, 0])
        foot = label(r"Parfit returned to it for the rest of his life: \ ``Can We Avoid the Repugnant Conclusion?'' "
                     r"\ (2016)", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Parfit called this the repugnant conclusion, and stated it carefully. <bookmark mark='a'/>For any "
            "possible population of at least ten billion people, all with a very high quality of life, there must be "
            "some much larger imaginable population whose existence, if other things are equal, would be better, "
            "even though its members have lives that are barely worth living. <bookmark mark='b'/>He thought it "
            "should be avoided, and he returned to the problem for the rest of his life; one of his last papers, in "
            "2016, asked whether we can avoid the repugnant conclusion at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def scope(self):
        d = load("scope")
        head = label(r"Can we trust the intuition? \ Scope insensitivity", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        assert d == {"birds": [2000, 20000, 200000], "dollars": [80, 78, 88]}
        bars = VGroup()
        for k, (n, v) in enumerate(zip(d["birds"], d["dollars"])):
            h = 0.03 * v
            b = Rectangle(width=1.2, height=h, stroke_width=0, fill_color=MONEY, fill_opacity=0.8)
            b.move_to([-5.2 + 2.0 * k, -2.4 + h / 2, 0])
            bars.add(VGroup(b, label(f"\\${v}", font_size=20, color=MONEY).next_to(b, UP, buff=0.12),
                            label(f"{n:,} birds", font_size=18, color=GREY_A).next_to(b, DOWN, buff=0.15)))
        side = stack([(r"Desvousges et al. \ (1993): \ what would you pay to save migrating birds from oil ponds?",
                       GREY_A),
                      (r"a hundredfold change in the good, \ almost no change in the valuation", MONEY),
                      (r"the debunking argument: \ feelings cannot register vast numbers, \ or how good a life just "
                       r"above zero is", WELL),
                      (r"the reply: \ the intuition is about quality, \ not quantity: \ Z lacks everything that makes "
                       r"lives go well", RISK)],
                     font_size=19, aligned_edge=LEFT, width=5.8, buff=0.3).move_to([3.4, -0.2, 0])
        with self.voiceover(
            "Can we trust the intuition against Z? <bookmark mark='a'/>Psychologists have a name for one way it "
            "might mislead: scope insensitivity. In a study by William Desvousges and colleagues, published in 1993, "
            "people were asked what they would pay to save migrating birds from drowning in oil ponds. "
            "<bookmark mark='b'/>Told that two thousand birds were at stake, they offered about eighty dollars on "
            "average; for twenty thousand, seventy eight; for two hundred thousand, eighty eight. A hundredfold change "
            "in the good barely moved the valuation. <bookmark mark='c'/>If our feelings cannot register the "
            "difference between thousands and hundreds of thousands, they may not register what an astronomically "
            "large population of lives just worth living contains. That is the debunking argument of Tännsjö and "
            "Huemer. <bookmark mark='d'/>The reply is that the intuition concerns quality, not quantity: what Z "
            "lacks is everything that makes lives go well, and no count of potatoes supplies it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3),
                      *[FadeIn(VGroup(b[1], b[2])) for b in bars], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def responses(self):
        d = load("vrc")
        head = label(r"Responses, \ and a worse conclusion", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["A"], d["agony"], d["barely"], d["units"]) == (100.0, -50.0, 0.25, 601)
        rows = [(r"accept it", r"Tännsjö \ (2002), \ Huemer \ (2008): \ we cannot imagine huge numbers or the zero "
                               r"level, \ so the intuition is unreliable; \ a joint statement of 2021: \ avoiding it "
                               r"should not be required", WELL),
                (r"reject the total view", r"the average view avoids it, \ at costs computed in chapter four", POP),
                (r"critical levels; \ variable value", r"avoid it too, \ at other costs", RISK),
                (r"the very repugnant conclusion", r"Arrhenius: \ the total view also prefers to A a world with as "
                                                   r"many lives in agony, \ at $-50$, \ plus enough lives at 0.25: \ "
                                                   r"601 times as many", BAD)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.0, x_text=-1.9, label_size=20, text_size=19)
        with self.voiceover(
            "The responses fall into families. <bookmark mark='a'/>Some accept the conclusion. Torbjörn Tännsjö and "
            "Michael Huemer argued that we cannot imagine huge numbers, or how good a life just above zero really is, "
            "so the intuition against Z is unreliable; in 2021, more than two dozen population ethicists signed a "
            "joint statement that avoiding the repugnant conclusion should not be a requirement for an acceptable "
            "theory. <bookmark mark='b'/>Others reject the total view. The average view avoids the conclusion, at "
            "costs we will compute in chapter four. <bookmark mark='c'/>Critical levels and variable value avoid it "
            "too, at other costs. <bookmark mark='d'/>And Gustaf Arrhenius found something worse that the total view "
            "accepts, the very repugnant conclusion. A world in which as many people as in A live in agony, at minus "
            "fifty, is better than A, provided enough lives barely worth living are added. The Reasoner counts how "
            "many: six hundred and one times A's population, at a quarter each."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
