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
            label('plus Luby restarts and saved phases; conflict-budget exhaustion returns UNKNOWN, never UNSAT', font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        rows = [[str(r["n"]), words(int(r["dpll_nodes"])), f"{r['dpll_s'] * 1000:.1f} ms",
                 words(int(r["cdcl_steps"])), f"{r['cdcl_s'] * 1000:.1f} ms"] for r in s["rows"]]
        tab = grid_table([r"$n$", r"DPLL nodes", r"time", r"CDCL steps", r"time"], rows,
                         widths=[1.0, 2.0, 1.6, 2.0, 1.6], row_h=0.36, font_size=18, mono_cols=(),
                         colors=[[WHITE, GREY_A, NO, DATA, YES]] * len(rows))
        tab.next_to(steps, DOWN, buff=0.35).set_x(0)
        tl = label('same 10 formulas per size; medians on this host; DPLL nodes differ from CDCL decisions + conflicts',
                   font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.12)
        with self.voiceover(
            "Clause learning explains many practical SAT successes. <bookmark mark='a'/> Decide a variable value, using activity to guide choices. <bookmark mark='b'/> Unit propagation forces a literal when every other literal of its clause is false. Two watched literals avoid scanning every clause at every step. <bookmark mark='c'/> When a clause is falsified, follow the implication reasons. <bookmark mark='d'/> First-UIP analysis learns a clause implied by the original formula. <bookmark mark='e'/> Backjump to a level where that clause propagates, retaining the learned information. <bookmark mark='f'/> Our teaching solver also uses Luby restarts and saved phases. Exhausting a conflict budget returns unknown, never a refutation. <bookmark mark='g'/> The retained comparison uses the same formulas for DPLL and CDCL. Recursive DPLL nodes and CDCL decisions plus conflicts are DIFFERENT work units; host timings exclude the separate native reference checks. Resolved and budget-exhausted trials are reported explicitly."
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
            label('finite trials: 40 per point at $n=50,100$, 20 at $n=150$; Wilson intervals in notes',
                  font_size=20, color=WHITE),
            label('finite sample peak near predicted 4.27; not an exact limiting-threshold measurement', font_size=20, color=NO),
            label('2026 preprints: threshold existence / computability; upper bound 4.268; dated claims in notes', font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Random SAT displays a striking finite-size pattern. <bookmark mark='a'/> For each plotted ratio and variable count, generate independent random clauses with three distinct variables and fair signs. We retain every formula, complete solver status and positive model, and cross-check resolved answers with a native solver. <bookmark mark='b'/> Our twenty or forty trials per point show a drop in satisfiability and a peak in median conflicts near the transition region. The notes give binomial uncertainty intervals. A coarse finite grid cannot locate an exact limiting threshold or establish a scaling exponent. The vertical line near four point two seven marks a prediction, not a theorem inferred from these plots. <bookmark mark='c'/> Friedgut proved sharp-threshold behaviour; Ding, Sly and Sun established the predicted limiting threshold for sufficiently large clause length. Those theorems and this small three-SAT experiment have different scopes. A dated update: 2026 preprints report existence and computability of the three-SAT limiting threshold, and an upper bound of four point two six eight. The notes identify these reported claims and the exact versions inspected; our finite plots establish none of them."
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
            label(rf"\textbf{{Schur}}: 13 works with 3 colours; 14 is UNSAT ({s14['conflicts']} conflicts); \\ 44 works with 4 colours; 45 is UNKNOWN at the conflict limit", font_size=21, color=WHITE),
            label(r"$S(5) = 160$: \ Heule \ (2017), \ a 2-petabyte proof", font_size=21, color=HEAD),
            label(rf"\textbf{{Pythagorean triples}}: \ colour 1 to $n$ in 2 colours with no one-coloured "
                  rf"$a^2 + b^2 = c^2$: \ our solver manages $n$ = {max(r['n'] for r in py if r['status'] == 'sat')}",
                  font_size=21, color=DATA),
            label(rf"Heule, \ Kullmann and Marek \ (2016): \ possible up to 7,824, \ impossible at 7,825 \ "
                  rf"({words(f['pythagorean_7825_triples'])} triples); \ a 200-terabyte proof", font_size=21,
                  color=YES),
            label('local models / one Schur RUP trace checked here; published huge refutations are separate evidence',
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(sl, DOWN, buff=0.4)
        with self.voiceover(
            "SAT solvers also support mathematical proofs. <bookmark mark='a'/> We find and check Schur colourings through thirteen in three colours and forty-four in four colours. For fourteen with three colours, a native solver supplies a refutation trace whose every retained addition is checked by independent unit propagation. Our budget-limited forty-five-in-four run remains unknown when exhausted. <bookmark mark='b'/> Heule's published result establishes the five-colour Schur boundary at a hundred and sixty, using a huge proof computation. We do not repeat that proof here. <bookmark mark='c'/> For Pythagorean triples, our local SAT models supply complete colourings up to the displayed finite sizes, and we check every integer triple. <bookmark mark='d'/> The separate 2016 result of Heule, Kullmann and Marek establishes the boundary at seven thousand eight hundred and twenty-four. We independently check the larger instance's triple encoding, not its two-hundred-terabyte refutation. <bookmark mark='e'/> Solving, retaining a proof, and checking that proof are separate operations. Each reported verification names the artifact and checker actually used."
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
