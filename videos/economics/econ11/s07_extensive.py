from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

DARA = island.CAST["dara"].color
CRUSOE = island.CAST["crusoe"].color


class Extensive(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Extensive form and subgame perfection", r"When players move one after another, which threats "
             r"should be believed?", "Chapter six. Extensive form and subgame perfection.",
             lit={1965: r"Selten's subgame perfection"}, scale=("firm", "market"), horizon=("a year",))
        self.tree()
        self.threat()
        self.lessons()

    def build(self, e):
        root = UP * 2.2 + LEFT * 2.6
        inc = root + DOWN * 2.0 + LEFT * 1.6
        out = root + DOWN * 2.0 + RIGHT * 1.9
        acc = inc + DOWN * 2.0 + LEFT * 1.4
        fig = inc + DOWN * 2.0 + RIGHT * 1.4
        n0 = tree_node(root, DARA)
        n1 = tree_node(inc, CRUSOE)
        e_in = tree_edge(root, inc, r"enter", DARA, side=LEFT)
        e_out = tree_edge(root, out, r"stay out", DARA, side=RIGHT)
        e_acc = tree_edge(inc, acc, r"accommodate", CRUSOE, side=LEFT)
        e_fig = tree_edge(inc, fig, r"fight", CRUSOE, side=RIGHT)
        cols = (DARA, CRUSOE)
        l_out = payoff_leaf(out + DOWN * 0.35, e["stay_out"], cols)
        l_acc = payoff_leaf(acc + DOWN * 0.35, e["accommodate"], cols)
        l_fig = payoff_leaf(fig + DOWN * 0.35, e["fight"], cols)
        who0 = label(r"Dara", font_size=20, color=DARA).next_to(n0, UP, buff=0.12)
        who1 = label(r"Crusoe", font_size=20, color=CRUSOE).next_to(n1, LEFT, buff=0.15)
        return VGroup(e_in, e_out, e_acc, e_fig, n0, n1, l_out, l_acc, l_fig, who0, who1)

    def tree(self):
        e = load("entry")
        t = self.build(e)
        e_in, e_out, e_acc, e_fig, n0, n1, l_out, l_acc, l_fig, who0, who1 = t
        side = VGroup(
            label(r"Crusoe's yard has the island's boat trade to itself", font_size=22),
            label(r"Dara could open a rival yard: \ enter, \ or stay out", font_size=22, color=DARA),
            label(r"if she enters, \ Crusoe can fight a price war \\ or share the trade", font_size=22, color=CRUSOE),
            label(r"payoffs: \ (Dara, \ Crusoe)", font_size=20, color=GREY_A),
            label(r"solve from the end: \ once Dara is in, \\ sharing gives Crusoe 1, \ fighting $-1$", font_size=22,
                  color=CRUSOE),
            label(r"so Dara knows he will share, \ and enters: \ (1, 1)", font_size=23, color=EQ),
            label(r"backward induction", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        hi_acc = e_acc[0].copy().set_stroke(EQ, 7)
        hi_in = e_in[0].copy().set_stroke(EQ, 7)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Many games unfold in time, and are drawn as trees. <bookmark mark='a'/> Crusoe's boatyard has the "
            "Island's trade to itself. <bookmark mark='b'/> Dara is thinking of opening a rival yard: she can enter, "
            "or stay out. <bookmark mark='c'/> If she enters, Crusoe can start a price war that hurts them both, or "
            "share the trade. <bookmark mark='d'/> At the end of each branch are the payoffs, Dara's first. "
            "<bookmark mark='e'/> Solve it from the end. Once Dara has entered, sharing gives Crusoe one and "
            "fighting gives him minus one, so he shares. <bookmark mark='f'/> Dara can work that out too, so she "
            "enters, and each gets one. <bookmark mark='g'/> This is backward induction: solve the last decision "
            "first, and work back to the start."
        ) as vo:
            self.play(FadeIn(n0), FadeIn(who0), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(e_in), Create(e_out), FadeIn(n1), FadeIn(who1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(e_acc), Create(e_fig), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(l_out), FadeIn(l_acc), FadeIn(l_fig), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(hi_acc), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(Create(hi_in), FadeIn(side[5]))
            vo.wait_until("g")
            self.play(FadeIn(side[6]))
        self.clear_scene()

    def threat(self):
        e = load("entry")
        A, B = np.array(e["A"]), np.array(e["B"])
        mat = matrix(A, B, [r"enter", r"stay out"], [r"share if in", r"fight if in"], row_name=r"Dara",
                     col_name=r"Crusoe", cell_w=2.2, cell_h=0.95, font_size=26, row_color=DARA, col_color=CRUSOE
                     ).shift(LEFT * 3.0 + UP * 0.5)
        f1 = frame_cell(mat, 0, 0)
        f2 = frame_cell(mat, 1, 1)
        side = VGroup(
            label(r"the same game in strategic form: \\ Crusoe's strategy is a plan, \ made in advance", font_size=21),
            label(r"two Nash equilibria", font_size=23, color=EQ),
            label(r"Dara enters, \ Crusoe shares", font_size=22, color=EQ),
            label(r"Crusoe threatens to fight, \ so Dara stays out: \\ the threat costs him nothing, \ because it "
                  r"is never tested", font_size=21, color=HOLD),
            label(r"but if Dara did enter, \ he would not carry it out: \\ an empty threat", font_size=22,
                  color=DEFECT),
            label(r"Selten (1965): \ a subgame-perfect equilibrium \\ must be an equilibrium in every subgame",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Selten, Zeitschrift f\"ur die gesamte Staatswissenschaft 121 (1965)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Written as a table, the same game has a second equilibrium. <bookmark mark='a'/> In the strategic form "
            "Crusoe's strategy is a plan, made in advance: share if Dara enters, or fight if she does. "
            "<bookmark mark='b'/> There are two Nash equilibria. <bookmark mark='c'/> One is the outcome we found: "
            "Dara enters, and Crusoe shares. <bookmark mark='d'/> In the other, Crusoe threatens to fight, so Dara "
            "stays out, and the threat costs him nothing, because it is never put to the test. "
            "<bookmark mark='e'/> But it is not believable: if Dara did enter, fighting would hurt Crusoe, and he "
            "would share instead. It is an empty threat. <bookmark mark='f'/> In 1965 Reinhard Selten proposed "
            "ruling out such equilibria: a subgame-perfect equilibrium must be an equilibrium in every part of the "
            "tree, including the parts that are never reached."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(f1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(f2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), f2.animate.set_stroke(DEFECT))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def lessons(self):
        head = label(r"making a threat credible", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"change your own payoffs before the other moves", font_size=26),
            label(r"build capacity you would use anyway in a price war; \ sign contracts that punish backing down",
                  font_size=24, color=GREY_A),
            label(r"a reputation, \ when the same incumbent meets many entrants: \ Selten's chain store (1978)",
                  font_size=24, color=GREY_A),
            label(r"commitment by tying your hands: \ the durable-goods monopolist of Part 10 again", font_size=24,
                  color=GREY_A),
            label(r"the strategic value of having fewer options: \ Part 12 uses it for firms", font_size=25,
                  color=EQ),
        ).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So how does an incumbent make a threat believable? <bookmark mark='a'/> By changing its own payoffs "
            "before the entrant moves, so that fighting really would be its best reply. <bookmark mark='b'/> It can "
            "build capacity it would use anyway in a price war, or sign contracts that make backing down expensive. "
            "<bookmark mark='c'/> When the same incumbent faces many entrants, one after another, it may fight early "
            "to build a reputation, the puzzle Selten called the chain-store paradox in 1978. "
            "<bookmark mark='d'/> It is the lesson of the durable-goods monopolist in Part ten: power needs "
            "commitment. <bookmark mark='e'/> Having fewer options can be worth something, and Part twelve uses that "
            "idea to explain how firms compete."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
