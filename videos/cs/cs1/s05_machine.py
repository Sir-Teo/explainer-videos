from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import (COST, CTRL, DATA, HEAD, HIST, NO, PART, YES, history_spacetime, load, replay,
                                  step_counter, tape_from)

SYM_FILL = {"_": "#151B26", "1": C.BIT1, "+": C.CS_DATA}


def mini_row(tape: str, head: int | None, cell=0.3) -> VGroup:
    """A configuration drawn small: coloured cells, the head's cell outlined."""
    g = VGroup()
    for i, c in enumerate(tape):
        sq = Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=SYM_FILL.get(c, GREY_B),
                    fill_opacity=1 if c != "_" else 0.9)
        g.add(sq)
    g.arrange(RIGHT, buff=0)
    if head is not None and 0 <= head < len(tape):
        g.add(Square(cell, stroke_width=2.5, stroke_color=HEAD).move_to(g[head]))
    return g


class Machine(VoiceoverScene):
    def construct(self):
        self.card()
        self.analysis()
        self.definition()
        self.adder()
        self.spacetime()
        self.forever()

    def card(self):
        card = chapter_card(4, r"Turing's machine", r"What exactly is a mechanical procedure?", lit=(1936,), part=PART)
        with self.voiceover("Chapter four. Turing's machine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def analysis(self):
        quote = label(r"``Computing is normally done by writing certain symbols on paper. \\ We may suppose this paper is "
                      r"divided into squares \\ like a child's arithmetic book.''", font_size=28).to_edge(UP, buff=0.35)
        src = note(r"Turing (1936), \S 9", font_size=22).next_to(quote, DOWN, buff=0.15)
        # a page of squared paper with a long multiplication on it
        rows, cols, cs = 5, 12, 0.5
        paper = VGroup(*[Square(cs, stroke_width=1, stroke_color=GREY_D) for _ in range(rows * cols)])
        paper.arrange_in_grid(rows=rows, cols=cols, buff=0).move_to(DOWN * 0.9)
        work = ["      1071", "     x 462", "      2142", "     6426 ", "    4284  "]
        digits = VGroup()
        for r, line in enumerate(work):
            for c, ch in enumerate(line.rjust(cols)):
                if ch.strip():
                    t = Text(ch, font="DejaVu Sans Mono", font_size=22, color=DATA if ch.isdigit() else GREY_A)
                    digits.add(t.move_to(paper[r * cols + c]))
        gaze = Square(cs, stroke_width=3.5, stroke_color=HEAD).move_to(paper[2 * cols + 7])
        rules = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"finitely many kinds of symbol", DATA),
            (r"looks at one square at a time", HEAD),
            (r"finitely many states of mind", CTRL),
            (r"each step: \ change the symbol, \ move to a neighbouring square, \ change state of mind", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Turing's definition came from looking at a person computing. <bookmark mark='a'/> Computing, he wrote, is "
            "normally done by writing symbols on paper, and we may suppose the paper is divided into squares, like a "
            "child's arithmetic book. <bookmark mark='b'/> What does the person actually do? <bookmark mark='c'/> They "
            "write symbols from some finite stock. <bookmark mark='d'/> They attend to only a few squares at a time; "
            "with a little more bookkeeping, to one. <bookmark mark='e'/> They have only finitely many states of mind "
            "that matter: remembering a carry, say. <bookmark mark='f'/> And each step is simple: change the symbol "
            "they are looking at, move their attention to a nearby square, and perhaps change their state of mind."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(src))
            vo.wait_until("b")
            self.play(Create(paper, lag_ratio=0.01), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(d) for d in digits], lag_ratio=0.03), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(rules[0]))
            vo.wait_until("d")
            self.play(FadeIn(gaze), FadeIn(rules[1]))
            vo.wait_until("e")
            self.play(FadeIn(rules[2]))
            vo.wait_until("f")
            self.play(FadeIn(rules[3]), gaze.animate.shift(RIGHT * cs))
        # the page collapses to one row: a tape
        tape = TapeView(list("__1071x462__"), head=6, state="q", cell=0.58, font_size=26).move_to(DOWN * 0.6)
        cap = label(r"two dimensions add nothing essential: \ one row of squares, \ the \textbf{tape}", font_size=30,
                    color=GREY_A).next_to(tape, DOWN, buff=0.6)
        with self.voiceover(
            "Turing then argued that nothing essential is lost if we simplify further. The page can be one long row of "
            "squares, a tape, unlimited in both directions. The person's attention becomes a head, sitting on one "
            "square. Their state of mind becomes one of finitely many states. What remains is a machine."
        ):
            self.play(FadeOut(rules), FadeOut(gaze), ReplacementTransform(VGroup(paper, digits), tape), run_time=2.2)
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        body = VGroup(
            label(r"a finite set of \textbf{states} $Q$, \ with a start state and halting states;", font_size=28,
                  color=GREY_A),
            label(r"a finite tape \textbf{alphabet} $\Gamma$, \ including a blank $\square$; \ and a "
                  r"\textbf{transition function}", font_size=28, color=GREY_A),
            cmath(r"\delta", r":\ ", r"Q \times \Gamma", r"\to", r"\Gamma \times \{\mathrm{L}, \mathrm{R}\} \times Q",
                  font_size=40, colors={r"\delta": CTRL}),
            label(r"in state $q$ reading $a$, \ with $\delta(q, a) = (b, d, q')$: \ write $b$, \ move one square "
                  r"in direction $d$, \ go to state $q'$", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        body[2].set_x(body.get_x())
        defn = definition_card(r"Turing machine", body, color=CTRL, width=11.6, font_size=30).move_to(UP * 0.9)
        conf = definition_card(r"Configuration", r"everything about the machine at one instant: \ its state, \ the tape's "
                               r"contents, \ and the head's position. \ A run is a sequence of configurations.",
                               color=HEAD, width=11.0, font_size=24, kind=r"Definition").next_to(defn, DOWN, buff=0.35)
        with self.voiceover(
            "Here it is, written precisely. A Turing machine has a finite set of states, including a start state and "
            "one or more halting states, and a finite alphabet of tape symbols, including a blank. Its whole behaviour "
            "is one table, the transition function. <bookmark mark='a'/> In state q, reading symbol a, the table gives "
            "three things: a symbol to write, a direction to move, and the next state. <bookmark mark='b'/> A "
            "configuration is a snapshot: the state, the tape, and where the head is. Running the machine means applying "
            "the table to get from each configuration to the next, until it reaches a halting state, if it ever does."
        ) as vo:
            self.play(FadeIn(defn, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(body[2], color=CTRL, scale_factor=1.06))
            vo.wait_until("b")
            self.play(FadeIn(conf, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def adder(self):
        d = load("adder")
        hist = d["history"]
        lo = d["lo"]
        head = label(r"A machine that adds: \ $3 + 2$ in unary", font_size=38).to_edge(UP, buff=0.35)
        view = tape_from(hist[0], lo, cell=0.7, font_size=32).move_to(UP * 1.1)
        rules = RuleTable(d["rules"], font_size=24).scale(0.95).move_to(DOWN * 1.9 + LEFT * 2.3)
        roles = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (
            r"$A$: \ walk right over the first number",
            r"$A$: \ at the $+$, \ write a $1$ \ (now one too many)",
            r"$B$: \ walk right over the second number",
            r"$B$: \ at the end, \ step back",
            r"$C$: \ erase the last $1$, \ and halt",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for r_, row in zip(roles, rules.rule_rows):
            r_.set_y(row.get_y())
        roles.next_to(rules, RIGHT, buff=0.5)
        cnt = step_counter().to_corner(UR, buff=0.4).shift(DOWN * 0.7)
        with self.voiceover(
            "Let's program one. Numbers in unary: three is one one one. <bookmark mark='a'/> On the tape, three, a "
            "plus sign, two. The head starts on the first square, in state A. <bookmark mark='b'/> The program is five "
            "rules. <bookmark mark='c'/> In state A, walk right over the ones. At the plus sign, write a one instead, and "
            "switch to state B. That joins the two numbers, with one one too many. <bookmark mark='d'/> In state B, walk "
            "right to the end, step back, and in state C erase the last one, and halt."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(view))
            vo.wait_until("b")
            self.play(FadeIn(rules))
            vo.wait_until("c")
            self.play(FadeIn(roles[:2]))
            vo.wait_until("d")
            self.play(FadeIn(roles[2:]), FadeIn(cnt))
        with self.voiceover(
            f"Now run it, one step at a time. Each step: find the rule for the current state and symbol, write, move, "
            f"change state. <bookmark mark='a'/> After {d['steps']} steps the machine halts with five ones on the tape. "
            f"Three plus two is five, and nothing in the machine knows what a number is."
        ) as vo:
            replay(self, view, hist, lo, table=rules, per_step=1.15, counter=cnt.num)
            self.play(rules.light(None))
            vo.wait_until("a")
            ones = VGroup(*[view.syms[i] for i, c in enumerate(hist[-1]["tapes"][0]) if c == "1"])
            br = Brace(ones, DOWN, color=YES)
            five = label(r"$5$", font_size=40, color=YES).next_to(br, DOWN, buff=0.1)
            self.play(GrowFromCenter(br), FadeIn(five))
        self.adder_view = (view, hist, lo)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spacetime(self):
        d = load("adder")
        hist, lo = d["history"], d["lo"]
        head = label(r"A run as a picture", font_size=38).to_edge(UP, buff=0.35)
        rows = VGroup(*[mini_row(e["tapes"][0], e["heads"][0] - lo, cell=0.36) for e in hist])
        rows.arrange(DOWN, buff=0.04).move_to(LEFT * 2.2 + DOWN * 0.4)
        t_arrow = Arrow(rows.get_corner(UL) + LEFT * 0.4, rows.get_corner(DL) + LEFT * 0.4, buff=0, color=GREY_B,
                        stroke_width=3)
        t_lab = label(r"time", font_size=24, color=GREY_B).next_to(t_arrow, LEFT, buff=0.12)
        x_lab = label(r"tape cells $\longrightarrow$", font_size=24, color=GREY_B).next_to(rows, UP, buff=0.2)
        legend_ = VGroup(*[VGroup(Square(0.3, stroke_width=0.8, stroke_color=GREY_D, fill_color=c, fill_opacity=1),
                                  label(t, font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.15)
                           for c, t in ((SYM_FILL["1"], r"a $1$"), (SYM_FILL["+"], r"the $+$"),
                                        (SYM_FILL["_"], r"blank"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        hl = VGroup(Square(0.3, stroke_width=2.5, stroke_color=HEAD), label(r"the head", font_size=22,
                                                                             color=GREY_A)).arrange(RIGHT, buff=0.15)
        legend_.add(hl)
        legend_.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.6 + UP * 0.6)
        txt = label(r"each row is one configuration; \\ the head's path is the machine's \textit{trace}", font_size=26,
                    color=GREY_A).next_to(legend_, DOWN, buff=0.5)
        with self.voiceover(
            "There is a better way to see a whole run at once. Draw each configuration as a row of coloured squares, "
            "and stack the rows, so that time runs down the page. <bookmark mark='a'/> The head's square is outlined. "
            "You can read the program off the picture: a march to the right across the ones, the plus turning into a "
            "one, the turn at the end, the last one erased. <bookmark mark='b'/> This space-time diagram will let us "
            "look at runs of millions of steps, where watching one step at a time would take years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(x_lab))
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in rows], lag_ratio=0.25), GrowArrow(t_arrow),
                      FadeIn(t_lab), run_time=2.6)
            vo.wait_until("a")
            self.play(FadeIn(legend_))
            vo.wait_until("b")
            self.play(FadeIn(txt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forever(self):
        head = label(r"Nothing forces a machine to stop", font_size=38).to_edge(UP, buff=0.35)
        rule = RuleTable([("A", "_", "_", "R", "A")], font_size=26).move_to(UP * 1.4)
        view = TapeView(["_"] * 14, head=2, state="A", cell=0.62).move_to(DOWN * 0.3)
        cnt = step_counter().to_corner(DR, buff=0.5)
        diag = VGroup(*[mini_row("_" * 14, 2 + k, cell=0.2) for k in range(9)]).arrange(DOWN, buff=0.02)
        diag.next_to(view, DOWN, buff=0.4)
        with self.voiceover(
            "One more machine, the simplest possible. One rule: in state A, reading a blank, write a blank, move right, "
            "stay in state A. <bookmark mark='a'/> It never reaches a halting state. It walks right forever, and its "
            "space-time diagram is a diagonal line that never ends. <bookmark mark='b'/> A Turing machine may halt, or "
            "it may run forever, and the table alone does not announce which. That gap, between running and halting, is "
            "where the whole second half of this part lives."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule), FadeIn(view), FadeIn(cnt))
            self.play(rule.light(0), run_time=0.3)
            vo.wait_until("a")
            for k in range(9):
                self.play(view.step("_", 1, "A", run_time=0.45), cnt.tracker.animate(run_time=0.45).set_value(k + 1))
            self.play(LaggedStart(*[FadeIn(r) for r in diag], lag_ratio=0.15), run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(rule, color=NO, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
