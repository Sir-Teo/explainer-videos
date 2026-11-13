from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Doctrine(VoiceoverScene):
    def construct(self):
        self.card()
        self.net_or_cells()
        self.anatomy()

    def card(self):
        card = chapter_card(1, r"One net, or many cells", r"What is the nervous system made of?",
                            lit={1906: r"Golgi and Cajal share a prize"}, part=PART, scale=("neuron",),
                            marr=("tissue",))
        with self.voiceover(
            "Chapter one. One net, or many cells."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def net_or_cells(self):
        d = archive.GOLGI_CAJAL_1906.data
        head = heading(rf"{d['year']}: \ one prize, two opposite lectures")
        rng = np.random.default_rng(8)
        cols, rows_ = 4, 3
        grid = np.array([[(i - 1.5) * 1.5 + rng.uniform(-0.3, 0.3), (1 - j) * 1.25 + rng.uniform(-0.25, 0.25)]
                         for j in range(rows_) for i in range(cols)])
        pairs = [(j * cols + i, j * cols + i + 1) for j in range(rows_) for i in range(cols - 1)]
        pairs += [(j * cols + i, (j + 1) * cols + i) for j in range(rows_ - 1) for i in range(cols)]
        pairs += [(0, 5), (2, 7), (5, 10), (6, 9)]

        def net(cx, joined):
            g = VGroup()
            off = np.array([cx, -0.55, 0])
            for i, j in pairs:
                a_, b_ = np.append(grid[i], 0) + off, np.append(grid[j], 0) + off
                if joined:
                    g.add(Line(a_, b_, color=VOLT, stroke_width=3))
                else:
                    end = a_ + 0.8 * (b_ - a_)
                    g.add(Line(a_, end, color=VOLT, stroke_width=3), Dot(end, radius=0.07, color=THRESH))
            for q in grid:
                g.add(Dot(np.append(q, 0) + off, radius=0.17, color=VOLT))
            return g

        left, right = net(-3.55, True), net(3.55, False)
        tangle = VGroup(*[
            ArcBetweenPoints(np.append(c_, 0), np.append(c_ + rng.uniform(-1.6, 1.6, 2), 0), angle=rng.uniform(-1.2, 1.2),
                             color=GREY_B, stroke_width=1.5, stroke_opacity=0.7)
            for c_ in rng.uniform([-4.5, -2.2], [4.5, 1.6], (90, 2))])
        tangle_l = label(r"brain tissue under the microscope: \ a tangle too fine to follow", font_size=26, color=GREY_A)
        tangle_l.to_edge(DOWN, buff=1.0)
        lt = VGroup(label(r"Camillo Golgi", font_size=34, color=DATA),
                    label(r"one continuous network", font_size=28, color=WHITE)).arrange(DOWN, buff=0.1)
        rt = VGroup(label(r"Santiago Ram\'on y Cajal", font_size=34, color=MODEL),
                    label(r"separate cells, with gaps between them", font_size=28, color=WHITE)).arrange(DOWN, buff=0.1)
        lt.move_to([-3.55, 2.25, 0])
        rt.move_to([3.55, 2.25, 0])
        end = wrapped_label(r"Cajal's evidence came from Golgi's own stain. \ The gaps were finally seen with the "
                            r"electron microscope, in the 1950s.", 12.4, 28, P.ACCENT).to_edge(DOWN, buff=0.6)
        src = historical_tag(archive.GOLGI_CAJAL_1906.cite)
        with self.voiceover(
            "Before asking what travels, we need to know what it travels in. In the nineteenth century that "
            "was an open question. Brain tissue under a microscope is a dense tangle, and the fibres are too "
            "fine to follow. <bookmark mark='a'/> The Italian anatomist Camillo Golgi found a stain that, for "
            "reasons still not fully understood, blackens only a few cells in a hundred, whole, down to their "
            "finest branches. Looking at his own preparations, Golgi held that the nervous system is one "
            "continuous net, with the fibres fused into each other like a plumbing system. <bookmark mark='b'/> "
            "A Spanish anatomist, Santiago Ramón y Cajal, used the same stain, on younger tissue, and drew "
            "what he saw thousands of times. He concluded the opposite. The nervous system is made of separate "
            "cells. Their branches come close, and never join. <bookmark mark='c'/> In 1906 the two men shared "
            "the Nobel Prize, and gave lectures contradicting each other. Cajal was right. But the gap "
            "between two cells is far too narrow for a light microscope, and it wasn't seen until the electron "
            "microscope, in the nineteen-fifties. The cell got a name, the neuron, and the claim that it's "
            "the unit of the nervous system is called the neuron doctrine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(Create(tangle, lag_ratio=0.02), FadeIn(tangle_l), run_time=5.0)
            vo.wait_until("a")
            self.play(FadeOut(tangle), FadeOut(tangle_l), run_time=0.8)
            self.play(FadeIn(lt), Create(left, lag_ratio=0.05), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rt), Create(right, lag_ratio=0.05), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()

    def anatomy(self):
        head = heading(r"A neuron, drawn")
        n = neuron_drawing(1.3).move_to([-0.2, 0.55, 0])
        soma_c, hill_c = n.soma.get_center(), n.hillock.get_center()
        specs = [
            (r"dendrites", r"where signals arrive", n.dend.get_bottom() + DOWN * 0.45 + LEFT * 0.6, GATE["n"]),
            (r"cell body", r"where they are added up", soma_c + np.array([1.0, -1.05, 0]), VOLT),
            (r"start of the axon", r"where the decision is made", hill_c + np.array([1.1, 0.95, 0]), THRESH),
            (r"axon", r"one output, up to a metre long", n.axon.get_center() + np.array([0.9, -0.6, 0]), MODEL),
            (r"terminals", r"where it meets the next cell", n.term.get_top() + np.array([-0.3, 0.6, 0]), NA),
        ]
        targets = [n.dend.get_bottom() + UP * 0.9 + RIGHT * 0.6, soma_c + DOWN * 0.6 * 1.0 + RIGHT * 0.25,
                   hill_c + UP * 0.12, None, None]
        labels = VGroup()
        for (name, role, pos, color), tgt in zip(specs, targets):
            t = VGroup(label(name, font_size=28, color=color), label(role, font_size=22, color=GREY_A)).arrange(
                DOWN, buff=0.05).move_to(pos)
            keep_in_frame(t)
            g = VGroup(t)
            if tgt is not None:
                g.add(Line(t.get_top() if tgt[1] > t.get_center()[1] else t.get_bottom(), tgt, color=color,
                           stroke_width=1.5, stroke_opacity=0.7))
            labels.add(g)
        flow = Arrow([-5.6, -3.0, 0], [5.2, -3.0, 0], color=GREY_B, stroke_width=4, buff=0)
        flow_l = label(r"signals go one way", font_size=26, color=GREY_A).next_to(flow, UP, buff=0.1)
        pulse = Dot(n.hillock.get_right(), radius=0.13, color=THRESH)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is one, simplified. <bookmark mark='a'/> On one side, a bush of fine branches, the "
            "dendrites. This is where signals from other cells arrive, thousands of them on a typical cell. "
            "<bookmark mark='b'/> They converge on the cell body, where their effects add up. "
            "<bookmark mark='c'/> Where the cell body narrows into its one long fibre, a decision is made, and "
            "we'll see exactly how. <bookmark mark='d'/> That fibre is the axon. A cell has one, and it can be "
            "very long: the axons that move your toes run from the base of your spine. "
            "<bookmark mark='e'/> At its far end it branches and meets the next cells. Those meeting points are "
            "the subject of Part 6. <bookmark mark='f'/> So a neuron has a direction. Signals come in at the "
            "dendrites, and one signal goes out along the axon. Cajal worked that out from the shapes alone. "
            "Our question for today is the one thing that happens in the axon. A brief electrical event starts "
            "at the near end <bookmark mark='g'/> and runs to the far end without getting any smaller. It's "
            "called the action potential, or the spike. Everything your brain does, it does with these."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(n, lag_ratio=0.02), run_time=3.0)
            for mark, t in zip("abcde", labels):
                vo.wait_until(mark)
                self.play(FadeIn(t, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(GrowArrow(flow), FadeIn(flow_l))
            vo.wait_until("g")
            self.play(FadeIn(pulse, scale=1.5))
            self.play(pulse.animate.move_to(n.axon.get_right()), run_time=2.5, rate_func=linear)
            self.play(FadeOut(pulse))
        self.clear_scene()
