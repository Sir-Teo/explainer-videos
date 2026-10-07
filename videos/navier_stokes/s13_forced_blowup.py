"""September 2026: OpenAI's claimed forced blow-up for 3D Navier–Stokes.

Facts on screen are restricted to what is documented in public reporting and
statements (see videos/navier_stokes/README.md, "Sources for Part 13").  The
cascade animation is explicitly labeled as a schematic.
"""

from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.navier_stokes.common import caption_box, label


def option_card(letter, verdict, domain, force, color, width=3.1, height=2.2):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, color=color, stroke_width=2.5)
    box.set_fill(color, opacity=0.06)
    content = VGroup(
        label(rf"\textbf{{({letter})}}", font_size=34, color=color),
        label(verdict, font_size=28),
        label(domain, font_size=26, color=GREY_A),
        label(force, font_size=26, color=C.FORCE),
    ).arrange(DOWN, buff=0.14)
    content.move_to(box)
    return VGroup(box, content)


class ForcedBlowup(VoiceoverScene):
    def construct(self):
        self.announcement()
        self.four_options()
        self.theorem()
        self.cascade()
        self.process()
        self.status()

    # ------------------------------------------------------------------
    def announcement(self):
        date = label(r"September 8, 2026", font_size=40, color=C.DIM)
        head = label(r"OpenAI announces: Navier--Stokes \emph{can} break down", font_size=46)
        VGroup(date, head).arrange(DOWN, buff=0.35).shift(UP * 0.6)
        sub = label(r"(a claimed proof, produced by an AI system)", font_size=32, color=GREY_A).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Which brings us to a remarkable recent development. <bookmark mark='d'/> On September 8th, 2026, OpenAI announced "
            "that an internal AI system had produced a proof that the answer is no: <bookmark mark='n'/> solutions can break down."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(date, shift=DOWN * 0.2))
            vo.wait_until("n")
            self.play(Write(head))
            self.play(FadeIn(sub))
        self.clear_scene()

    # ------------------------------------------------------------------
    def four_options(self):
        title = label(r"The official problem (C.\ Fefferman, Clay Institute): prove \emph{one} of", font_size=34).to_edge(UP, buff=0.45)
        cards = VGroup(
            option_card("A", r"smooth forever", r"all of space $\mathbb{R}^3$", r"no force: $\mathbf{f} = 0$", C.VISCOUS),
            option_card("B", r"smooth forever", r"periodic box", r"no force: $\mathbf{f} = 0$", C.VISCOUS),
            option_card("C", r"\emph{breakdown}", r"all of space $\mathbb{R}^3$", r"smooth force allowed", C.PRESSURE),
            option_card("D", r"\emph{breakdown}", r"periodic box", r"smooth force allowed", C.PRESSURE),
        ).arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.55)
        eq = MathTex(r"{\partial \vu \over \partial t}", r"+", r"(\vu\cdot\nabla)\vu", r"=", r"-{1\over\rho}\nabla p", r"+",
                     r"\nu\nabla^2\vu", r"+", r"\vf", font_size=44)
        for i, col in {0: C.TIME, 2: C.ADVECT, 4: C.PRESSURE, 6: C.VISCOUS, 8: C.FORCE}.items():
            eq[i].set_color(col)
        eq.to_edge(DOWN, buff=1.0)
        fbox = SurroundingRectangle(eq[8], color=C.FORCE, buff=0.12)
        fnote = label(r"you may push on the fluid --- but the push itself must be perfectly smooth", font_size=28, color=C.FORCE)
        fnote.next_to(eq, DOWN, buff=0.3)

        with self.voiceover(
            "There's a subtlety in how the prize problem is phrased. The official statement, written by Charles Fefferman, offers "
            "four ways to win. <bookmark mark='ab'/> Two ask you to prove that smooth solutions last forever, in all of space or in a "
            "periodic box, with no external force at all. <bookmark mark='cd'/> The other two ask for the opposite: show that a "
            "solution can break down. <bookmark mark='f'/> And for those, you're allowed to push on the fluid with an external force, "
            "as long as the force itself is perfectly smooth."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("ab")
            self.play(FadeIn(cards[0], shift=UP * 0.2), FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("cd")
            self.play(FadeIn(cards[2], shift=UP * 0.2), FadeIn(cards[3], shift=UP * 0.2))
            vo.wait_until("f")
            self.play(FadeIn(eq), Create(fbox))
            self.play(FadeIn(fnote))

        with self.voiceover(
            "That second door, breakdown with a smooth force, is the one OpenAI's result walks through."
        ) as vo:
            self.play(cards[:2].animate.set_opacity(0.25), cards[2:].animate.scale(1.06), run_time=1.2)
            self.play(Indicate(cards[2][0], color=C.PRESSURE), Indicate(cards[3][0], color=C.PRESSURE))
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        head = label(r"The claimed theorem (as announced)", font_size=38).to_edge(UP, buff=0.5)
        items = VGroup(
            MathTex(r"\text{for every viscosity } \nu > 0,", font_size=38),
            MathTex(r"\text{a smooth force }", r"\vf", r"\text{, confined to a bounded region,}", font_size=38),
            MathTex(r"\text{acting on a fluid that starts at rest, } \vu(\vx, 0) = 0,", font_size=38),
            MathTex(r"\text{keeps the total energy bounded}", font_size=38),
            MathTex(r"\text{but drives the solution to a singularity at a finite time } T^*", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        items[1][1].set_color(C.FORCE)
        items[4].set_color(YELLOW)

        ax = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1], x_length=4.2, y_length=2.6,
                  axis_config={"include_ticks": False, "stroke_color": GREY_B}).to_corner(DR, buff=0.5)
        T = 3.0
        curve = ax.plot(lambda t: min(4.9, 0.25 + 0.35 / (T - t) - 0.35 / T), x_range=[0, T - 0.075], color=C.PRESSURE, stroke_width=4)
        tline = DashedLine(ax.c2p(T, 0), ax.c2p(T, 5), color=GREY_B)
        tl = MathTex("T^*", font_size=30).next_to(ax.c2p(T, 0), DOWN, buff=0.12)
        yl = label(r"size of the flow's gradients", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.05)

        with self.voiceover(
            "Here is the claim, as announced. <bookmark mark='nu'/> For any viscosity, <bookmark mark='f'/> there is a smooth force, "
            "confined to a bounded region, <bookmark mark='r'/> which, acting on a fluid that starts completely at rest, "
            "<bookmark mark='e'/> keeps the total energy bounded, <bookmark mark='s'/> yet drives the flow to a singularity in a "
            "finite amount of time."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate(["nu", "f", "r", "e", "s"]):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2), run_time=0.8)
            self.play(Create(ax), FadeIn(yl))
            self.play(Create(curve), Create(tline), FadeIn(tl), run_time=1.5)

        why = label(r"Without a force, the flow must tear itself apart on its own.\\"
                    r"With one, you may keep feeding it --- if you never cheat with a rough push.", font_size=30, color=GREY_A)
        why.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.8)
        with self.voiceover(
            "Why does the force matter so much? Without it, you would need a flow that tears itself apart entirely on its own. "
            "<bookmark mark='w'/> With a force, you get to keep feeding the flow, as long as you never cheat by using a force that is "
            "itself rough, or infinite."
        ) as vo:
            self.play(FadeOut(VGroup(ax, curve, tline, tl, yl)))
            vo.wait_until("w")
            self.play(FadeIn(why))
        self.clear_scene()

    # ------------------------------------------------------------------
    def cascade(self):
        title = label(r"The idea: an infinite cascade \quad (C\'ordoba \& Mart\'inez-Zoroa)", font_size=36).to_edge(UP, buff=0.4)
        schematic = label(r"schematic", font_size=24, color=GREY_B).to_corner(UR, buff=0.45).shift(DOWN * 0.55)
        center = np.array([-2.6, 0.2, 0])
        n_layers = 7
        layers = VGroup()
        for k in range(n_layers):
            r = 2.2 * 0.62**k
            col = interpolate_color(ManimColor(BLUE_C), ManimColor(YELLOW), k / (n_layers - 1))
            arc = Arc(radius=r, start_angle=0.3 * k, angle=1.65 * PI, color=col, stroke_width=max(1.5, 4 - 0.35 * k))
            arc.add_tip(tip_length=max(0.07, 0.22 * r), tip_width=max(0.07, 0.22 * r))
            arc.move_arc_center_to(center)
            arc.rate = 0.6 / (0.62**k) ** 1.2
            arc.add_updater(lambda m, dt: m.rotate(m.rate * dt, about_point=center))
            layers.add(arc)
        star = Dot(center, radius=0.06, color=WHITE)

        # Timeline: times t_k accumulating at T*
        line = NumberLine(x_range=[0, 1, 1], length=5.2, include_tip=False, color=GREY_B).move_to(RIGHT * 3.6 + DOWN * 2.6)
        tk = [1 - 0.55**k for k in range(1, n_layers + 1)]
        ticks = VGroup(*[Line(UP * 0.12, DOWN * 0.12, color=interpolate_color(ManimColor(BLUE_C), ManimColor(YELLOW), k / (n_layers - 1)))
                         .move_to(line.n2p(t)) for k, t in enumerate(tk)])
        T_lab = MathTex("T^*", font_size=32).next_to(line.n2p(1), DOWN, buff=0.18)
        t_lab = MathTex("t", font_size=30).next_to(line.n2p(0), DOWN, buff=0.18)

        notes = VGroup(
            label(r"each layer: a smaller, faster swirl", font_size=28),
            label(r"each layer on its own: perfectly smooth", font_size=28),
            label(r"infinitely many, packed into finite time $\Rightarrow$ singularity", font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.7 + UP * 1.0)

        with self.voiceover(
            "The strategy goes back to Diego Córdoba and Luis Martínez-Zoroa, who had spent years building what they call an infinite "
            "cascade. <bookmark mark='l'/> Roughly speaking: an infinite sequence of layers, each one a smaller, faster swirl, "
            "<bookmark mark='s'/> each perfectly smooth on its own, <bookmark mark='t'/> timed so that infinitely many of them pile up "
            "in a finite amount of time, producing a singularity."
        ) as vo:
            self.play(FadeIn(title), FadeIn(schematic))
            vo.wait_until("l")
            self.play(FadeIn(notes[0]), Create(line), FadeIn(t_lab), FadeIn(T_lab))
            for k in range(3):
                self.play(FadeIn(layers[k], scale=0.8), FadeIn(ticks[k]), run_time=0.6)
            vo.wait_until("s")
            self.play(FadeIn(notes[1]))
            vo.wait_until("t")
            for k in range(3, n_layers):
                self.play(FadeIn(layers[k], scale=0.8), FadeIn(ticks[k]), run_time=max(0.25, 0.5 * 0.7 ** (k - 3)))
            self.play(FadeIn(star, scale=3), FadeIn(notes[2]))

        fsum = MathTex(r"\vf", r"=", r"\vf_1 + \vf_2 + \vf_3 + \cdots", font_size=46).move_to(RIGHT * 3.6 + DOWN * 0.9)
        fsum[0].set_color(C.FORCE)
        fsum[2].set_color(C.FORCE)
        before = label(r"earlier constructions: the total force came out \emph{rough}", font_size=26, color=GREY_A)
        after = label(r"the missing step: make the total force \emph{smooth}", font_size=26, color=YELLOW)
        VGroup(before, after).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(fsum, DOWN, buff=0.3)
        VGroup(fsum, before, after).shift(UP * 0.0)
        with self.voiceover(
            "Each layer needs its own little push, and the total force is the sum of all of them. "
            "<bookmark mark='b'/> In their earlier constructions, that infinite sum ended up rough, which falls short of the prize "
            "rules. <bookmark mark='a'/> The missing step was to build the cascade so that the total force stays smooth."
        ) as vo:
            self.play(FadeOut(notes), line.animate.shift(DOWN * 0.4), ticks.animate.shift(DOWN * 0.4),
                      T_lab.animate.shift(DOWN * 0.4), t_lab.animate.shift(DOWN * 0.4))
            self.play(Write(fsum))
            vo.wait_until("b")
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeIn(after))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def process(self):
        stats = VGroup(
            VGroup(MathTex(r"\sim 10{,}000", font_size=60, color=YELLOW), label(r"AI agents in parallel", font_size=28)),
            VGroup(MathTex(r"\sim 88\ \text{h}", font_size=60, color=YELLOW), label(r"to a proof", font_size=28)),
            VGroup(MathTex(r"+17\ \text{h}", font_size=60, color=YELLOW), label(r"Lean formalization\\(also by AI)", font_size=28)),
        )
        for s in stats:
            s.arrange(DOWN, buff=0.25)
        stats.arrange(RIGHT, buff=1.4).shift(UP * 1.2)
        src = label(r"figures as reported by OpenAI", font_size=24, color=GREY_B).next_to(stats, DOWN, buff=0.4)
        lean = label(r"Lean: a language in which a computer checks every logical step", font_size=30, color=GREY_A)
        lean.next_to(src, DOWN, buff=0.5)

        with self.voiceover(
            "According to OpenAI, <bookmark mark='a'/> about ten thousand AI agents running on an unreleased model worked in parallel "
            "<bookmark mark='h'/> for about 88 hours to close that gap. <bookmark mark='l'/> Another model then translated the proof "
            "into Lean, a language in which a computer can check every single logical step."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(stats[0], shift=UP * 0.2))
            vo.wait_until("h")
            self.play(FadeIn(stats[1], shift=UP * 0.2), FadeIn(src))
            vo.wait_until("l")
            self.play(FadeIn(stats[2], shift=UP * 0.2))
            self.play(FadeIn(lean))

        people = VGroup(
            label(r"\textbf{Charles Fefferman} (Princeton), who wrote the official statement:", font_size=28),
            label(r"``I was thrilled that the problem was solved.''", font_size=32, color=YELLOW),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Charles Fefferman, who wrote the official problem statement, said he was <bookmark mark='q'/> thrilled that the problem "
            "was solved, and credited Córdoba and Martínez-Zoroa as the heroes of the story."
        ) as vo:
            self.play(FadeOut(lean))
            vo.wait_until("q")
            self.play(FadeIn(people))
        self.clear_scene()

        rival = VGroup(
            label(r"Hours earlier: \textbf{Tristan Buckmaster} (NYU) \& \textbf{Levent Alp\"oge}", font_size=32),
            label(r"posted Lean-verified forced blow-up for related equations, including 3D Euler", font_size=30, color=GREY_A),
            label(r"The two sides dispute how the timelines relate.", font_size=30),
            label(r"OpenAI says it will not claim the \$1M prize.", font_size=30),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "The story is also tangled. <bookmark mark='b'/> Just hours before the announcement, mathematicians Tristan Buckmaster and "
            "Levent Alpöge, who had been using AI tools themselves, posted Lean-verified forced blow-up results for closely related "
            "equations, including Euler, the version with no viscosity. <bookmark mark='d'/> The two sides dispute how the timelines "
            "relate, <bookmark mark='p'/> and OpenAI has said it will not claim the prize."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(rival[0]))
            self.play(FadeIn(rival[1]))
            vo.wait_until("d")
            self.play(FadeIn(rival[2]))
            vo.wait_until("p")
            self.play(FadeIn(rival[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def status(self):
        title = label(r"So, is it over?", font_size=48).to_edge(UP, buff=0.6)
        rows = [
            (r"AI-generated proof + Lean formalization", r"announced", C.VISCOUS),
            (r"independent checking by mathematicians", r"in progress", YELLOW),
            (r"Clay Institute recognition", r"awaits publication \& review", YELLOW),
            (r"a fluid with \emph{no} force: can it blow up?", r"still open", C.PRESSURE),
        ]
        table = VGroup()
        for left, right, col in rows:
            l = label(left, font_size=32)
            r = label(right, font_size=32, color=col)
            table.add(VGroup(l, r))
        for row in table:
            row[1].next_to(row[0], RIGHT, buff=0.6)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(title, DOWN, buff=0.7)
        # align the right column
        xr = max(row[0].get_right()[0] for row in table) + 0.6
        for row in table:
            row[1].align_to([xr, 0, 0], LEFT)
        table.move_to(DOWN * 0.3)
        caveat = label(r"(status as of the making of this video, October 2026)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.4)

        with self.voiceover(
            "So, is it over? Not quite. <bookmark mark='a'/> As of this video, the proof is still being checked by human "
            "mathematicians, <bookmark mark='c'/> and the Clay Institute only recognizes a solution after publication and review. "
            "A formal proof is only as good as the check that its formal statement really says what we think it says."
        ) as vo:
            self.play(FadeIn(title), FadeIn(caveat))
            self.play(FadeIn(table[0]))
            vo.wait_until("a")
            self.play(FadeIn(table[1]))
            vo.wait_until("c")
            self.play(FadeIn(table[2]))

        with self.voiceover(
            "And notice what it doesn't answer: <bookmark mark='u'/> whether a fluid left alone, with no force at all, can ever form "
            "a singularity. For the physical question that started all of this, the mystery remains."
        ) as vo:
            vo.wait_until("u")
            self.play(FadeIn(table[3]))
            self.play(Circumscribe(table[3], color=C.PRESSURE, buff=0.15))
        self.wait(0.5)
        self.clear_scene()
