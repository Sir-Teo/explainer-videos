from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, GOOD, HURDLE, LEV_C, NET_C, PART, SAFE_C, SPIRAL_C, load)


class Networks(VoiceoverScene):
    def construct(self):
        n = load("network")
        self.card(n)
        self.en_model()
        self.example(n)
        self.senior()
        self.sweep(n)
        self.threshold(n)
        self.clusters(n)
        self.real()
        self.question()

    def card(self, n):
        sw = n["sweeps"]
        c = chapter_card(4, r"Networks", r"When do links between banks share losses, and when do they spread them?",
                         part=PART)
        with self.voiceover(
            'Chapter four. In the chosen symmetric senior-debt model, the effect of links depends on shock size and interbank debt relative to the buffer. With no more than a half-dollar shock, nobody defaults. Above that and up to five, only the directly hit bank defaults in the complete network. Above five all ten default for our chosen debt level. This phase transition is conditional on the model; it does not rank every real network or imply that one bank must fail after any arbitrarily small loss.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def en_model(self):
        rows = [cmath(r"\bar p_i", r"=", r"\textstyle\sum_j L_{ij}", font_size=42),
                cmath(r"\Pi_{ij}", r"=", r"L_{ij}/\bar p_i", font_size=42),
                cmath(r"p_i", r"=", r"\min\Bigl(\bar p_i,\ e_i + \textstyle\sum_j \Pi_{ji}\,p_j\Bigr)", font_size=40,
                      colors={r"p_i": NET_C})]
        whys = [why(r"Eisenberg and Noe (2001): bank $i$ owes $L_{ij}$ to bank $j$; its total obligation"),
                why('pro rata among equal-priority creditors; set the row to zero when total debt is zero'),
                why(r"each bank pays in full or pays everything it has, its outside assets plus what others pay it: a "
                    r"clearing vector solves all of these at once")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "How interbank payments clear, after Larry Eisenberg and Thomas Noe. <bookmark mark='a'/> Each bank owes a "
            "total to the others. <bookmark mark='b'/> A defaulter pays its creditors in proportion to what it owes them. "
            "<bookmark mark='c'/> And each bank pays in full, or pays everything it has: its outside assets plus what the "
            "others pay it. A clearing vector solves every bank's equation at once."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def example(self, n):
        L = np.asarray(n["L"], float)
        e = np.asarray(n["e"], float)
        p = np.asarray(n["p"], float)
        pbar = np.asarray(n["pbar"], float)
        dft = n["default"]
        names = ["A", "B", "C", "D", "E"]
        ang = np.linspace(90, 90 - 360, 6)[:-1] * np.pi / 180
        pos = [np.array([2.4 * np.cos(t) - 2.0, 2.0 * np.sin(t) - 0.2, 0]) for t in ang]
        nodes = VGroup()
        for i in range(5):
            col = BAD if dft[i] else SAFE_C
            c_ = Circle(radius=0.45, color=col, fill_color=col, fill_opacity=0.2).move_to(pos[i])
            t = VGroup(label(names[i], font_size=22, color=col), label(rf"$e = {e[i]:.1f}$", font_size=14, color=GREY_A))
            t.arrange(DOWN, buff=0.04).move_to(pos[i])
            nodes.add(VGroup(c_, t))
        edges = VGroup()
        for i in range(5):
            for j in range(5):
                if L[i, j] > 0:
                    a = Arrow(pos[i], pos[j], buff=0.5, stroke_width=2 + L[i, j], color=NET_C, tip_length=0.18)
                    edges.add(a)
        side = VGroup(*[label(rf"{names[i]}: owes {pbar[i]:.1f}, pays {p[i]:.1f}", font_size=18,
                              color=BAD if dft[i] else GREY_A) for i in range(5)])
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Five banks. <bookmark mark='a'/> Arrows are debts, thicker for larger; each bank also holds some outside "
            "assets. <bookmark mark='b'/> The fictitious default algorithm starts by assuming everyone pays, finds who "
            f"cannot, recomputes, and stops: here after {n['rounds']} rounds. Bank A, with little outside, pays "
            f"{p[0]:.1f} of its {pbar[0]:.0f}; the shortfall passes to its creditors, who absorb it."
        ) as vo:
            self.play(FadeIn(nodes), LaggedStart(*[GrowArrow(a_) for a_ in edges], lag_ratio=0.1))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(side), Indicate(nodes[0], color=BAD))
        self.wait(0.4)
        self.clear_scene()

    def senior(self):
        rows = [cmath(r"x_i", r"=", r"\min\Bigl(y,\ \max\bigl(0,\ a - \varepsilon_i + \textstyle\sum_j \Pi_{ji}x_j - v\bigr)\Bigr)",
                      font_size=34, colors={r"x_i": NET_C}),
                cmath(r"a - v", r":", r"\text{each bank's buffer}", font_size=40, colors={r"a - v": SAFE_C}),
                cmath(r"\Pi", r":", r"\text{ring, complete, or clusters}", font_size=40)]
        whys = [why(r"Acemoglu, Ozdaglar and Tahbaz-Salehi (2015): each bank holds a project worth $a$, owes $v$ to "
                    r"senior outside creditors first and $y$ to other banks; bank 1 takes a shock $\varepsilon$"),
                why('positive net-resource buffer $a-v$; for very large shocks, $a-\\varepsilon$ represents a shortfall against senior obligations, not negative gross assets'),
                why(r"the same total interbank debt, arranged three ways")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A sharper version. <bookmark mark='a'/> Each bank holds a project worth a, owes v to senior outside creditors "
            "first, and y to other banks; one bank takes a shock epsilon. <bookmark mark='b'/> A minus v is each bank's "
            "buffer. <bookmark mark='c'/> And the same total interbank debt can be arranged as a ring, each owing only its "
            "neighbour; as a complete network, each owing all the others a little; or as clusters."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def sweep(self, n):
        g = axes([0, 8], [0, 10.5], x_length=7.6, y_length=4.2, xlabel=r"shock to bank 1", ylabel=r"banks in default",
                 xticks=[0, 2, 4, 5, 6, 8], yticks=[0, 2, 4, 6, 8, 10], font_size=16).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        cols = {"ring": NET_C, "complete": SPIRAL_C, "clusters": SAFE_C}
        lines = {}
        for kind in ("ring", "complete"):
            s = np.asarray(n["sweeps"][kind]["shock"], float)
            d = np.asarray(n["sweeps"][kind]["defaults"], float)
            pts = []
            for i in range(len(s)):
                pts.append(ax.c2p(s[i], d[i]))
                if i + 1 < len(s):
                    pts.append(ax.c2p(s[i + 1], d[i]))
            lines[kind] = VMobject(color=cols[kind], stroke_width=3).set_points_as_corners(pts)
        leg = legend([(NET_C, r"ring"), (SPIRAL_C, r"complete")], font_size=18).to_corner(UL, buff=0.6).shift(RIGHT * 1.0)
        with self.voiceover(
            f"Ten banks, each owing six to the others and with a buffer of half a dollar. <bookmark mark='a'/> In the "
            "ring, defaults climb step by step with the shock: each failure passes the loss to the next bank. "
            "<bookmark mark='b'/> In the complete network, nothing spreads at all, until the shock passes five, and then "
            "all ten fail together."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), Create(lines['ring']))
            vo.wait_until("a")
            self.play(Indicate(lines['ring'], color=HURDLE), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines["complete"]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def threshold(self, n):
        rows = [cmath(r"\varepsilon > a - v", r":", r"\text{bank 1 defaults}", font_size=40),
                cmath(r"\text{its shortfall}", r"=", r"\min(y,(\varepsilon-(a-v))_+),\ \text{shared among }n-1", font_size=36),
                cmath(r"\frac{\varepsilon - (a - v)}{n - 1} > a - v", r"\iff", r"\varepsilon > n\,(a - v) = 5", font_size=36,
                      colors={r"\varepsilon > n\,(a - v) = 5": SPIRAL_C})]
        whys = [why(r"while the others pay in full, bank 1 fails once the shock exceeds its own buffer"),
                why('while others pay, shortfall is $\\min(y,\\max(0,\\varepsilon-(a-v)))$, shared equally by the other banks'),
                why(r"each of them fails when its share exceeds its own buffer: then all do at once, and their failures "
                    r"feed back. With $n = 10$ and a buffer of 0.5, the threshold is 5")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why five for these chosen parameters. <bookmark mark='a'/> Let b equal a minus v, positive. The hit bank defaults only when epsilon exceeds b. <bookmark mark='b'/> If all other banks pay, its interbank shortfall is the smaller of y and the positive part of epsilon minus b. That shortfall is shared among n minus one creditors. <bookmark mark='c'/> If y exceeds n minus one times b, a sufficiently large hit can breach every creditor's buffer, giving the threshold epsilon above n b. Here y is six, exceeding nine times a half. Below the half-dollar buffer there is no default; up to five, only one; above five, all ten. Without the debt-size condition, this conclusion need not hold."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def clusters(self, n):
        s = np.asarray(n["sweeps"]["clusters"]["shock"], float)
        d = np.asarray(n["sweeps"]["clusters"]["defaults"], float)
        d_max = int(d.max())
        g = axes([0, 8], [0, 10.5], x_length=7.6, y_length=4.2, xlabel=r"shock to bank 1", ylabel=r"banks in default",
                 xticks=[0, 2, 4, 6, 8], yticks=[0, 5, 10], font_size=16).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = g.ax
        pts = []
        for i in range(len(s)):
            pts.append(ax.c2p(s[i], d[i]))
            if i + 1 < len(s):
                pts.append(ax.c2p(s[i + 1], d[i]))
        line = VMobject(color=SAFE_C, stroke_width=3).set_points_as_corners(pts)
        with self.voiceover(
            f"""The third chosen network has two groups of five and a two-percent cross-group share. <bookmark mark='a'/> Over this finite shock grid, the maximum default count is {d_max}. The weak link limits transmission in this example. That is not a universal five-bank cap or a global ranking of all clustered networks. The literature's comparisons depend on the admissible network class, liabilities, buffers and shock regime."""
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.play(Indicate(line, color=HURDLE), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def real(self):
        cards = VGroup(
            desk_question(r"real networks are core and periphery", r"a few large dealers are linked to everyone; most "
                          r"banks to a few of them: robust to random failures, fragile to the failure of a hub", width=12.4,
                          font_size=19),
            desk_question(r"direct exposures are often small", r"simulations on supervisors' interbank data found direct "
                          r"contagion rarely large on its own, as surveys reported; it is the combination with fire sales "
                          r"and runs that bites", width=12.4, font_size=19),
            desk_question(r"clearing changed the network", r"central clearing (Part 21) replaced many bilateral links with "
                          r"one hub per market: less contagion between banks, more resting on the clearing house", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And real networks. <bookmark mark='a'/> They are core and periphery: a few large dealers linked to everyone, "
            "robust to random failures and fragile to the failure of a hub. <bookmark mark='b'/> Simulations on "
            "supervisors' interbank data found direct contagion rarely large on its own, as surveys reported: it is the "
            "combination with fire sales and runs that bites. <bookmark mark='c'/> And central clearing, Part twenty-one, "
            "replaced many bilateral links with one hub per market."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"three financial industries: banks, insurers, and other finance. Which matters most for the "
                       r"market in a crash: the one that falls most, or the one whose distress moves the market most?")
        with self.voiceover(
            "Pause and predict. Three financial industries: banks, insurers and other finance. Which matters most for the "
            "market in a crash: the one that falls the most, or the one whose distress moves the market the most?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
