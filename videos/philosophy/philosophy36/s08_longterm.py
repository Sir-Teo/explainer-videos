from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Longterm(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"The long future", r"Does the far future dominate what we should do now?",
                            lit=(2020, 2021), part=PART)
        with self.voiceover("Chapter seven. The long future."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.case()
        self.three()
        self.perils()
        self.critics()

    def case(self):
        head = label(r"The case for longtermism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the argument", r"if the future could hold vastly more lives than the present, \ and we can affect "
                                  r"its course, \ the best acts are those with the best long-run effects \ (Greaves "
                                  r"and MacAskill, \ 2021)", FUT),
                (r"existential risk", r"a catastrophe that ends humanity, \ or permanently curtails its potential, \ "
                                      r"would lose all of that \ (Bostrom, \ 2002)", RISK),
                (r"an estimate, \ labelled", r"Ord's \textit{The Precipice} \ (2020): \ about 1 in 6 that such a "
                                             r"catastrophe happens this century: \ one author's subjective judgment", MONEY),
                (r"the lever", r"total view plus large numbers: \ tiny changes in risk carry enormous expected value",
                 WELL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.2, x_text=-2.0, label_size=20, text_size=19)
        with self.voiceover(
            "Combine the total view with the size of the possible future, and a striking thesis follows. "
            "<bookmark mark='a'/>Hilary Greaves and William MacAskill called it strong longtermism, in 2021: if the "
            "future could hold vastly more lives than the present, and we can affect its course, then the best acts "
            "available to us are, in large part, those with the best effects on the very long run. "
            "<bookmark mark='b'/>The clearest case is existential risk, Nick Bostrom's term for a catastrophe that "
            "ends humanity or permanently curtails its potential. <bookmark mark='c'/>How large is it? Toby Ord, in The "
            "Precipice of 2020, put the chance of such a catastrophe this century at about one in six. That is one "
            "author's considered judgment, not a measurement, and others put it far lower. "
            "<bookmark mark='d'/>The lever is arithmetic: with the total view and a future this large, even tiny "
            "changes in risk carry enormous expected value. Whether they do depends on more than the size of the "
            "future, as the Reasoner shows next."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def three(self):
        d = load("three")
        head = label(r"Parfit's three outcomes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pa, tt = d["person_affecting"], d["total"]
        assert (d["present"], d["future"]) == (8e9, 1e16)
        assert (pa["ratio_23_12"], tt["ratio_23_12"]) == (0.0101, 1262626.0)
        rows = stack([(r"(1) \ peace", WELL), (r"(2) \ a nuclear war that kills 99\% of the world's existing "
                                                r"population", RISK),
                      (r"(3) \ a nuclear war that kills 100\%", BAD)],
                     font_size=21, aligned_edge=LEFT, buff=0.2).move_to([-2.0, 1.7, 0])
        q = label(r"which difference is greater: \ (1) to (2), \ or (2) to (3)?", font_size=21, color=GOAL).next_to(
            rows, DOWN, buff=0.3).align_to(rows, LEFT)
        hd = [r"\text{counting}", r"\text{(1) to (2)}", r"\text{(2) to (3)}", r"\text{ratio}"]
        cells = [[label(r"existing people only", font_size=18, color=POP), MathTex(r"7.92 \times 10^{9}", font_size=26),
                  MathTex(r"8 \times 10^{7}", font_size=26), label(r"0.01", font_size=19, color=POP)],
                 [label(r"the future too: \ $10^{16}$ lives", font_size=18, color=FUT),
                  MathTex(r"7.92 \times 10^{9}", font_size=26), MathTex(r"\approx 10^{16}", font_size=26),
                  label(r"1.3 million", font_size=19, color=FUT)]]
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.4, 2.4, 2.0], cell_h=0.62, font_size=17).move_to([0, -1.1, 0])
        foot = label(r"lives lost; \ after (2) humanity recovers; \ $10^{16}$: \ Bostrom's conservative figure for "
                     r"lives on Earth alone", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Parfit's sentence from the opening of this part came with an example. <bookmark mark='a'/>Compare three "
            "outcomes: peace; a nuclear war that kills ninety nine percent of the world's existing population; and a "
            "nuclear war that kills a hundred percent. <bookmark mark='b'/>Most people think the greater difference "
            "is between peace and the first war. Parfit thought the difference between the two wars is very much "
            "greater. <bookmark mark='c'/>The Reasoner counts lives lost. Counting only existing people, the first "
            "step costs seven point nine two billion lives and the second eighty million: the second is a hundredth "
            "of the first. <bookmark mark='d'/>Counting the future too, with Nick Bostrom's conservative figure of "
            "ten to the sixteen lives that Earth alone could support, the second step loses all of it: about one "
            "point three million times the first. <bookmark mark='e'/>Which answer is right is the whole question of "
            "this part: whether the lives that would have been lived count."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]], FadeIn(foot))
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("e")
            self.wait(0.5)
        self.clear_scene()

    def perils(self):
        d = load("xrisk")
        head = label(r"What is a point of risk worth? \ (Thorstad, \ 2023)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (round(d["risk"], 4), d["low"], d["cut"]) == (0.1667, 0.0001, 0.01)
        assert (d["constant_gain"], d["closed_constant"], d["perils_gain"], d["closed_perils"]) == (0.06, 0.06, 100.0,
                                                                                                   100.0)
        assert (d["future_constant"], d["future_perils"]) == (5.0, 8333.0)
        f1 = MathTex(r"V \;=\; v\,(1 - r_1)\Big(1 + (1-r) + (1-r)^2 + \cdots\Big) \;=\; \frac{v\,(1 - r_1)}{r}",
                     font_size=32, color=FUT).move_to([0, 2.0, 0])
        f2 = MathTex(r"\Delta V \;=\; \frac{v\,\Delta r_1}{r}", font_size=34, color=GOAL).next_to(f1, DOWN, buff=0.3)
        hd = [r"\text{risk after this century}", r"\text{expected future}", r"\text{one point less risk now}"]
        cells = [[label(r"stays at 1 in 6", font_size=18, color=RISK), label(r"5.0 centuries", font_size=18),
                  label(r"0.06 of a century", font_size=18, color=RISK)],
                 [label(r"falls to 1 in 10,000", font_size=18, color=WELL), label(r"8333 centuries", font_size=18),
                  label(r"100 centuries", font_size=18, color=WELL)]]
        grid = ValueGrid(hd, cells, col_w=[3.6, 3.0, 3.6], cell_h=0.56, font_size=17).move_to([0, -0.5, 0])
        foot = stack([(r"$v$: \ the value of one century; \ $r_1$: \ this century's risk; \ $r$: \ each later "
                       r"century's", GREY_A),
                      (r"summed to 100,000 centuries, \ and checked against the closed form", GREY_A),
                      (r"the value depends on the time of perils ending, \ not only on how big the future could be",
                       GOAL)], font_size=18, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "David Thorstad showed in 2023 that the answer turns on a hidden assumption. <bookmark mark='a'/>Measure "
            "value in centuries of civilization like ours, v each. If this century's risk of extinction is r one, and "
            "every later century's is r, the expected value of the future is a geometric series: v times one minus r "
            "one, over r. <bookmark mark='b'/>So cutting this century's risk by delta r one adds v delta r one over r: "
            "the gain is divided by the risk in all later centuries. <bookmark mark='c'/>If the risk stays at one in "
            "six, the expected future is only five centuries, and cutting this century's risk by a full percentage "
            "point is worth six hundredths of a century. <bookmark mark='d'/>If instead we are in a time of perils, "
            "after which risk falls to one in ten thousand, the expected future is eight thousand centuries, and the "
            "same cut is worth a hundred. <bookmark mark='e'/>The Reasoner sums the series to a hundred thousand "
            "centuries and matches the formula. The astronomical value of reducing risk requires not only a vast "
            "possible future, but a reason to think the dangerous period will end."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("e")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()

    def critics(self):
        head = label(r"Objections", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"cluelessness", r"Greaves \ (2016): \ the long-run effects of almost any act are unknowable, \ and "
                                  r"may swamp the short-run ones in either direction", GREY_A),
                (r"washing out", r"Tarsney \ (2023): \ our ability to predict decays with time; \ whether "
                                 r"longtermism survives depends on how fast", FUT),
                (r"population ethics", r"on person-affecting or average views, \ merely possible future people "
                                       r"carry far less weight", POP),
                (r"fanaticism", r"tiny probabilities of astronomical value can dominate every decision: \ the next "
                                r"chapter", RISK)]
        g = rows_table(rows, top=1.6, gap=0.48, width=8.2, x_text=-2.0)
        with self.voiceover(
            "Longtermism has serious critics. <bookmark mark='a'/>Hilary Greaves herself described cluelessness in "
            "2016: the long-run effects of almost anything we do are unknowable, and they may swamp the short-run "
            "effects in either direction. <bookmark mark='b'/>Christian Tarsney studied in 2023 how our ability to "
            "predict decays with time; whether longtermism survives depends on how fast. "
            "<bookmark mark='c'/>On person-affecting or average views, the merely possible people of the future carry "
            "far less weight. <bookmark mark='d'/>And the argument leans on tiny probabilities of astronomical value, "
            "which can dominate every decision. That is the problem of fanaticism, the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
