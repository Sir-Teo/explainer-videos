from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MONO, PART, PATH, SYMBOL, load


def planner_summary(rows):
    """Separate recorded search work from completion and paired plan lengths.

    Legacy caches use -1 for an unresolved length and omit algorithms not run.
    A work count without a valid length establishes an attempt, not a solution.
    The cache does not distinguish exhausted from capped legacy failures.
    """
    def number(value):
        return (isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value) and value >= 0)

    def attempted(row, key):
        return number(row.get(key)) and row.get(key + "_status") not in ("not-run", "not_run")

    def solved(row, key):
        length = row.get(key + "_len")
        return (attempted(row, key) and number(length) and int(length) == length
                and row.get(key + "_status") not in ("capped", "unresolved", "unknown", "failed"))

    def stats(group, key):
        runs = [r for r in group if attempted(r, key)]
        complete = [r for r in runs if solved(r, key)]
        return {"attempted": len(runs), "solved": len(complete),
                "unresolved": len(runs) - len(complete), "not_run_or_unknown": len(group) - len(runs),
                "mean_expanded": sum(r[key] for r in runs) / len(runs) if runs else None}

    keys = ("bfs", "hmax", "ff")
    ns = sorted({r["n"] for r in rows})
    by_n = {n: {key: stats([r for r in rows if r["n"] == n], key) for key in keys} for n in ns}
    n_bfs = max((n for n in ns if by_n[n]["bfs"]["attempted"]), default=ns[-1] if ns else None)
    paired = [r for r in rows if r["n"] == n_bfs and solved(r, "bfs") and solved(r, "ff")]
    return {"ns": ns, "by_n": by_n, "all": {key: stats(rows, key) for key in keys}, "n_bfs": n_bfs,
            "paired_solved": len(paired),
            "paired_bfs_length": sum(r["bfs_len"] for r in paired) / len(paired) if paired else None,
            "paired_ff_length": sum(r["ff_len"] for r in paired) / len(paired) if paired else None}


def sudoku_mob(puzzle, D=None, cell=0.5, center=ORIGIN, clue_color=WHITE):
    """The grid, the clues, and (if D is given) each empty cell's candidates as small digits."""
    g = VGroup()
    lines = VGroup()
    for k in range(10):
        w = 3 if k % 3 == 0 else 1
        lines.add(Line([-4.5 * cell + k * cell, 4.5 * cell, 0], [-4.5 * cell + k * cell, -4.5 * cell, 0],
                       stroke_width=w, color=GREY_B if k % 3 == 0 else GREY_D))
        lines.add(Line([-4.5 * cell, 4.5 * cell - k * cell, 0], [4.5 * cell, 4.5 * cell - k * cell, 0],
                       stroke_width=w, color=GREY_B if k % 3 == 0 else GREY_D))
    g.add(lines)
    clues = VGroup()
    cands = {}
    for i in range(81):
        r, c = divmod(i, 9)
        ctr = np.array([-4 * cell + c * cell, 4 * cell - r * cell, 0])
        if puzzle[i]:
            clues.add(Text(str(puzzle[i]), font=MONO, font_size=int(52 * cell), color=clue_color).move_to(ctr))
        elif D is not None:
            for v in sorted(D[i]):
                a, b = divmod(v - 1, 3)
                m = Text(str(v), font=MONO, font_size=int(20 * cell), color=FCOL).move_to(
                    ctr + np.array([(b - 1) * cell * 0.3, (1 - a) * cell * 0.3, 0]))
                cands[(i, v)] = m
    g.add(clues)
    g.cands = cands
    g.add(VGroup(*cands.values()))
    return g.move_to(center)


def blocks_mob(towers, names="ABC", w=0.7, center=ORIGIN, colors=None, held=None):
    colors = colors or {0: HEUR, 1: GCOST, 2: PATH, 3: FCOL, 4: LEARN}
    g = VGroup()
    table = Line(LEFT * 2.0, RIGHT * 2.0, color=GREY_C, stroke_width=3)
    g.add(table)
    xs = np.linspace(-1.2, 1.2, max(len(towers), 1)) if len(towers) > 1 else [0.0]
    for t, x in zip(towers, xs):
        for k, b in enumerate(t):
            sq = Square(w, stroke_color=WHITE, stroke_width=2, fill_color=colors.get(b, GREY_B), fill_opacity=0.8)
            sq.move_to([x, w / 2 + k * w + 0.02, 0])
            g.add(VGroup(sq, Text(names[b], font=MONO, font_size=28, color=WHITE).move_to(sq)))
    return g.move_to(center)


class Plans(VoiceoverScene):
    def construct(self):
        self.card()
        self.csp()
        self.ac3()
        self.strips()
        self.sussman()
        self.planners()

    def card(self):
        card = chapter_card(10, r"Constraints and plans", r"How do you search when the problem has structure?",
                            lit=(1971,), part=PART)
        with self.voiceover("Chapter ten. Constraints and plans."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def csp(self):
        d = load("sudoku")
        grid = sudoku_mob(d["puzzle"], cell=0.62, center=[-3.3, -0.2, 0])
        dc = definition_card(r"constraint satisfaction problem", r"variables, \ each with a domain of values; \ "
                             r"constraints on combinations of them; \ find an assignment that breaks none",
                             width=6.0, font_size=22, color=FCOL).move_to([3.4, 1.6, 0])
        sud = label(r"Sudoku: \ $81$ variables, \ domains $\{1, \dots, 9\}$, \\ ``all different'' in every row, "
                    r"column and box", font_size=22, color=GREY_A).next_to(dc, DOWN, buff=0.35)
        hcs = VGroup(history_card(1975, r"David Waltz", r"labelling the lines of a drawing by constraint propagation",
                                  width=5.4, color=HIST, font_size=18),
                     history_card(1977, r"Alan Mackworth", r"arc consistency: \ AC-3", width=5.4, color=HIST,
                                  font_size=18)).arrange(DOWN, buff=0.2).next_to(sud, DOWN, buff=0.35)
        tag = note(rf"a puzzle made here: \ ${d['clues']}$ clues, \ one solution").next_to(grid, DOWN, buff=0.15)
        with self.voiceover(
            "Many problems are sets of constraints rather than paths. <bookmark mark='a'/> A constraint satisfaction problem "
            "has variables, each with a domain of values, and constraints that rule out some combinations. "
            "<bookmark mark='b'/> A Sudoku: eighty-one cells, each one to nine, all different in every row, column and box. "
            "<bookmark mark='c'/> Such structure invites propagation: David Waltz used it in 1975 to label the lines of "
            "drawings, and Alan Mackworth gave the general algorithm in 1977."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sud))
            vo.wait_until("c")
            self.play(FadeIn(hcs, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ac3(self):
        d = load("sudoku")
        D0 = [set(range(1, 10)) if not v else {v} for v in d["puzzle"]]
        grid = sudoku_mob(d["puzzle"], D0, cell=0.66, center=[-3.1, -0.15, 0])
        log = [tuple(x) for x in d["ac3_log"]]
        rule = VGroup(label(r"arc $X \to Y$: \ delete every value of $X$ \\ that no value of $Y$ allows", font_size=22,
                            color=FCOL),
                      label(r"if $X$ shrank, \ recheck the arcs into $X$", font_size=22, color=GREY_A))
        rule.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.6, 2.2, 0])
        num = DecimalNumber(0, num_decimal_places=0, font_size=34, color=FCOL)
        cnt = VGroup(label(r"values deleted", font_size=24, color=GREY_A), num).arrange(RIGHT, buff=0.25)
        cnt.move_to([3.6, 0.9, 0])
        sizes = d["ac3_sizes"]
        empty = sum(1 for v in d["puzzle"] if not v)
        left = sum(s for s, v in zip(sizes, d["puzzle"]) if not v)
        res = label(rf"after AC-3: \ ${d['ac3_solved']}$ of ${empty}$ empty cells settled, \\ ${left}$ candidates "
                    r"left", font_size=22, color=GREY_A).move_to([3.6, -0.2, 0])
        names = [(r"plain backtracking", "plain", GREY_B), (r"forward checking", "fc", GCOST),
                 (r"\ + fewest values first (MRV)", "mrv", HEUR), (r"arc consistency at every step (MAC)", "mac", PATH)]
        vals = [d[f"nodes_{k}"] for _, k, _ in names]
        bars = VGroup()
        for (nm, k, col), v in zip(names, vals):
            b = Rectangle(width=max(3.0 * np.log10(v) / np.log10(max(vals)), 0.05), height=0.3, stroke_width=0,
                          fill_color=col, fill_opacity=0.85)
            bars.add(VGroup(label(nm, font_size=18, color=col), VGroup(b, MathTex(f"{v:,}".replace(",", "{,}"),
                                                                                   font_size=22, color=col))))
        for r in bars:
            r[1][1].next_to(r[1][0], RIGHT, buff=0.12)
            r[1].next_to(r[0], DOWN, buff=0.06, aligned_edge=LEFT)
        bars.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([3.6, -2.1, 0])
        bh = label(r"assignments tried \ (log scale)", font_size=18, color=GREY_B).next_to(bars, UP, buff=0.1)
        tag = note(r"computed").to_corner(DR, buff=0.15)
        batches = np.array_split(np.arange(len(log)), 24)
        with self.voiceover(
            "Arc consistency looks at one constraint at a time. <bookmark mark='a'/> For each pair of cells that must differ, "
            "delete any value of the first that the second leaves no room for; when a cell shrinks, recheck its neighbours. "
            "<bookmark mark='b'/> Every clue knocks its value out of its row, column and box, and the deletions cascade. "
            f"<bookmark mark='c'/> AC-3 deletes {len(log)} values and settles {d['ac3_solved']} more cells, but not the puzzle: "
            "propagation alone is not enough here. <bookmark mark='d'/> With search, it is decisive. Plain backtracking in "
            f"reading order tries {vals[0]:,} assignments; forward checking, {vals[1]:,}; also choosing the cell with the fewest "
            f"values left, {vals[2]:,}; full arc consistency after every choice, {vals[3]:,}."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(cnt))
            done = 0
            for bt in batches:
                ms = [grid.cands[log[j]] for j in bt if log[j] in grid.cands]
                done += len(bt)
                self.play(*[FadeOut(m, scale=0.5) for m in ms], num.animate.set_value(done), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.5),
                      run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def strips(self):
        act = VGroup(
            Text("stack(x, y)", font=MONO, font_size=28, color=FCOL),
            VGroup(label(r"pre:", font_size=24, color=GREY_A),
                   Text("holding(x), clear(y)", font=MONO, font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"add:", font_size=24, color=PATH),
                   Text("on(x, y), clear(x), handempty", font=MONO, font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"delete:", font_size=24, color=FAIL),
                   Text("holding(x), clear(y)", font=MONO, font_size=24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-3.2, 1.0, 0])
        box = SurroundingRectangle(act, color=FCOL, buff=0.25, corner_radius=0.1)
        hc = history_card(1971, r"Richard Fikes \& Nils Nilsson: \ STRIPS", r"the planner of Shakey the robot: \ "
                          r"a state is a set of facts; \ an action has preconditions, \ an add list and a delete list",
                          width=5.8, color=HIST, font_size=20).move_to([3.6, 1.6, 0])
        frame = history_card(1969, r"John McCarthy \& Patrick Hayes: \ the frame problem", r"in logic you must also "
                             r"say what an action does \textit{not} change: \ painting a block leaves its position, "
                             r"\ and everything else in the world, alone", width=5.8, color=FAIL,
                             font_size=20).move_to([3.6, -1.2, 0])
        assume = label(r"STRIPS: \ whatever isn't listed stays as it was", font_size=24, color=PATH)
        assume.next_to(box, DOWN, buff=0.4)
        state = VGroup(label(r"a state: \ a set of facts", font_size=24, color=GCOST),
                       Text("on(C, A)  ontable(A)  ontable(B)", font=MONO, font_size=22),
                       Text("clear(C)  clear(B)  handempty", font=MONO, font_size=22))
        state.arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-3.2, -2.5, 0])
        with self.voiceover(
            "Planning is search where the states are descriptions. <bookmark mark='a'/> STRIPS, from Richard Fikes and Nils "
            "Nilsson in 1971, for Shakey the robot, describes a state as a set of facts, and an action by three lists. "
            "<bookmark mark='b'/> To stack x on y you must hold x, and y must be clear; afterwards x is on y, x is clear and the "
            "hand is empty, and you no longer hold x, nor is y clear. <bookmark mark='c'/> Why a delete list? The frame "
            "problem, posed by John McCarthy and Patrick Hayes in 1969: in pure logic, an action must also state everything it "
            "leaves unchanged, which is almost everything. <bookmark mark='d'/> STRIPS simply assumes that whatever an action "
            "doesn't mention stays as it was."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in state], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Create(box), LaggedStart(*[FadeIn(r) for r in act], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(frame, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(assume))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sussman(self):
        d = load("blocks")
        A, B, C = 0, 1, 2
        start = blocks_mob([[A, C], [B]], center=[-4.6, 1.2, 0])
        goal = blocks_mob([[C, B, A]], center=[-4.6, -1.8, 0])
        sl = label(r"start", font_size=24, color=GREY_A).next_to(start, UP, buff=0.15)
        gl = label(r"goal: \ $A$ on $B$, \ $B$ on $C$", font_size=24, color=PATH).next_to(goal, UP, buff=0.15)
        first = VGroup(label(r"$A$ on $B$ first:", font_size=22, color=HEUR),
                       *[Text(s, font=MONO, font_size=20) for s in d["sussman_first"]])
        first.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        second = VGroup(label(r"then $B$ on $C$:", font_size=22, color=HEUR),
                        *[Text(s, font=MONO, font_size=20) for s in d["sussman_second"]])
        second.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        lost = label(r"\ldots which takes $A$ off $B$ again" if not d["sussman_first_kept"] else
                     r"both goals hold", font_size=22, color=FAIL if not d["sussman_first_kept"] else PATH)
        col1 = VGroup(first, second, lost).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-0.6, 0.0, 0])
        plan = VGroup(label(rf"the shortest plan: \ ${len(d['sussman_plan'])}$ steps, \ interleaved", font_size=22,
                            color=PATH), *[Text(s, font=MONO, font_size=20) for s in d["sussman_plan"]])
        plan.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([4.2, 0.4, 0])
        other = ("Doing B on C first fails too: then A can't be freed without taking B off C." if
                 not d["sussman_other_kept"] else "Doing B on C first happens to work here.")
        hc = history_card(1973, r"Gerald Sussman", r"goals that interfere: \ no order of solving them one at a time "
                          r"works", width=4.6, color=HIST, font_size=18).to_corner(DR, buff=0.25)
        tag = note(r"computed: \ breadth-first search").to_corner(DL, buff=0.2)
        with self.voiceover(
            "Early planners solved goals one at a time. Gerald Sussman found the simplest case where that fails. "
            "<bookmark mark='a'/> C sits on A; B is on the table. The goal: A on B, and B on C. <bookmark mark='b'/> Put A on B "
            "first: clear C off A, put it down, stack A on B. Now B must go on C, <bookmark mark='c'/> and moving B means taking "
            "A off again, undoing the first goal. " + other + f" <bookmark mark='d'/> The shortest plan, found by "
            f"breadth-first search, has {len(d['sussman_plan'])} steps and interleaves the two goals."
        ) as vo:
            self.play(FadeIn(start), FadeIn(sl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(goal), FadeIn(gl))
            vo.wait_until("b")
            self.play(FadeIn(first))
            vo.wait_until("c")
            self.play(FadeIn(second), FadeIn(lost))
            vo.wait_until("d")
            self.play(FadeIn(plan), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def planners(self):
        d = load("blocks")
        towers = d["towers"]
        rows = d["rows"]
        summary = planner_summary(rows)
        ns = summary["ns"] or [4, 10]

        def mean(key, n):
            return summary["by_n"].get(n, {}).get(key, {}).get("mean_expanded")

        tab = VGroup(*[VGroup(MathTex(str(n), font_size=26), MathTex(f"{t:,}".replace(",", "{,}"), font_size=26, color=GCOST))
                       .arrange(RIGHT, buff=0.6) for n, t in zip(range(1, len(towers) + 1), towers)])
        tab.arrange(DOWN, buff=0.12, aligned_edge=RIGHT).move_to([-5.3, -0.4, 0])
        th = label(r"blocks \ \ arrangements", font_size=20, color=GREY_A).next_to(tab, UP, buff=0.2)
        n_bfs = summary["n_bfs"]
        largest = max((s["mean_expanded"] for group in summary["by_n"].values() for s in group.values()
                       if s["mean_expanded"] is not None), default=1)
        ymax = max(5, math.ceil(math.log10(max(largest, 1))))
        g = axes([ns[0] - 0.5, ns[-1] + 0.5], [0, ymax], x_length=5.6, y_length=3.8, xlabel=r"blocks",
                 ylabel=r"observed expansions \ (mean, log scale)", xticks=ns, yticks=list(range(ymax + 1)),
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[0.6, -0.3, 0])
        series = (("bfs", GREY_B, r"breadth-first"), ("hmax", GCOST, r"A*, \ $h_{\max}$"),
                  ("ff", PATH, r"greedy, \ FF-style relaxed plans"))
        lines = VGroup()
        for k, col, _ in series:
            xs = [n for n in ns if mean(k, n) is not None]
            ys = [np.log10(max(mean(k, n), 1)) for n in xs]
            lines.add(VGroup(*([curve(g.ax, xs, ys, col, 4)] if len(xs) > 1 else []),
                             *[Dot(g.ax.c2p(x, y), radius=0.05, color=col) for x, y in zip(xs, ys)]))
        lg = legend([(c, t) for _, c, t in series], font_size=21).move_to([5.0, 2.5, 0])
        paired = summary["paired_solved"]
        L_opt, L_ff = summary["paired_bfs_length"], summary["paired_ff_length"]
        relax = label(r"relaxed heuristics: \ ignore delete lists, \\ estimate remaining cost cheaply",
                      font_size=21, color=PATH).move_to([5.0, 1.3, 0])
        cost = label((rf"${paired}$ matched solved problems \\ at ${n_bfs}$ blocks \\ optimal ${L_opt:.1f}$ steps; "
                      rf"greedy ${L_ff:.1f}$" if paired else r"no matched solved problems: \\ plan lengths unavailable"),
                     font_size=21, color=GREY_A).move_to([5.0, 0.2, 0])
        if cost.width > 3.8:
            cost.scale_to_fit_width(3.8)
        counts = summary["all"]
        coverage_rows = VGroup()
        for key, color, name in (("bfs", GREY_B, "BFS"), ("hmax", GCOST, "A*"), ("ff", PATH, "greedy")):
            c = counts[key]
            coverage_rows.add(VGroup(
                label(rf"{name}: ${c['solved']}/{c['attempted']}$", font_size=24, color=color),
                label(rf"${c['unresolved']}$ unresolved; ${c['not_run_or_unknown']}$ not run / unknown",
                      font_size=18, color=FAIL if c["unresolved"] else GREY_A)
            ).arrange(DOWN, buff=0.06))
        coverage_rows.arrange(DOWN, buff=0.17)
        coverage = VGroup(label(rf"all ${len(rows)}$ problems \\ solved / attempted", font_size=20, color=GREY_A),
                          coverage_rows).arrange(DOWN, buff=0.15).move_to([5.0, -1.9, 0])
        hcs = label(r"1995: \ Graphplan (Blum \& Furst) \qquad 2001: \ FF (Hoffmann \& Nebel)",
                    font_size=18, color=HIST).move_to([1.5, -3.65, 0])
        tag = note(rf"computed: \ ${len(rows)}$ random problems")
        tag.to_corner(DL, buff=0.2)
        bfs_n, hm_n, ff_n = mean("bfs", n_bfs), mean("hmax", n_bfs), mean("ff", n_bfs)
        bfs_report = (f"On random {n_bfs}-block problems, breadth-first search records {bfs_n:,.0f} expanded states "
                      "on average." if bfs_n is not None else "No breadth-first expansion work was recorded at this size.")
        hm_report = (f"With h max, the observed mean is {hm_n:,.0f} expanded states." if hm_n is not None else
                     "No h max expansion work was recorded at this size.")
        ff_report = (f"Greedy search records {ff_n:,.0f} expanded states on average." if ff_n is not None else
                     "No greedy expansion work was recorded at this size.")
        length_report = (f"On the {paired} matched problems both breadth-first and greedy solved at {n_bfs} blocks, "
                         f"greedy's mean plan length is {L_ff:.1f} steps against the optimum's {L_opt:.1f}." if paired else
                         "There are no matched solved problems here, so no comparative plan-length mean is available.")
        if not any(c["attempted"] for c in counts.values()):
            coverage_report = "No algorithm attempts are established by these records; no successes are inferred."
        elif not any(c["unresolved"] for c in counts.values()):
            coverage_report = "Every recorded attempt here solved its task; the panel also shows unrun or unknown cases."
        else:
            coverage_report = ("Some recorded attempts ended capped or unresolved. Observed expansion means include those "
                               "unfinished attempts; the panel separates them from solved and unrun or unknown cases.")
        with self.voiceover(
            f"And the search space explodes. <bookmark mark='a'/> {len(towers)} blocks can be stacked {towers[-1]:,} different "
            "ways. <bookmark mark='b'/> " + bfs_report + " <bookmark mark='c'/> The cure is chapter four's idea: "
            "relax the problem. Ignore delete lists, "
            "then compute cheap approximations to the remaining cost; finding the shortest relaxed plan is still NP-hard. "
            "With admissible h max, A* returns an optimal plan when it solves this unit-cost task. " + hm_report +
            " <bookmark mark='d'/> Inspired by "
            "Hoffmann and Nebel's FF planner of 2001, our FF-style heuristic counts distinct actions in an extracted relaxed "
            "plan. " + ff_report + " The matched comparison is this: " + length_report +
            " Check completion as well: " + coverage_report +
            " Such heuristics, Graphplan, and planning as satisfiability made general "
            "planners practical."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(th), LaggedStart(*[FadeIn(t) for t in tab], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(lg[0]))
            vo.wait_until("c")
            self.play(FadeIn(relax), Create(lines[1]), FadeIn(lg[1]))
            vo.wait_until("d")
            self.play(Create(lines[2]), FadeIn(lg[2]), FadeIn(cost), FadeIn(coverage), FadeIn(hcs))
        self.wait(0.3)
        self.clear_scene()
