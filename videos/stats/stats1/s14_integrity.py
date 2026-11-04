from __future__ import annotations

import numpy as np

from videos.stats.stats1.common import *  # noqa: F403

DISEASE, WOUNDS, OTHER = "#7EB6E8", "#F26D6D", "#8A8F98"
ADV, RET = "#E3B98A", "#9AA3AE"


class Integrity(VoiceoverScene):
    def construct(self):
        self.card()
        self.playfair()
        self.nightingale()
        self.minard()
        self.perception()
        self.lie_factor()

    def card(self):
        card = chapter_card(13, r"Honest pictures", r"A graph is an argument. Make it a fair one.",
                            lit=(1786, 1858, 1869), part=PART)
        with self.voiceover("Chapter thirteen. Honest pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def playfair(self):
        yr = np.array(museum.PLAYFAIR_YEAR)
        wheat = np.array([np.nan if v is None else v for v in museum.PLAYFAIR_WHEAT])
        wages = np.array([np.nan if v is None else v for v in museum.PLAYFAIR_WAGES])
        A = axes([1560, 1825], [0, 105], x_length=10.6, y_length=4.4, xlabel=r"year",
                 ylabel=r"shillings", xticks=[1600, 1650, 1700, 1750, 1800], yticks=[0, 25, 50, 75, 100],
                 center=[0, -0.6, 0])
        ax = A.ax
        bars = VGroup()
        for y, w in zip(yr, wheat):
            if np.isfinite(w):
                lo, hi = ax.c2p(y - 2.2, 0), ax.c2p(y + 2.2, w)
                bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0.5,
                                   stroke_color=BACKGROUND, fill_color=S.MUSEUM, fill_opacity=0.7)
                         .move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
        ok = np.isfinite(wages)
        wl = curve(ax, yr[ok], wages[ok], S.RESID, 4)
        leg = legend([(S.MUSEUM, r"price of a quarter of wheat"), (S.RESID, r"a good mechanic's weekly wage")],
                     font_size=22).to_corner(UL, buff=0.45)
        r = wages / wheat
        hc = history_card(1786, r"William Playfair, \emph{The Commercial and Political Atlas}",
                          r"the line chart and the bar chart; \ the pie chart in 1801", color=S.MUSEUM, width=5.2,
                          font_size=20).to_corner(UR, buff=0.3)
        src = historical_tag(r"Playfair (1821), \emph{A Letter on our Agricultural Distresses}; via Friendly")
        with self.voiceover(
            "Most of the pictures in this part were invented by one man. <bookmark mark='a'/> William Playfair, a "
            "Scottish engineer and pamphleteer, published the first line charts and bar charts in 1786, and the "
            "first pie chart fifteen years later. <bookmark mark='b'/> Here is one of his last, from 1821, redrawn "
            "from his numbers: the price of a quarter of wheat over two and a half centuries, as bars, and a "
            "skilled worker's weekly wage, as a line. <bookmark mark='c'/> Two series on one picture invite a "
            f"comparison. In the 1590s a week's wages bought about {np.nanmin(r[:10]):.2f} of a quarter of wheat; by "
            f"the 1780s, about {np.nanmax(r):.2f}. Playfair's point was that bread had become cheaper relative to "
            "labour than ever before, and the picture makes the argument at a glance, which is both the power and "
            "the danger of a chart."
        ) as vo:
            self.play(FadeIn(src), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(leg[0]),
                      run_time=2.5)
            self.play(Create(wl), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(wl, color=S.RESID, scale_factor=1.02))
        self.clear_scene()

    def rose(self, center, months, rates, R=2.6, rmax=None):
        """Nightingale's wedges: area proportional to the death rate (radius ~ sqrt), largest layer drawn first."""
        g = VGroup()
        rmax = rmax or max(max(r) for r in rates)
        for k in range(len(months)):
            a0 = PI / 2 - k * TAU / 12
            layers = sorted(zip((DISEASE, WOUNDS, OTHER), (rates[0][k], rates[1][k], rates[2][k])), key=lambda t: -t[1])
            for col, v in layers:
                rr = R * np.sqrt(max(v, 0) / rmax)
                if rr < 0.01:
                    continue
                g.add(AnnularSector(inner_radius=0, outer_radius=rr, angle=-TAU / 12, start_angle=a0, color=col,
                                    fill_opacity=0.75, stroke_width=0.8, stroke_color=BACKGROUND).move_arc_center_to(center))
        return g

    def nightingale(self):
        army = np.array(museum.NIGHT_ARMY, float)
        dis, wou, oth = (np.array(v, float) for v in (museum.NIGHT_DISEASE, museum.NIGHT_WOUNDS, museum.NIGHT_OTHER))
        rate = lambda v: 12000 * v / army  # noqa: E731  deaths per 1000 per year
        rd, rw, ro = rate(dis), rate(wou), rate(oth)
        rmax = rd.max()
        y1 = self.rose(np.array([-3.4, -0.4, 0]), range(12), (rd[:12], rw[:12], ro[:12]), R=2.7, rmax=rmax)
        y2 = self.rose(np.array([3.6, -0.4, 0]), range(12), (rd[12:], rw[12:], ro[12:]), R=2.7, rmax=rmax)
        t1 = label(r"April 1854 -- March 1855", font_size=24, color=GREY_A).move_to([-3.4, 3.2, 0])
        t2 = label(r"April 1855 -- March 1856", font_size=24, color=GREY_A).move_to([3.6, 3.2, 0])
        leg = legend([(DISEASE, r"preventable disease"), (WOUNDS, r"wounds"), (OTHER, r"other causes")],
                     font_size=22).to_corner(DR, buff=0.4)
        src = historical_tag(r"Nightingale (1858); \ Pearson \& Short (2007)")
        with self.voiceover(
            "Florence Nightingale used a chart as evidence before a royal commission. <bookmark mark='a'/> Each "
            "wedge is a month of the Crimean War, and its area is that month's death rate in the British army in "
            "the East: blue for preventable disease, red for wounds, grey for everything else. "
            "<bookmark mark='b'/> In the first year, "
            f"{money(dis[:12].sum())} soldiers died of disease and {money(wou[:12].sum())} of wounds. In the worst "
            f"month, January 1855, disease alone was killing at a rate of {rd.max():.0f} per thousand per year: at "
            "that pace the whole army would have died of it within the year. <bookmark mark='c'/> In March 1855 a "
            "sanitary commission arrived, cleaned the water and the drains. The second year's rose is drawn to the "
            f"same scale: {money(dis[12:].sum())} deaths from disease. <bookmark mark='d'/> Nightingale chose area, "
            "not radius, deliberately: double the radius and the wedge looks four times as bad. She wanted the "
            "picture to be true at a glance, and to be unarguable."
        ) as vo:
            hn = history_card(1858, r"Florence Nightingale", r"\emph{Notes on Matters Affecting the Health \dots\ of "
                              r"the British Army}", color=S.MUSEUM, width=5.0, font_size=20).move_to([3.6, 0.6, 0])
            self.play(FadeIn(src), FadeIn(leg), FadeIn(hn, shift=UP * 0.2), FadeIn(t1))
            vo.wait_until("a")
            self.play(FadeOut(hn), LaggedStart(*[GrowFromPoint(w, np.array([-3.4, -0.4, 0]))
                                                for w in y1], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(t2), LaggedStart(*[GrowFromPoint(w, np.array([3.6, -0.4, 0])) for w in y2],
                                              lag_ratio=0.02), run_time=2.5)
        self.clear_scene()

    def minard(self):
        pts = museum.MINARD
        lon = np.array([p[0] for p in pts])
        lat = np.array([p[1] for p in pts])
        X = lambda a: -6.4 + 12.6 * (a - 23.5) / (38.5 - 23.5)  # noqa: E731
        Y = lambda b: -1.6 + 4.6 * (b - 53.8) / (56.0 - 53.8)  # noqa: E731
        bands, adv, ret = VGroup(), [], []
        top = max(p[2] for p in pts)

        def ribbon(seq, col):
            """A band through the points, as wide as the army at each one (Minard's flow)."""
            P = np.array([[X(q[0]), Y(q[1])] for q in seq])
            W = np.array([0.04 + 0.75 * q[2] / top for q in seq])
            left, right = [], []
            for i in range(len(P)):
                d0 = P[i] - P[i - 1] if i > 0 else P[1] - P[0]
                d1 = P[i + 1] - P[i] if i < len(P) - 1 else P[-1] - P[-2]
                t_ = d0 / (np.linalg.norm(d0) + 1e-9) + d1 / (np.linalg.norm(d1) + 1e-9)
                nrm = np.array([-t_[1], t_[0]]) / (np.linalg.norm(t_) + 1e-9)
                left.append([*(P[i] + nrm * W[i] / 2), 0])
                right.append([*(P[i] - nrm * W[i] / 2), 0])
            return Polygon(*left, *right[::-1], stroke_width=0, fill_color=col, fill_opacity=0.9)

        for grp in sorted({p[4] for p in pts}):
            seq = [p for p in pts if p[4] == grp]
            for direction, col, store in (("A", ADV, adv), ("R", RET, ret)):
                part = [p for p in seq if p[3] == direction]
                if direction == "R":  # the retreat starts where the advance turned back
                    turn = [p for p in seq if p[3] == "A"]
                    part = turn[-1:] + part if turn else part
                if len(part) >= 2:
                    rb = ribbon(part, col)
                    bands.add(rb)
                    store.append(rb)
        g1 = [p for p in pts if p[4] == 1]
        start, moscow, end = g1[0][2], max(p[2] for p in g1 if p[3] == "R"), g1[-1][2]
        labels = VGroup(label(rf"{fmt_int(start)}", font_size=22, color=ADV).move_to([X(24.0), Y(55.6), 0]),
                        label(rf"Moscow: \ {fmt_int(moscow)}", font_size=22, color=ADV).move_to([X(37.0), Y(56.0), 0]),
                        label(rf"{fmt_int(end)}", font_size=22, color=RET).move_to([X(24.6), Y(54.0), 0]))
        src = historical_tag(r"Minard (1869); \ data via Wilkinson, \emph{The Grammar of Graphics}")
        cap = label(r"width $\propto$ survivors \qquad tan: \ advance \qquad grey: \ retreat", font_size=22,
                    color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "And the picture often called the best statistical graphic ever drawn. <bookmark mark='a'/> In 1869 "
            "Charles Joseph Minard, a retired French engineer, mapped Napoleon's invasion of Russia in 1812. The "
            "band follows the army's route; its width is the number of men still alive. "
            f"<bookmark mark='b'/> The main column set out {money(start)} strong. <bookmark mark='c'/> It reached "
            f"Moscow with {money(moscow)}. <bookmark mark='d'/> And the grey band is the retreat, through the "
            f"Russian winter, narrowing to {money(end)}. <bookmark mark='e'/> Six variables on one flat page: the "
            "size of the army, its position in two dimensions, its direction, and, in Minard's original, the "
            "dates and the temperature during the retreat. Nothing is decorative. Every mark carries data."
        ) as vo:
            self.play(FadeIn(src), FadeIn(cap))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in adv], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(labels[0]))
            vo.wait_until("c")
            self.play(FadeIn(labels[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b) for b in ret], lag_ratio=0.2), run_time=3.0)
            self.play(FadeIn(labels[2]))
        self.clear_scene()

    def perception(self):
        vals = np.array([23, 21, 20, 19, 17], float)
        cols = REGION_COLORS[:5]
        pie = VGroup()
        a0 = PI / 2
        for v, c in zip(vals, cols):
            ang = TAU * v / vals.sum()
            pie.add(AnnularSector(inner_radius=0, outer_radius=2.0, angle=-ang, start_angle=a0, color=c, fill_opacity=0.85,
                                  stroke_width=1.5, stroke_color=BACKGROUND))
            a0 -= ang
        pie.move_to([-3.6, -0.3, 0])
        names = "ABCDE"
        A = axes([0, 5.6], [0, 25], x_length=5.0, y_length=4.0, yticks=[0, 10, 20], center=[3.4, -0.4, 0])
        ax = A.ax
        bars = VGroup()
        for k, (v, c) in enumerate(zip(vals, cols)):
            lo, hi = ax.c2p(k + 0.6, 0), ax.c2p(k + 1.4, v)
            bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=c,
                               fill_opacity=0.85).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
        bl = VGroup(*[label(n, font_size=24, color=c).next_to(ax.c2p(k + 1.0, 0), DOWN, buff=0.12)
                      for k, (n, c) in enumerate(zip(names, cols))])
        q = label(r"Which is larger, \ B or C?", font_size=30).to_edge(UP, buff=0.5)
        rank = VGroup(*[label(t, font_size=22, color=GREY_A) for t in (
            r"1.\ position on a common scale", r"2.\ position on unaligned scales", r"3.\ length",
            r"4.\ angle, \ slope", r"5.\ area", r"6.\ volume, \ colour")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rank.to_corner(DR, buff=0.35)
        rh = label(r"Cleveland \& McGill (1984)", font_size=24, color=S.ACCENT).next_to(rank, UP, buff=0.15)
        tag = note(r"illustrative: \ 23, 21, 20, 19, 17").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Some picture forms are easier to read than others, and this has been measured. "
            "<bookmark mark='a'/> Here are five numbers as a pie. Which slice is bigger, B or C? Hard to say. "
            "<bookmark mark='b'/> The same five numbers as bars: B is bigger, and you can see by how much. "
            "<bookmark mark='c'/> In 1984 William Cleveland and Robert McGill tested how accurately people judge "
            "different encodings. Positions along a common scale came first; then lengths; then angles; areas and "
            "colours came last. A pie chart asks you to compare angles. A bar chart asks you to compare positions. "
            "That's why nearly every chart in this series is a position on an axis."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in pie], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(A), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15), FadeIn(bl))
            vo.wait_until("c")
            self.play(pie.animate.scale(0.7).shift(UP * 0.3 + LEFT * 0.3), A.animate.shift(LEFT * 2.6),
                      bars.animate.shift(LEFT * 2.6), bl.animate.shift(LEFT * 2.6))
            self.play(FadeIn(rh), LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rank], lag_ratio=0.15))
        self.clear_scene()

    def lie_factor(self):
        A1 = axes([0, 3], [97, 100.5], x_length=4.0, y_length=4.2, yticks=[97, 98, 99, 100], center=[-3.6, -0.5, 0])
        A2 = axes([0, 3], [0, 105], x_length=4.0, y_length=4.2, yticks=[0, 25, 50, 75, 100], center=[3.0, -0.5, 0])

        def two(ax, base):
            g = VGroup()
            for k, (v, c) in enumerate(((98.0, S.CTRL), (100.0, S.TREAT))):
                lo, hi = ax.c2p(k + 0.6, base), ax.c2p(k + 1.4, v)
                g.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=c,
                                fill_opacity=0.85).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
            return g

        b1, b2 = two(A1.ax, 97.0), two(A2.ax, 0.0)
        t1 = label(r"axis from 97", font_size=26, color=S.RESID).next_to(A1, UP, buff=0.2)
        t2 = label(r"axis from 0", font_size=26, color=S.KEPT).next_to(A2, UP, buff=0.2)
        visual = (100 - 97) / (98 - 97)
        data = 100 / 98
        lf = (visual - 1) / (data - 1)
        eq = cmath(r"\text{lie factor}", r"=", r"\frac{\text{size of effect in the graphic}}{\text{size of effect in the data}}",
                   font_size=30).to_edge(UP, buff=0.35)
        val = MathTex(rf"= \frac{{{visual:.0f} - 1}}{{{data:.3f} - 1}} \approx {lf:.0f}", font_size=30,
                      color=S.RESID).next_to(eq, DOWN, buff=0.2)
        with self.voiceover(
            "And the commonest dishonesty of all. <bookmark mark='a'/> Two bars: ninety-eight and a hundred. Start "
            "the axis at ninety-seven, and the second bar is three times the height of the first. "
            "<bookmark mark='b'/> Start it at zero, and they're nearly equal, which is the truth: a two percent "
            "difference. <bookmark mark='c'/> Edward Tufte gave the distortion a number in 1983, the lie factor: "
            "the size of the effect shown in the graphic divided by the size of the effect in the data. A bar "
            f"three times as tall for a value two percent larger has a lie factor of about {lf:.0f}. "
            "<bookmark mark='d'/> A truncated axis isn't always wrong; for a line chart of a slowly changing "
            "quantity it's often right. But a bar's length is a claim about an amount, and bars should start at "
            "zero."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A1), FadeIn(t1), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b1], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(A2), FadeIn(t2), LaggedStart(*[GrowFromEdge(b, DOWN) for b in b2], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Write(eq))
            self.play(FadeIn(val))
        self.clear_scene()
