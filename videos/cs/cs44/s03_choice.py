from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, mono, trace


def _box(text, color, w, h=0.55, size=19):
    b = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=1.8,
                         fill_color=BG, fill_opacity=1)
    t = label(text, font_size=size, color=color)
    if t.width > w - 0.2:
        t.width = w - 0.2
    return VGroup(b, t.move_to(b))


class Choice(VoiceoverScene):
    def construct(self):
        self.card()
        self.hick()
        self.entropy()
        self.limits()
        self.goms()
        self.klm()

    def card(self):
        card = chapter_card(2, r"Choosing, \ and predicting a task's time", r"How long does a decision take?",
                            lit=(1952, 1953, 1980), extra=((1952, r"Hick: \ the rate of gain of information"),
                                                     (1953, r"Hyman"),
                                                     (1980, r"Card, \ Moran and Newell: \ keystroke-level model")),
                            part=PART)
        with self.voiceover("Chapter two. Choosing, and predicting how long a task will take."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hick(self):
        h = load("hick")
        head = label(r"Hick's law: \ time grows with information", font_size=36).to_edge(UP, buff=0.3)
        lamps = VGroup(*[Square(0.5, stroke_color=HEAD, stroke_width=2, fill_color=HEAD, fill_opacity=0.15)
                         for _ in range(8)]).arrange(RIGHT, buff=0.15).move_to([-3.65, 1.5, 0])
        names = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(lamps[k], DOWN, buff=0.1)
                         for k, t in enumerate([str(i) for i in range(1, 8)] + [r"none"])])
        target = 4
        steps = [(4, 8), (4, 6), (4, 5)]
        marks = VGroup()
        for k, (lo, hi) in enumerate(steps):
            y = 0.6 - 0.48 * k
            ln = Line([lamps[lo].get_left()[0], y, 0], [lamps[hi - 1].get_right()[0], y, 0], color=DATA,
                      stroke_width=4)
            t = label(rf"comparison {k + 1}", font_size=18, color=DATA).next_to([lamps[0].get_left()[0], y, 0],
                                                                               RIGHT, buff=0)
            marks.add(VGroup(ln, t))
        ex = wrapped_label(r"7 lamps and the chance of none: \ 8 possibilities, \ found in $\log_2 8 = 3$ halvings "
                           r"\ (binary search, \ Part 16)", 5.6, font_size=20, color=WHITE)
        ex.next_to(marks, DOWN, buff=0.35).align_to(lamps, LEFT)
        g = axes([0, 4, 1], [0, 0.8, 0.2], x_length=5.0, y_length=3.2, x_label=r"$\log_2(n + 1)$, \ bits",
                 y_label=r"mean reaction time, \ s", xticks=range(0, 5), yticks=[0.2, 0.4, 0.6, 0.8],
                 fy=lambda v: f"{v:.1f}").move_to([3.6, 0.5, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(r["H"], r["RT"]), radius=0.06, color=DATA) for r in h["rows"]])
        fit = Line(ax.c2p(0, h["a"]), ax.c2p(4, h["a"] + 4 * h["b"]), color=HEAD, stroke_width=2.5)
        res = VGroup(
            MathTex(r"\mathrm{RT} = a + b\,\log_2(n + 1)", font_size=34, color=HEAD),
            label(rf"simulated: \ $a = {h['a']:.3f}$ s, \ $b = {h['b']:.3f}$ s per bit, \ $R^2 = {h['r2']:.3f}$",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(g, DOWN, buff=0.25)
        with self.voiceover(
            "In 1952 William Hick lit one of several lamps and timed how long people took to press the key beneath "
            "it. Reaction time grew with the logarithm of the number of lamps plus one, the one counting the chance "
            "that no lamp lit at all. <bookmark mark='a'/> Here is a chooser who halves the candidates with each "
            "comparison, the binary search of Part 16. Seven lamps and the chance of none make eight possibilities, "
            "and three comparisons find any of them. <bookmark mark='b'/> We simulated that chooser, at a fifth of "
            "a second to start and about 0.15 seconds per comparison, for one to ten lamps. Time against bits is a "
            "line, with R squared of 0.999: each bit of uncertainty costs the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lamps), FadeIn(names))
            vo.wait_until("a")
            for k, (lo, hi) in enumerate(steps):
                self.play(*[lamps[i].animate.set_opacity(0.15) for i in range(8) if not lo <= i < hi],
                          FadeIn(marks[k]), run_time=0.6)
            self.play(lamps[target].animate.set_fill(HEAD, opacity=0.9), FadeIn(ex))
            vo.wait_until("b")
            self.play(Create(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.2))
            self.play(Create(fit), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def entropy(self):
        sk = load("hick")["skewed"]
        head = label(r"Hyman: \ the entropy, \ not the count", font_size=36).to_edge(UP, buff=0.3)
        items = [r"Reply", r"Forward", r"Archive", r"Delete", r"Spam"]
        bars = VGroup()
        for k, (nm, p) in enumerate(zip(items, sk["p"])):
            n = label(nm, font_size=19, color=GREY_A)
            b = Rectangle(width=p * 5.0, height=0.36, stroke_width=0, fill_color=DATA, fill_opacity=0.8)
            v = label(f"{p:.2f}", font_size=18, color=DATA)
            row = VGroup(n, b, v)
            n.move_to([-5.6, 1.9 - 0.52 * k, 0]).align_to([-6.5, 0, 0], LEFT)
            b.next_to([-4.6, n.get_y(), 0], RIGHT, buff=0)
            v.next_to(b, RIGHT, buff=0.12)
            bars.add(row)
        tag = note(r"menu items illustrative; \ probabilities as simulated", font_size=16).next_to(
            bars, UP, buff=0.15).align_to(bars, LEFT)
        hs = VGroup(
            label(rf"entropy $H = -\sum p \log_2 p = {sk['H']:.2f}$ bits", font_size=21, color=HEAD),
            label(rf"five equal choices: \ $\log_2 5 = {sk['uniform_H']:.2f}$ bits", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(bars, DOWN, buff=0.45).align_to(bars, LEFT)
        q1 = _box(r"Reply?", HEAD, 1.8).move_to([2.6, 2.0, 0])
        y1 = _box(r"1 question", YES, 2.0).move_to([0.9, 0.7, 0])
        q2 = _box(r"Forward or Archive?", HEAD, 3.0).move_to([4.4, 0.7, 0])
        q3 = VGroup(_box(r"which of the two?", HEAD, 2.6).move_to([3.0, -0.6, 0]),
                    _box(r"which of the two?", HEAD, 2.6).move_to([5.75, -0.6, 0]))
        leaf = _box(r"3 questions", YES, 2.0).move_to([4.4, -1.8, 0])
        edges = VGroup(
            Line(q1.get_bottom(), y1.get_top(), color=GREY_B), Line(q1.get_bottom(), q2.get_top(), color=GREY_B),
            Line(q2.get_bottom(), q3[0].get_top(), color=GREY_B), Line(q2.get_bottom(), q3[1].get_top(), color=GREY_B),
            Line(q3[0].get_bottom(), leaf.get_top(), color=GREY_B), Line(q3[1].get_bottom(), leaf.get_top(),
                                                                         color=GREY_B))
        yn = VGroup(label(rf"yes, \ {sk['p'][0]:.2f}", font_size=16, color=GREY_B).next_to(edges[0].get_center(),
                                                                                         UL, buff=0.12),
                    label(r"no", font_size=16, color=GREY_B).next_to(edges[1].get_center(), UR, buff=0.12))
        p0 = sk["p"][0]
        mean = wrapped_label(rf"best yes/no questioning \ (a Huffman code, \ \textit{{AI, Built}} Part 1): \ "
                             rf"${p0:.1f} \times 1 + {1 - p0:.1f} \times 3 = {sk['questions']:.1f}$ questions on "
                             rf"average; \ never below $H$", 6.2, font_size=19, color=YES).move_to([3.6, -2.95, 0])
        with self.voiceover(
            "A year later Ray Hyman made the choices unequally likely, and reaction time followed the entropy of the "
            "choice rather than the number of options. <bookmark mark='a'/> Take a menu whose first item is chosen "
            f"seventy percent of the time. Its entropy is {sk['H']:.2f} bits, against {sk['uniform_H']:.2f} for five "
            "equal choices. <bookmark mark='b'/> The best way to ask yes or no questions starts with the likely item: "
            "one question settles seventy percent of cases, and three settle the rest, <bookmark mark='c'/> "
            f"{sk['questions']:.1f} questions on average. That is the Huffman code of AI, Built Part 1, and it is "
            "never shorter than the entropy. The design rule follows: put the likely choice first, or make it the "
            "default."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(hs))
            vo.wait_until("b")
            self.play(FadeIn(q1), Create(edges[:2]), FadeIn(y1), FadeIn(q2), FadeIn(yn))
            self.play(Create(edges[2:4]), FadeIn(q3), Create(edges[4:]), FadeIn(leaf))
            vo.wait_until("c")
            self.play(FadeIn(mean))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        head = label(r"Where Hick's law stops", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 16, 4], [0, 4, 1], x_length=6.2, y_length=3.8, x_label=r"number of choices $n$",
                 y_label=r"time \ (arbitrary units)", xticks=range(0, 17, 4)).move_to([-3.0, -0.2, 0])
        ax = g.ax
        ns = [i / 4 for i in range(0, 65)]
        decide = trace(ax, [(n, 0.6 * math.log2(n + 1)) for n in ns], HEAD, width=3)
        search = trace(ax, [(n, 0.22 * n) for n in ns], NO, width=3)
        practised = trace(ax, [(n, 0.2 * math.log2(n + 1)) for n in ns], YES, width=3)
        lb = VGroup(label(r"decide: \ $\log_2(n + 1)$", font_size=18, color=HEAD).next_to(ax.c2p(16, 2.45), DOWN,
                                                                                      buff=0.45).shift(LEFT * 0.9),
                    label(r"scan an unfamiliar list: \ linear", font_size=18, color=NO).next_to(ax.c2p(13, 3.4), LEFT,
                                                                                         buff=0.15),
                    label(r"after long practice: \ flatter", font_size=18, color=YES).next_to(ax.c2p(16, 0.82), UP,
                                                                                      buff=0.1).shift(LEFT * 0.9))
        tag = note(r"illustrative shapes", font_size=16).next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        W = 5.0
        side = VGroup(
            wrapped_label(r"the law is for choices you must \textbf{decide} among, \ with the options known", W,
                          font_size=20, color=HEAD),
            wrapped_label(r"reading a menu item by item is \textbf{search}: \ time grows with the number of items, "
                          r"\ not its logarithm", W, font_size=20, color=NO),
            wrapped_label(r"practice flattens the slope, \ and familiar layouts become pointing, \ not choosing",
                          W, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.9, 0.0, 0])
        with self.voiceover(
            "Hick's law is often stretched too far. <bookmark mark='a'/> It describes choices you must decide "
            "among, when you already know the options. <bookmark mark='b'/> Reading an unfamiliar menu item by item "
            "is a search, and search time grows with the number of items, not with its logarithm. "
            "<bookmark mark='c'/> And practice flattens the slope: an expert who knows where everything is no longer "
            "chooses at all, but simply points."
        ) as vo:
            self.play(FadeIn(head), Create(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(decide), FadeIn(lb[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(search), FadeIn(lb[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(practised), FadeIn(lb[2]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def goms(self):
        head = label(r"GOMS: \ goals, \ operators, \ methods, \ selection rules", font_size=36).to_edge(UP, buff=0.3)
        goal = _box(r"goal: \ delete a file", HEAD, 3.6, h=0.6, size=21).move_to([0, 1.9, 0])
        m1 = _box(r"method: \ the menu", DATA, 3.6, h=0.6, size=20).move_to([-3.4, 0.5, 0])
        m2 = _box(r"method: \ a keyboard shortcut", LAM, 4.2, h=0.6, size=20).move_to([3.4, 0.5, 0])
        o1 = wrapped_label(r"reach for the mouse; \ point at the file; \ click; \ point at Delete; \ click", 4.4,
                           font_size=19, color=GREY_A).next_to(m1, DOWN, buff=0.35)
        o2 = wrapped_label(r"point at the file; \ click; \ hand to the keyboard; \ press two keys", 4.4,
                           font_size=19, color=GREY_A).next_to(m2, DOWN, buff=0.35)
        ed = VGroup(Line(goal.get_bottom(), m1.get_top(), color=GREY_B), Line(goal.get_bottom(), m2.get_top(),
                                                                                color=GREY_B))
        sel = _box(r"selection rule: \ if you know the shortcut, \ use it", YES, 6.4, h=0.6, size=20).move_to(
            [0, -1.7, 0])
        foot = wrapped_label(r"Card, \ Moran and Newell \ (1983, \ \textit{The Psychology of Human-Computer "
                             r"Interaction}): \ a task as goals, \ methods made of \textbf{operators}, \ and rules "
                             r"for choosing a method; \ give each operator a time, \ and the task has a predicted "
                             r"time", 12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Stuart Card, Thomas Moran and Allen Newell turned these laws into an engineering tool. "
            "<bookmark mark='a'/> Their GOMS analysis describes a task as a goal, such as deleting a file; "
            "<bookmark mark='b'/> methods that achieve it, each a sequence of elementary operators: reach for the "
            "mouse, point, click, press a key; <bookmark mark='c'/> and selection rules for choosing between "
            "methods. Give every operator a time, and you can predict how long a task will take before anyone "
            "has built it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(goal))
            vo.wait_until("b")
            self.play(Create(ed), FadeIn(m1), FadeIn(m2), FadeIn(o1), FadeIn(o2))
            vo.wait_until("c")
            self.play(FadeIn(sel), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def klm(self):
        k = load("klm")
        ops, cases = k["operators"], k["cases"]
        head = label(r"The keystroke-level model", font_size=36).to_edge(UP, buff=0.3)
        col = {"K": DATA, "P": LAM, "B": GREY_B, "H": KERN, "M": HEAD}
        desc = {"K": r"key", "P": r"point", "B": r"button", "H": r"home hands", "M": r"think"}
        legend = VGroup(*[VGroup(Square(0.3, stroke_width=0, fill_color=col[o], fill_opacity=0.9),
                                 label(rf"\textbf{{{o}}} \ {desc[o]} \ {ops[o]:.2f} s", font_size=18, color=col[o]))
                          .arrange(RIGHT, buff=0.12) for o in "KPBHM"]).arrange(RIGHT, buff=0.4)
        legend.next_to(head, DOWN, buff=0.35)
        src = note(r"operator times: \ Card, \ Moran and Newell \ (1980); \ B from Kieras's later KLM guide",
                   font_size=16).next_to(legend, DOWN,
                                                                                                buff=0.12)
        scale, x0 = 0.78, -2.3
        names = {"delete a file: menu": r"delete a file: \ menu",
                 "delete a file: keyboard shortcut": r"delete a file: \ shortcut",
                 "rename: dialog": r"rename: \ dialog", "rename: inline (F2)": r"rename: \ inline \ (F2)"}
        rows = []
        for i, (nm, c) in enumerate(cases.items()):
            y = 0.95 - 0.95 * i
            name = label(names[nm], font_size=19, color=WHITE)
            name.move_to([x0 - 0.25, y + 0.1, 0], aligned_edge=RIGHT)
            seq = mono(c["ops"], size=16, color=GREY_B)
            if seq.width > 4.0:
                seq.width = 4.0
            seq.next_to(name, DOWN, buff=0.08).align_to(name, RIGHT)
            blocks, x = VGroup(), x0
            for o in c["ops"]:
                w = ops[o] * scale
                r = Rectangle(width=w, height=0.42, stroke_color=BG, stroke_width=1.2, fill_color=col[o],
                              fill_opacity=0.9).move_to([x + w / 2, y, 0])
                blk = VGroup(r)
                if w > 0.25:
                    blk.add(label(o, font_size=16, color=BLACK).move_to(r))
                blocks.add(blk)
                x += w
            tot = label(rf"{c['seconds']:.2f} s", font_size=20, color=HEAD).next_to([x, y, 0], RIGHT, buff=0.15)
            rows.append((name, seq, blocks, tot))
        foot = wrapped_label(r"the mental operators dominate: \ the shortcut saves less than its keys suggest; \ "
                             r"what saves time is removing an $M$, \ a moment of deciding", 12.4, font_size=20,
                             color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The keystroke-level model, which Card, Moran and Newell published in 1980, is the simplest version. "
            "<bookmark mark='a'/> A keystroke takes 0.28 seconds for an average typist, pointing with a mouse 1.1, "
            "a button press a tenth, moving a hand between keyboard and mouse 0.4, and a moment of mental "
            "preparation 1.35. <bookmark mark='b'/> Write each method as a string of operators and add them up. "
            f"Deleting a file through a menu: {cases['delete a file: menu']['seconds']:.1f} seconds. With a shortcut: "
            f"{cases['delete a file: keyboard shortcut']['seconds']:.2f}. <bookmark mark='c'/> Renaming through a "
            f"dialog: {cases['rename: dialog']['seconds']:.2f}; inline: "
            f"{cases['rename: inline (F2)']['seconds']:.2f}. <bookmark mark='d'/> The yellow blocks are moments of "
            "thought, and they dominate. A faster design is usually one that asks for fewer decisions, not fewer "
            "keys."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in legend], lag_ratio=0.3), FadeIn(src))
            for i, (name, seq, blocks, tot) in enumerate(rows):
                if i in (0, 2):
                    vo.wait_until("b" if i == 0 else "c")
                self.play(FadeIn(name), FadeIn(seq), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in blocks],
                                                                 lag_ratio=0.15), run_time=1.6)
                self.play(FadeIn(tot), run_time=0.4)
            vo.wait_until("d")
            thinks = [b for (_, _, blocks, _), c in zip(rows, cases.values()) for b, o in zip(blocks, c["ops"])
                      if o == "M"]
            self.play(*[Indicate(b, color=HEAD, scale_factor=1.08) for b in thinks], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
