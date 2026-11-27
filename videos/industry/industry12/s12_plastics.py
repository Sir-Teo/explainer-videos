from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Plastics(VoiceoverScene):
    def construct(self):
        card(self, 10, "Plastics, and where they go", "The industry's biggest product lasts for centuries. What happens to it?",
             "Chapter ten. Plastics, and where they go.", lit=("make", "state"))
        self.polymer()
        self.growth()
        self.fate()
        self.trend()

    def polymer(self):
        mols = VGroup(*[draw.molecule("C2H4", bond=0.32) for _ in range(8)])
        for k, m in enumerate(mols):
            m.move_to([-5.6 + 1.6 * (k % 4) + 0.3 * (k // 4), 1.6 - 1.3 * (k // 4), 0]).rotate(0.25 * (k % 3 - 1))
        lab = tx("ethylene: a double bond between the carbons", 16, ETHYL).next_to(mols, UP, buff=0.3).align_to(mols, LEFT)
        ch = draw.chain(16, bond=0.42).move_to([0, -1.7, 0])
        cl = tx("polyethylene: the double bonds open and the molecules link into a chain", 16, PLASTIC).next_to(ch, DOWN, buff=0.3)
        more = tx("thousands of links long", 15, GREY_A).next_to(ch, RIGHT, buff=0.2)
        prods = VGroup(draw.pellet_bag(1.1), draw.bottle(1.1)).arrange(RIGHT, buff=0.6).move_to([4.6, 1.2, 0])
        pl = tx("pellets, then bottles, film and bags", 15, GREY_A).next_to(prods, DOWN, buff=0.15)
        with self.voiceover(
            "The largest product of the cracker is plastic. <bookmark mark='a'/> Ethylene molecules each carry a double "
            "bond between their two carbons. <bookmark mark='b'/> With the right catalyst, the double bonds open, and the "
            "molecules link hand to hand into a chain, thousands of units long. That is polyethylene. "
            "<bookmark mark='c'/> It leaves the plant as pellets, by the bag and the railcar, and becomes bottles, film, "
            "bags and pipes. Polypropylene, PVC and the rest are made the same way from other building blocks."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in mols], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(lab), *[Indicate(m.bonds[0:2], color=ETHYL) for m in mols], run_time=1.0)
            vo.wait_until("b")
            self.play(TransformFromCopy(mols, ch), mols.animate.set_opacity(0.3), run_time=2.0)
            self.play(FadeIn(cl), FadeIn(more))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in prods], lag_ratio=0.3), FadeIn(pl), run_time=1.5)
        self.clear_scene()

    def growth(self):
        P_ = R["plastics"]
        pr = P_["production"]
        ys = sorted(pr)
        pa = viz.plot_axes([ys[0] - 0.5, ys[-1] + 0.5], [0, 500], x_length=10.0, y_length=4.6, xticks=[1950, 1960, 1970, 1980, 1990,
                                                                                                    2000, 2010, 2019],
                           yticks=[100, 200, 300, 400, 500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f} Mt",
                           ylabel="world plastic production, million tonnes a year", size=14).move_to([-0.3, -0.5, 0])
        area = Polygon(*[pa.ax.c2p(y, pr[y]) for y in ys], pa.ax.c2p(ys[-1], 0), pa.ax.c2p(ys[0], 0), stroke_width=0,
                       fill_color=PLASTIC, fill_opacity=0.35)
        line = VMobject(stroke_color=PLASTIC, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, pr[y]) for y in ys])
        d0 = Dot(pa.ax.c2p(ys[0], pr[ys[0]]), radius=0.07, color=WHITE)
        l0 = tx(f"{ys[0]}: {pr[ys[0]]:.0f} Mt", 16, WHITE, bold=True).next_to(d0, UP + RIGHT, buff=0.1)
        d1 = Dot(pa.ax.c2p(ys[-1], pr[ys[-1]]), radius=0.07, color=WHITE)
        l1 = tx(f"{ys[-1]}: {pr[ys[-1]]:.0f} Mt", 16, WHITE, bold=True).next_to(d1, LEFT, buff=0.15)
        half = next(y for y in ys if sum(pr[k] for k in ys if k <= y) >= sum(pr.values()) / 2)
        hl = tx(f"half of all the plastic made in {ys[0]}-{ys[-1]} was made after {half - 1}", 17, GOLD, bold=True).move_to(
            [-2.0, 1.1, 0])
        per = tx(f"about {1000 * P_['per_person']:.0f} kg for every person on earth in {ys[-1]}", 16, GREY_A).next_to(hl, DOWN, buff=0.12)
        src = source("Geyer, Jambeck and Law (2017) and the OECD, via Our World in Data; population: UN via Our World in Data", size=13)
        with self.voiceover(
            f"And the world makes a great deal of it. <bookmark mark='a'/> In {ys[0]}, about {pr[ys[0]]:.0f} million "
            f"tonnes. <bookmark mark='b'/> By {ys[-1]}, about {pr[ys[-1]]:.0f} million tonnes a year, roughly "
            f"{1000 * P_['per_person']:.0f} kilograms for every person on earth. <bookmark mark='c'/> It grew so fast "
            f"that half of all the plastic made between {ys[0]} and {ys[-1]} was made after {half - 1}."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(d0), FadeIn(l0))
            self.play(Create(line), FadeIn(area), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(d1), FadeIn(l1), FadeIn(per))
            vo.wait_until("c")
            self.play(FadeIn(hl, shift=DOWN * 0.1))
        self.clear_scene()

    def fate(self):
        P_ = R["plastics"]
        f = P_["fate"]
        tot = P_["total_waste"]
        parts = [("landfilled", f["value_landfilled"], "#8A6E52"), ("littered or mismanaged", f["littered_mismanaged_combined"], BAD),
                 ("burned", f["value_incinerated"], PRICE), ("recycled", f["value_recycled"], GOOD)]
        shares = [v / tot for _, v, _ in parts]
        counts = [int(round(100 * s_)) for s_ in shares]
        counts[0] += 100 - sum(counts)
        cells = VGroup()
        colors = sum(([c] * n for (_, _, c), n in zip(parts, counts)), [])
        for k, c in enumerate(colors):
            cells.add(Square(0.36, stroke_color="#0E1117", stroke_width=2, fill_color=GREY_D, fill_opacity=0.5).move_to(
                [-5.6 + 0.4 * (k % 10), 1.9 - 0.4 * (k // 10), 0]))
        groups, i0 = [], 0
        for n in counts:
            groups.append(cells[i0:i0 + n])
            i0 += n
        legend = VGroup()
        for (name, v, c), n in zip(parts, counts):
            legend.add(VGroup(Square(0.3, stroke_width=0, fill_color=c, fill_opacity=0.9),
                              VGroup(tx(f"{name}: {n}%", 20, c, bold=True), tx(f"about {v:.0f} million tonnes", 14, GREY_A)).arrange(
                                  DOWN, aligned_edge=LEFT, buff=0.03)).arrange(RIGHT, buff=0.2))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.2, 0.0, 0])
        head = tx(f"What became of the world's plastic waste in 2019: {tot:.0f} million tonnes", 21, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("OECD, Global Plastics Outlook (2022), via Our World in Data", size=13)
        with self.voiceover(
            f"Most of it is used briefly and thrown away. In 2019 the world threw out about {tot:.0f} million tonnes of "
            "plastic, by the OECD's count. Here is what became of it, each square one per cent. <bookmark mark='a'/> "
            f"About half, {counts[0]} per cent, went into landfills. <bookmark mark='b'/> About {counts[1]} per cent was "
            "littered or dumped where it was not managed, which is how it reaches rivers and seas. <bookmark mark='c'/> "
            f"{counts[2]} per cent was burned. <bookmark mark='d'/> And {counts[3]} per cent was recycled."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(c_, scale=0.6) for c_ in cells], lag_ratio=0.01), run_time=1.5)
            for m_, g_, l_, (_, _, col) in zip("abcd", groups, legend, parts):
                vo.wait_until(m_)
                self.play(LaggedStart(*[c_.animate.set_fill(col, opacity=0.9) for c_ in g_], lag_ratio=0.02),
                          FadeIn(l_, shift=LEFT * 0.1), run_time=1.5)
        self.clear_scene()

    def trend(self):
        F_ = R["plastics"]["fate_years"]
        keys = [("value_recycled", "recycled", GOOD), ("value_incinerated", "burned", PRICE),
                ("littered_mismanaged_combined", "littered or mismanaged", BAD), ("value_landfilled", "landfilled", "#8A6E52")]
        ys = sorted(F_["value_recycled"])
        pa = viz.plot_axes([ys[0], ys[-1]], [0, 400], x_length=8.6, y_length=4.4, xticks=[2000, 2005, 2010, 2015, 2019],
                           yticks=[100, 200, 300, 400], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f} Mt",
                           ylabel="plastic waste, million tonnes a year", size=14).move_to([-1.6, -0.4, 0])
        below = {y: 0.0 for y in ys}
        bands = VGroup()
        labels = VGroup()
        for k, name, c in keys:
            top = {y: below[y] + F_[k][y] for y in ys}
            bands.add(Polygon(*[pa.ax.c2p(y, top[y]) for y in ys], *[pa.ax.c2p(y, below[y]) for y in reversed(ys)], stroke_width=0,
                              fill_color=c, fill_opacity=0.8))
            labels.add(tx(f"{name}: {F_[k][ys[0]]:.0f} → {F_[k][ys[-1]]:.0f} Mt", 15, c, bold=True).move_to(
                [4.6, 0, 0]).set_y(pa.ax.c2p(ys[-1], (below[ys[-1]] + top[ys[-1]]) / 2)[1]))
            below = top
        r0 = F_["value_recycled"][ys[0]] / sum(F_[k][ys[0]] for k, _, _ in keys)
        r1 = F_["value_recycled"][ys[-1]] / sum(F_[k][ys[-1]] for k, _, _ in keys)
        note = tx(f"recycled share: {100 * r0:.0f}% in {ys[0]}, {100 * r1:.0f}% in {ys[-1]}", 18, GOOD, bold=True).to_edge(UP, buff=0.4)
        src = source("OECD, Global Plastics Outlook (2022), via Our World in Data", size=13)
        with self.voiceover(
            f"Over time, recycling has grown, from about {100 * r0:.0f} per cent of plastic waste in {ys[0]} to "
            f"{100 * r1:.0f} in {ys[-1]}. <bookmark mark='a'/> But the pile it is a share of grew faster, so more "
            "plastic went to landfill, and more was mismanaged, every year. <bookmark mark='b'/> There is an economic "
            "reason recycling struggles. Recycled plastic has to compete with new plastic, and new plastic is made from "
            "gas and oil at the lowest-cost crackers in the world. Collecting, sorting and cleaning a mixed bale of "
            "used packaging costs money that the price of new resin does not always cover. <bookmark mark='c'/> Which "
            "is why the question of who pays for plastic waste has become a question for governments."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(note))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bands], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_, shift=LEFT * 0.1) for l_ in labels], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("b")
            self.play(Circumscribe(labels[0], color=GOOD), bands[0].animate.set_fill(opacity=1.0))
            vo.wait_until("c")
            self.play(Indicate(note, color=GOOD))
        self.clear_scene()
