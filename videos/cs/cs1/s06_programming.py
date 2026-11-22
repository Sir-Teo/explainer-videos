from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import (COST, CTRL, DATA, HEAD, NO, PART, YES, load, spacetime_mob, step_counter,
                                  tape_from)

NODES = {"start": (-3.6, 0.0), "acc1": (-3.6, 2.0), "have0": (-1.3, 1.5), "have1": (-1.3, -1.5),
         "want0": (1.5, 1.5), "want1": (1.5, -1.5), "back": (0.1, 0.0), "acc2": (3.9, 0.0), "rej0": (3.9, 2.3),
         "rej1": (3.9, -2.3)}
NAMES = {"start": "start", "acc1": "acc", "have0": "have0", "have1": "have1", "want0": "want0", "want1": "want1",
         "back": "back", "acc2": "acc", "rej0": "rej", "rej1": "rej"}
B = "□"
EDGES = [("start", "have0", f"0→{B},R", 0), ("start", "have1", f"1→{B},R", 0), ("start", "acc1", f"{B}", 0),
         ("have0", "have0", "0,1: R", UP), ("have1", "have1", "0,1: R", DOWN),
         ("have0", "want0", f"{B}: L", 0), ("have1", "want1", f"{B}: L", 0),
         ("want0", "back", f"0→{B},L", 0), ("want1", "back", f"1→{B},L", 0),
         ("back", "back", "0,1: L", UP), ("back", "start", f"{B}: R", 0),
         ("want0", "acc2", f"{B}", 0), ("want1", "acc2", f"{B}", 0),
         ("want0", "rej0", "1", 0), ("want1", "rej1", "0", 0)]


def node_of(state: str, pos: int, n: int) -> str:
    if state == "accept":
        return "acc1" if pos <= 0 else "acc2"
    if state == "reject":
        return "rej0"
    return state


class Programming(WatchScene):
    def construct(self):
        self.card()
        self.problem()
        self.run_it()
        self.cost()

    def card(self):
        self.chapter(5, r"Programming with a table", r"How do you write a program with nothing but rules?", lit=(1936,), part=PART, said="Chapter five. Programming with a table.")

    # ------------------------------------------------------------------
    def problem(self):
        head = label(r"Is the input a palindrome?", font_size=42).to_edge(UP, buff=0.4)
        exs = VGroup(*[VGroup(TapeView(list(w), head=None, state=None, cell=0.5, font_size=24, ellipsis=False),
                              label(r"yes" if w == w[::-1] else r"no", font_size=28, color=YES if w == w[::-1] else NO))
                       .arrange(RIGHT, buff=0.4) for w in ("0110", "1001001", "0111")]).arrange(DOWN, buff=0.3,
                                                                                                aligned_edge=LEFT)
        exs.move_to(UP * 1.0)
        plan = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"1. \ erase the first symbol, \ and \textit{remember} it", CTRL),
            (r"2. \ run to the far end", GREY_A),
            (r"3. \ check the last symbol matches; \ erase it", GREY_A),
            (r"4. \ run back, \ and repeat until nothing is left", GREY_A),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.9)
        with self.voiceover(
            "A harder program. Given a string of zeros and ones, decide whether it is a palindrome: the same read "
            "forwards and backwards. <bookmark mark='a'/> Zero one one zero, yes. One zero zero one zero zero one, yes. "
            "Zero one one one, no. <bookmark mark='b'/> A plan a person might follow: erase the first symbol and remember "
            "it; run to the far end; check that the last symbol is the same, and erase it; run back; repeat until "
            "nothing is left. <bookmark mark='c'/> The tricky word is remember. The machine has no memory except the "
            "tape and its state."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.2) for e in exs], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in plan], lag_ratio=0.35), run_time=2.4)
            vo.wait_until("c")
            self.play(Indicate(plan[0], color=CTRL))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run_it(self):
        d = load("palindrome")
        hist = d["run1_0110"]
        lo = -1
        sd = StateDiagram(NODES, EDGES, names=NAMES, accept=("acc1", "acc2"), reject=("rej0", "rej1"),
                          radius=0.45, font_size=20, edge_font=17).scale(0.88).move_to(UP * 0.7 + RIGHT * 0.5)
        key = VGroup(label(r"$\mathtt{have0}$: \ ``I erased a 0''", font_size=27, color=CTRL),
                     label(r"$\mathtt{want0}$: \ ``the last symbol must be 0''", font_size=27, color=CTRL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.3)
        with self.voiceover(
            "So the memory goes into the state. Here is the whole program as a diagram: each circle is a state, each "
            "arrow a rule, labelled with the symbol read, and what to write and which way to move. "
            "<bookmark mark='a'/> State have zero means: I erased a zero, and I am carrying that fact to the far end. "
            "Have one is its twin. <bookmark mark='b'/> At the end, want zero checks that the last symbol is a zero, "
            "erases it, and hands over to back, which returns to the start. <bookmark mark='c'/> Any mismatch goes to "
            "reject. Running out of symbols goes to accept. Eight working states, eighteen rules."
        ) as vo:
            self.play(FadeIn(sd.nodes), run_time=1.0)
            self.play(LaggedStart(*[Create(e[0]) for e in sd.edge], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(e[1]) for e in sd.edge], lag_ratio=0.08), run_time=2.4)
            vo.wait_until("a")
            self.play(FadeIn(key[0]), Indicate(sd.node["have0"], color=HEAD), Indicate(sd.node["have1"], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(key[1]), Indicate(sd.node["want0"], color=HEAD), Indicate(sd.node["back"], color=HEAD))
            vo.wait_until("c")
            self.play(*[Indicate(sd.node[k], color=HEAD) for k in ("acc1", "acc2", "rej0", "rej1")])
        view = tape_from(hist[0], lo, cell=0.6, font_size=28).move_to(DOWN * 2.95)
        cnt = step_counter().to_corner(DR, buff=0.35)
        with self.voiceover(
            f"Run it on zero one one zero. Watch the lit state carry the erased symbol across the tape. "
            f"<bookmark mark='a'/> First pass: erase the zero, carry it to the end, match it, erase it, come back. "
            f"<bookmark mark='b'/> Second pass: the same for the ones. <bookmark mark='c'/> Nothing left: accept, after "
            f"{len(hist) - 1} steps."
        ) as vo:
            self.play(FadeIn(view), FadeIn(cnt), sd.light("start"))
            marks = {7: "a", 12: "b"}
            for i in range(len(hist) - 1):
                a, b = hist[i], hist[i + 1]
                if i in marks:
                    vo.wait_until(marks[i])
                move = b["heads"][0] - a["heads"][0]
                new = b["tapes"][0][a["heads"][0] - lo]
                self.play(view.step(new, move, b["state"], run_time=0.75),
                          sd.light(node_of(b["state"], b["heads"][0], 4), run_time=0.4),
                          cnt.tracker.animate(run_time=0.75).set_value(i + 1))
            vo.wait_until("c")
            self.play(Indicate(sd.node["acc1"], color=YES, scale_factor=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        self.ask(r"Double the length of the input. \\ How many more steps does the palindrome check take?",
                 [r"twice as many", r"four times as many", r"eight times as many"], 1,
                 say="Double the length of the string. How many more steps does the palindrome machine need?",
                 reveal="Four times as many: the steps grow like the square of the length.")
        d = load("palindrome")
        st = np.asarray(d["st_long"])
        n = len(d["long"])
        img = spacetime_mob(st, width=3.0, height=5.6).move_to(LEFT * 4.6 + DOWN * 0.3)
        frame = SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1)
        cap = label(rf"one tape, \ $n = {n}$: \ {fmt_(d['long_steps'])} steps", font_size=24, color=GREY_A)
        cap.next_to(img, UP, buff=0.2)
        t_lab = label(r"time $\downarrow$", font_size=22, color=GREY_B).next_to(img, LEFT, buff=0.12)
        ns, one = np.array(d["n"], float), np.array(d["one"], float)
        ax = CornerAxes(x_range=[0, 60, 10], y_range=[0, 1900, 500], x_length=6.2, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_numbers": True, "font_size": 20})
        ax.move_to(RIGHT * 2.6 + DOWN * 0.3)
        xl = label(r"length of the input, $n$", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yl = label(r"steps", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.035, color=COST) for x, y in zip(ns, one)])
        a, b = d["fit_one"]
        fit = ax.plot(lambda x: a * x * x + b * x, x_range=[1, 60], color=WHITE, stroke_width=2)
        fit_l = label(rf"$\approx {a:.2f}\, n^2$", font_size=30, color=WHITE).next_to(ax.c2p(42, a * 42 * 42 + b * 42),
                                                                                      LEFT, buff=0.3)
        with self.voiceover(
            "How long does this take? Here is a longer run as a space-time diagram: an input of twenty-four symbols, "
            "time running down. <bookmark mark='a'/> The head zig-zags across the whole remaining input on every pass, "
            "and the passes get shorter by two each time: a long sawtooth. <bookmark mark='b'/> Measured on inputs of "
            "every length up to sixty, the number of steps grows like the square of the length: about one half of n "
            "squared. Double the input, and the machine takes four times as long."
        ) as vo:
            self.play(FadeIn(img), Create(frame), FadeIn(cap), FadeIn(t_lab))
            vo.wait_until("a")
            self.play(Indicate(img, scale_factor=1.03, color=HEAD))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[FadeIn(dt, scale=2) for dt in dots], lag_ratio=0.02), run_time=1.6)
            self.play(Create(fit), FadeIn(fit_l))
        self.wait(0.3)
        self.clear_scene()



def fmt_(n) -> str:
    return f"{int(n):,}".replace(",", "{,}")
