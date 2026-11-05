from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403


class Zeno(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Zeno's race", r"Can reason prove that motion is impossible?", lit=(-475, -450),
                            part=PART)
        with self.voiceover("Chapter three. Zeno's race."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.parmenides()
        self.race()
        self.sum_()
        self.lamp()

    def parmenides(self):
        hcs = VGroup(history_card(r"c.\ 475 BCE", r"Parmenides of Elea", r"what is not cannot be thought; so change, "
                                  r"which needs what-is-not, is impossible", width=5.6, color=HIST),
                     history_card(r"c.\ 450 BCE", r"Zeno of Elea", r"paradoxes in defence of his teacher, preserved "
                                  r"by Aristotle, \textit{Physics} VI.9", width=5.6, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        four = VGroup(*[label(t, font_size=28) for t in (r"the dichotomy", r"Achilles and the tortoise",
                                                          r"the arrow", r"the stadium")]).arrange(DOWN, buff=0.22)
        four.move_to([0, -1.6, 0])
        with self.voiceover(
            "The first great test of pure reasoning came from Elea, in southern Italy. <bookmark mark='a'/>Parmenides "
            "argued, from premises he took to be undeniable, that change is impossible, since becoming requires what "
            "is not. <bookmark mark='b'/>His student Zeno defended him with paradoxes, which we know mostly through "
            "Aristotle. <bookmark mark='c'/>Four of them are about motion: the dichotomy, Achilles and the tortoise, "
            "the arrow, and the stadium. Each argues, step by careful step, that something we see every day cannot "
            "happen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hcs[0], shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hcs[1], shift=DOWN * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in four], lag_ratio=0.25))
        self.clear_scene()

    def race(self):
        d = load("zeno")
        st = d["stages"]
        L = 13.0
        x0 = -6.5
        scale = L / 125.0

        def X(m):
            return x0 + m * scale

        track = Line([X(0), -0.5, 0], [X(125), -0.5, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(m), -0.58, 0], [X(m), -0.42, 0], color=GREY_C),
                                MathTex(str(m), font_size=20, color=GREY_B).move_to([X(m), -0.82, 0]))
                         for m in (0, 25, 50, 75, 100, 125)])
        ach = Dot([X(0), -0.5, 0], radius=0.13, color=P.CLAIM)
        tor = Dot([X(100), -0.5, 0], radius=0.11, color=P.TRUE)
        la = label(r"Achilles, \ 10 m/s", font_size=24, color=P.CLAIM).next_to(ach, UP, buff=0.25)
        lt = label(r"tortoise, \ 1 m/s", font_size=24, color=P.TRUE).next_to(tor, UP, buff=0.25)
        rows = VGroup()
        for s in st[:5]:
            dt = s["dt"][0] / s["dt"][1]
            gap = s["gap"][0] / s["gap"][1]
            rows.add(MathTex(rf"\text{{stage }} {s['k']}:\ \ {dt:g}\text{{ s}},\quad \text{{gap left }} {gap:g}\text{{ m}}",
                             font_size=30))
        rows.add(MathTex(r"\vdots", font_size=30))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, 2.0, 0])
        with self.voiceover(
            "Achilles, the fastest runner, races a tortoise and gives it a hundred metres' start. Say he runs ten "
            "metres a second and the tortoise one. <bookmark mark='a'/>To catch the tortoise, Achilles must first "
            "reach the place where it started. That takes him ten seconds, and by then the tortoise has moved ten "
            "metres on. <bookmark mark='b'/>So he must reach that place: one more second, and the tortoise is a "
            "metre ahead. <bookmark mark='c'/>Then a tenth of a second, and a tenth of a metre. "
            "<bookmark mark='d'/>However many stages you complete, there is always another. So, says Zeno, Achilles "
            "never catches the tortoise."
        ) as vo:
            self.play(Create(track), FadeIn(ticks), FadeIn(ach), FadeIn(tor), FadeIn(la), FadeIn(lt))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                s = st[k]
                a = s["achilles"][0] / s["achilles"][1]
                tpos = a + s["gap"][0] / s["gap"][1]
                self.play(ach.animate.move_to([X(a), -0.5, 0]), tor.animate.move_to([X(tpos), -0.5, 0]),
                          la.animate.next_to([X(a), -0.5, 0], UP, buff=0.35),
                          lt.animate.next_to([X(tpos), -0.5, 0], DOWN, buff=0.45), FadeIn(rows[k]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def sum_(self):
        d = load("zeno")
        meet = d["meet"]
        series = MathTex(r"10", r"+", r"1", r"+", r"0.1", r"+", r"0.01", r"+", r"\cdots", r"=", r"\frac{100}{9}",
                         font_size=56).move_to([0, 1.8, 0])
        series[-1].set_color(GOAL)
        G = axes([0, 12], [0, 12], x_length=6.4, y_length=3.4, xticks=[0, 4, 8, 12], yticks=[0, 5, 10],
                 xlabel=r"stages completed", ylabel=r"seconds elapsed", center=[-2.4, -1.4, 0])
        ax = G.ax
        ts = [s["t"][0] / s["t"][1] for s in d["stages"]]
        pts = VGroup(*[Dot(ax.c2p(k + 1, t), radius=0.06, color=P.CLAIM) for k, t in enumerate(ts)])
        lim = DashedLine(ax.c2p(0, meet[0] / meet[1]), ax.c2p(12, meet[0] / meet[1]), color=GOAL)
        ll = MathTex(rf"\tfrac{{100}}{{9}} = {d['meet_float']:.4f}\ \text{{s}}", font_size=30, color=GOAL)
        ll.next_to(lim, UP, buff=0.1).align_to(lim, RIGHT)
        dich = MathTex(r"\tfrac12 + \tfrac14 + \tfrac18 + \cdots = 1", font_size=40).move_to([3.8, -0.6, 0])
        dl = label(r"the dichotomy: \ to cross a room, first cross half of it", font_size=22, color=GREY_A)
        dl.next_to(dich, DOWN, buff=0.25)
        hc = history_card(1821, r"Cauchy", r"a sum of infinitely many terms is the limit of its partial sums",
                          width=4.6, color=HIST, font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "What Zeno showed is that the catch-up has infinitely many stages. What he assumed is that infinitely "
            "many stages must take an infinite time. <bookmark mark='a'/>But the stages shrink: ten seconds, one, a "
            "tenth, a hundredth. Their total is a geometric series, and it sums to one hundred over nine: eleven and "
            "one ninth seconds. <bookmark mark='b'/>The partial sums climb toward that number and never pass it: this "
            "is when Achilles draws level, exactly where simple algebra says he should. <bookmark mark='c'/>The "
            "dichotomy dissolves the same way: half, plus a quarter, plus an eighth, and so on, sums to one. "
            "<bookmark mark='d'/>The tool that makes this precise, the limit, took until the nineteenth century, "
            "with Cauchy and Weierstrass. Zeno's challenge took two thousand years to meet."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(series))
            vo.wait_until("b")
            self.play(FadeIn(G), LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.12), Create(lim),
                      FadeIn(ll))
            vo.wait_until("c")
            self.play(Write(dich), FadeIn(dl))
            vo.wait_until("d")
            self.play(FadeIn(hc))
        self.clear_scene()

    def lamp(self):
        d = load("zeno")["lamp"]
        hc = history_card(1954, r"James Thomson", r"`Tasks and super-tasks': a lamp switched infinitely often "
                          r"before a deadline", width=5.4, color=HIST).to_corner(UL, buff=0.4)
        ax_l = Line([-5.5, -1.6, 0], [5.5, -1.6, 0], color=GREY_C)
        X = lambda t: -5.5 + 11 * t  # noqa: E731
        marks = VGroup()
        for st in d:
            t = st["t"][0] / st["t"][1]
            marks.add(Rectangle(width=0.06, height=0.5, stroke_width=0, fill_color=GOAL if st["on"] else GREY_D,
                                fill_opacity=1).move_to([X(t), -1.6, 0]))
        end = MathTex(r"t = 1:\ \ ?", font_size=40, color=BAD).next_to([X(1), -1.6, 0], UP, buff=0.4)
        lab = VGroup(MathTex(r"0", font_size=26, color=GREY_B).next_to([X(0), -1.6, 0], DOWN),
                     MathTex(r"1", font_size=26, color=GREY_B).next_to([X(1), -1.6, 0], DOWN))
        bulb = Circle(radius=0.5, stroke_color=GOAL, stroke_width=3, fill_color=GOAL, fill_opacity=0.6).move_to(
            [3.6, 1.6, 0])
        grandi = MathTex(r"1 - 1 + 1 - 1 + \cdots\ =\ ?", font_size=40).move_to([0, 0.2, 0])
        brick = label(r"Wall: \ Zeno's paradoxes, and the supertasks they leave behind", font_size=26,
                      color=P.WALL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Has mathematics, then, solved Zeno? Not entirely. <bookmark mark='a'/>In 1954 the philosopher James "
            "Thomson imagined a lamp, switched on at time zero, off at a half, on at three quarters, off at seven "
            "eighths, and so on, infinitely many times, before one minute is up. <bookmark mark='b'/>At the end of "
            "the minute, is the lamp on or off? <bookmark mark='c'/>The switching sequence has no last member, and "
            "the series one minus one plus one, and so on, has no sum. Paul Benacerraf replied that nothing in the "
            "story fixes the final state at all. <bookmark mark='d'/>The limit tells us where Achilles is. It does "
            "not tell us whether an infinite sequence of acts can be completed, and philosophers still argue about "
            "these supertasks. That is the first brick in the Wall."
        ) as vo:
            self.play(FadeIn(hc), Create(ax_l), FadeIn(lab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2), FadeIn(bulb), run_time=2.5)
            for k in range(6):
                self.play(bulb.animate.set_fill(opacity=0.6 if k % 2 else 0.05), run_time=0.4 / (k + 1) + 0.15)
            vo.wait_until("b")
            self.play(FadeIn(end))
            vo.wait_until("c")
            self.play(Write(grandi))
            vo.wait_until("d")
            self.play(FadeIn(brick))
        self.clear_scene()
