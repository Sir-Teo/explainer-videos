from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import (FAIL, FCOL, GCOST, HEUR, HIST, LEARN, MONO, PART, PATH, SYMBOL, image_from_rgb,
                                  load, node_box, rgb)


def tape_cells(symbols, cell=0.62, center=ORIGIN):
    g = VGroup()
    for i, s in enumerate(symbols):
        sq = Square(cell, stroke_color=GREY_B, stroke_width=2, fill_color="#141A24", fill_opacity=1)
        sq.move_to([(i - (len(symbols) - 1) / 2) * cell, 0, 0])
        t = Text("" if s == "_" else s, font=MONO, font_size=30, color=WHITE).move_to(sq)
        g.add(VGroup(sq, t))
    return g.move_to(center)


class Turing(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.halting()
        self.beaver()
        self.imitation()
        self.dartmouth()

    def card(self):
        card = chapter_card(1, r"Can machines think?", r"What can a machine compute, and how would we know it thinks?",
                            lit=(1950, 1956), part=PART)
        with self.voiceover("Chapter one. Can machines think?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def machine(self):
        d = load("tm")
        tapes, heads, states = d["inc_tape"], list(d["inc_head"]), list(d["inc_state"])
        rules = d["inc_rules"]
        cell = 0.7
        tape = tape_cells(tapes[0], cell=cell, center=[-2.6, 0.9, 0])

        def head_at(i, st):
            x = tape[i][0].get_center()[0]
            tri = Triangle(color=FCOL, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI)
            tri.move_to([x, tape.get_top()[1] + 0.25, 0])
            lab = MathTex(rf"\text{{state }}{st}", font_size=28, color=FCOL).next_to(tri, UP, buff=0.1)
            return VGroup(tri, lab)

        head = head_at(heads[0], states[0])
        rows = VGroup()
        for s, b, w, m, n in rules:
            b_ = r"\sqcup" if b == "_" else b
            w_ = r"\sqcup" if w == "_" else w
            n_ = r"\text{halt}" if n == "H" else n
            rows.add(MathTex(rf"{s},\ {b_}", r"\;\to\;", rf"{w_},\ {m},\ {n_}", font_size=30))
        rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([4.4, 0.5, 0])
        rhead = label(r"rules: \ state, read $\to$ write, move, next state", font_size=20, color=GREY_A)
        rhead.next_to(rows, UP, buff=0.3)
        if rhead.get_right()[0] > 6.9:
            rhead.shift(LEFT * (rhead.get_right()[0] - 6.9))
        task = label(r"adds one to a number in binary: \ $1011 \to 1100$ \ (eleven $\to$ twelve)", font_size=26,
                     color=GREY_A).move_to([-2.6, -0.9, 0])
        hc = history_card(1936, r"Alan Turing, \textit{On Computable Numbers, with an Application to the "
                                r"Entscheidungsproblem}",
                          r"a tape, a head, a finite table of rules: \ anything a person can compute by rule, "
                          r"\ one machine reading another's table can compute too", width=8.4, color=HIST)
        hc.to_edge(DOWN, buff=0.25)

        def rule_index(i):
            st, sym = states[i], tapes[i][heads[i]]
            for k, (s, b, *_ ) in enumerate(rules):
                if s == st and b == sym:
                    return k
            return None

        with self.voiceover(
            "Before anyone could ask whether machines think, someone had to say what a machine is. Alan Turing did, in 1936. "
            "<bookmark mark='a'/> A tape of cells holding symbols, and a head that reads one cell; <bookmark mark='b'/> and a "
            "finite table of rules: in this state, reading this symbol, write, move left or right, and switch state. "
            "<bookmark mark='c'/> This table adds one to a binary number: watch it carry. <bookmark mark='d'/> Turing argued "
            "that such a machine can compute anything a person can compute by rule, and that one universal machine, reading "
            "another's table from its own tape, can imitate them all: the idea of the stored-program computer."
        ) as vo:
            self.play(FadeIn(tape), FadeIn(head))
            vo.wait_until("b")
            self.play(FadeIn(rhead), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(task))
            hl = None
            for i in range(len(tapes) - 1):
                k = rule_index(i)
                box = SurroundingRectangle(rows[k], color=FCOL, buff=0.08) if k is not None else None
                anims = []
                if box is not None:
                    anims.append(Create(box) if hl is None else Transform(hl, box))
                self.play(*anims, run_time=0.35)
                if hl is None and box is not None:
                    hl = box
                new_tape = tape_cells(tapes[i + 1], cell=cell, center=tape.get_center())
                self.play(Transform(tape, new_tape), Transform(head, head_at(heads[i + 1], states[i + 1])),
                          run_time=0.55)
            vo.wait_until("d")
            self.play(FadeOut(task), FadeIn(hc, shift=UP * 0.2), *([FadeOut(hl)] if hl is not None else []))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def halting(self):
        head = label(r"Can one program decide, for every program and input, whether it ever stops?", font_size=30)
        head.to_edge(UP, buff=0.4)
        rows = [
            cmath(r"\text{suppose }", r"H(P, x)", r"=", r"\text{yes if } P(x) \text{ stops, else no}", font_size=36),
            cmath(r"D(P)", r":", r"\text{if } H(P, P) = \text{yes, loop forever; else stop}", font_size=36),
            cmath(r"D(D) \text{ stops}", r"\iff", r"H(D, D) = \text{no}", r"\iff", r"D(D) \text{ never stops}",
                  font_size=36),
            cmath(r"\Rightarrow", r"\text{no such } H \text{ can exist}", font_size=38, color=FAIL),
        ]
        whys = [why(r"a decider, assumed"), why(r"a contrarian built from it"), why(r"feed $D$ its own text"),
                why(r"contradiction")]
        for r in rows[:3]:
            r[1 if len(r) > 2 else 0].set_color(SYMBOL)
        step = ladder(self, rows, whys, keep=4, top=2.4, align_index=None, x=-0.8)
        tag = note(r"what we now call the halting problem \ (Turing 1936; \ the name came later)")
        church = note(r"the same year, by another route: \ Alonzo Church's $\lambda$-calculus")
        VGroup(church, tag).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_corner(DL, buff=0.25)
        with self.voiceover(
            "Turing also showed what no machine can do. <bookmark mark='a'/> Suppose a program H could take any program P and "
            "input x, and always answer: does P eventually stop on x? <bookmark mark='b'/> Build a contrarian, D: given a "
            "program, D asks H whether it stops when fed its own text, and does the opposite. <bookmark mark='c'/> Now run D on "
            "its own text. It stops exactly when H says it doesn't: exactly when it doesn't stop. <bookmark mark='d'/> So H "
            "cannot exist: no program can decide, in general, whether programs halt. Alonzo Church reached the same limit that "
            "year, by another route."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                step(i)
            self.play(FadeIn(tag), FadeIn(church))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beaver(self):
        d = load("tm")
        st4 = np.asarray(d["bb4_st"], float)
        one, zero = rgb(FCOL), rgb("#1B2130")
        img4 = image_from_rgb(zero[None, None, :] * (1 - st4[..., None]) + one[None, None, :] * st4[..., None],
                              width=1.9, height=5.0)
        img4.move_to([-5.2, -0.35, 0])
        b5 = np.asarray(d["bb5_img"])
        b5 = b5 / max(b5.max(), 1e-9)
        img5 = image_from_rgb(zero[None, None, :] * (1 - b5[..., None]) + one[None, None, :] * b5[..., None],
                              width=3.8, height=5.0, smooth=True)
        img5.move_to([-1.5, -0.35, 0])
        f4, f5 = SurroundingRectangle(img4, buff=0, color=GREY_C, stroke_width=1.5), \
            SurroundingRectangle(img5, buff=0, color=GREY_C, stroke_width=1.5)
        l4 = label(rf"$4$ states: \ ${d['bb4_steps']}$ steps", font_size=22, color=FCOL).next_to(img4, UP, buff=0.15)
        steps5 = f"{d['bb5_steps']:,}"
        l5 = label(rf"$5$ states: \ ${steps5.replace(',', '{,}')}$ steps", font_size=22, color=FCOL)
        l5.next_to(img5, UP, buff=0.15)
        tl = label(r"time $\downarrow$", font_size=20, color=GREY_B).rotate(PI / 2).next_to(img4, LEFT, buff=0.15)
        xl = label(r"the tape $\rightarrow$", font_size=20, color=GREY_B).next_to(img5, DOWN, buff=0.12)
        side = VGroup(
            definition_card(r"the busy beaver", r"of all machines with $n$ states that halt when started on a blank "
                            r"tape, \ the one that runs longest", width=4.2, font_size=21, color=FCOL),
            label(rf"ours: \ halted after ${steps5.replace(',', '{,}')}$ steps, \\ with "
                  rf"${str(d['bb5_ones'])}$ ones on the tape", font_size=21, color=GREY_A),
            label(r"proved the longest in $2024$ \\ (bbchallenge, \ checked in Coq)", font_size=21, color=PATH),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(img5, RIGHT, buff=0.45).set_y(0.2)
        if side.get_right()[0] > 6.95:
            side.shift(LEFT * (side.get_right()[0] - 6.95))
        tag = note(r"computed: \ both champions run to their halts here \ (Brady 1983; \ Marxen \& Buntrock 1990)")
        tag.to_corner(DL, buff=0.2)
        with self.voiceover(
            "The limit appears even in tiny machines. Start one on a blank tape: how long can it run and still halt? The "
            "longest runner is called the busy beaver, Tibor Radó's name, from 1962. <bookmark mark='a'/> The four-state "
            f"champion, run here row by row, halts after {d['bb4_steps']} steps. <bookmark mark='b'/> The five-state champion "
            f"runs {d['bb5_steps']:,} steps; we replayed them in {d['bb5_seconds']:.1f} seconds. <bookmark mark='c'/> Proving "
            "that no five-state machine runs longer took until 2024, and a proof checked by computer. For six states, nobody "
            "knows."
        ) as vo:
            self.play(FadeIn(img4), Create(f4), FadeIn(l4), FadeIn(tl), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(img5), Create(f5), FadeIn(l5), FadeIn(xl), FadeIn(side[0]))
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def imitation(self):
        def person(col, txt):
            body = VGroup(Circle(radius=0.22, color=col, fill_opacity=0.25, stroke_width=2),
                          Arc(radius=0.42, start_angle=PI * 0.15, angle=PI * 0.7, color=col, stroke_width=3)
                          .shift(DOWN * 0.55))
            return VGroup(body, label(txt, font_size=22, color=col).next_to(body, DOWN, buff=0.12))

        judge = person(FCOL, r"interrogator").move_to([-4.6, 0.8, 0])
        a = person(HIST, r"a person").move_to([-0.6, 2.0, 0])
        b = person(LEARN, r"a machine").move_to([-0.6, -0.4, 0])
        wall = DashedLine([-2.4, 2.9, 0], [-2.4, -1.4, 0], color=GREY_C, dash_length=0.12)
        links = VGroup(Arrow(judge.get_right(), a.get_left(), buff=0.25, color=GREY_B, stroke_width=2),
                       Arrow(judge.get_right(), b.get_left(), buff=0.25, color=GREY_B, stroke_width=2))
        typed = label(r"typed messages only", font_size=20, color=GREY_B).next_to(wall, DOWN, buff=0.15)
        hc = history_card(1950, r"Turing, \textit{Computing Machinery and Intelligence}, \textit{Mind}",
                          r"replace ``Can machines think?'' \ by a game: \ can the interrogator tell which is the "
                          r"machine?", width=5.6, color=HIST).move_to([3.9, 1.6, 0])
        pred = label(r"his forecast, for about $2000$: \\ an average interrogator, after five minutes, \\ right no "
                     r"more than $70\%$ of the time", font_size=22, color=GREY_A).move_to([3.9, -0.55, 0])
        res = VGroup(
            label(r"$2025$, \ Jones \& Bergen \ (five-minute, three-party tests):", font_size=22, color=PATH),
            label(r"GPT-4.5 with a persona: \ judged the human $73\%$ of the time", font_size=22, color=PATH),
            label(r"ELIZA, \ from $1966$: \ $23\%$", font_size=22, color=SYMBOL),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([3.9, -2.5, 0])
        if res.get_right()[0] > 6.95:
            res.shift(LEFT * (res.get_right()[0] - 6.95))
        with self.voiceover(
            "In 1950 Turing turned to thinking itself, and proposed a game instead of a definition. <bookmark mark='a'/> An "
            "interrogator exchanges typed messages with two hidden players, a person and a machine, and must say which is "
            "which. <bookmark mark='b'/> He forecast that by about 2000, an average interrogator would be right no more than "
            "seventy percent of the time after five minutes. <bookmark mark='c'/> In 2025 Cameron Jones and Benjamin Bergen ran "
            "the test: GPT-4.5, playing a persona, was judged human seventy-three percent of the time, more often than the real "
            "people. ELIZA, from 1966, managed twenty-three percent."
        ) as vo:
            self.play(FadeIn(judge), FadeIn(a), FadeIn(b), Create(wall), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(GrowArrow(links[0]), GrowArrow(links[1]), FadeIn(typed))
            vo.wait_until("b")
            self.play(FadeIn(pred))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in res], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dartmouth(self):
        quote = label(r"``every aspect of learning or any other feature of intelligence \\ can in principle be so "
                      r"precisely described \\ that a machine can be made to simulate it.''", font_size=30)
        quote.move_to(UP * 2.3)
        src = note(r"McCarthy, Minsky, Rochester \& Shannon, \ proposal for the Dartmouth summer project "
                   r"(31 August 1955)", font_size=20).next_to(quote, DOWN, buff=0.2)
        lt = history_card(1956, r"Newell, Shaw \& Simon: \ the Logic Theorist",
                          r"proved $38$ of the first $52$ theorems of chapter 2 of Whitehead and Russell's "
                          r"\textit{Principia Mathematica}, \ one of them more neatly than the book", width=6.2,
                          color=SYMBOL).move_to([-3.4, -1.0, 0])
        # the Logic Theorist's way: work backward from the goal, a tree of subgoals
        t = {"children": [{"children": [{"children": []}, {"children": []}]}, {"children": [{"children": []}]},
                          {"children": [{"children": []}, {"children": []}]}]}
        tree = SearchTree(t, width=4.4, level_height=0.85, radius=0.1, center=[3.6, -0.75, 0])
        tl = VGroup(label(r"the theorem", font_size=20, color=FCOL).next_to(tree.nodes[0], UP, buff=0.12),
                    label(r"subgoals, \ by rules of inference", font_size=20, color=GREY_A)
                    .next_to(tree, DOWN, buff=0.15))
        win = tree.path_to(len(tree.nodes) - 2)
        pssh = label(r"\textit{A physical symbol system has the necessary and sufficient means for general "
                     r"intelligent action.} \ (Newell \& Simon, 1976)", font_size=22, color=GREY_A)
        pssh.to_edge(DOWN, buff=0.3)
        names = VGroup(*[node_box(n, HIST, font_size=24) for n in
                         (r"John McCarthy", r"Marvin Minsky", r"Nathaniel Rochester", r"Claude Shannon")])
        names.arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        named = label(r"the proposal's name for the field: \ \textbf{artificial intelligence}", font_size=30,
                      color=FCOL).next_to(names, DOWN, buff=0.6)
        shrager = note(r"$2026$: \ the original code, rerun, proves $16$ of $23$ theorems tried (Shrager)",
                       font_size=19).next_to(lt, DOWN, buff=0.15)
        with self.voiceover(
            "Six years later, in the summer of 1956, John McCarthy, Marvin Minsky, Nathaniel Rochester and Claude Shannon "
            "gathered researchers at Dartmouth College, on the conjecture that every aspect of learning or any other feature of "
            "intelligence can in principle be so precisely described that a machine can be made to simulate it. McCarthy's "
            "proposal named the field: artificial intelligence. <bookmark mark='a'/> Allen Newell, Cliff Shaw and Herbert Simon "
            "brought a working program, the Logic Theorist. It proved thirty-eight of the first fifty-two theorems in a chapter "
            "of Principia Mathematica. <bookmark mark='b'/> It worked backward from each theorem to subgoals, choosing by rules "
            "of thumb: a search through a tree of symbols. <bookmark mark='c'/> In 1976 Newell and Simon stated the era's creed: "
            "a physical symbol system has the necessary and sufficient means for general intelligent action."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in names], lag_ratio=0.3), run_time=2.0)
            self.wait(max(0.1, vo.until("a") - 6.0))  # the field's name lands near the end of the sentence
            self.play(FadeIn(named, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(names), FadeOut(named))
            self.play(FadeIn(lt, shift=UP * 0.2), FadeIn(shrager))
            vo.wait_until("b")
            self.play(Create(tree.edge_group), FadeIn(tree.nodes), FadeIn(tl))
            self.play(*[tree.nodes[i].animate.set_color(PATH) for i in win],
                      *[tree.edges[i].animate.set_stroke(PATH, 5) for i in win[1:]])
            vo.wait_until("c")
            self.play(FadeIn(pssh, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()
