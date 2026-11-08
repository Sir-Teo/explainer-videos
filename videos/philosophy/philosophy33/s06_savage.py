from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Savage(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Savage", r"Can probability itself be read off preferences?", lit=(1954,), part=PART)
        with self.voiceover("Chapter five. Savage."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.framework()
        self.surething()
        self.tickets()

    def framework(self):
        hc = history_card(1954, r"Leonard J. Savage", r"\textit{The Foundations of Statistics}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"states", r"ways the world might be, \ none of them up to you", RISK),
                (r"consequences", r"what you get", MONEY),
                (r"acts", r"functions from states to consequences", AGENT),
                (r"the theorem", r"if preferences over acts satisfy Savage's postulates, \ there is a unique "
                                 r"probability $P$ and a utility $u$ with $f \succeq g$ iff $\mathbb{E}_P[u(f)] \ge "
                                 r"\mathbb{E}_P[u(g)]$", GOAL)]
        g = rows_table(rows, top=1.3, gap=0.5)
        with self.voiceover(
            "Von Neumann and Morgenstern took probabilities as given. In 1954 Leonard Savage derived them, together "
            "with utilities, from preferences alone. <bookmark mark='a'/>There are states of the world, none of them "
            "up to you; <bookmark mark='b'/>consequences, what you get; <bookmark mark='c'/>and acts, which are "
            "functions from states to consequences. <bookmark mark='d'/>If your preferences over acts satisfy his "
            "postulates, there is a unique probability and a utility, unique up to scale, such that you prefer one "
            "act to another exactly when its expected utility is greater. Your probabilities, like the Ramsey and de "
            "Finetti betting rates of Part 13, are written in your choices."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def surething(self):
        head = label(r"The sure-thing principle", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        q = quote_card(r"If the person would not prefer $f$ to $g$, \ either knowing that the event $B$ obtained, \ "
                       r"or knowing that $B$ did not obtain, \ then he does not prefer $f$ to $g$.",
                       r"Savage", r"\textit{The Foundations of Statistics}, \ \S 2.7", width=9.6,
                       font_size=26).move_to([0, 0.9, 0])
        rows = stack([(r"his example: \ a businessman deciding whether to buy a house before an election", GREY_A),
                      (r"he would buy if the Republican won, \ and buy if the Democrat won: \ so buy", AGENT),
                      (r"in the lottery form: \ outcomes common to two acts should not affect the choice", GOAL)],
                     font_size=20, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Savage's central postulate is the sure-thing principle. <bookmark mark='a'/>In his words: if the person "
            "would not prefer f to g, either knowing that the event B obtained, or knowing that B did not obtain, "
            "then he does not prefer f to g. <bookmark mark='b'/>His example was a businessman deciding whether to "
            "buy a house before an election. <bookmark mark='c'/>He would buy if the Republican won, and he would "
            "buy if the Democrat won, so he should buy now. <bookmark mark='d'/>For lotteries it says what "
            "independence said: outcomes the two acts share should not affect the choice between them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tickets(self):
        head = label(r"Savage's tickets", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{ticket}", r"1", r"2\text{--}11", r"12\text{--}100"]
        rows = [(r"1A", r"1", r"1", r"1"), (r"1B", r"0", r"5", r"1"), (r"2A", r"1", r"1", r"0"),
                (r"2B", r"0", r"5", r"0")]
        cells = []
        for k, (a, b, c, e) in enumerate(rows):
            cells.append([label(a, font_size=21, color=PREF), label(b, font_size=20, color=GREY_A),
                          label(c, font_size=20, color=GREY_A), label(e, font_size=20, color=MONEY)])
        grid = ValueGrid(hd, cells, col_w=[1.6, 1.6, 2.0, 2.4], cell_h=0.6, font_size=19).move_to([-2.6, 0.0, 0])
        col = SurroundingRectangle(VGroup(*[grid.cell[k][3] for k in range(4)]), color=MONEY, buff=0.08)
        unit = label(r"prizes in millions; \ a ticket drawn from 100", font_size=17, color=GREY_A).next_to(
            grid, DOWN, buff=0.3)
        side = stack([(r"tickets 12--100 pay the same within each pair", MONEY),
                      (r"on tickets 1--11 the two pairs are identical", PREF),
                      (r"so the sure-thing principle ties the choices together", GOAL),
                      (r"Savage first chose like Allais's subjects, \ then, \ on reflection, \ changed his second "
                       r"choice", HIST)], font_size=19, aligned_edge=LEFT, width=5.0, buff=0.3).move_to([3.8, 0.0, 0])
        with self.voiceover(
            "Savage rewrote Allais's choices as lottery tickets. <bookmark mark='a'/>A ticket is drawn from a hundred. "
            "1A pays a million whatever the ticket. 1B pays nothing on ticket one, five million on tickets two to "
            "eleven, and a million on the rest. 2A and 2B are the same, except that tickets twelve to a hundred pay "
            "nothing. <bookmark mark='b'/>Within each pair, tickets twelve to a hundred pay the same, so by the "
            "sure-thing principle they should not matter. <bookmark mark='c'/>And on tickets one to eleven, the two "
            "pairs are identical. So whoever prefers 1A must prefer 2A. <bookmark mark='d'/>Savage confessed that "
            "when he first met the problem he chose as Allais's subjects do. Seeing the tickets, he changed his "
            "second choice, and concluded that it was his first reaction, not the principle, that was in error. "
            "Many decision theorists have not been persuaded."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), FadeIn(unit))
            vo.wait_until("a")
            for r in range(4):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("b")
            self.play(Create(col), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
