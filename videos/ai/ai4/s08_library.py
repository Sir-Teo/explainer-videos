from __future__ import annotations

import inspect
import math
import textwrap

import numpy as np

from explainer.ai import *  # noqa: F403
from explainer.ai.autodiff import Tensor
from videos.ai.ai4.common import GRAD, HIST, MONO, PART, VALUE, ComputeGraph, load


def source(fn) -> str:
    return textwrap.dedent(inspect.getsource(fn)).rstrip()


class Library(VoiceoverScene):
    def construct(self):
        self.card()
        self.code()
        self.order()
        self.check()
        self.tools()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"Calculus in a few pages of code", r"How small can the machine be?", part=PART)
        with self.voiceover("Chapter seven. The machine, in code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def code(self):
        mul = Code(code_string=source(Tensor.__mul__), language="python", formatter_style="monokai", background="window",
                   add_line_numbers=False, paragraph_config={"font": "DejaVu Sans Mono", "font_size": 20})
        back = Code(code_string=source(Tensor.backward), language="python", formatter_style="monokai", background="window",
                    add_line_numbers=False, paragraph_config={"font": "DejaVu Sans Mono", "font_size": 18})
        # the whole library, as a wall, before zooming in on one operation
        import explainer.ai.autodiff as ad

        lines = inspect.getsource(ad).rstrip().split("\n")
        k = (len(lines) + 2) // 3
        wall = VGroup(*[Code(code_string="\n".join(lines[i * k:(i + 1) * k]), language="python", formatter_style="monokai",
                             background="rectangle", add_line_numbers=False,
                             paragraph_config={"font": "DejaVu Sans Mono", "font_size": 12}) for i in range(3)])
        wall.arrange(RIGHT, buff=0.2, aligned_edge=UP)
        wall.scale_to_fit_height(6.2) if wall.height / 6.2 > wall.width / 13.4 else wall.scale_to_fit_width(13.4)
        wall.move_to(DOWN * 0.25)
        count = label(rf"${len(lines)}$ lines", font_size=30, color=GRAD).to_corner(UR, buff=0.35)
        mul.move_to([0, 0.6, 0])
        back.move_to([0, -0.3, 0])
        for c in (mul, back):
            if c.width > 13.0:
                c.width = 13.0
        path = label(r"\texttt{explainer/ai/autodiff.py}", font_size=26, color=GREY_B).to_edge(UP, buff=0.35)
        note1 = label(r"$\partial(ab)/\partial a = b$: \ the incoming gradient, times the other input", font_size=28,
                      color=GRAD).to_edge(DOWN, buff=0.45)
        n_lines = int(round(len(lines) / 10.0)) * 10
        with self.voiceover(
            f"Here it is in code: the series' own automatic differentiation, about {n_lines} lines in all. "
            "<bookmark mark='a'/> Every operation remembers its inputs, along with a small function that sends a "
            "gradient back to each one. Here's multiplication: the gradient for one input is the incoming gradient, "
            "times the other input. <bookmark mark='b'/> And backward visits the graph in reverse order, adds up what "
            "arrives at each node, and passes it on."
        ) as vo:
            self.play(FadeIn(path), LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in wall], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(count))
            vo.wait_until("a")
            self.play(FadeOut(wall), FadeOut(count), FadeIn(mul, shift=UP * 0.2))
            self.play(FadeIn(note1))
            vo.wait_until("b")
            self.play(FadeOut(mul), FadeOut(note1), FadeIn(back, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        c = load("check")
        assert c["fd_diff"] < 1e-9 and c["torch_diff"] < 1e-15
        head = label(rf"A small network: \ ${c['n_params']}$ numbers, \ every gradient checked", font_size=32)
        head.to_edge(UP, buff=0.45)
        rows = VGroup()
        hdr = VGroup(label(r"ours", font_size=26, color=GRAD), label(r"nudge by $10^{-6}$", font_size=26, color=VALUE))
        for ours, fd in c["shown"]:
            rows.add(VGroup(MathTex(f"{ours:+.10f}", font_size=30, color=GRAD), MathTex(f"{fd:+.10f}", font_size=30,
                                                                                    color=VALUE)))
        tab = VGroup(hdr, *rows)
        for r in tab:
            r.arrange(RIGHT, buff=0.6)
        tab.arrange(DOWN, buff=0.22).move_to([-2.6, -0.1, 0])
        for k in range(2):
            hdr[k].set_x(rows[0][k].get_x())

        def sci(x):
            e = int(f"{x:e}".split("e")[1])
            return rf"{x / 10 ** e:.1f} \times 10^{{{e}}}"

        res = VGroup(
            MathTex(r"\text{finite differences: \ worst gap } " + sci(c["fd_diff"]), font_size=34, color=VALUE),
            MathTex(r"\text{PyTorch: \ worst gap } " + sci(c["torch_diff"]), font_size=34, color=GRAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.6, -0.1, 0])
        if res.get_right()[0] > 6.9:
            res.shift(LEFT * (res.get_right()[0] - 6.9))
        fd_digits = int(math.floor(-math.log10(c["fd_diff"])))
        pt_digits = int(math.floor(-math.log10(max(c["torch_diff"], 1e-18))))
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> Nudge each number by a millionth, measure how much the loss changes, "
            f"and compare: the gradients agree to {fd_digits} decimal places, which, as chapter ten shows, is all a "
            "nudge can tell. <bookmark mark='b'/> Against PyTorch, the library most of today's models are trained "
            f"with, they agree to {pt_digits} decimal places, the limit of the computer's own arithmetic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=1.5)
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        t = load("tape")
        tp = t["tape"]
        assert [e["op"] for e in tp] == ["input", "*", "input", "+", "sigmoid", "+", "*"]
        names = [r"w", r"u", r"b", r"z", r"a", r"e", r"\mathcal L"]
        pos = [(-6.0, 1.3), (-4.6, 1.3), (-4.6, -0.7), (-3.2, 0.3), (-1.8, 0.3), (-0.4, 0.3), (1.0, 0.3)]
        cols = {"w": C.BITS, "b": C.BITS, "6": C.LOSS}
        nodes = {str(i): (names[i], (x, y, 0)) for i, (x, y) in enumerate(pos)}
        edges = [(str(a), str(e["i"])) for e in tp for a in sorted(set(e["args"]))]
        cg = ComputeGraph(nodes, edges, radius=0.36, font_size=30, colors={"0": C.BITS, "2": C.BITS, "6": C.LOSS})
        nums = VGroup(*[MathTex(str(i), font_size=22, color=GREY_B).next_to(cg.node[str(i)], UP, buff=0.08)
                        for i in range(len(tp))])
        what = {"*": r"\times", "+": r"+"}
        consts = {1: r"x", 5: r"(-y)"}
        lines = VGroup()
        for e in tp:
            i, a = e["i"], e["args"]
            if e["op"] == "input":
                rhs = r"\text{input } " + names[i]
            elif e["op"] == "sigmoid":
                rhs = rf"\sigma(v_{a[0]})"
            elif len(a) == 2:
                rhs = "v_" + str(a[0]) + " " + what[e["op"]] + " v_" + str(a[1])
            else:
                rhs = "v_" + str(a[0]) + " " + what[e["op"]] + " " + consts[i]
            lines.add(MathTex(rf"v_{i} = {rhs}", font_size=30, color=WHITE))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.6, 0.2, 0])
        box = SurroundingRectangle(lines, color=GREY_D, buff=0.25, corner_radius=0.1)
        tl = label(r"the tape \ (a Wengert list)", font_size=24, color=GREY_A).next_to(box, UP, buff=0.12)
        head = label(r"a topological order: \ every node after its inputs", font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        hist = history_card(1964, r"R.~E.~Wengert, \ General Electric", r"a program as a list of elementary steps, "
                            r"each carrying its derivative along", width=6.4, font_size=19, color=HIST).to_corner(DL, buff=0.3)
        fwd = [cg.pulse(a, b, VALUE) for a, b in edges]
        bwd = [cg.pulse(a, b, GRAD, backwards=True) for a, b in reversed(edges)]
        with self.voiceover(
            "Backward needs an order: a node may pass its gradient on only after every use of it has reported. "
            "A depth-first search through the graph gives exactly that, a topological order, each node after its "
            "inputs. Here is chapter six's example, numbered by our library in that order. <bookmark mark='a'/> "
            "Written out, the graph is a list, each line one elementary operation on earlier lines. In 1964 R. E. "
            "Wengert had programs keep such lists to carry derivatives along with their values; tools today call the "
            "record a tape. <bookmark mark='b'/> Forwards, the values run down the list. <bookmark mark='c'/> "
            "Backwards, the list runs from the bottom up, each line sending its gradient to the lines it used."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cg), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nums], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(box), FadeIn(tl), LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.1) for l_ in lines], lag_ratio=0.2),
                      run_time=2.0)
            self.play(FadeIn(hist, shift=UP * 0.2))
            vo.wait_until("b")
            for k, an in enumerate(fwd):
                self.play(an, lines[min(k + 1, len(lines) - 1)].animate.set_color(VALUE), run_time=0.35)
            vo.wait_until("c")
            for an in bwd:
                self.play(an, run_time=0.35)
            self.play(lines.animate.set_color(GRAD), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tools(self):
        kw = dict(width=4.15, font_size=19, color=HIST)
        events = VGroup(
            history_card(1980, r"Bert Speelpenning, \ PhD thesis", r"reverse mode compiled from an ordinary program", **kw),
            history_card(2010, r"Theano \ (Montr\'eal)", r"declare a graph, \ then compile it and its gradients", **kw),
            history_card(2015, r"Chainer; \ TensorFlow", r"define-by-run: \ the graph recorded as the code runs; "
                         r"\ TensorFlow: a static graph", **kw),
            history_card(2017, r"PyTorch", r"define-by-run on GPUs, \ like ours on the CPU", **kw),
            history_card(2018, r"JAX", r"trace a function, \ then transform it: \ \texttt{grad}, \texttt{jvp}, "
                         r"\texttt{vjp}, \texttt{jit}, \texttt{vmap}", **kw),
            history_card(2026, r"this series", r"\texttt{explainer/ai/autodiff.py}: \ define-by-run, \ numpy, "
                         r"\ one file", **kw),
        )
        events.arrange_in_grid(rows=2, cols=3, buff=(0.22, 0.25), cell_alignment=UL)
        head = label(r"automatic differentiation, \ 1980 to today", font_size=32).to_edge(UP, buff=0.3)
        events.next_to(head, DOWN, buff=0.3)
        snippets = [
            ("ours", ["loss = cross_entropy(model(x), y)", "loss.backward()", "w.grad"]),
            ("PyTorch", ["loss = F.cross_entropy(model(x), y)", "loss.backward()", "w.grad"]),
            ("JAX", ["g = jax.grad(loss_fn)(params, x, y)"]),
        ]
        code = VGroup()
        for name, ls in snippets:
            cb = code_block(ls, font_size=19, font=MONO)
            code.add(VGroup(label(name, font_size=24, color=GRAD), cb).arrange(DOWN, aligned_edge=LEFT, buff=0.14))
        code.arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(DOWN, buff=0.45)
        if code.width > 13.2:
            code.scale_to_fit_width(13.2)
        with self.voiceover(
            "Ours is the smallest member of a long family. <bookmark mark='a'/> In 1980 Bert Speelpenning compiled "
            "reverse mode from ordinary programs. <bookmark mark='b'/> In 2010 Theano, from Montreal, had you declare "
            "a graph first and then compiled it, gradients included. <bookmark mark='c'/> In 2015 Chainer recorded the "
            "graph as the code ran, define by run, while TensorFlow kept a static graph. <bookmark mark='d'/> "
            "PyTorch, in 2017, ran define by run on GPUs, as ours does on the CPU, <bookmark mark='e'/> and in 2018 "
            "JAX traced whole functions and transformed them: gradients, both kinds of product, compilation, "
            "batching. <bookmark mark='f'/> The line you write is almost the same in all three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(events[5], shift=UP * 0.15))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                self.play(FadeIn(events[k], shift=UP * 0.15))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.3), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
