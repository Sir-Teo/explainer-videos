from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load, mono)

POS = {0: (-6.0, -2.3), 1: (-5.0, -2.3), 2: (-4.0, -2.3), 3: (-3.0, -2.3), 4: (-5.5, -1.2), 5: (-3.5, -1.2),
       6: (-4.5, -0.1), 7: (-1.6, -2.3), 8: (-1.1, -1.5), 9: (-0.6, -0.7), 10: (-0.1, 0.1), 11: (0.4, 0.9),
       12: (-2.2, 1.5), 13: (-2.2, 2.4)}


def dag_mob(preds, r=0.26):
    nodes = {k: VGroup(Circle(radius=r, stroke_color=GREY_B, stroke_width=2, fill_color=BG, fill_opacity=1
                              ).set_z_index(1),
                       Text(str(k), font="DejaVu Sans Mono", font_size=16, color=WHITE).set_z_index(3)).move_to(
        [*POS[k], 0]) for k in POS}
    edges = VGroup()
    emap = {}
    for v, ps in enumerate(preds):
        for u in ps:
            a = Arrow(nodes[u][0].get_center(), nodes[v][0].get_center(), buff=r + 0.02, color=GREY_D,
                      stroke_width=2, max_tip_length_to_length_ratio=0.15, tip_length=0.14)
            edges.add(a)
            emap[(u, v)] = a
    return nodes, edges, emap


class WorkSpan(VoiceoverScene):
    def construct(self):
        self.card()
        self.dag()
        self.greedy()
        self.brent()
        self.checked()
        self.stealing()

    def card(self):
        card = chapter_card(9, r"Work, \ span and Brent's theorem", r"How fast can a computation go on $p$ processors?",
                            lit=(1974, 1999), extra=((1974, r"Brent"), (1999, r"Blumofe and Leiserson: \ work "
                                                                              r"stealing")), part=PART)
        with self.voiceover("Chapter nine. Work, span, and Brent's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def dag(self):
        ws = load("workspan")["small"]
        head = label(r"A computation as a graph", font_size=34).to_edge(UP, buff=0.3)
        nodes, edges, emap = dag_mob(ws["preds"])
        path = ws["path"]
        defs = VGroup(
            label(r"each node: \ one unit of work", font_size=22, color=GREY_A),
            label(r"each arrow: \ must finish before", font_size=22, color=GREY_A),
            label(rf"\textit{{work}} $T_1$: \ all the nodes \ $= {ws['work']}$", font_size=24, color=DATA),
            label(rf"\textit{{span}} $T_\infty$: \ the longest path \ $= {ws['span']}$", font_size=24, color=NO),
            label(rf"\textit{{parallelism}} $T_1 / T_\infty = {ws['work'] / ws['span']:g}$", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        laws = VGroup(MathTex(r"T_p \ge T_1 / p", font_size=32, color=DATA),
                      MathTex(r"T_p \ge T_\infty", font_size=32, color=NO)).arrange(RIGHT, buff=0.8).next_to(
            defs, DOWN, buff=0.45)
        ll = note(r"$p$ processors do at most $p$ units a step; \\ a path's nodes run one after another",
                  font_size=17).next_to(laws, DOWN, buff=0.15)
        with self.voiceover(
            (
            "To reason about parallel programs without fixing a machine, draw the computation as a graph. "
            "<bookmark mark='a'/> Each node is a unit of work. Each arrow says one node must finish before "
            "another starts. On the left, four numbers summed as a tree; on the right, a chain of steps, each "
            "needing the one before. <bookmark mark='b'/> Two numbers describe it. The work, T one, is the total "
            "number of nodes: the time on one processor, here fourteen. <bookmark mark='c'/> The span, T "
            "infinity, is the longest path: the time on infinitely many processors, here seven, along the chain. "
            "<bookmark mark='d'/> Their ratio, the parallelism, is average available parallelism along an ideal "
            "span-length execution, here two. Some steps can have more ready work; the ratio is not a maximum "
            "instantaneous width. <bookmark mark='e'/> And they give two lower bounds for any machine with p "
            "processors. It can do at most p nodes a step, so it needs at least T one over p steps. And the nodes "
            "of a path must run one after another, so it needs at least T infinity."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*nodes.values())), Create(edges))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]), FadeIn(defs[1]))
            vo.wait_until("b")
            self.play(FadeIn(defs[2]), LaggedStart(*[nodes[k][0].animate.set_stroke(DATA) for k in nodes],
                                                   lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(defs[3]), *[nodes[k][0].animate.set_stroke(NO, width=3.5) for k in path],
                      *[emap[(a, b)].animate.set_color(NO) for a, b in zip(path, path[1:])])
            vo.wait_until("d")
            self.play(FadeIn(defs[4]))
            vo.wait_until("e")
            self.play(FadeIn(laws), FadeIn(ll))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def greedy(self):
        ws = load("workspan")["small"]
        head = label(r"A greedy schedule on 2 processors", font_size=34).to_edge(UP, buff=0.3)
        nodes, edges, emap = dag_mob(ws["preds"])
        steps = ws["schedules"]["2"]
        rule = label(r"greedy: \ never leave a processor idle \\ while some node is ready", font_size=22,
                     color=HEAD).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
        log = VGroup()
        cols = [DATA, CTRL]
        with self.voiceover(
            "A schedule decides which nodes run at each step. The simplest good rule is greedy: at every step, if "
            "any node is ready, because everything it depends on has finished, never leave a processor idle. "
            "<bookmark mark='a'/> Here is a greedy schedule on two processors. Step by step, up to two ready nodes "
            "run. <bookmark mark='b'/> Notice the steps where only one node was ready, and a processor had to "
            f"wait: they all come from the chain. The schedule takes {len(steps)} steps, against lower bounds of seven "
            "from the work and seven from the span. The best possible schedule, which starts the chain at once, "
            "needs eight: the bounds are not always reachable, but as the next theorem shows, greedy is never far "
            "from them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*nodes.values())), Create(edges), FadeIn(rule))
            vo.wait_until("a")
            frame = 1.0 / float(config.frame_rate)
            budget = vo.start + vo.mark_time("b") - self.renderer.time
            step_time = min(0.7, max(frame, budget / len(steps) - frame))
            for t, run in enumerate(steps):
                anims = [nodes[v][0].animate.set_fill(cols[i], 0.6).set_stroke(cols[i]) for i, v in enumerate(run)]
                e = label(rf"step {t + 1}: \ " + r", \ ".join(str(v) for v in run) + (
                    r" \ (one idle)" if len(run) < 2 else ""), font_size=19, color=NO if len(run) < 2 else GREY_A)
                e.move_to([3.6, 1.3 - 0.36 * t, 0], aligned_edge=LEFT).set_x(2.0, LEFT)
                e.align_to([2.0, 0, 0], LEFT)
                log.add(e)
                self.play(*anims, FadeIn(e), run_time=step_time)
            vo.wait_until("b")
            self.play(*[Indicate(e, color=NO) for e, run in zip(log, steps) if len(run) < 2])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def brent(self):
        head = label(r"Brent's theorem", font_size=36).to_edge(UP, buff=0.3)
        thm = MathTex(r"T_p \;\le\; \frac{T_1}{p} \;+\; T_\infty", font_size=54, color=HEAD).next_to(head, DOWN,
                                                                                                    buff=0.3)
        sub = label(r"for every greedy schedule \ (Brent 1974; \ Graham 1966 for the scheduling form)", font_size=20,
                    color=GREY_B).next_to(thm, DOWN, buff=0.15)
        proof = VGroup(
            label(r"call a step \textit{complete} if all $p$ processors work, \ \textit{incomplete} otherwise",
                  font_size=22, color=GREY_A),
            label(r"complete steps: \ each does $p$ units of the $T_1$, \ so at most $T_1 / p$ of them", font_size=22,
                  color=DATA),
            label(r"incomplete steps: \ fewer than $p$ nodes were ready, \ so \textit{every} ready node ran", font_size=22,
                  color=NO),
            label(r"every longest remaining path starts at a ready node: \ each incomplete step shortens it by one",
                  font_size=22, color=NO),
            label(r"so at most $T_\infty$ incomplete steps. \quad $\blacksquare$", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(sub, DOWN, buff=0.4)
        cor = label(r"and since $\max(T_1/p, \ T_\infty)$ is a lower bound, \ greedy is never worse than twice the "
                    r"best schedule", font_size=22, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How much worse than the lower bounds can a greedy schedule be? Not much, and the proof fits on a slide. "
            "<bookmark mark='a'/> The theorem, from Richard Brent in 1974 and in scheduling form from Ronald Graham in "
            "1966: any greedy schedule on p processors finishes within T one over p, plus T infinity. <bookmark "
            "mark='b'/> Call a step complete if all p processors are busy, and incomplete otherwise. <bookmark "
            "mark='c'/> Each complete step does p units of the total work, so there are at most T one over p of them. "
            "<bookmark mark='d'/> In an incomplete step, fewer than p nodes were ready, so greedy ran every one of "
            "them. <bookmark mark='e'/> Now look at the longest path through the work that remains. Its first node "
            "is ready, because everything before it is done, so it runs in that step, and the longest remaining path "
            "gets one shorter. <bookmark mark='f'/> That can happen at most T infinity times. Add the two kinds of "
            "step, and the theorem is proved. <bookmark mark='g'/> Since the larger of T one over p and T infinity is "
            "a lower bound for every schedule, greedy is always within a factor of two of the best possible."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(thm), FadeIn(sub), run_time=0.6)
            vo.wait_until('a')
            for mk, p in zip("bcdef", proof):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(cor))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checked(self):
        ws = load("workspan")["random"]
        t1, tinf = ws["t1"], ws["tinf"]
        ex = ws["example"]
        head = label(rf"Checked: \ a random computation of {t1:,} nodes, \ span {tinf}", font_size=32).to_edge(
            UP, buff=0.3)
        ps = [e["p"] for e in ex]
        ax = Axes(x_range=[0, 6.3, 1], y_range=[1, 3.5, 1], x_length=7.5, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).shift(LEFT * 1.6 + DOWN * 0.4)
        lx = lambda p: np.log2(p)
        ly = lambda t: np.log10(t)
        xt = VGroup(*[label(str(p), font_size=17, color=GREY_B).next_to(ax.c2p(lx(p), 1), DOWN, buff=0.12)
                      for p in ps])
        yt = VGroup(*[label(rf"{v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(0, ly(v)), LEFT, buff=0.1)
                      for v in (10, 100, 1000)])
        xl = label(r"processors $p$", font_size=18, color=GREY_B).next_to(ax, DOWN, buff=0.45)
        yl = label(r"steps \ (log)", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        pp = np.linspace(0, 6, 60)
        up = ax.plot_line_graph([*pp], [ly(t1 / 2 ** x + tinf) for x in pp], add_vertex_dots=False,
                                line_color=CTRL, stroke_width=3)
        lo = ax.plot_line_graph([*pp], [ly(max(t1 / 2 ** x, tinf)) for x in pp], add_vertex_dots=False,
                                line_color=GREY_B, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(lx(e["p"]), ly(e["makespan"])), radius=0.07, color=YES) for e in ex])
        lu = label(r"Brent: \ $T_1/p + T_\infty$", font_size=20, color=CTRL).next_to(ax.c2p(2.0, ly(t1 / 4 + tinf)),
                                                                                    UR, buff=0.1)
        ll = label(r"$\max(T_1/p, \ T_\infty)$", font_size=20, color=GREY_B).next_to(ax.c2p(5.0, ly(tinf)), DOWN,
                                                                                   buff=0.15)
        w = ws["worst"]
        worst = max(v["ratio_to_lower"] for v in w.values())
        side = VGroup(label(r"greedy, \ measured", font_size=20, color=YES),
                      label(r"40 random graphs, \ $p$ from 1 to 64:", font_size=20, color=GREY_A),
                      label(r"never above Brent's bound", font_size=20, color=GREY_A),
                      label(rf"at worst {worst:.2f} times \\ the lower bound", font_size=20, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax, RIGHT, buff=0.5)
        with self.voiceover(
            f"Here is the theorem checked on a larger computation: two thousand nodes, each depending on up to three recent ones, with a span of {tinf}. <bookmark mark='a'/> The grey curve is the lower bound, the larger of T one over p and T infinity. The orange curve is Brent's upper bound. <bookmark mark='b'/> And the green dots are a greedy schedule, from one processor to sixty-four. These points approach the lower bound as processors are added, then flatten near the span. This is one graph and one priority order; another greedy schedule need not achieve the lower bound. <bookmark mark='c'/> Over forty random graphs, greedy was never above Brent's bound, and never more than {worst:.2f} times the lower bound."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(lo), FadeIn(ll))
            self.play(Create(up), FadeIn(lu))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.2), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stealing(self):
        st = load("stealing")
        head = label(r"Work stealing", font_size=36).to_edge(UP, buff=0.3)
        deqs = VGroup()
        for k in range(4):
            d = VGroup(*[Rectangle(width=0.55, height=0.32, stroke_color=CORE_COLORS[k], stroke_width=1.5,
                                   fill_color=CORE_COLORS[k], fill_opacity=0.35 if j < (3, 1, 0, 2)[k] else 0)
                         for j in range(4)]).arrange(DOWN, buff=0.02)
            deqs.add(VGroup(d, label(rf"core {k}", font_size=17, color=CORE_COLORS[k]).next_to(d, DOWN, buff=0.1)))
        deqs.arrange(RIGHT, buff=0.7).to_edge(LEFT, buff=0.8).shift(UP * 0.6)
        steal = CurvedArrow(deqs[0][0][0].get_top() + UP * 0.05, deqs[2][0][0].get_top() + UP * 0.05, angle=-0.8,
                            color=HEAD, stroke_width=3)
        sl = label(r"an idle core steals the oldest task \\ of a random victim", font_size=18, color=HEAD).next_to(
            steal, UP, buff=0.05)
        rules = VGroup(
            label(r"each core: \ a deque of tasks, \ works on its newest", font_size=20, color=GREY_A),
            label(r"a spawned task goes on the spawner's own deque", font_size=20, color=GREY_A),
            label(r"Blumofe and Leiserson \ (1999): \ $E[T_p] \le T_1/p + O(T_\infty)$, \ $O(p\,T_\infty)$ steals",
                  font_size=20, color=HEAD),
            label(r"Cilk, \ Intel TBB, \ Java's fork/join, \ Rust's Rayon, \ Go's scheduler", font_size=20,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(deqs, DOWN, buff=0.55).align_to(deqs, LEFT)
        rows = st["rows"]
        tab = VGroup(label(rf"simulated: \ a fork-join tree, \ $T_1 = {st['t1']:,}$, \ $T_\infty = {st['tinf']}$",
                           font_size=18, color=GREY_B))
        for r in rows[1:]:
            c = (r["makespan"] - st["t1"] / r["p"]) / st["tinf"]
            tab.add(label(rf"$p = {r['p']}$: \ {r['makespan']:.0f} steps \ $= T_1/p + {c:.1f}\,T_\infty$, \ "
                          rf"{r['steals']:.0f} steal{'' if round(r['steals']) == 1 else 's'}", font_size=18,
                          color=GREY_A))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        worst = max((r["makespan"] - st["t1"] / r["p"]) / st["tinf"] for r in rows[1:])
        with self.voiceover(
            f"Greedy assumes someone hands out the ready nodes. Real runtimes cannot afford a central list that every core fights over, so they use work stealing. <bookmark mark='a'/> Each core keeps its own double-ended queue of tasks and works on the newest. When a task spawns another, the new one goes on the same core's queue. <bookmark mark='b'/> A core with nothing to do picks another core at random and steals the oldest task from its queue, which tends to be a big one. <bookmark mark='c'/> In 1999 Robert Blumofe and Charles Leiserson proved, for fully strict computations under their scheduler and cost assumptions, an expected bound of T one over p plus a constant times T infinity, in expectation, with expected steal attempts bounded by order p times the span. This is an upper bound under a specific model, not a universal claim about communication. <bookmark mark='d'/> Our simplified deque simulation illustrates the scaling on one fork-join tree; it is not the full theorem model: the extra time stays under {worst + 0.05:.1f} spans, and steals are rare. <bookmark mark='e'/> Work stealing appears in Cilk, oneTBB, Java fork-join, Rayon and Go, with different task, queue and scheduling policies; the theorem does not automatically cover each runtime."
        ) as vo:
            self.play(FadeIn(head), FadeIn(deqs))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(Create(steal), FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            vo.wait_until("e")
            self.play(FadeIn(rules[3]))
        self.wait(0.3)
        self.clear_scene()
