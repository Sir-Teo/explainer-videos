from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403


class Boole(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Boole's algebra of thought", r"Can reasoning be written as equations?",
                            lit=(-300, 1854), part=PART)
        with self.voiceover("Chapter one. Boole's algebra of thought."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.stoics()
        self.classes()
        self.duality()
        self.jevons()

    def stoics(self):
        hc = history_card(r"3rd c.\ BCE", r"Chrysippus of Soli", r"five `indemonstrable' arguments, from which "
                          r"every other was to follow", width=5.0, color=HIST).to_corner(UL, buff=0.4)
        forms = [r"p \to q,\ \ p \ \vdash\ q", r"p \to q,\ \ \lnot q \ \vdash\ \lnot p",
                 r"\lnot(p \land q),\ \ p \ \vdash\ \lnot q", r"p \veebar q,\ \ p \ \vdash\ \lnot q",
                 r"p \lor q,\ \ \lnot p \ \vdash\ q"]
        rows = VGroup()
        for i, f in enumerate(forms, 1):
            rows.add(VGroup(MathTex(rf"{i}.", font_size=34, color=GREY_B), MathTex(f, font_size=38)).arrange(
                RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.2, 0.3, 0])
        for r in rows:
            r.set_opacity(0.25)
        names = VGroup(label(r"modus ponens", font_size=24, color=CONN), label(r"modus tollens", font_size=24,
                                                                                 color=CONN))
        names[0].next_to(rows[0], RIGHT, buff=0.5)
        names[1].next_to(rows[1], RIGHT, buff=0.5)
        src = cite(r"Diogenes Laertius, \textit{Lives} VII.80; Sextus Empiricus, \textit{Outlines} II.157")
        q = quote_card(r"Even the crows on the rooftops are cawing about which conditionals are true.",
                       r"Callimachus, quoted by Sextus Empiricus", r"\textit{Against the Mathematicians} I.309",
                       width=8.0, font_size=28).move_to([0, -2.4, 0])
        with self.voiceover(
            "The logic of whole sentences is older than Boole. In the third century before our era, the Stoic "
            "Chrysippus listed five arguments he called indemonstrable: the starting points from which every other "
            "inference was to follow. <bookmark mark='a'/>The first: if the first, then the second; the first; "
            "therefore the second. <bookmark mark='b'/>The second: if the first, then the second; not the second; "
            "therefore not the first. <bookmark mark='c'/>Then three more, about 'not both', 'either, or' and "
            "exclusion. We still use the first two every day, under their Latin names: modus ponens and modus "
            "tollens."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2), FadeIn(src), FadeIn(rows))
            vo.wait_until("a")
            self.play(rows[0].animate.set_opacity(1), Indicate(rows[0], color=CONN))
            vo.wait_until("b")
            self.play(rows[1].animate.set_opacity(1), Indicate(rows[1], color=CONN))
            vo.wait_until("c")
            self.play(*[r.animate.set_opacity(1) for r in rows[2:]], FadeIn(names))
        with self.voiceover(
            "The Stoics also argued about what 'if' means. Philo of Megara held that 'if p then q' is false in only "
            "one case: when p is true and q is false. Diodorus Cronus demanded more, a connection that holds at "
            "every time. <bookmark mark='a'/>The dispute was so famous that the poet Callimachus joked that even the "
            "crows on the rooftops were cawing about which conditionals are true. Philo's answer is the one this "
            "part will use, and in Part 14 we will see why the crows were right to keep cawing."
        ) as vo:
            self.play(rows.animate.scale(0.8).shift(UP * 0.5), FadeOut(names))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def classes(self):
        hc = history_card(1854, r"George Boole", r"\textit{An Investigation of the Laws of Thought}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.4)
        U = Rectangle(width=6.0, height=4.2, stroke_color=GREY_B, stroke_width=2).move_to([3.4, -0.4, 0])
        cx = Circle(radius=1.45, stroke_color=ATOM, stroke_width=3).move_to(U.get_center() + LEFT * 0.85)
        cy = Circle(radius=1.45, stroke_color=P.AGENT, stroke_width=3).move_to(U.get_center() + RIGHT * 0.85)
        lx = MathTex("x", font_size=40, color=ATOM).next_to(cx, UL, buff=-0.35)
        ly = MathTex("y", font_size=40, color=P.AGENT).next_to(cy, UR, buff=-0.35)
        l1 = MathTex("1", font_size=36, color=GREY_B).next_to(U.get_corner(UL), DR, buff=0.15)
        both = Intersection(cx, cy, stroke_width=0, fill_color=P.CONCL, fill_opacity=0.6)
        notx = Difference(U, cx, stroke_width=0, fill_color=ATOM, fill_opacity=0.25)
        uni = Union(cx, cy, stroke_width=0, fill_color=P.TRUE, fill_opacity=0.35)
        eqs = VGroup(MathTex(r"xy", r"\ :\ \text{white sheep}", font_size=34),
                     MathTex(r"x + y", r"\ :\ \text{either (when they don't overlap)}", font_size=34),
                     MathTex(r"1 - x", r"\ :\ \text{everything not white}", font_size=34),
                     MathTex(r"0", r"\ :\ \text{nothing}", font_size=34))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        if eqs.width > 6.2:
            eqs.width = 6.2
        eqs.to_edge(LEFT, buff=0.45).set_y(-1.3)
        for e, c in zip(eqs, (P.CONCL, P.TRUE, ATOM, GREY_B)):
            e[0].set_color(c)
        key = VGroup(MathTex(r"x", r"=\text{the white things}", font_size=30),
                     MathTex(r"y", r"=\text{the sheep}", font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key[0][0].set_color(ATOM)
        key[1][0].set_color(P.AGENT)
        key.next_to(U, UP, buff=0.25)
        with self.voiceover(
            "Two thousand years later, George Boole, a self-taught schoolmaster from Lincoln who became a professor "
            "in Cork, did something new. In 1847, and then in An Investigation of the Laws of Thought in 1854, he "
            "wrote logic as algebra. <bookmark mark='a'/>Let x stand for the class of white things and y for the class "
            "of sheep. <bookmark mark='b'/>Then x times y is the class of white sheep. <bookmark mark='c'/>x plus y "
            "gathers the two, when they don't overlap. <bookmark mark='d'/>One is the universe of everything we are "
            "talking about, and one minus x is everything that is not white. <bookmark mark='e'/>Zero is the empty class."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2), Create(U), FadeIn(l1))
            vo.wait_until("a")
            self.play(Create(cx), Create(cy), FadeIn(lx), FadeIn(ly), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(both), Write(eqs[0]))
            vo.wait_until("c")
            self.play(FadeOut(both), FadeIn(uni), Write(eqs[1]))
            vo.wait_until("d")
            self.play(FadeOut(uni), FadeIn(notx), Write(eqs[2]))
            vo.wait_until("e")
            self.play(FadeOut(notx), Write(eqs[3]))
        self.clear_scene()

    def duality(self):
        G = axes([-0.5, 1.6], [-0.5, 2.0], x_length=4.4, y_length=4.2, xticks=[0, 1], yticks=[0, 1],
                 center=[4.6, -0.3, 0])
        ax = G.ax
        ts = np.linspace(-0.5, 1.4, 120)
        par = curve(ax, ts, ts * ts, CONN, stroke_width=4)
        ts2 = np.linspace(-0.5, 1.6, 2)
        line = curve(ax, ts2, ts2, ATOM, stroke_width=4)
        lp = MathTex(r"x^2", font_size=34, color=CONN).next_to(ax.c2p(1.35, 1.82), LEFT, buff=0.1)
        ll = MathTex(r"x", font_size=34, color=ATOM).next_to(ax.c2p(1.6, 1.6), DOWN, buff=0.15)
        dots = VGroup(glow_dot(ax.c2p(0, 0), color=OK), glow_dot(ax.c2p(1, 1), color=OK))
        dl = VGroup(MathTex("0", font_size=34, color=OK).next_to(ax.c2p(0, 0), DR, buff=0.12),
                    MathTex("1", font_size=34, color=OK).next_to(ax.c2p(1, 1), DR, buff=0.12))
        law = MathTex(r"x", r"\,x", r"=", r"x", font_size=54).move_to([-2.6, 2.2, 0])
        law[0].set_color(ATOM)
        law[1].set_color(ATOM)
        law[3].set_color(ATOM)
        words = label(r"the white things that are white are the white things", font_size=24, color=GREY_A)
        words.next_to(law, DOWN, buff=0.25)
        rows = [MathTex(r"x^2", r"=", r"x", font_size=44), MathTex(r"x - x^2", r"=", r"0", font_size=44),
                MathTex(r"x(1 - x)", r"=", r"0", font_size=44)]
        whys = [why(r"the law of duality"), why(r"subtract $x^2$"), why(r"factor: nothing is both $x$ and not $x$")]
        for r in rows:
            r.set_x(-3.4)
        step = ladder(self, rows, whys, keep=3, top=0.8, x=-3.9, edge=2.0)
        with self.voiceover(
            "One of Boole's laws is unlike ordinary algebra. The white things that are white are just the white "
            "things: x times x is x. Boole called it the law of duality. <bookmark mark='a'/>As an equation about "
            "numbers, it has only two solutions: the curve x squared meets the line x at zero and at one. "
            "<bookmark mark='b'/>That is where the two truth values come from. Read one as true and zero as false, and "
            "Boole's algebra of classes becomes an algebra of sentences."
        ) as vo:
            self.play(Write(law), FadeIn(words))
            vo.wait_until("a")
            self.play(FadeIn(G), Create(line), Create(par), FadeIn(lp), FadeIn(ll))
            self.play(FadeIn(dots, scale=1.5))
            vo.wait_until("b")
            self.play(FadeIn(dl))
        with self.voiceover(
            "And from that one law Boole derived the oldest principle in logic, Aristotle's principle of "
            "contradiction. <bookmark mark='a'/>Start from x squared equals x. <bookmark mark='b'/>Subtract x squared "
            "from both sides. <bookmark mark='c'/>Factor. x times one minus x is zero: the class of things that are "
            "both x and not x is empty. Nothing is both white and not white. A law of thought, derived by algebra."
        ) as vo:
            self.play(FadeOut(law), FadeOut(words))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Indicate(rows[2], color=OK))
        self.clear_scene()

    def jevons(self):
        d = load("jevons")
        hc = history_card(1869, r"William Stanley Jevons", r"the logic piano, shown to the Royal Society in 1870",
                          width=5.0, color=HIST).to_corner(UL, buff=0.4)
        prem = VGroup(MathTex(r"I \to M", r"\quad\text{iron is a metal}", font_size=32),
                      MathTex(r"M \to E", r"\quad\text{every metal is an element}", font_size=32))
        prem.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(hc, DOWN, buff=0.5).align_to(hc, LEFT)
        prem[0][0].set_color(BAD)
        prem[1][0].set_color(P.AGENT)
        rows = []
        for r in d["rows"]:
            v = r["v"]
            rows.append([v["I"], v["M"], v["E"]])
        grid = ValueGrid([r"I", r"M", r"E"], rows, col_w=1.0, cell_h=0.52, font_size=30).move_to([3.4, 0.0, 0])
        strikes = {0: VGroup(), 1: VGroup()}
        for i, r in enumerate(d["rows"]):
            if r["struck_by"]:
                k = r["struck_by"][0]
                strikes[k].add(grid.strike(i, color=BAD if k == 0 else P.AGENT))
        surv = [i for i, r in enumerate(d["rows"]) if not r["struck_by"]]
        iron = [i for i in surv if d["rows"][i]["v"]["I"]]
        boxes = VGroup(*[grid.row_box(i, color=OK) for i in iron])
        concl = MathTex(r"\therefore\ I \to E", r"\quad\text{iron is an element}", font_size=34, color=OK)
        concl.next_to(prem, DOWN, buff=0.5).align_to(prem, LEFT)
        with self.voiceover(
            "Boole's algebra could be done by a machine, and in 1869 the economist William Stanley Jevons built one: "
            "the logic piano. Its method is the one we used on the island. <bookmark mark='a'/>Take two premises: iron "
            "is a metal, and every metal is an element. <bookmark mark='b'/>Write out every combination of the three "
            f"terms: there are {len(rows)}."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(prem, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      LaggedStart(*[FadeIn(grid.row(i)) for i in range(len(rows))], lag_ratio=0.1), run_time=2)
        with self.voiceover(
            f"The first premise strikes out the {len(strikes[0])} combinations with iron that is not a metal. "
            "<bookmark mark='a'/>"
            f"The second strikes out the {len(strikes[1])} remaining ones with a metal that is not an element. "
            f"<bookmark mark='b'/>{len(surv)} combinations survive, and in every surviving one that contains iron, "
            "element is there too. <bookmark mark='c'/>So iron is an element. Jevons's keys and levers did exactly "
            "this, for up to four terms: they enumerated the cases and threw away the impossible ones. Our island "
            "solver, and every truth table in this part, works the same way."
        ) as vo:
            self.play(LaggedStart(*[Create(s) for s in strikes[0]], lag_ratio=0.2), Indicate(prem[0], color=BAD))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in strikes[1]], lag_ratio=0.2), Indicate(prem[1], color=P.AGENT))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Write(concl))
        with self.voiceover(
            "So by 1870 the pieces were on the table: sentences as variables that take two values; connectives as "
            "operations on them; and validity as something checked by exhausting the cases. What was missing was a "
            "precise account of what a formula is, and of what the connectives can and cannot build. That comes next."
        ):
            self.play(Indicate(grid, color=GREY_A, scale_factor=1.02))
        self.clear_scene()
