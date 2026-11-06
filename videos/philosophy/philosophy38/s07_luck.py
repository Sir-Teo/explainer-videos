from __future__ import annotations

from videos.philosophy.philosophy38.common import *  # noqa: F403


class Luck(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Equality of what?", r"What should be equal: \ resources, \ welfare, \ or capabilities?", lit=(1979, 1981), part=PART)
        with self.voiceover("Chapter six. Equality of what?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dworkin()
        self.auction()
        self.anderson()
        self.capabilities()
        self.sufficiency()

    def dworkin(self):
        head = label(r"Luck egalitarianism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Dworkin \ (1981)", r"\textit{What is Equality?}: \ distribution should be ambition-sensitive and endowment-insensitive", FAIR),
                (r"brute and option luck", r"being born blind is brute luck; \ losing a deliberate gamble is option luck: \ compensate only the first", LIB),
                (r"insurance", r"compensate as people would have insured themselves against handicaps, \ behind a thin veil", MKT),
                (r"Cohen; \ Arneson", r"equal access to advantage; \ equal opportunity for welfare: \ the same idea, \ refined", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Ronald Dworkin's essays of 1981 asked: equality of what? <bookmark mark='a'/>His answer was equality of "
            "resources, with a distribution that is ambition-sensitive, so that people bear the costs of their "
            "choices, and endowment-insensitive, so that they do not bear the costs of their circumstances. <bookmark "
            "mark='b'/>Being born blind is brute luck; losing a deliberate gamble is option luck; only the first "
            "calls for compensation. <bookmark mark='c'/>How much? As much as people would have insured themselves "
            "for, had they faced the risk of the handicap behind a thin veil. <bookmark mark='d'/>G. A. Cohen's equal "
            "access to advantage and Richard Arneson's equal opportunity for welfare refined the same idea, which "
            "came to be called luck egalitarianism."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def auction(self):
        d = load("ceei")
        head = label(r"Dworkin's auction, \ built \ (Varian, \ 1974)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["prices"] == [1.1111, 0.8889, 1.0] and d["envy_free"] and d["max_envy"] == 0.0
        assert d["alloc"] == [[0.9, 0.0, 0.0], [0.1, 1.0, 0.0], [0.0, 0.0, 1.0]]
        assert d["utility"] == [5.4, 4.5, 5.0] and d["cross"][1] == [4.5, 4.5, 1.0]
        hd = [r"", r"\text{good 1}", r"\text{good 2}", r"\text{good 3}", r"\text{utility}", r"\text{best other bundle}"]
        names = [r"Ana", r"Ben", r"Cy"]
        cells = []
        for i in range(3):
            cells.append([label(names[i], font_size=19, color=COM)] +
                         [label(f"{d['values'][i][j]:g} \\ $\\to$ \\ {d['alloc'][i][j]:g}", font_size=17) for j in range(3)] +
                         [label(f"{d['utility'][i]:g}", font_size=18, color=FAIR),
                          label(f"{max(d['cross'][i][j] for j in range(3) if j != i):g}", font_size=18, color=GREY_A)])
        cells.append([label(r"price", font_size=18, color=MKT)] +
                     [label(f"{p:.3f}", font_size=17, color=MKT) for p in d["prices"]] +
                     [label(r"", font_size=17), label(r"", font_size=17)])
        grid = ValueGrid(hd, cells, col_w=[1.4, 2.1, 2.1, 2.1, 1.6, 2.6], cell_h=0.55, font_size=16).move_to([0, 0.8, 0])
        foot = stack([(r"value $\to$ share: \ equal budgets of 1 clamshell; \ prices clear the market", GREY_A),
                      (r"proportional response: \ each bids in proportion to the value she gets from each good", MKT),
                      (r"envy-free: \ no one prefers anyone else's bundle; \ Ben is exactly indifferent", FAIR),
                      (r"the envy test \ (Foley, \ 1967): \ equality of resources, \ checked", GOAL)],
                     font_size=18, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Dworkin's device can be run as a market. <bookmark mark='a'/>Three people, Ana, Ben and Cy, each get the "
            "same budget, a hundred clamshells in Dworkin's story, here one unit of money, to spend on three "
            "divisible goods. Their values for the goods differ. <bookmark mark='b'/>The Reasoner finds the "
            "competitive equilibrium from equal incomes, which Hal Varian studied in 1974, by proportional response: "
            "each person repeatedly bids for each good in proportion to the value she gets from it. Prices settle at "
            "about one point one one, point eight nine and one. <bookmark mark='c'/>Ana buys nine tenths of good one; "
            "Ben the last tenth and all of good two; Cy good three. <bookmark mark='d'/>Then the envy test: no one "
            "prefers anyone else's bundle. Ben values Ana's bundle exactly as much as his own, four and a half, and "
            "envies no one. Equality of resources, as Duncan Foley defined envy-freeness in 1967, is achieved."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[i][0]) for i in range(3)], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[3]], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for i in range(3) for c in grid.cell[i][1:5]])
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[i][5]) for i in range(3)], FadeIn(foot[2]), FadeIn(foot[3]))
        self.clear_scene()

    def anderson(self):
        head = label(r"What is the point of equality? \ (Anderson, \ 1999)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the objection", r"luck egalitarianism abandons the reckless driver who chose his risk, \ and pities the disabled for their bad luck", BAD),
                (r"relational equality", r"the point of equality is to end oppression: \ to let people stand as equals in a democratic community", FAIR),
                (r"democratic equality", r"guarantee the capabilities needed to function as a free and equal citizen, \ not compensation for bad luck", COM)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Elizabeth Anderson's What is the Point of Equality?, of 1999, attacked the whole programme. <bookmark "
            "mark='a'/>Luck egalitarianism, she argued, would abandon an uninsured driver injured by his own "
            "negligence, and would treat the disabled as objects of pity for their bad luck. <bookmark mark='b'/>The "
            "point of equality is not to neutralize luck but to end oppression: to let people stand to one another as "
            "equals in a democratic community. <bookmark mark='c'/>Her democratic equality guarantees the "
            "capabilities a person needs to function as a free and equal citizen, which leads to the next view."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def capabilities(self):
        head = label(r"Capabilities \ (Sen; \ Nussbaum)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Sen \ (1979)", r"``Equality of What?'': \ not resources, \ which people convert into living well at different rates, \ nor utility, \ which adapts", FAIR),
                (r"functionings", r"beings and doings a person has reason to value: \ being nourished, \ reading, \ taking part in public life", COM),
                (r"capabilities", r"the real freedom to achieve them: \ the set of lives one could choose", LIB),
                (r"Nussbaum \ (2000)", r"a list of ten central capabilities, \ from life and health to play and control over one's environment", GOAL),
                (r"practice", r"the UN Human Development Index \ (1990) \ grew from this view", MKT)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Amartya Sen's lecture Equality of What?, of 1979, proposed a different currency. <bookmark mark='a'/>Not "
            "resources, which people convert into living well at very different rates, as a wheelchair user needs "
            "more resources to get around; nor utility, which adapts to deprivation, as Part 35's sour grapes showed. "
            "<bookmark mark='b'/>Functionings are the beings and doings a person has reason to value: being "
            "nourished, reading, taking part in public life. <bookmark mark='c'/>Capabilities are the real freedom to "
            "achieve them: the set of lives one could choose. <bookmark mark='d'/>Martha Nussbaum's list of ten "
            "central capabilities, from life and bodily health to play and control over one's environment, gave the "
            "idea content. <bookmark mark='e'/>And the United Nations' Human Development Index, from 1990, grew out "
            "of this view."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def sufficiency(self):
        head = label(r"Enough, \ or equal?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Frankfurt \ (1987)", r"``Equality as a Moral Ideal'': \ what matters is that everyone has enough", COM),
                (r"levelling down", r"if equality matters in itself, \ making the better off worse off, \ helping no one, \ is in one way better", BAD),
                (r"Roemer \ (1998)", r"\textit{Equality of Opportunity}: \ sort people into types by circumstance; \ equalize outcomes across types at each rank of effort", FAIR),
                (r"Casal \ (2007)", r"``Why Sufficiency Is Not Enough'': \ above the threshold, \ inequality and priority still matter", LIB)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Two further positions complete the map. <bookmark mark='a'/>Harry Frankfurt's Equality as a Moral Ideal, "
            "of 1987, argued that what matters is not that everyone has the same, but that everyone has enough. "
            "<bookmark mark='b'/>Equality faces the levelling-down objection: if equality matters in itself, then "
            "making the better off worse off, while helping no one, is in one respect an improvement. <bookmark "
            "mark='c'/>John Roemer's Equality of Opportunity, of 1998, made luck egalitarianism precise: sort people "
            "into types by their circumstances, measure effort by a person's rank within their type, and equalize "
            "outcomes across types at each rank. <bookmark mark='d'/>And Paula Casal replied to Frankfurt that "
            "sufficiency is not enough: above any threshold, inequality and priority still matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
