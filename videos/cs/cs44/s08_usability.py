from __future__ import annotations

import random

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, tag_box, trace


class Usability(VoiceoverScene):
    def construct(self):
        self.card()
        self.heuristics()
        self.thinkaloud()
        self.model()
        self.curves()
        self.caveats()

    def card(self):
        card = chapter_card(7, r"Evaluating usability", r"How many people do you need to watch?", lit=(1990, 1993),
                            extra=((1990, r"Nielsen and Molich: \ heuristic evaluation"),
                                   (1993, r"Nielsen and Landauer")), part=PART)
        with self.voiceover("Chapter seven. Evaluating usability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def heuristics(self):
        head = label(r"Nielsen's ten heuristics \ (1994)", font_size=36).to_edge(UP, buff=0.3)
        items = [r"visibility of system status", r"match between system and the real world",
                 r"user control and freedom", r"consistency and standards", r"error prevention",
                 r"recognition rather than recall", r"flexibility and efficiency of use",
                 r"aesthetic and minimalist design", r"help users recognize, \ diagnose and recover from errors",
                 r"help and documentation"]
        cells = VGroup()
        for k, t in enumerate(items):
            num = label(f"{k + 1}", font_size=24, color=HEAD)
            txt = label(t, font_size=24, color=WHITE)
            cells.add(VGroup(num, txt).arrange(RIGHT, buff=0.2))
        left = VGroup(*cells[:5]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        right = VGroup(*cells[5:]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        for col in (left, right):
            for c in col:
                c[0].set_x(col[0][0].get_x())
        cols = VGroup(left, right).arrange(RIGHT, buff=0.7, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        if cols.width > 12.8:
            cols.width = 12.8
        lines = VGroup(
            wrapped_label(r"\textbf{heuristic evaluation} \ (Nielsen and Molich, \ 1990): \ a few evaluators each "
                          r"inspect the design against the list, \ alone, \ then pool what they found", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"cheap and fast, \ but it finds what experts expect; \ watching real users finds what "
                          r"they do not", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How do you find out what is wrong with a design before your users do? The cheapest way is to inspect "
            "it. <bookmark mark='a'/> In 1994 Jakob Nielsen distilled ten rules of thumb from hundreds of usability "
            "problems: show people what the system is doing, speak their language, let them undo, be consistent, "
            "prevent errors, make choices visible instead of remembered, and so on. "
            "<bookmark mark='b'/> In a heuristic evaluation, a few evaluators each check the design against the list "
            "on their own, then pool what they found. <bookmark mark='c'/> It is fast and cheap. But it finds the "
            "problems experts expect, and real people find others."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cells], lag_ratio=0.25), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def thinkaloud(self):
        head = label(r"Thinking aloud", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, y = -6.0, 6.0, 0.2
        axis = Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([x0 + (x1 - x0) * m / 30, y - 0.08, 0], [x0 + (x1 - x0) * m / 30, y + 0.08, 0],
                                     color=GREY_C), label(f"{m} min", font_size=16, color=GREY_B).move_to(
            [x0 + (x1 - x0) * m / 30, y - 0.35, 0])) for m in (0, 10, 20, 30)])
        task = label(r"task: \ buy a train ticket for a friend", font_size=20, color=GREY_A).next_to(axis, UP,
                                                                                                buff=1.9)
        events = [(3, r"``where do I say it's not for me?''", HEAD, True),
                  (11, r"``is that the price for both ways?''", HEAD, False),
                  (17, r"``I'll just go back and start again''", NO, True),
                  (25, r"``oh --- it was under Options''", NO, False)]
        marks = VGroup()
        for m, q, c, up in events:
            x = x0 + (x1 - x0) * m / 30
            d = Dot([x, y, 0], radius=0.09, color=c)
            stem = Line([x, y, 0], [x, y + (0.8 if up else -0.8), 0], color=c, stroke_width=1.5)
            t = label(q, font_size=18, color=c).next_to(stem, UP if up else DOWN, buff=0.08)
            if t.get_left()[0] < -6.8:
                t.shift(RIGHT * (-6.8 - t.get_left()[0]))
            if t.get_right()[0] > 6.8:
                t.shift(LEFT * (t.get_right()[0] - 6.8))
            marks.add(VGroup(d, stem, t))
        ill = note(r"illustrative session", font_size=16).next_to(task, RIGHT, buff=0.4)
        lines = VGroup(
            wrapped_label(r"a participant does real tasks and says what they are thinking; \ the facilitator stays "
                          r"quiet, \ and asks only ``what are you thinking?''", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"Clayton Lewis brought the method to interface design at IBM \ (1982), \ from the "
                          r"psychology of verbal reports \ (Ericsson and Simon); \ watch what people do, \ not what "
                          r"they say they would do", 12.4, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "To find what real people stumble on, watch them. <bookmark mark='a'/> In a think-aloud study a "
            "participant is given real tasks, like buying a ticket for a friend, and asked to say what they are "
            "thinking as they work. <bookmark mark='b'/> Every hesitation, wrong guess and retreat marks a problem, "
            "and the words say why: the person did not know where to say the ticket was for someone else. "
            "<bookmark mark='c'/> The facilitator stays quiet, and never helps. Clayton Lewis brought the method into "
            "interface design at IBM in 1982, from the psychology of verbal reports. The rule is to watch what "
            "people do, and not to ask what they would do."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(task), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            for mk in marks:
                self.play(FadeIn(mk[0], scale=1.6), Create(mk[1]), FadeIn(mk[2]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def model(self):
        u = load("users")["uniform"]
        L = u[1]["found"]
        head = label(r"Five users find 85\%?", font_size=36).to_edge(UP, buff=0.3)
        rng = random.Random(7)
        n_users, n_prob, cell = 5, 12, 0.36
        hits = [[rng.random() < L for _ in range(n_prob)] for _ in range(n_users)]
        grid = VGroup()
        for i in range(n_users):
            for j in range(n_prob):
                grid.add(Square(cell, stroke_color=GREY_D, stroke_width=1, fill_color=HEAD,
                                fill_opacity=0.8 if hits[i][j] else 0).move_to([j * cell, -i * cell, 0]))
        anyone = VGroup(*[Square(cell, stroke_color=GREY_D, stroke_width=1, fill_color=YES,
                                 fill_opacity=0.8 if any(hits[i][j] for i in range(n_users)) else 0).move_to(
            [j * cell, -(n_users + 0.4) * cell, 0]) for j in range(n_prob)])
        board = VGroup(grid, anyone).move_to([-3.6, 0.9, 0])
        rl = VGroup(*[label(f"user {i + 1}", font_size=16, color=GREY_B).next_to(grid[i * n_prob], LEFT, buff=0.15)
                      for i in range(n_users)])
        al = label(r"anyone", font_size=16, color=YES).next_to(anyone[0], LEFT, buff=0.15)
        pl = label(r"twelve problems in the design", font_size=17, color=GREY_B).next_to(board, UP, buff=0.15)
        ill = note(rf"illustrative draw, \ each cell on with probability {L:.2f}", font_size=16).next_to(
            board, DOWN, buff=0.2)
        eqs = VGroup(
            MathTex(r"P(\text{one user misses a problem}) = 1 - L", font_size=30),
            MathTex(r"P(\text{all } n \text{ miss it}) = (1 - L)^n", font_size=30),
            MathTex(r"\text{found} = 1 - (1 - L)^n", font_size=34, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.4, 0])
        why = note(r"users independent: \ multiply \ (Part 2)", font_size=17).next_to(eqs[1], DOWN, buff=0.08
                                                                                      ).align_to(eqs[1], LEFT)
        eqs[2].next_to(why, DOWN, buff=0.25).align_to(eqs[1], LEFT)
        vals = [u[n]["found"] for n in range(1, 6)]
        bars = VGroup()
        for n, v in enumerate(vals, 1):
            b = Rectangle(width=0.7, height=2.0 * v, stroke_width=0, fill_color=YES, fill_opacity=0.8)
            b.move_to([0, v, 0])
            t = label(f"{100 * v:.0f}\\%", font_size=18, color=YES).next_to(b, UP, buff=0.06)
            nl = label(f"{n}", font_size=17, color=GREY_B).next_to([0, 0, 0], DOWN, buff=0.1)
            bars.add(VGroup(b, t, nl).shift(RIGHT * 1.0 * n))
        bars.move_to([3.4, -1.9, 0])
        bl = label(r"users", font_size=17, color=GREY_B).next_to(bars, LEFT, buff=0.3).align_to(bars, DOWN)
        src = note(rf"Nielsen and Landauer \ (1993): \ $L = {L:.2f}$", font_size=17).next_to(board, DOWN, buff=0.7)
        with self.voiceover(
            "How many participants are enough? Jakob Nielsen and Thomas Landauer answered with a model in 1993. "
            "<bookmark mark='a'/> Suppose each user, independently, runs into each problem with the same "
            f"probability L. Averaged over the projects they studied, L was about {L:.2f}. "
            "<bookmark mark='b'/> One user misses a given problem with probability one minus L. All n users miss it "
            "with probability one minus L to the power n, because independent chances multiply, as in Part 2. "
            "<bookmark mark='c'/> So the share of problems found is one minus that. <bookmark mark='d'/> One user "
            f"finds {100 * vals[0]:.0f} per cent, two find {100 * vals[1]:.0f}, three {100 * vals[2]:.0f}, four "
            f"{100 * vals[3]:.0f}, and five {100 * vals[4]:.0f}: the famous claim that five users find most of the "
            "problems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(rl), FadeIn(ill), FadeIn(src))
            self.play(FadeIn(anyone), FadeIn(al))
            vo.wait_until("b")
            self.play(Write(eqs[0]))
            self.play(Write(eqs[1]), FadeIn(why))
            vo.wait_until("c")
            self.play(Write(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def curves(self):
        d = load("users")
        uni, var = d["uniform"], d["varied"]
        n_max = uni[-1]["n"]
        head = label(r"When problems differ", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, n_max, 1], [0, 1, 0.25], x_length=7.0, y_length=4.4, x_label=r"test users, \ $n$",
                 y_label=r"share of problems found", xticks=[0, 5, 10, 15], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 fy=lambda v: f"{100 * v:.0f}\\%").move_to([-2.6, -0.2, 0])
        ax = g.ax
        cu = trace(ax, [(r["n"], r["found"]) for r in uni], YES, width=3.5)
        cv = trace(ax, [(r["n"], r["found"]) for r in var], NO, width=3.5)
        u5, v5 = uni[5]["found"], var[5]["found"]
        n_match = next(r["n"] for r in var if r["found"] >= u5)
        du = Dot(ax.c2p(5, u5), color=YES)
        dv = Dot(ax.c2p(5, v5), color=NO)
        lu = label(f"{100 * u5:.0f}\\%", font_size=19, color=YES).next_to(du, UL, buff=0.08)
        lv = label(f"{100 * v5:.0f}\\%", font_size=19, color=NO).next_to(dv, DR, buff=0.08)
        dm = Dot(ax.c2p(n_match, var[n_match]["found"]), color=NO)
        lm = label(rf"{n_match} users", font_size=18, color=NO).next_to(dm, DOWN, buff=0.15)
        notes = VGroup(
            wrapped_label(rf"every problem equally visible: \ $L = {uni[1]['found']:.2f}$",
                          4.6, font_size=19, color=YES),
            wrapped_label(r"visibility varying from problem to problem, \ drawn from a Beta distribution with the "
                          rf"same mean: \ five users find {100 * v5:.0f}\%", 4.6, font_size=19, color=NO),
            wrapped_label(rf"to reach {100 * u5:.0f}\% \ now takes {n_match} users: \ the rare problems are the slow "
                          r"ones to find", 4.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, 0.1, 0])
        src = note(r"both curves computed from the model", font_size=16).next_to(
            notes, DOWN, buff=0.35).align_to(notes, LEFT)
        with self.voiceover(
            "The model assumed every problem is equally easy to find. Real ones are not. <bookmark mark='a'/> Here is "
            "the curve when each problem is found with the same probability. <bookmark mark='b'/> Now let "
            "visibility vary: a few problems hit almost everyone, many hit only a few. We drew each problem's "
            "probability from a Beta distribution with the same average, point three one. With five users the "
            f"share found falls from {100 * u5:.0f} to {100 * v5:.0f} per cent. <bookmark mark='c'/> To find "
            f"{100 * u5:.0f} per cent now takes {n_match} users, because the problems few people hit are the ones "
            "that take longest to see, and the average hides them."
        ) as vo:
            self.play(FadeIn(g))
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(notes[0]), run_time=1.5)
            self.play(FadeIn(du), FadeIn(lu))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(notes[1]), FadeIn(src), run_time=1.5)
            self.play(FadeIn(dv), FadeIn(lv))
            vo.wait_until("c")
            self.play(FadeIn(dm), FadeIn(lm), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def caveats(self):
        u = load("users")["uniform"]
        head = label(r"Test small, \ test often", font_size=36).to_edge(UP, buff=0.3)
        centre = np.array([-3.6, 0.5, 0])
        nodes = VGroup()
        for (t, c), off in zip(((r"test with five", HEAD), (r"fix what they hit", YES), (r"new design", DATA)),
                               ([0, 1.5, 0], [2.0, -0.9, 0], [-2.0, -0.9, 0])):
            nodes.add(tag_box(t, color=c, size=19).move_to(centre + np.array(off)))
        ends = [(nodes[0].get_right() + RIGHT * 0.1, nodes[1].get_top() + UP * 0.1),
                (nodes[1].get_bottom() + DOWN * 0.1, nodes[2].get_bottom() + DOWN * 0.1),
                (nodes[2].get_top() + UP * 0.1, nodes[0].get_left() + LEFT * 0.1)]
        arcs = VGroup(*[CurvedArrow(a, b, angle=-0.8, color=GREY_B, stroke_width=2, tip_length=0.15)
                        for a, b in ends])
        notes = VGroup(
            wrapped_label(r"$L$ varies with the product, \ the task and the people: \ one value of 0.31 is an "
                          r"average, \ not a law", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"a problem that hits one user in twenty is found by five users with probability "
                          rf"$1 - 0.95^5 = {100 * (1 - 0.95 ** 5):.0f}\%$, \ however severe it is", 5.6,
                          font_size=19, color=NO),
            wrapped_label(r"Nielsen's own advice \ (2000): \ rather than one study of fifteen, \ run three of "
                          r"five, \ fixing in between; \ and test each distinct group of users", 5.6, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 0.2, 0])
        one = note(rf"one round of fifteen: \ {100 * u[15]['found']:.1f}\% of today's problems \ (model)",
                   font_size=17).next_to(nodes, DOWN, buff=0.85).set_x(centre[0])
        with self.voiceover(
            "So the five-user rule needs care. <bookmark mark='a'/> L is an average over projects, and it varies "
            "with the product, the task and the people. <bookmark mark='b'/> A problem that only one user in twenty "
            "hits is found by five users less than a quarter of the time, however severe it is, which is why "
            "rare but costly failures need other methods too: logs, support calls, and the experiments of the next "
            "chapter. <bookmark mark='c'/> What the curve does support is iteration. One round of fifteen users "
            "would find nearly everything in today's design, but most of it is found by the first five; fix that, "
            "and the next five find the problems the old ones were hiding. Nielsen's own advice was three rounds of "
            "five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), Create(arcs))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), FadeIn(one))
            for _ in range(2):
                self.play(*[Indicate(n, scale_factor=1.08) for n in nodes], run_time=0.8)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
