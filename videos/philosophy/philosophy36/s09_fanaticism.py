from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Fanaticism(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Fanaticism", r"Should a tiny chance of an enormous good decide what we do?",
                            lit=(2009, 2022), part=PART)
        with self.voiceover("Chapter eight. Fanaticism."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mugging()
        self.chain()
        self.defence()

    def mugging(self):
        head = label(r"Pascal's mugging \ (Bostrom, \ 2009)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the offer", r"a mugger with no weapon asks for Pascal's wallet, \ and promises in return, \ by "
                               r"magic, \ a thousand quadrillion happy days of life", RISK),
                (r"the credence", r"Pascal thinks it almost certainly false: \ but not as unlikely as one in a "
                                  r"thousand quadrillion", GREY_A),
                (r"the arithmetic", r"so handing over the wallet has positive expected value, \ and an expected-value "
                                    r"maximizer pays", MONEY),
                (r"the escalation", r"whatever Pascal's doubt, \ the mugger can raise the offer faster than the "
                                    r"probability falls", BAD)]
        g = rows_table(rows, top=1.5, gap=0.48, width=8.2, x_text=-2.2)
        with self.voiceover(
            "Nick Bostrom told a story in 2009. <bookmark mark='a'/>A mugger without a weapon approaches Pascal and "
            "asks for his wallet. In return he promises, by magic, an extra thousand quadrillion happy days of life. "
            "<bookmark mark='b'/>Pascal thinks this is almost certainly false; but not, surely, as unlikely as one in "
            "a thousand quadrillion. <bookmark mark='c'/>So the expected value of handing over the wallet is positive, "
            "and a maximizer of expected value must pay. <bookmark mark='d'/>Worse, whatever Pascal's doubt, the "
            "mugger can raise his offer faster than the probability falls. The same structure, small probabilities "
            "and astronomical payoffs, runs through the arguments of the last chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def chain(self):
        d = load("fanatic")
        rows = d["rows"]
        head = label(r"A chain of long shots \ (Beckstead and Thomas)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["peak_bounded"], d["discount_breaks_at"], d["bound"], d["threshold"]) == (3, 10, 1000.0, 0.001)
        assert [r["ev"] for r in rows[:4]] == [1.0, 5.0, 25.0, 125.0] and rows[12]["ev"] == 244140625.0
        show = [rows[k] for k in (0, 1, 2, 3, 4, 6, 8, 9, 10, 12)]
        hd = [r"k", r"\text{chance}", r"\text{prize}", r"\text{expected value}", r"\text{bounded utility}",
              r"\text{ignore chances} < 10^{-3}"]
        cells = []
        for r in show:
            k = r["k"]
            cells.append([label(f"{k}", font_size=16, color=GOAL), MathTex(rf"2^{{-{k}}}", font_size=22, color=GREY_A),
                          MathTex(rf"10^{{{k}}}", font_size=22, color=GREY_A),
                          label(f"{r['ev']:,.0f}", font_size=16, color=MONEY),
                          label(f"{r['bounded']:.4f}", font_size=16, color=WELL if k == 3 else WHITE),
                          label(f"{r['discounted']:,.0f}", font_size=16, color=RISK if k == 10 else WHITE)])
        grid = ValueGrid(hd, cells, col_w=[0.8, 1.6, 1.6, 2.4, 2.4, 3.0], cell_h=0.4, font_size=16).move_to(
            [-1.1, -0.35, 0])
        i3, i10 = [r["k"] for r in show].index(3), [r["k"] for r in show].index(10)
        b3 = SurroundingRectangle(grid.cell[i3][4], buff=0.06, color=WELL, stroke_width=2)
        b10 = SurroundingRectangle(grid.cell[i10][5], buff=0.06, color=RISK, stroke_width=2)
        side = stack([(r"each step: \ half the chance, \ ten times the prize", GREY_A),
                      (r"expected value: \ $\times 5$ a step, \ for ever: \ reckless", MONEY),
                      (r"$u(x) = x / (x + 1000)$: \ peaks at step 3: \ timid", WELL),
                      (r"discounting stops at step 10, \ a step like all the others", RISK),
                      (r"reckless, \ timid, \ or intransitive: \ choose", GOAL)],
                     font_size=17, aligned_edge=LEFT, width=3.4, buff=0.3).move_to([5.3, -0.3, 0])
        with self.voiceover(
            "The Reasoner builds the chain that Nick Beckstead and Teruji Thomas used to make the problem precise. "
            "<bookmark mark='a'/>Lottery zero gives one unit of value for sure. Each next lottery halves the chance "
            "of winning and multiplies the prize by ten. <bookmark mark='b'/>Every step looks like an improvement, "
            "and expected value agrees, multiplying by five each time. By transitivity, a one in four thousand chance "
            "of a trillion beats the sure thing, and the chain never stops: that is recklessness, or fanaticism. "
            "<bookmark mark='c'/>A bounded utility, here x over x plus a thousand, stops climbing: it peaks at the "
            "third lottery and declines after. It is timid: at some step it refuses to trade a small loss of "
            "probability for a vast gain in the prize. <bookmark mark='d'/>Ignoring every chance below one in a "
            "thousand stops abruptly at step ten, a step that looks exactly like the nine before it. "
            "<bookmark mark='e'/>Beckstead and Thomas proved that every theory of choice must be reckless, timid, or "
            "give up transitivity. There is no fourth way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for row in grid.cell for c in row[:3]], FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(row[3]) for row in grid.cell], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(row[4]) for row in grid.cell], FadeIn(side[2]))
            self.play(Create(b3))
            vo.wait_until("d")
            self.play(*[FadeIn(row[5]) for row in grid.cell], FadeIn(side[3]))
            self.play(Create(b10))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def defence(self):
        head = label(r"Living with the trilemma", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"be reckless", r"Wilkinson, \ ``In Defence of Fanaticism'' \ (2022): \ refusing long shots means "
                                 r"breaking a dominance principle, \ or letting the right choice depend on far-away "
                                 r"events the choice cannot affect", MONEY),
                (r"be timid", r"bounded utility, \ as with St Petersburg in Part 33; \ or Monton's discounting of "
                              r"small probabilities \ (2019)", WELL),
                (r"question the inputs", r"credences in wild claims may not be precise numbers at all \ (Part 13)",
                 GREY_A),
                (r"in practice", r"the stakes of the last chapter rest on such probabilities: \ how far to trust the "
                                 r"arithmetic is itself a decision", FUT)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.2, x_text=-2.2, label_size=20, text_size=19)
        with self.voiceover(
            "How should we live with the trilemma? <bookmark mark='a'/>Hayden Wilkinson, in In Defence of "
            "Fanaticism, 2022, chose recklessness. He argued that every alternative is worse: a theory that refuses "
            "the long shots must break a principle of dominance, or let the right choice depend on events far away, "
            "in distant galaxies or the distant past, that the choice cannot affect. <bookmark mark='b'/>Others accept "
            "timidity: a bounded utility, as Part 33 used against St Petersburg, or Bradley Monton's proposal of 2019 "
            "to discount small probabilities. <bookmark mark='c'/>Some question the inputs: a credence about a "
            "mugger's magic may not be a precise number at all, as Part 13 allowed. <bookmark mark='d'/>The question "
            "is practical. The case for spending on remote catastrophes rests on such probabilities, and how far to "
            "trust the arithmetic is itself a decision."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
