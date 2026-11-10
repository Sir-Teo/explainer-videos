from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


def positions():
    pos = {}
    for k in range(8):
        a = math.pi / 2 + 2 * math.pi * k / 8
        pos[k] = np.array([-3.0 + 1.45 * math.cos(a), -0.55 + 1.45 * math.sin(a), 0])
        pos[8 + k] = np.array([3.0 - 1.45 * math.cos(a), -0.55 + 1.45 * math.sin(a), 0])
    return pos


class Karger(VoiceoverScene):
    def construct(self):
        self.card()
        self.contract("trace", "groups", True)
        self.contract("fail_trace", "fail_groups", False)
        self.proof()
        self.measured()
        self.faster()

    def card(self):
        card = chapter_card(4, r"A minimum cut by contraction", r"Can random choices find the weakest link?",
                            lit=(1993,), extra=((1993, r"Karger's contraction"),), part=PART)
        with self.voiceover((
            'Chapter four. A minimum cut by contraction.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def contract(self, key, gkey, good):
        d = load("karger")
        pos = positions()
        edges = [tuple(e) for e in d["edges"]]
        dots = {v: Dot(pos[v], radius=0.13, color=DATA if v < 8 else LAM) for v in range(16)}
        lines = {}
        for i, (u, v) in enumerate(edges):
            ln = Line(pos[u], pos[v], stroke_width=2, color=GREY_B)
            lines[i] = ln
        owner = {v: v for v in range(16)}
        if good:
            head = label(r"Contract random edges until two vertices are left", font_size=32).to_edge(UP, buff=0.3)
        else:
            head = label(r"The same algorithm, \ other coins", font_size=32).to_edge(UP, buff=0.3)
        count = label(rf"16 vertices, \ {d['m']} edges", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(head), *[Create(ln) for ln in lines.values()], *[FadeIn(x) for x in dots.values()],
                  FadeIn(count))
        merges = d[key]
        with self.voiceover(
            (
            'A cut of a graph splits its vertices into two sides; its size is the number of edges between them. This'
            ' graph has two dense clusters joined by three edges, so its minimum cut has size three. Finding a '
            "minimum cut is a classic problem, usually solved with maximum flows. <bookmark mark='a'/> David "
            "Karger's algorithm, from 1993, is almost embarrassingly simple. Pick an edge at random and contract it:"
            ' merge its two ends into one vertex, keep all the other edges, and throw away the loops. Repeat until '
            "two vertices are left. The edges between them are a cut. <bookmark mark='b'/> This run kept all three "
            'bridges to the end and found the minimum cut.'
        )
            if good else
            (
            f"Run it again with other coins. <bookmark mark='a'/> This time a bridge was contracted along the way, "
            f"and the two clusters were merged. <bookmark mark='b'/> What is left cuts a single vertex off from the "
            f'rest, a cut of size '
            f"{d['fail_cut']}"
            f'. Each run can fail, so how often does it succeed?'
        )
        ) as vo:
            vo.wait_until("a")
            rt = 0.35
            for a, b in merges:
                ga = [v for v in owner if owner[v] == a]
                target = dots[b].get_center()
                for v in ga:
                    owner[v] = b
                gone = [i for i, (u, v) in enumerate(edges) if i in lines and owner[u] == owner[v]]
                anims = [dots[v].animate.move_to(target).set_opacity(0) for v in ga]
                anims += [FadeOut(lines.pop(i)) for i in gone]
                # the surviving edges of the merged vertices follow it
                for i, (u, v) in enumerate(edges):
                    if i in lines and (owner[u] == b or owner[v] == b) and (u in ga or v in ga):
                        p = target if u in ga else lines[i].get_start()
                        q = target if v in ga else lines[i].get_end()
                        anims.append(lines[i].animate.put_start_and_end_on(p, q))
                self.play(*anims, run_time=rt)
                dots[b].scale(1.12)
            vo.wait_until("b")
            col = YES if good else NO
            a_, b_ = [dots[v] for v in set(owner.values())]
            pa, pb = a_.get_center(), b_.get_center()
            k = len(lines)
            arcs = VGroup(*[ArcBetweenPoints(pa, pb, angle=(i - (k - 1) / 2) * 0.22, color=col, stroke_width=4)
                            for i in range(k)])
            self.play(*[FadeOut(ln) for ln in lines.values()], *[Create(a) for a in arcs])
            res = label(rf"{len(lines)} edges cross: \ " + (r"the minimum cut" if good else r"not the minimum"),
                        font_size=24, color=col).to_edge(DOWN, buff=0.35)
            self.play(FadeOut(count), FadeIn(res))
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        head = label(r"Why it succeeds often enough", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label('connected graph, \\ minimum cut $k>0$: \\ every vertex has degree $\\ge k$',
                  font_size=22, color=WHITE),
            MathTex(r"m \ge \frac{nk}{2} \quad\Longrightarrow\quad \Pr[\text{the first edge is in } C] = "
                    r"\frac{k}{m} \le \frac{2}{n}", font_size=34, color=LAM),
            label(r"contraction never shrinks the minimum cut, \ so the same holds with $i$ vertices left", font_size=22,
                  color=WHITE),
            MathTex(r"\Pr[C \text{ survives}] \ge \Big(1 - \frac{2}{n}\Big)\Big(1 - \frac{2}{n-1}\Big)\cdots"
                    r"\Big(1 - \frac{2}{3}\Big) = \frac{n-2}{n}\cdot\frac{n-3}{n-1}\cdot\frac{n-4}{n-2}\cdots"
                    r"\frac{1}{3}", font_size=30, color=YES),
            MathTex(r"= \frac{2}{n(n-1)} = \binom{n}{2}^{-1}", font_size=38, color=HEAD),
            label('connected graph: \\ at most $\\binom{n}{2}$ minimum cuts; \\ each specific cut has success probability at least $\\binom{n}{2}^{-1}$', font_size=21, color=CTRL),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 13.2:
                ln.width = 13.2
        with self.voiceover(
            (
            (
            'The analysis is as short as the algorithm. Fix a connected undirected multigraph with positive minimum-'
            "cut size k, and one minimum cut C. <bookmark mark='a'/> Every vertex has at least k edges, because "
            "otherwise the edges around that one vertex would be a smaller cut. <bookmark mark='b'/> So there are at"
            ' least n k over two edges, and the first random edge lands in C with probability at most two over n. '
            "<bookmark mark='c'/> Contracting never creates a smaller cut, so the same argument works at every step,"
            " with n minus one vertices, then n minus two, and so on. <bookmark mark='d'/> C survives to the end if "
            "it survives every step. Write the product out, and almost everything cancels: <bookmark mark='e'/> the "
            'success probability is at least two over n times n minus one, one over n choose two. <bookmark '
            "mark='f'/> There is a free corollary. A specific minimum cut is the output with at least that "
            'probability, and different cuts are different outcomes, so no connected graph has more than n choose '
            'two minimum cuts.'
        )
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(Indicate(ln, color=WHITE) if mk == "a" else FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("karger")
        head = label(rf"Measured: \ {d['trials']:,} runs".replace(",", "{,}"), font_size=34).to_edge(UP, buff=0.35)
        cuts = {int(k): v for k, v in d["cuts"].items()}
        ks = sorted(cuts)[:12]
        top = max(cuts.values())
        bars = VGroup()
        for i, k in enumerate(ks):
            h = 2.6 * cuts[k] / top
            b = Rectangle(width=0.36, height=max(h, 0.02), stroke_width=0, fill_color=YES if k == 3 else GREY_B,
                          fill_opacity=0.85).move_to([-6.0 + i * 0.46, -1.6 + h / 2, 0])
            bars.add(b)
        names = VGroup(*[mono(str(k), 14, GREY_A).next_to(b, DOWN, buff=0.08) for k, b in zip(ks, bars)])
        cap = label(r"the size of the cut found", font_size=18, color=GREY_A).next_to(names, DOWN, buff=0.2)
        res = VGroup(
            label(rf"the minimum cut, \ size 3: \ {d['success']:.1%} of runs".replace("%", r"\%"), font_size=24,
                  color=YES),
            label(rf"the success lower bound $2/(n(n-1))$: \ {d['bound']:.2%}".replace("%", r"\%"), font_size=24, color=HEAD),
            label(r"repeat $\binom{n}{2} \ln n$ times and keep the smallest: \ wrong with probability $\le 1/n$",
                  font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        if res.width > 6.6:
            res.width = 6.6
        res.to_edge(RIGHT, buff=0.4).set_y(1.5)
        cx, cy, rr = 5.6, -1.6, 0.85
        cyc = VGroup(*[Dot([cx + rr * math.cos(2 * math.pi * i / 10), cy + rr * math.sin(2 * math.pi * i / 10),
                            0], radius=0.07, color=LAM) for i in range(10)])
        ring = Circle(radius=rr, color=GREY_B, stroke_width=2).move_to([cx, cy, 0])
        cyc_t = VGroup(
            label(rf"a 10-cycle: \ ${d['cycle_expected']} = \binom{{10}}{{2}}$ minimum cuts", font_size=20,
                  color=LAM),
            label(rf"all {d['cycle_mincuts']} found, \ each in {d['cycle_min_share']:.1%}--"
                  rf"{d['cycle_max_share']:.1%} of runs".replace("%", r"\%"), font_size=20, color=WHITE),
            label(rf"$1/45 = {1 / 45:.1%}$: \ the success lower bound is tight here".replace("%", r"\%"), font_size=20,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        if cyc_t.width > 4.3:
            cyc_t.width = 4.3
        cyc_t.next_to(ring, LEFT, buff=0.35)
        with self.voiceover(
            (
            f'We ran the contraction twenty thousand times on the two-cluster graph. Each bar counts the runs that '
            f"ended with a cut of that size. <bookmark mark='a'/> The minimum cut came out in "
            f"{d['success']:.0%}"
            f' of runs. The lower bound promised at least one in a hundred and twenty, under one percent, so the '
            f"observed rate on this graph is about fifteen times the lower bound. <bookmark mark='b'/> The bound is a"
            f' worst case, and repetition does the rest: run it n choose two times log n times and keep the smallest '
            f"cut, and it is wrong with probability at most one over n. <bookmark mark='c'/> The worst case is real. "
            f'In a ring of ten vertices, any two of the ten edges form a minimum cut, which makes forty-five of them,'
            f' exactly n choose two. The runs found all forty-five, each about once in forty-five tries, so here the '
            f'bound is exact.'
        )
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08),
                      FadeIn(names), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(res[0]), FadeIn(res[1]), Indicate(bars[0], color=YES))
            vo.wait_until("b")
            self.play(FadeIn(res[2]))
            vo.wait_until("c")
            self.play(Create(ring), FadeIn(cyc), FadeIn(cyc_t))
        self.wait(0.3)
        self.clear_scene()

    def faster(self):
        d = load("karger")
        head = label(r"Karger--Stein: \ repeat only where it is risky", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"early contractions are safe: \ $1 - 2/n$ is close to 1", font_size=22, color=WHITE),
            label(r"the risk is at the end, \ with few vertices left", font_size=22, color=WHITE),
            label(r"contract to $n/\sqrt{2}$ vertices: \ the cut survives with probability $\ge \tfrac12$",
                  font_size=22, color=LAM),
            label(r"then recurse \textbf{twice}, \ independently, \ and keep the better cut", font_size=22,
                  color=LAM),
            MathTex(r"T(n) = 2\,T(n/\sqrt{2}) + O(n^2) = O(n^2 \log n), \qquad \Pr[\text{success}] = "
                    r"\Omega(1/\log n)", font_size=32, color=YES),
            label(r"$O(n^2 \log^3 n)$ in all, \ for a high-confidence answer",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            f"Where is the waste? <bookmark mark='a'/> Early contractions have a small individual risk of hitting a "
            f"fixed minimum cut, <bookmark mark='b'/> while the risk increases near the end. <bookmark mark='c'/> "
            f'Karger and Clifford Stein contract to roughly n over root two vertices, with rounding chosen to retain '
            f"a survival probability at least one half. <bookmark mark='d'/> Then two independent recursive branches "
            f"compete and we keep the smaller cut. <bookmark mark='e'/> The standard implementation has order n "
            f'squared log n running time per recursive trial and success at least order one over log n. <bookmark '
            f"mark='f'/> Our forty-eight-vertex graph has an independently certified minimum cut. Plain contraction "
            f'succeeded in '
            f"{d['karger_success']:.0%}"
            f' of two hundred trials; Karger–Stein succeeded in all forty observed trials. These fractions describe '
            f'this graph and seed, not a universal success guarantee.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
