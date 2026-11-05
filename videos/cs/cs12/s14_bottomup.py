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
        with self.voiceover(
            "Donald Knuth showed in 1965 how to make the decision mechanical. <bookmark mark='a'/> An item is a "
            "rule with a dot in it, marking how much of the rule is already on the stack. A state is the set of "
            "all items that could be in progress at once. For our grammar there are twelve states. <bookmark "
            "mark='b'/> The remarkable fact is that the stack can be tracked by a finite automaton: the numbers on "
            "the stack are a path through these states, and the state on top says what to do. <bookmark mark='c'/> "
            "But in two of them, shown in red, a T has just been completed, and the machine cannot tell whether to "
            "reduce it, or to shift a times sign that may follow. Using no lookahead, LR zero, the grammar has "
            "conflicts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(pts[0]))
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[1:]], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), *[Indicate(boxes[k], color=NO) for k in conf])
        self.wait(0.3)
        self.clear_scene()

    def family(self):
        lr = load("lr")
        head = label(r"Lookahead: \ SLR, \ LR(1), \ LALR", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"LR(0)", r"no lookahead", str(lr["lr0_states"]), str(len(lr["lr0"]["conflicts"]))],
                [r"SLR \ (DeRemer, \ 1971)", r"reduce only on FOLLOW", str(lr["lr0_states"]), str(lr["slr"]["conflicts"])],
                [r"LR(1) \ (Knuth, \ 1965)", r"each item carries its lookahead", str(lr["lr1_states"]), "0"],
                [r"LALR \ (DeRemer, \ 1969)", r"LR(1), \ states with equal items merged", str(lr["lalr_states"]), "0"]]
        t = grid_table([r"method", r"how it decides", r"states", r"conflicts"], rows, [3.4, 4.6, 1.5, 1.8],
                       row_h=0.55, font_size=20, colors=[[HEAD, GREY_A, CTRL, NO]] * 4, mono_cols=()).next_to(
            head, DOWN, buff=0.4)
        lslr = VGroup(Text("S → L = R | R    L → * R | id    R → L", font="DejaVu Sans Mono", font_size=19,
                           color=CODE),
                      label(rf"SLR: \ a shift/reduce conflict on \texttt{{=}}; \ LALR: \ none, \ in "
                            rf"{lr['lslr_lalr_states']} states", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.12)
        lslr.next_to(t, DOWN, buff=0.45)
        sw = label(r"LALR: \ almost all the power of LR(1), \ in the size of LR(0) \ --- \ what yacc and bison build",
                   font_size=21, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The cure is to look at the next token before deciding. <bookmark mark='a'/> The simplest version, "
            "SLR, reduces by a rule only if the next token can follow the rule's left side. After a T, a times "
            "sign cannot follow an E, so the conflict disappears. <bookmark mark='b'/> Knuth's full method, LR one, "
            "carries a lookahead token inside every item. It handles every deterministic context-free language, "
            "but even this small grammar grows from twelve states to twenty-two, and real languages to thousands. "
            "<bookmark mark='c'/> Frank DeRemer's LALR merges the LR one states that contain the same items, "
            "getting back to twelve. It is strictly stronger than SLR: this grammar for assignments through "
            "pointers defeats SLR, but not LALR. <bookmark mark='d'/> LALR is the method yacc made famous in 1975, "
            "and bison still uses it today."
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
            "We checked our parser generator against bison, on this computer. <bookmark mark='a'/> For each "
            "grammar, bison builds exactly one state more than ours, an extra state it uses after shifting the end "
            "of input. <bookmark mark='b'/> And on the dangling else, both report the same single shift-reduce "
            "conflict. <bookmark mark='c'/> The conflict is the ambiguity from chapter nine: with an else coming "
            "after an inner if, reduce the if, or shift the else? Bison resolves it by shifting, which attaches the "
            "else to the nearest if: exactly the rule C uses."
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
