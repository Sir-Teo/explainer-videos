from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)

PRODS = ["E' → E", "E → E + T", "E → T", "T → T * F", "T → F", "F → ( E )", "F → id"]


def act(a):
    if a[0] == "s":
        return f"shift, go to {a[1]}"
    if a[0] == "r":
        return f"reduce {PRODS[a[1]]}"
    return "accept"


class BottomUp(VoiceoverScene):
    def construct(self):
        self.card()
        self.shift_reduce()
        self.items()
        self.family()
        self.tools()

    def card(self):
        card = chapter_card(13, r"Bottom-up parsing", r"Can a parser decide \textit{after} seeing the whole phrase?",
                            lit=(1965, 1975), extra=((1965, r"Knuth: \ LR($k$)"), (1975, r"Johnson: \ yacc")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Bottom-up parsing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shift_reduce(self):
        lr = load("lr")
        head = label(r"Shift and reduce: \ \texttt{id * id + id}", font_size=34).to_edge(UP, buff=0.3)
        rows = [[" ".join(map(str, s["stack"])), " ".join(s["symbols"]), " ".join(s["input"]), act(s["action"])]
                for s in lr["trace"]]
        t = grid_table([r"states", r"symbols", r"input", r"action"], rows, [2.4, 2.4, 3.2, 3.8], row_h=0.36,
                       font_size=15, colors=[[GREY_B, CTRL, CODE, YES]] * len(rows), mono_cols=(0, 1, 2, 3)).next_to(
            head, DOWN, buff=0.3)
        pts = VGroup(
            label(r"\textbf{shift}: \ move the next token onto the stack", font_size=19, color=GREY_A),
            label(r"\textbf{reduce}: \ the top of the stack is a complete right side: \ replace it by its left side",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A top-down parser must choose a rule before it has seen the phrase. A bottom-up parser waits until it "
            "has seen all of it. <bookmark mark='a'/> It has two moves. Shift: push the next token onto a stack. "
            "Reduce: when the top of the stack is the complete right side of a rule, replace it by the rule's left "
            "side. <bookmark mark='b'/> Watch id times id plus id. Shift id, and reduce it to F, then to T. Now "
            "the next token is times: shift it, and the second id, and reduce T times F to T. <bookmark mark='c'/> "
            "Then the plus comes: reduce T to E, shift, and reduce the last id all the way up, until the stack "
            "holds a single E and the input is empty. Read backwards, the reductions are a rightmost derivation; "
            "the parser built the tree from the leaves up. <bookmark mark='d'/> The hard part is knowing when to "
            "reduce, and by which rule. That is what the numbers on the stack are for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(FadeIn(pts))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, 8)], lag_ratio=0.5), run_time=6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(8, len(t.cells))], lag_ratio=0.5),
                      run_time=4)
            vo.wait_until("d")
            self.play(Indicate(VGroup(*[t.cells[r][0] for r in range(1, len(t.cells))]), color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def items(self):
        lr = load("lr")
        st = lr["lr0"]["states"]
        conf = {c[0] for c in lr["lr0"]["conflicts"]}
        head = label(r"The LR(0) automaton: \ 12 states of items", font_size=34).to_edge(UP, buff=0.3)
        boxes = VGroup()
        for k, items in enumerate(st):
            c = NO if k in conf else CTRL
            txt = VGroup(*[Text(i, font="DejaVu Sans Mono", font_size=15, color=GREY_A) for i in items]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04)
            r = SurroundingRectangle(txt, buff=0.1, color=c, stroke_width=1.5, corner_radius=0.06)
            num = Text(str(k), font="DejaVu Sans Mono", font_size=14, color=c).next_to(r, UP, buff=0.04).align_to(
                r, LEFT)
            boxes.add(VGroup(r, txt, num))
        boxes.arrange_in_grid(3, 4, buff=(0.35, 0.3), cell_alignment=UP).next_to(head, DOWN, buff=0.3)
        if boxes.width > 13.4:
            boxes.scale_to_fit_width(13.4)
        if boxes.height > 4.7:
            boxes.scale_to_fit_height(4.7)
        boxes.next_to(head, DOWN, buff=0.3)
        pts = VGroup(
            label(r"an item: \ a rule with a dot, \ how much of it is on the stack; \ a state: \ every item that could "
                  r"be in progress", font_size=19, color=GREY_A),
            label(r"the stack of state numbers is a path through this automaton: \ a DFA over the stack", font_size=19,
                  color=YES),
            label(r"states 5 and 10, \ in red: \ ``reduce $E \to T$'' \ or \ ``shift \texttt{*}''? \ LR(0) cannot "
                  r"tell", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        transitions = {(a, symbol): b for a, symbol, b in lr["lr0"]["trans"]}
        path_states = [0]
        for symbol in ["T", "*", "F"]:
            path_states.append(transitions[path_states[-1], symbol])
        path = StateDiagram({str(q): (x, -1.8) for q, x in zip(path_states, [-4.1, -1.4, 1.3, 4.0])},
                            [(str(a), str(b), symbol, 0) for a, b, symbol in
                             zip(path_states, path_states[1:], ["T", "*", "F"])],
                            radius=.2, font_size=16, edge_font=16, color=YES)
        # The hidden glow starts at the origin; use only visible nodes/edges for layout.
        path_layout = VGroup(path.edges, path.nodes)
        path.shift(UP * (boxes.get_bottom()[1] - 0.18 - path_layout.get_top()[1]))
        with self.voiceover("LR items make the shift-or-reduce decision mechanical. <bookmark mark='a'/> An item is a production with a dot marking progress. Each state collects items that can be active together; this grammar has twelve such states. <bookmark mark='b'/> Read a viable stack prefix through the automaton. The connected example follows T, then star, then F; the state numbers under the item boxes are the corresponding stack path. The current state summarizes what prefixes can follow. <bookmark mark='c'/> In the two red states, a completed E-to-T item requests reduction, while another item permits shifting star. LR zero supplies no lookahead to distinguish those actions, so the table has conflicts.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(boxes[0]), FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[1:]], lag_ratio=0.15), run_time=3)
            vo.wait_until('b')
            self.play(FadeIn(pts[1]), FadeIn(path))
            for state in path_states:
                self.play(Indicate(boxes[state], color=YES), run_time=0.4)
            vo.wait_until('c')
            self.play(FadeIn(pts[2]), *[Indicate(boxes[k], color=NO) for k in conf])
        self.wait(0.3)
        self.clear_scene()

    def family(self):
        lr = load("lr")
        head = label(r"Lookahead: \ SLR, \ LR(1), \ LALR", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"LR(0)", r"no lookahead", str(lr["lr0_states"]), str(len(lr["lr0"]["conflicts"]))],
                [r"SLR \ (DeRemer, \ 1971)", r"reduce only on FOLLOW", str(lr["lr0_states"]), str(lr["slr"]["conflicts"])],
                [r"LR(1) \ (Knuth, \ 1965)", r"each item carries its lookahead", str(lr["lr1_states"]), "0"],
                [r"LALR \ (DeRemer, \ 1969)", "LR(1) states with equal LR(0) cores merged", str(lr["lalr_states"]), "0"]]
        t = grid_table([r"method", r"how it decides", r"states", r"conflicts"], rows, [3.4, 4.6, 1.5, 1.8],
                       row_h=0.55, font_size=20, colors=[[HEAD, GREY_A, CTRL, NO]] * 4, mono_cols=()).next_to(
            head, DOWN, buff=0.4)
        lslr = VGroup(Text("S → L = R | R    L → * R | id    R → L", font="DejaVu Sans Mono", font_size=19,
                           color=CODE),
                      label(rf"SLR: \ a shift/reduce conflict on \texttt{{=}}; \ LALR: \ none, \ in "
                            rf"{lr['lslr_lalr_states']} states", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.12)
        lslr.next_to(t, DOWN, buff=0.45)
        sw = label("LALR merges LR(0) cores: fewer states than LR(1), but merging can introduce conflicts",
                   font_size=21, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Lookahead can resolve these conflicts. <bookmark mark='a'/> SLR allows a reduction only when the "
            "next token belongs to FOLLOW of the rule's left side. In this expression grammar, that removes the "
            "LR zero conflicts. <bookmark mark='b'/> Canonical LR one attaches lookahead to items. This example "
            "grows from twelve states to twenty-two. With standard end-marker conventions, LR grammars "
            "characterize deterministic context-free languages, but not every grammar describing such a language "
            "is already LR one. <bookmark mark='c'/> LALR merges canonical states with the same LR zero core and "
            "combines lookaheads. It returns this example to twelve states, and handles the assignment grammar "
            "that defeats SLR. Merging can introduce conflicts in other grammars that canonical LR one handles. "
            "<bookmark mark='d'/> Yacc popularized LALR. Bison supports LALR and other construction modes; the "
            "comparison here uses the selected LALR configuration rather than a claim about every Bison "
            "invocation."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule), FadeIn(VGroup(*t.cells[1])))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*t.cells[4])), FadeIn(lslr))
            vo.wait_until("d")
            self.play(FadeIn(sw))
        self.wait(0.3)
        self.clear_scene()

    def tools(self):
        lr = load("lr")
        b = lr["bison"]
        head = label(r"Checked against bison \ (this machine)", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"expressions \ $E, T, F$", str(lr["lalr_states"]), str(b["expr"]["states"]), r"none"],
                [r"assignments \ $S \to L = R$", str(lr["lslr_lalr_states"]), str(b["lslr"]["states"]), r"none"],
                [r"the dangling \texttt{else}", str(lr["dangling_states"]), str(b["dangling"]["states"]),
                 r"1 shift/reduce, \ both"]]
        t = grid_table([r"grammar", r"our LALR states", r"bison's states", r"conflicts"], rows, [3.8, 2.4, 2.4, 3.2],
                       row_h=0.6, font_size=20, colors=[[GREY_A, YES, CTRL, NO]] * 3, mono_cols=()).next_to(
            head, DOWN, buff=0.5)
        note_ = label(r"bison adds one state of its own: \ after shifting the end-of-input marker", font_size=20,
                      color=GREY_B).next_to(t, DOWN, buff=0.3)
        dang = VGroup(
            label(r"the conflict is the dangling \texttt{else}: \ reduce the inner \texttt{if}, \ or shift the "
                  r"\texttt{else}?", font_size=20, color=GREY_A),
            label(r"yacc and bison choose \textit{shift}: \ the \texttt{else} binds to the nearest \texttt{if}, \ "
                  r"exactly C's rule", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            (
            "Bison supplies an external cross-check on these grammar tables. <bookmark mark='a'/> In the selected "
            "configurations, its state counts are one above ours because of its extra end-of-input acceptance "
            "state. Agreement in counts is useful evidence, but does not by itself prove the transition tables "
            "are identical. <bookmark mark='b'/> On the dangling-else grammar, both tools report one shift-reduce "
            "conflict. <bookmark mark='c'/> With else as lookahead, reducing the inner if competes with shifting "
            "else. Bison's default shift resolution attaches it to the nearest unmatched if. A language can "
            "express that convention through grammar design, parser precedence or other specification rules; the "
            "ambiguous grammar alone allows both trees."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t.cells[1])), FadeIn(VGroup(*t.cells[2])), FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(dang))
        self.wait(0.3)
        self.clear_scene()
