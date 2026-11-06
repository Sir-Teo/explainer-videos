from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)

COLS = [DATA, HEAD, YES, NO]


class Sat(VoiceoverScene):
    def construct(self):
        self.card()
        self.cdcl()
        self.phase()
        self.famous()

    def card(self):
        card = chapter_card(13, r"SAT in practice", r"Why do solvers for an NP-complete problem work so well?",
                            lit=(1962, 2016), extra=((1962, r"DPLL"), (1996, r"CDCL"), (2016, r"Pythagorean triples")),
                            part=PART)
        with self.voiceover("Chapter thirteen. SAT in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cdcl(self):
        s = load("solvers")
        head = label(r"Conflict-driven clause learning", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"\textbf{1. decide}: \ pick a variable and a value \ (the most active one: \ VSIDS)", font_size=21,
                  color=WHITE),
            label(r"\textbf{2. propagate}: \ a clause with one free literal forces it \ (two watched literals)",
                  font_size=21, color=DATA),
            label(r"\textbf{3. conflict}: \ some clause is false: \ trace the implications back to a cut",
                  font_size=21, color=NO),
            label(r"\textbf{4. learn}: \ add the clause that forbids that cut \ (the first unique implication point)",
                  font_size=21, color=YES),
            label(r"\textbf{5. backjump}: \ undo to the level where the new clause becomes unit, \ and repeat",
                  font_size=21, color=HEAD),
            label(r"plus restarts \ (Luby) \ and saved phases: \ the solver used throughout this part, \ about 200 "
                  r"lines of Python", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        rows = [[str(r["n"]), words(r["dpll_nodes"]), f"{r['dpll_s'] * 1000:.1f} ms",
                 words(r["cdcl_steps"]), f"{r['cdcl_s'] * 1000:.1f} ms"] for r in s["rows"]]
        tab = grid_table([r"$n$", r"DPLL nodes", r"time", r"CDCL steps", r"time"], rows,
                         widths=[1.0, 2.0, 1.6, 2.0, 1.6], row_h=0.36, font_size=18, mono_cols=(),
                         colors=[[WHITE, GREY_A, NO, DATA, YES]] * len(rows))
        tab.next_to(steps, DOWN, buff=0.35).set_x(0)
        tl = label(r"random 3-SAT at $m = 4.26\,n$, \ median of 10; \ DPLL = Davis, \ Logemann, \ Loveland \ (1962)",
                   font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.12)
        with self.voiceover(
            "Satisfiability is NP-complete, yet industrial solvers handle formulas with millions of variables. "
            "Here is how ours works. <bookmark mark='a'/> Decide: pick a variable, preferring ones involved in recent "
            "conflicts, and give it a value. <bookmark mark='b'/> Propagate: any clause with all but one literal "
            "false forces the last one, and watching just two literals per clause makes this cheap. <bookmark "
            "mark='c'/> Sooner or later some clause becomes false. Trace the chain of implications back to find "
            "which decisions caused it. <bookmark mark='d'/> Learn a new clause that rules out that combination "
            "forever. <bookmark mark='e'/> Then jump back, not one level but to wherever the new clause first "
            "applies, and continue. <bookmark mark='f'/> Add restarts, and you have the solver this part has been "
            "using, about two hundred lines of Python. <bookmark mark='g'/> Against the older DPLL procedure from "
            "1962 on hard random formulas, it needs fewer steps and much less time as n grows."
        ) as vo:
            self.play(FadeIn(head))
            for mk, st in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(st, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(tab), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    def phase(self):
        d = load("phase")
        head = label(r"The phase transition of random 3-SAT", font_size=32).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[3.0, 6.0, 0.5], y_range=[0, 1.05, 0.25], x_length=5.6, y_length=3.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        ax2 = Axes(x_range=[3.0, 6.0, 0.5], y_range=[0, 3.6, 1], x_length=5.6, y_length=3.4,
                   axis_config={"color": GREY_D, "include_numbers": False}).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        cols = {"50": GREY_A, "100": DATA, "150": HEAD}
        c1, c2, leg = VGroup(), VGroup(), VGroup()
        for n, rows in d["by_n"].items():
            pts = [ax.c2p(r["ratio"], r["p_sat"]) for r in rows]
            c1.add(VMobject(color=cols[n], stroke_width=3).set_points_as_corners(pts))
            pts2 = [ax2.c2p(r["ratio"], np.log10(max(r["median_conflicts"], 1))) for r in rows]
            c2.add(VMobject(color=cols[n], stroke_width=3).set_points_as_corners(pts2))
            leg.add(label(rf"$n$ = {n}", font_size=18, color=cols[n]))
        leg.arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.25)
        thr = VGroup(DashedLine(ax.c2p(4.27, 0), ax.c2p(4.27, 1.05), color=NO, stroke_width=1.5),
                     DashedLine(ax2.c2p(4.27, 0), ax2.c2p(4.27, 3.6), color=NO, stroke_width=1.5))
        xl = VGroup(*[VGroup(*[label(f"{x:g}", font_size=15, color=GREY_A).next_to(a.c2p(x, 0), DOWN, buff=0.1)
                               for x in (3, 4, 5, 6)]) for a in (ax, ax2)])
        yl1 = VGroup(*[label(f"{y:g}", font_size=15, color=GREY_A).next_to(ax.c2p(3.0, y), LEFT, buff=0.1)
                       for y in (0, 0.5, 1)])
        yl2 = VGroup(*[label(rf"$10^{y}$", font_size=15, color=GREY_A).next_to(ax2.c2p(3.0, y), LEFT, buff=0.1)
                       for y in (0, 1, 2, 3)])
        t1 = label(r"fraction satisfiable", font_size=19, color=WHITE).next_to(ax, UP, buff=0.1)
        t2 = label(r"median conflicts \ (log)", font_size=19, color=WHITE).next_to(ax2, UP, buff=0.1)
        x1 = label(r"clauses per variable, \ $m/n$", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        x2 = label(r"clauses per variable, \ $m/n$", font_size=18, color=GREY_A).next_to(ax2, DOWN, buff=0.45)
        r150 = {r["ratio"]: r for r in d["by_n"]["150"]}
        notes = VGroup(
            label(r"few clauses: \ almost always satisfiable, \ found at once; \ many: \ refuted quickly",
                  font_size=20, color=WHITE),
            label(rf"near 4.27 clauses per variable the probability drops through $\tfrac12$, \ and the work peaks: "
                  rf"\ {words(r150[4.3]['median_conflicts'])} conflicts at $n$ = 150", font_size=20, color=NO),
            label(r"the curves sharpen with $n$: \ the threshold is sharp \ (Friedgut, 1999); \ its exact place is "
                  r"proved only for large $k$ \ (Ding, \ Sly, \ Sun, \ 2015)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Where are the hard instances? <bookmark mark='a'/> Generate random three-SAT formulas with n variables "
            "and m clauses, and vary the ratio. With few clauses, a formula is almost always satisfiable, and the "
            "solver finds an assignment at once. With many, it is almost always unsatisfiable, and contradictions "
            "come quickly. <bookmark mark='b'/> In between, near four point two seven clauses per variable, the "
            "probability of satisfiability falls through one half, and the solver's work peaks: over two thousand "
            "conflicts at a hundred and fifty variables, against a handful at either end. <bookmark mark='c'/> The "
            "drop sharpens as n grows: Ehud Friedgut proved in 1999 that the threshold is sharp. Its exact location "
            "was proved in 2015 by Jian Ding, Allan Sly and Nike Sun, but only for long clauses. For three-SAT, the "
            "predicted value of about four point two seven is still a conjecture."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(ax2), FadeIn(xl), FadeIn(yl1), FadeIn(yl2), FadeIn(t1),
                      FadeIn(t2), FadeIn(x1), FadeIn(x2), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c1), run_time=2.0)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(c2), Create(thr), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def famous(self):
        f = load("famous")
        head = label(r"Mathematics by SAT solver", font_size=34).to_edge(UP, buff=0.3)
        col = f.get("schur_44_colouring")
        strip = VGroup()
        if col:
            for i, c in enumerate(col):
                sq = Square(side_length=0.27, stroke_color=BG, stroke_width=1, fill_color=COLS[c], fill_opacity=0.9)
                sq.move_to(RIGHT * i * 0.27)
                strip.add(VGroup(sq, mono(str(i + 1), 9, BG).move_to(sq)))
        strip.next_to(head, DOWN, buff=0.35).set_x(0)
        sl = label(r"1 to 44 in 4 colours, \ no $x + y = z$ in one colour: \ found by our solver", font_size=19,
                   color=GREY_A).next_to(strip, DOWN, buff=0.12)
        s13, s14 = f["schur_13_3"], f["schur_14_3"]
        py = f["pythagorean"]
        lines = VGroup(
            label(rf"\textbf{{Schur numbers}}: \ 3 colours work up to 13 \ ({s13['seconds'] * 1000:.0f} ms), \ not 14 "
                  rf"\ (refuted in {s14['conflicts']} conflicts); \ 4 colours: \ 44", font_size=21, color=WHITE),
            label(r"$S(5) = 160$: \ Heule \ (2017), \ a 2-petabyte proof", font_size=21, color=HEAD),
            label(rf"\textbf{{Pythagorean triples}}: \ colour 1 to $n$ in 2 colours with no one-coloured "
                  rf"$a^2 + b^2 = c^2$: \ our solver manages $n$ = {max(r['n'] for r in py if r['status'] == 'sat')}",
                  font_size=21, color=DATA),
            label(rf"Heule, \ Kullmann and Marek \ (2016): \ possible up to 7,824, \ impossible at 7,825 \ "
                  rf"({words(f['pythagorean_7825_triples'])} triples); \ a 200-terabyte proof", font_size=21,
                  color=YES),
            label(r"the proofs are checked by small verified programs: \ trust the checker, \ not the solver",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(sl, DOWN, buff=0.4)
        with self.voiceover(
            "Solvers now settle questions in mathematics. <bookmark mark='a'/> Colour the numbers from one up to n "
            "so that no single colour contains x, y and x plus y. With three colours you can reach thirteen but not "
            "fourteen; our solver refutes fourteen in a moment. With four colours, forty-four, and here is our "
            "solver's colouring. <bookmark mark='b'/> With five colours the answer is a hundred and sixty, proved by "
            "Marijn Heule in 2017 with a two-petabyte proof. <bookmark mark='c'/> Or colour the numbers with two "
            "colours, so that no Pythagorean triple is all one colour. Our solver colours the first three thousand "
            "easily. <bookmark mark='d'/> Heule, Oliver Kullmann and Victor Marek proved in 2016 that it can be done "
            "up to seven thousand eight hundred and twenty-four, and not one further. Their proof is two hundred "
            "terabytes. <bookmark mark='e'/> Nobody reads such proofs. They are checked by small programs whose own "
            "correctness has been verified, so we trust the checker, not the solver."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in strip], lag_ratio=0.03), FadeIn(sl), FadeIn(lines[0]),
                      run_time=2.5)
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
