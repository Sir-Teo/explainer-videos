from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy2.common import *  # noqa: F403


class Cost(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"The price of calculation", r"How much can a calculation cost?",
                            lit=(1971, 1985), part=PART)
        with self.voiceover("Chapter twelve. The price of calculation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pnp()
        self.cook()
        self.pigeons()
        self.systems()
        self.brick()

    def pnp(self):
        NPc = Ellipse(width=7.0, height=4.6, stroke_color=CONN, stroke_width=3, fill_color=CONN, fill_opacity=0.08)
        Pc = Ellipse(width=3.2, height=2.2, stroke_color=OK, stroke_width=3, fill_color=OK,
                     fill_opacity=0.12).move_to(NPc.get_center() + LEFT * 1.6 + DOWN * 0.4)
        G = VGroup(NPc, Pc).move_to([-2.6, -0.5, 0])
        lp = label(r"P: \ answers found fast", font_size=26, color=OK).move_to(Pc)
        lnp = label(r"NP: \ answers checked fast", font_size=26, color=CONN).next_to(NPc.get_top(), DOWN, buff=0.35)
        ex = VGroup(label(r"sorting, shortest paths", font_size=22, color=OK).next_to(lp, DOWN, buff=0.15),
                    label(r"SAT, scheduling, sudoku", font_size=22, color=CONN).move_to(
                        NPc.get_center() + RIGHT * 1.6 + UP * 0.3))
        q = MathTex(r"\mathrm{P} \overset{?}{=} \mathrm{NP}", font_size=72, color=GOAL).move_to([4.0, 1.2, 0])
        prize = label(r"a Clay Millennium Problem (2000)", font_size=24, color=GREY_A).next_to(q, DOWN, buff=0.3)
        check = label(r"a valuation is checked clause by clause in a moment", font_size=24, color=GREY_A)
        check.next_to(prize, DOWN, buff=0.6)
        if check.get_right()[0] > 6.9:
            check.shift(LEFT * (check.get_right()[0] - 6.9))
        with self.voiceover(
            "Every solver we have built works on small examples. The real question is how the work grows with the "
            "size of the problem. <bookmark mark='a'/>Some problems can be solved in time that grows like a "
            "polynomial in their size: sorting a list, finding a shortest path. Call that class P. "
            "<bookmark mark='b'/>Others have answers that are quick to check, once someone hands you one. A "
            "satisfying valuation is checked clause by clause in a moment. Call that class NP. "
            "<bookmark mark='c'/>Whether every problem with quickly checked answers also has quickly found answers, "
            "whether P equals NP, is the most famous open problem in computer science, one of the Clay Institute's "
            "million-dollar Millennium Problems."
        ) as vo:
            self.play(Create(NPc), FadeIn(lnp))
            vo.wait_until("a")
            self.play(Create(Pc), FadeIn(lp), FadeIn(ex[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex[1]), FadeIn(check))
            vo.wait_until("c")
            self.play(Write(q), FadeIn(prize))
        self.clear_scene()

    def cook(self):
        hcs = VGroup(history_card(1971, r"Stephen Cook", r"`The complexity of theorem-proving procedures'",
                                  width=4.6, color=HIST, font_size=20),
                     history_card(1973, r"Leonid Levin", r"universal search problems, independently", width=4.6,
                                  color=HIST, font_size=20)).arrange(DOWN, buff=0.25).to_corner(UR, buff=0.35)
        rows, cols = 7, 10
        cell = 0.42
        grid = VGroup()
        rng = np.random.default_rng(2)
        for r in range(rows):
            for c in range(cols):
                sq = Square(cell, stroke_width=1, stroke_color=GREY_D, fill_color=WHITE,
                            fill_opacity=0.08 + 0.25 * rng.random())
                sq.move_to([(c - (cols - 1) / 2) * cell, ((rows - 1) / 2 - r) * cell, 0])
                grid.add(sq)
        grid.move_to([-2.6, -0.2, 0])
        tl = label(r"tape cells $\rightarrow$", font_size=22, color=GREY_A).next_to(grid, UP, buff=0.15)
        tt = label(r"time $\downarrow$", font_size=22, color=GREY_A).next_to(grid, LEFT, buff=0.15)
        win = SurroundingRectangle(VGroup(grid[2 * cols + 3], grid[2 * cols + 5], grid[3 * cols + 4]), buff=0.02,
                                   color=GOAL, stroke_width=3)
        rule = label(r"clauses: \ each row follows from the one above by the machine's rules", font_size=24,
                     color=GOAL).next_to(grid, DOWN, buff=0.35)
        atom = MathTex(r"x_{t,i,s}", r":\ \text{at time } t \text{, cell } i \text{ holds } s", font_size=30)
        atom[0].set_color(ATOM)
        atom.next_to(hcs, DOWN, buff=0.5).align_to(hcs, LEFT)
        sch = schematic_tag(corner=DL)
        thm = theorem_card(r"Cook--Levin", r"SAT is NP-complete: every problem in NP rewrites, efficiently, as SAT",
                           width=5.4, font_size=22).next_to(atom, DOWN, buff=0.4).align_to(atom, LEFT)
        with self.voiceover(
            "In 1971 Stephen Cook, and independently Leonid Levin in Moscow, proved that SAT is NP-complete. "
            "<bookmark mark='a'/>Take any problem whose answers can be checked quickly, by some machine. Write the "
            "machine's whole run as a grid: one row for each moment, one column for each cell of its tape. "
            "<bookmark mark='b'/>Make an atom for every fact of the form 'at time t, cell i holds symbol s'. "
            "<bookmark mark='c'/>Then write clauses saying that each row follows from the one above by the machine's "
            "rules, and that the last row says 'accept'. <bookmark mark='d'/>These clauses are satisfiable exactly "
            "when the problem has an answer. So a fast method for SAT would be a fast method for everything whose "
            "answers can be checked: timetables, protein design, and breaking most of today's encryption. Most "
            "researchers believe there is none."
        ) as vo:
            self.play(FadeIn(hcs, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.004), FadeIn(tl), FadeIn(tt), FadeIn(sch),
                      run_time=2)
            vo.wait_until("b")
            self.play(Write(atom))
            vo.wait_until("c")
            self.play(Create(win), FadeIn(rule))
            vo.wait_until("d")
            self.play(FadeIn(thm, shift=UP * 0.2))
        self.clear_scene()

    def pigeons(self):
        php = load("solvers")["php"]
        holes = VGroup(*[Rectangle(width=1.1, height=0.9, stroke_color=GREY_B, stroke_width=2) for _ in range(3)])
        holes.arrange(RIGHT, buff=0.25).move_to([-4.0, 1.3, 0])
        birds = VGroup(*[Dot(radius=0.16, color=P.AGENT) for _ in range(4)])
        for i in range(3):
            birds[i].move_to(holes[i])
        birds[3].move_to(holes[1].get_center() + RIGHT * 0.25)
        birds[1].shift(LEFT * 0.25)
        bad = SurroundingRectangle(holes[1], color=BAD, buff=0.05)
        cap = label(r"4 pigeons, 3 holes", font_size=24, color=GREY_A).next_to(holes, DOWN, buff=0.25)
        cl = VGroup(MathTex(r"p_{i1} \lor p_{i2} \lor \cdots \lor p_{in}", r"\quad\text{every pigeon in a hole}",
                            font_size=28),
                    MathTex(r"\lnot p_{ij} \lor \lnot p_{kj}", r"\quad\text{no two in one hole}", font_size=28))
        cl.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(cap, DOWN, buff=0.4).align_to(holes, LEFT)
        hc = history_card(1985, r"Armin Haken", r"every resolution refutation of the pigeonhole formulas is "
                          r"exponentially long", width=5.0, color=HIST).next_to(cl, DOWN, buff=0.4).align_to(cl, LEFT)
        ns = [r["n"] for r in php]
        G = axes([0.5, len(ns) + 0.5], [0, 6.2], x_length=5.6, y_length=4.4, xticks=ns, yticks=[0, 2, 4, 6],
                 yfmt=lambda v: f"10^{{{int(v)}}}", xlabel=r"holes $n$", center=[3.6, -0.3, 0])
        ax = G.ax
        res = [r for r in php if "resolution_derived" in r]
        rc = curve(ax, [r["n"] for r in res], [np.log10(r["resolution_derived"]) for r in res], BAD, stroke_width=4)
        rd = VGroup(*[Dot(ax.c2p(r["n"], np.log10(r["resolution_derived"])), radius=0.06, color=BAD) for r in res])
        cc_rows = [r for r in php if r["cdcl_conflicts"] > 0]
        cc = curve(ax, [r["n"] for r in cc_rows], [np.log10(r["cdcl_conflicts"]) for r in cc_rows], OK,
                   stroke_width=4)
        cd = VGroup(*[Dot(ax.c2p(r["n"], np.log10(r["cdcl_conflicts"])), radius=0.06, color=OK) for r in cc_rows])
        leg = legend([(BAD, r"resolution: clauses generated"), (OK, r"CDCL: conflicts")], font_size=22)
        leg.next_to(G, UP, buff=0.2).align_to(G, LEFT)
        last = php[-1]
        growth = [b["cdcl_conflicts"] / a["cdcl_conflicts"] for a, b in zip(php, php[1:]) if a["cdcl_conflicts"]]
        tbl = MathTex(rf"n={last['n']}:\ \ \text{{table rows}} = 2^{{{last['vars']}}}", font_size=28, color=GREY_A)
        tbl.next_to(G, DOWN, buff=0.5)
        res_txt = ", ".join(f"{r['resolution_derived']:,}" for r in res)
        with self.voiceover(
            "Even a formula that is obviously false can be expensive to refute. <bookmark mark='a'/>Put n plus one "
            "pigeons into n holes, at most one pigeon per hole. Anyone can see it can't be done. "
            "<bookmark mark='b'/>As clauses: every pigeon is in some hole; no two pigeons share a hole. "
            "<bookmark mark='c'/>In 1985 Armin Haken proved that every resolution refutation of these formulas is "
            "exponentially long, however cleverly it is found."
        ) as vo:
            self.play(FadeIn(holes), FadeIn(birds), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(bad))
            vo.wait_until("b")
            self.play(FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        with self.voiceover(
            f"Here is what our own solvers did. <bookmark mark='a'/>Resolution generated {res_txt} clauses as the "
            f"holes went from one to {res[-1]['n']}. <bookmark mark='b'/>CDCL needed {php[-1]['cdcl_conflicts']:,} "
            f"conflicts for {php[-1]['n']} holes, roughly {np.mean(growth[-3:]):.1f} times more with each hole "
            f"added. <bookmark mark='c'/>And the truth table, for {last['n']} holes, would need two to the "
            f"{last['vars']} rows."
        ) as vo:
            self.play(FadeIn(G), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(rc), FadeIn(rd), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cc), FadeIn(cd), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(tbl))
        self.clear_scene()

    def systems(self):
        ladder_ = VGroup(
            label(r"truth tables \ $<$ \ resolution \ $<$ \ extended resolution \ $<$ \ \dots", font_size=32),
            label(r"extended resolution may name new ideas, as Tseitin did: \ short pigeonhole proofs (Cook 1976)",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to([0, 1.2, 0])
        q = theorem_card(r"Cook--Reckhow, 1979", r"some proof system has short proofs of every tautology \ "
                         r"$\iff$ \ NP $=$ coNP. \ Open.", kind=r"Question", width=8.6, font_size=26,
                         color=GOAL).move_to([0, -1.4, 0])
        with self.voiceover(
            "Is that a limit of proof itself, or only of resolution? <bookmark mark='a'/>Stronger proof systems do "
            "better. Extended resolution, which may name new ideas the way Tseitin's encoding names subformulas, has "
            "short proofs of the pigeonhole principle, as Cook showed in 1976. <bookmark mark='b'/>Whether some proof "
            "system has short proofs of every tautology turns out to be the same question as whether NP equals its "
            "mirror image, coNP, posed by Stephen Cook and Robert Reckhow in 1979. It is open."
        ) as vo:
            self.play(FadeIn(ladder_[0]))
            vo.wait_until("a")
            self.play(FadeIn(ladder_[1]))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def brick(self):
        w = wall(upto=2, current=2).move_to([0, -0.3, 0])
        head = label(r"The Wall", font_size=40, color=P.WALL).to_edge(UP, buff=0.35)
        wc = wall_card(2).move_to([0, 0.2, 0])
        with self.voiceover(
            "So here is the second brick of the Wall. <bookmark mark='a'/>Leibniz's calculation exists: every question "
            "of propositional validity can be settled mechanically, by anyone, with the same answer every time. "
            "<bookmark mark='b'/>But unless P equals NP, some of those questions cost more to settle than the universe "
            "can pay. The dream survives, with a price tag."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[2], color=P.CONCL))
            vo.wait_until("b")
            self.play(FadeOut(w), FadeIn(wc, scale=0.9))
        self.clear_scene()
