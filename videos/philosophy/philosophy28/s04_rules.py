from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Rules(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Following a rule", r"What fact makes `plus' mean addition?", lit=(1953, 1982),
                            part=PART)
        with self.voiceover("Chapter three. Following a rule."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.quus()
        self.sceptic()
        self.solution()
        self.wall_brick()

    def quus(self):
        d = load("quus")
        head = label(r"Plus and quus", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = VGroup(MathTex(r"x + y", font_size=32, color=WORD),
                      MathTex(r"x \oplus y = \begin{cases} x + y & \text{if } x, y < 57 \\ 5 & \text{otherwise} "
                              r"\end{cases}", font_size=32, color=BAD)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(
            [3.6, 1.6, 0])
        step = d["grid_step"]
        grid = d["grid"]
        n = len(grid)
        size = 0.2
        o = np.array([-6.0, -2.8, 0])
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                cells.add(Square(size, stroke_width=0, fill_color=OK if grid[i][j] else BAD, fill_opacity=0.75).move_to(
                    o + np.array([(i + 0.5) * size * 1.05, (j + 0.5) * size * 1.05, 0])))
        side_len = n * size * 1.05
        xl = label(r"$x$, \ 0 to 76", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.1)
        yl = label(r"$y$", font_size=17, color=GREY_A).next_to(cells, LEFT, buff=0.1)
        line57 = DashedLine(o + np.array([57 / step * size * 1.05, 0, 0]), o + np.array([57 / step * size * 1.05,
                                                                                      side_len, 0]), color=TRUTH)
        assert d["agree"] == d["history"] == 1000 and d["biggest"] == 56
        assert d["plus_68_57"] == 125 and d["quus_68_57"] == 5
        rows = stack([(r"green: \ plus and quus agree; \ red: \ they differ", WHITE),
                      (r"your record: \ 1000 sums, \ every number below 57: \ the two agree on all 1000", OK),
                      (r"$68 + 57 = 125$; \ \ $68 \oplus 57 = 5$", BAD)], font_size=21, aligned_edge=LEFT, width=6.4,
                     buff=0.3).move_to([3.6, -1.2, 0])
        with self.voiceover(
            "Saul Kripke's book of 1982 drew from Wittgenstein's remarks on rules a paradox he called the most radical "
            "and original sceptical problem that philosophy has seen. <bookmark mark='a'/>Define a function, quus. For "
            "numbers below fifty-seven, quus is just plus. For anything else, the answer is five. "
            "<bookmark mark='b'/>Here are all the pairs up to seventy-six, green where plus and quus agree, red where "
            "they differ. <bookmark mark='c'/>Suppose every sum you have ever done involved numbers below fifty-seven. "
            "The Reasoner makes a record of a thousand such sums: plus and quus agree on all of them. "
            "<bookmark mark='d'/>Now you are asked for sixty-eight plus fifty-seven, for the first time. You answer one "
            "hundred and twenty-five. But what makes that the answer that accords with what you meant before, rather "
            "than five?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defs[0]))
            self.play(Write(defs[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.002), FadeIn(xl), FadeIn(yl), run_time=2)
            self.play(Create(line57), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def sceptic(self):
        d = load("quus")
        head = label(r"The sceptic's challenge", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"past use", r"finite: \ every sum you did fits plus and quus alike", WORD),
            (r"rival rules", rf"for every bound $b$ from 57 to 199, \ `quus$_b$' fits your record too: \ "
                             rf"{d['rival_bounds_below_200']} rivals, \ and infinitely many beyond", BAD),
            (r"inner states", r"an image, \ a feeling, \ an instruction to `count': \ each needs interpreting in turn", RULE_C),
            (r"dispositions", r"what you \textit{would} answer: \ finite too, \ and includes mistakes; \ it says what you "
                              r"do, \ not what you \textit{should} do", USE),
            (r"the conclusion", r"there is no fact about you that makes `plus' mean addition rather than quus", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        assert d["rival_bounds_below_200"] == 143
        with self.voiceover(
            "The sceptic asks for a fact, any fact, that makes it true that you meant plus. <bookmark mark='a'/>Not "
            "your past use: it is finite, and fits both. <bookmark mark='b'/>Worse, for every bound from fifty-seven "
            "up, there is a rival rule like quus that fits your record. The Reasoner counts a hundred and forty-three "
            "below two hundred, and there are infinitely many beyond. <bookmark mark='c'/>Not anything in your mind: "
            "an image, a feeling, an instruction to count, each needs interpreting in its turn, and could be "
            "interpreted quus-wise. <bookmark mark='d'/>Not your dispositions, what you would answer: they are finite "
            "too, they include mistakes, and they tell what you would do, not what you ought to do. Meaning is "
            "normative. <bookmark mark='e'/>So, the sceptic concludes, there is no fact about you that makes plus mean "
            "addition. And the argument generalizes to every word."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def solution(self):
        head = label(r"The sceptical solution", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"concede", r"no fact makes `Jones means plus' true, \ in the way the sceptic demands", BAD),
            (r"assertability", r"we may \textit{say} Jones means plus when his answers agree with ours, \ often enough",
             WORD),
            (r"the role", r"such talk lets us trust Jones as a cashier, \ a carpenter, \ a colleague", USE),
            (r"the community", r"so meaning lives in shared practice: \ a person considered in isolation cannot follow a "
                               r"rule", HEAR),
            (r"the critics", r"Kripke's reading is `Kripkenstein': \ many say Wittgenstein meant the paradox as a "
                             r"\textit{reductio} \ (\S 201)", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Kripke offered what he called a sceptical solution. <bookmark mark='a'/>Concede the sceptic's point: no "
            "fact makes it true that Jones means plus, in the sense the sceptic demands. <bookmark mark='b'/>But look "
            "at when we are entitled to say it. We say Jones means plus when his answers agree with ours, often "
            "enough. <bookmark mark='c'/>And look at what the saying does: it lets us trust Jones at the shop till, in "
            "the workshop, in the laboratory. <bookmark mark='d'/>So meaning lives in a community's shared practice. "
            "A person considered in isolation, with no community to agree with, cannot be said to follow a rule. "
            "<bookmark mark='e'/>Many readers call this view Kripkenstein: neither Kripke's own nor clearly "
            "Wittgenstein's. Section 201 of the Investigations states the paradox, then says it rests on a "
            "misunderstanding: there is a way of grasping a rule which is not an interpretation."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=28, current=28).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(28, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twenty-eighth brick in the Wall. <bookmark mark='a'/>The dream was a fact that fixes what a "
            "rule means: something in the speaker, her history or her mind, that settles every future case. The "
            "rule-following paradox says no such fact can do the job. <bookmark mark='b'/>The way through is meaning "
            "located in community and use, with all the questions that raises about who counts as the community, and "
            "what agreement can and cannot settle."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[28], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
