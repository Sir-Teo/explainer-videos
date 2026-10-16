from __future__ import annotations

import inspect
import textwrap

from explainer.ai import *  # noqa: F403
from explainer.ai.autodiff import Tensor
from videos.ai.ai3.common import GRAD, VALUE, load


def source(fn) -> str:
    return textwrap.dedent(inspect.getsource(fn)).rstrip()


class Library(VoiceoverScene):
    def construct(self):
        self.card()
        self.code()
        self.check()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(6, r"Calculus in a few pages of code", r"How small can the machine be?", part=3)
        with self.voiceover("Chapter six. The machine, in code."):
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
        with self.voiceover(
            "Here it is in code: the series' own automatic differentiation, about a hundred and fifty lines in all. "
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
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> Nudge each number by a millionth, measure how much the loss changes, "
            "and compare: the gradients agree to ten decimal places. <bookmark mark='b'/> Against PyTorch, the library "
            "most of today's models are trained with, they agree to sixteen, the limit of the computer's own "
            "arithmetic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=1.5)
            self.play(FadeIn(res[0]))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()
