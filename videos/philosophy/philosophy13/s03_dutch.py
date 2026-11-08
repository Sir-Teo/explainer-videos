from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403


def money(v: float) -> str:
    return (r"+" if v > 1e-9 else r"-" if v < -1e-9 else r"") + f"{abs(v):.1f}"


class Dutch(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The Dutch book", r"Why should degrees of belief obey the axioms?",
                            lit=(1926, 1937), part=PART)
        with self.voiceover("Chapter two. The Dutch book."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bookie()
        self.lp()
        self.four()
        self.theorem()
        self.objections()

    def bookie(self):
        d = load("dutch")["two"]
        head = label(r"The bookie and the incoherent agent", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rules = stack([(r"you announce a price for each ticket", WHITE),
                       (r"the bookie may buy any ticket from you, \ or sell you any ticket, \ at your price", WHITE),
                       (r"he knows nothing you don't", GREY_A)], font_size=24).next_to(head, DOWN, buff=0.35)
        prices = VGroup(MathTex(r"c(A) = 0.6", font_size=34, color=CRED),
                        MathTex(r"c(\lnot A) = 0.6", font_size=34, color=INC)).arrange(RIGHT, buff=1.0).next_to(
            rules, DOWN, buff=0.4)
        hd = [r"\text{world}", r"\text{ticket } A", r"\text{ticket } \lnot A", r"\text{paid}", r"\text{net}"]
        rows = [[r"A", r"+1", r"0", r"-1.2", money(d["payoff"]["w1"])],
                [r"\lnot A", r"0", r"+1", r"-1.2", money(d["payoff"]["w2"])]]
        grid = ValueGrid(hd, rows, col_w=[1.6, 2.0, 2.0, 1.6, 1.6], cell_h=0.56, font_size=26).next_to(
            prices, DOWN, buff=0.45)
        for r in range(2):
            grid.cell[r][4].set_color(BAD)
        foot = label(r"a sure loss of 20 cents, \ whatever happens: \ a \textit{Dutch book}", font_size=26,
                     color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is Ramsey's argument. <bookmark mark='a'/>You announce a price for each ticket. A bookie may buy "
            "any ticket from you or sell you any ticket, at your price, as many as he likes. He knows nothing you "
            "don't; he only reads your prices. <bookmark mark='b'/>Suppose your credence in A is point six, and "
            "your credence in not A is also point six. <bookmark mark='c'/>The bookie sells you both tickets, for a "
            "dollar twenty. <bookmark mark='d'/>If A happens, the A ticket pays one dollar; if not, the other one "
            "does. Either way, exactly one ticket pays, and you collect a dollar. <bookmark mark='e'/>You lose twenty "
            "cents, whatever happens. A set of bets that loses in every possible world is called a Dutch book."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(prices))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("d")
            for r in range(2):
                self.play(*[FadeIn(grid.cell[r][c]) for c in range(4)], run_time=0.7)
            vo.wait_until("e")
            self.play(*[FadeIn(grid.cell[r][4]) for r in range(2)])
            self.play(FadeIn(foot))
        self.clear_scene()

    def lp(self):
        head = label(r"The Reasoner finds the book: \ a linear program", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        net = MathTex(r"\text{net}(w) \;=\; \sum_i s_i \,\bigl(\mathbf{1}_{A_i}(w) - c(A_i)\bigr)", font_size=38)
        net.next_to(head, DOWN, buff=0.5)
        notes = stack([(r"$s_i > 0$: \ you buy $s_i$ tickets on $A_i$; \ \ $s_i < 0$: \ you sell them", GREY_A),
                       (r"$\mathbf{1}_{A_i}(w) = 1$ if $A_i$ is true in world $w$, \ else 0", GREY_A)],
                      font_size=22).next_to(net, DOWN, buff=0.3)
        prog = MathTex(r"\max_{s,\,t}\ t \quad \text{subject to} \quad \text{net}(w) \leq -t \ \text{ for every world } w,"
                       r"\quad -1 \leq s_i \leq 1", font_size=32, color=CRED).next_to(notes, DOWN, buff=0.5)
        if prog.width > 12.6:
            prog.width = 12.6
        verdict = stack([(r"$t > 0$: \ a book, \ with a guaranteed loss of $t$", BAD),
                         (r"$t = 0$: \ no book exists: \ the credences are coherent", OK)], font_size=25).next_to(
            prog, DOWN, buff=0.45)
        with self.voiceover(
            "With two tickets the book is easy to see. With many propositions, finding it is a computation. "
            "<bookmark mark='a'/>Give each ticket a stake, s. A positive stake means you buy that many tickets; a "
            "negative one, that you sell. In each world your net gain is the sum, over the tickets, of the stake "
            "times the ticket's payoff minus its price. <bookmark mark='b'/>The net gain is linear in the stakes. So "
            "the search for the worst book is a linear program: find stakes, each between minus one and one, that "
            "make your net gain at most minus t in every world, and make t as large as possible. "
            "<bookmark mark='c'/>If the best t is positive, the program has found a Dutch book. If it is zero, no book "
            "exists. The Reasoner solves it with an off-the-shelf solver."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(net), FadeIn(notes))
            vo.wait_until("b")
            self.play(FadeIn(prog, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(v) for v in verdict], lag_ratio=0.5))
        self.clear_scene()

    def four(self):
        d = load("dutch")
        cred, book = d["four_cred"], d["four"]
        head = label(r"Four propositions, \ one hidden incoherence", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cr = MathTex(rf"c(A) = {cred['A']}", r",\ \ ", rf"c(B) = {cred['B']}", r",\ \ ", rf"c(A \land B) = {cred['A&B']}",
                     r",\ \ ", rf"c(A \lor B) = {cred['AvB']}", font_size=32, color=CRED).next_to(head, DOWN, buff=0.35)
        law = MathTex(r"c(A \lor B) \overset{?}{=} c(A) + c(B) - c(A \land B) = 0.6", font_size=30, color=INC).next_to(
            cr, DOWN, buff=0.3)
        names = {"A": r"A", "B": r"B", "A&B": r"A \land B", "AvB": r"A \lor B"}
        worlds = [("AB", r"A B"), ("A~B", r"A \bar B"), ("~AB", r"\bar A B"), ("~A~B", r"\bar A \bar B")]
        W = {"AB": {"A", "B", "A&B", "AvB"}, "A~B": {"A", "AvB"}, "~AB": {"B", "AvB"}, "~A~B": set()}
        keys = ["A", "B", "A&B", "AvB"]
        st = book["stakes"]
        verb = {True: r"\text{buy }", False: r"\text{sell }"}
        hd = [r"\text{world}"] + [verb[st[k] > 0] + names[k] for k in keys] + [r"\text{net}"]
        rows = []
        for w, wt in worlds:
            row = [wt]
            for k in keys:
                row.append(money(st[k] * ((1 if k in W[w] else 0) - cred[k])))
            row.append(money(book["payoff"][w]))
            rows.append(row)
        grid = ValueGrid(hd, rows, col_w=[1.4, 1.7, 1.7, 2.1, 2.1, 1.3], cell_h=0.5, font_size=24).next_to(
            law, DOWN, buff=0.45)
        for r in range(4):
            grid.cell[r][5].set_color(BAD)
        foot = VGroup(label(rf"sure loss: \ {book['sure_loss']:.1f} \ in all four worlds", font_size=24, color=BAD),
                      label(r"repair: \ $c(A \land B) = 0.25,\ c(A \lor B) = 0.75$ \ $\Rightarrow$ \ LP finds no book",
                            font_size=24, color=OK)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        assert d["fixed_coherent"]
        with self.voiceover(
            "Here is a case where the incoherence is less obvious. <bookmark mark='a'/>Credence one half in A, one half "
            "in B, point four in A and B, and one half in A or B. Each looks reasonable. <bookmark mark='b'/>But the "
            "laws demand that the credence in A or B be the credence in A plus that in B minus that in both: point "
            "six, not point five. <bookmark mark='c'/>The linear program finds the book: buy A, buy B, sell A and B, "
            "and sell A or B. <bookmark mark='d'/>Check it world by world. In each of the four worlds, the four bets "
            "net to minus ten cents. <bookmark mark='e'/>A sure loss of ten cents. <bookmark mark='f'/>Repair the "
            "credences, a quarter for both and three quarters for either, and the program reports that no book "
            "exists."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cr))
            vo.wait_until("b")
            self.play(FadeIn(law))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("d")
            for r in range(4):
                self.play(*[FadeIn(grid.cell[r][c]) for c in range(5)], run_time=0.6)
            vo.wait_until("e")
            self.play(*[FadeIn(grid.cell[r][5]) for r in range(4)])
            self.play(FadeIn(foot[0]))
            vo.wait_until("f")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def theorem(self):
        head = label(r"The Dutch book theorem", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        thm = VGroup(label(r"incoherent \ $\Longrightarrow$ \ some book is a sure loss \ (Ramsey; \ de Finetti)",
                           font_size=24, color=BAD),
                     label(r"coherent \ $\Longrightarrow$ \ no book is a sure loss \ (Kemeny; \ Lehman, \ 1955)",
                           font_size=24, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(
            head, DOWN, buff=0.3)
        pl = Plane2(center=[-3.4, -1.2, 0], size=3.6)
        c = Dot(pl.p(0.6, 0.6), color=INC, radius=0.09)
        cl = MathTex(r"c", font_size=28, color=INC).next_to(c, UR, buff=0.05)
        hyper = DashedLine(pl.p(0.2, 1.0), pl.p(1.0, 0.2), color=BET, stroke_width=3)
        s = Arrow(pl.p(0.6, 0.6), pl.p(0.82, 0.82), buff=0, color=BET, stroke_width=5,
                  max_tip_length_to_length_ratio=0.3)
        sl = MathTex(r"s", font_size=28, color=BET).next_to(s.get_end(), RIGHT, buff=0.08)
        rows = stack([
            (r"$\text{net}(w) = s \cdot (v_w - c)$, \ \ $v_w$ = the truth vector of world $w$", WHITE),
            (r"a sure loss: \ $s \cdot (v_w - c) < 0$ \ for every world", BAD),
            (r"$\Leftrightarrow$ \ a hyperplane through $c$ \ with every $v_w$ on one side", BET),
            (r"$\Leftrightarrow$ \ $c$ lies outside the convex hull of the $v_w$: \ the simplex", COH),
            (r"separating hyperplane theorem \ (Farkas, \ 1902)", GREY_A),
        ], font_size=22, aligned_edge=LEFT, width=6.8).move_to([3.0, -1.3, 0])
        with self.voiceover(
            "This always works. <bookmark mark='a'/>The Dutch book theorem: if your credences violate the axioms, "
            "some book is a sure loss. And its converse, proved in 1955 by John Kemeny and by Sherman Lehman: if they "
            "obey the axioms, no book is. <bookmark mark='b'/>The proof is geometry. Write your credences as a point, "
            "c, and each world as its truth vector, a corner. The net gain of a book with stakes s, in world w, is "
            "the dot product of s with the arrow from c to that corner. <bookmark mark='c'/>A sure loss means that "
            "dot product is negative for every corner. <bookmark mark='d'/>That says a hyperplane through c, "
            "perpendicular to s, has every corner strictly on one side. <bookmark mark='e'/>And such a hyperplane "
            "exists exactly when c lies outside the convex hull of the corners, which is the simplex. "
            "<bookmark mark='f'/>That is the separating hyperplane theorem, in Farkas's form. For point six, point six, "
            "the stakes are one and one: buy both tickets."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm[0]))
            self.play(FadeIn(thm[1]))
            vo.wait_until("b")
            self.play(FadeIn(pl), FadeIn(c), FadeIn(cl), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(hyper), GrowArrow(s), FadeIn(sl), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), Indicate(pl.line, color=COH))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def objections(self):
        head = label(r"Does a betting argument show anything about belief?", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        items = [
            (r"`I never bet'", r"Christensen: \ incoherent credences judge a losing package fair: \ a defect of "
                               r"belief, \ not of wallets"),
            (r"money isn't utility", r"Ramsey bet in utility, \ via an `ethically neutral' proposition"),
            (r"bets interact", r"the package principle: \ a book is judged as a whole \ (Schick, \ 1986)"),
            (r"betting changes the world", r"bets on your own actions, \ or on things the bet affects"),
            (r"only finite additivity", r"countable additivity needs infinitely many bets: \ de Finetti rejected it"),
        ]
        grid = VGroup()
        for t, n in items:
            a = label(t, font_size=23, color=BAD)
            b = label(n, font_size=21, color=GREY_A)
            if b.width > 8.4:
                b.width = 8.4
            grid.add(VGroup(a, b))
        lw = max(g[0].width for g in grid)
        for i, g in enumerate(grid):
            g[0].move_to([-6.6 + g[0].width / 2, 1.9 - i * 0.92, 0])
            g[1].move_to([-6.4 + lw + 0.3 + g[1].width / 2, 1.9 - i * 0.92, 0])
        foot = label(r"so look for a purely epistemic argument: \ accuracy", font_size=25, color=GOAL).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Is a betting argument the right kind of argument about belief? Five objections. "
            "<bookmark mark='a'/>First: I never bet. David Christensen's reply: the point is not that you will lose "
            "money, but that your credences judge each bet in a losing package fair. That is a defect in the "
            "credences themselves. <bookmark mark='b'/>Second: money is not utility; a dollar matters less to the "
            "rich. Ramsey already measured stakes in utility, calibrated by an ethically neutral proposition. "
            "<bookmark mark='c'/>Third: bets interact, so valuing each bet separately is not valuing the package. "
            "This is the package principle, questioned by Frederic Schick. <bookmark mark='d'/>Fourth: betting can "
            "change what you bet on, as with bets on your own actions. <bookmark mark='e'/>Fifth: the argument "
            "supports only finite additivity. Countable additivity needs infinitely many bets at once, and de "
            "Finetti himself rejected it. <bookmark mark='f'/>These pressures led to a different argument, one with no "
            "bookie at all, about accuracy."
        ) as vo:
            self.play(FadeIn(head))
            for mk, g in zip("abcde", grid):
                vo.wait_until(mk)
                self.play(FadeIn(g[0]), FadeIn(g[1], shift=LEFT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
