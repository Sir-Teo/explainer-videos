from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

BUY = [("households", "pce", "#F2A65A"), ("investment", "investment", "#7EC8F5"), ("government", "government", "#8B95A7"),
       ("buyers abroad", "exports", "#7BD88F")]


class Buyers(VoiceoverScene):
    def construct(self):
        card(self, 11, "Who buys", "Who does the final buying in the economy?", "Chapter eleven. Who buys.",
             lit=("dollar",))
        self.waterfall()
        self.mix()

    def waterfall(self):
        Bt = R["buyers"]["total"]
        inv = Bt["investment"] + Bt["inventories"]
        steps = [("Households", Bt["pce"], "#F2A65A", "for themselves"),
                 ("Investment", inv, "#7EC8F5", "buildings, machines,\nsoftware, new homes"),
                 ("Government", Bt["government"], "#8B95A7", "mostly its own\nemployees' work"),
                 ("Buyers abroad", Bt["exports"], "#7BD88F", "exports")]
        top = sum(v for _, v, _, _ in steps)
        s = 4.2 / top
        base_y = -2.05
        xs = [-5.4, -3.3, -1.2, 0.9]
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        acc = 0.0
        for (name, v, col, note), x in zip(steps, xs):
            r = Rectangle(width=1.45, height=v * s, fill_color=col, fill_opacity=0.9, stroke_width=0)
            r.move_to(np.array([x, base_y + (acc + v / 2) * s, 0]))
            acc += v
            bars.add(r)
            lab = VGroup(TB(name, 19, I.TEXT), T(note, 15, I.DIM, line_spacing=0.8)).arrange(DOWN, buff=0.06)
            labs.add(lab.next_to(np.array([x, base_y, 0]), DOWN, buff=0.15))
            vals.add(TB(f"${v:.1f}tn", 19, col).next_to(r, UP, buff=0.08))
        imp = -Bt["imports"]
        ri = Rectangle(width=1.45, height=imp * s, fill_color=I.COST, fill_opacity=0.9, stroke_width=0)
        ri.move_to(np.array([3.0, base_y + (top - imp / 2) * s, 0]))
        li = VGroup(TB("less imports", 19, I.TEXT), T("made abroad", 15, I.DIM)).arrange(DOWN, buff=0.05).next_to(
            np.array([3.0, base_y, 0]), DOWN, buff=0.15)
        vi = TB(f"-${imp:.1f}tn", 19, I.COST).next_to(ri, DOWN, buff=0.08)
        gdp = R["buyers"]["gdp"]
        rg = Rectangle(width=1.45, height=gdp * s, fill_color=I.MONEY, fill_opacity=0.95, stroke_width=0)
        rg.move_to(np.array([5.3, base_y + gdp * s / 2, 0]))
        lg = VGroup(TB("GDP", 19, I.TEXT), T("2023", 15, I.DIM)).arrange(DOWN, buff=0.05).next_to(
            np.array([5.3, base_y, 0]), DOWN, buff=0.15)
        vg = TB(f"${gdp:.1f}tn", 21, I.MONEY).next_to(rg, UP, buff=0.08)
        links = VGroup(*[DashedLine(np.array([xs[i] + 0.72, base_y + sum(v for _, v, _, _ in steps[:i + 1]) * s, 0]),
                                    np.array([(xs[i + 1] if i + 1 < 4 else 3.0) - 0.72,
                                              base_y + sum(v for _, v, _, _ in steps[:i + 1]) * s, 0]),
                                    color=I.FAINT, stroke_width=1.2) for i in range(4)])
        axis = Line(np.array([-6.4, base_y, 0]), np.array([6.3, base_y, 0]), color=I.EDGE, stroke_width=1.5)
        head = T("America's GDP counted from the buyers' side, 2023", 24, I.TEXT).to_edge(UP, buff=0.35)
        src = source("BEA, 2023 use table: final uses (personal consumption, private fixed investment and inventories, "
                     "government, exports, imports)", corner=DL, size=13)
        sh = {k: Bt[k] / gdp for k in Bt}
        with self.voiceover(
            "There is a second way to measure an economy: not by who makes things, but by who finally buys them. "
            "<bookmark mark='a'/> In 2023 American households bought 18.8 trillion dollars of goods and services for "
            f"themselves, {say_pct(sh['pce'])} of the total. <bookmark mark='b'/> Businesses investing in buildings, "
            "machines and software, and families buying new homes, which also count as investment: 4.9 trillion. "
            "<bookmark mark='c'/> Governments: 4.7 trillion, most of it the work of their own teachers, soldiers and "
            "officials. <bookmark mark='d'/> Buyers abroad: 2.6 trillion of American exports. <bookmark mark='e'/> "
            "That adds up to 31 trillion. But 3.4 trillion of what those buyers bought was made abroad, so it comes "
            "off. <bookmark mark='f'/> What is left, 27.7 trillion dollars, is America's GDP for 2023: exactly the "
            "total that the industries' value added gave, counted from the other end of the table."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(src))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                anims = [GrowFromEdge(bars[i], DOWN), FadeIn(labs[i]), FadeIn(vals[i])]
                if i:
                    anims.append(Create(links[i - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(Create(links[3]), GrowFromEdge(ri, UP), FadeIn(li), FadeIn(vi))
            vo.wait_until("f")
            self.play(GrowFromEdge(rg, DOWN), FadeIn(lg), FadeIn(vg))
            self.play(Indicate(vg, color=I.MONEY))
        self.clear_scene()

    def mix(self):
        S = R["buyers"]["by_sector"]
        show = [("Education and health", "Education, health"), ("Retail", "Retail"), ("Leisure and hotels",
                "Restaurants, hotels"), ("Finance and real estate", "Finance, real estate"), ("Manufacturing",
                "Manufacturing"), ("Information", "Information"), ("Business services", "Business services"),
                ("Mining", "Mining, oil, gas"), ("Construction", "Construction"), ("Government", "Government")]
        W = 7.6
        rows = VGroup()
        for k, (key, name) in enumerate(show):
            d = S[key]
            vals = [d["pce"], d["investment"] + max(d["inventories"], 0), d["government"], d["exports"]]
            tot = sum(vals)
            y = 2.05 - k * 0.47
            nm = T(name, 17, I.TEXT).move_to(np.array([-4.55, y, 0]), aligned_edge=RIGHT)
            seg = VGroup()
            x = -4.2
            for v, (_, _, col) in zip(vals, BUY):
                w = W * v / tot
                if w > 0.004:
                    seg.add(Rectangle(width=w, height=0.34, fill_color=col, fill_opacity=0.9, stroke_color=BACKGROUND,
                                      stroke_width=1).move_to(np.array([x + w / 2, y, 0])))
                x += w
            amt = T(f"${tot:.1f}tn", 15, I.DIM).move_to(np.array([3.95, y, 0]), aligned_edge=LEFT)
            rows.add(VGroup(nm, seg, amt))
        key = VGroup(*[VGroup(Square(0.2, fill_color=c, fill_opacity=0.9, stroke_width=0), T(n, 16, I.TEXT)).arrange(
            RIGHT, buff=0.1) for n, _, c in BUY]).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.55)
        head = T("Who buys each industry's output, 2023 (share of its sales to final users)", 22, I.TEXT).to_edge(
            UP, buff=0.35)
        note = T("Medicare and Medicaid count as households' spending: the households receive the care", 15, I.DIM
                 ).next_to(key, UP, buff=0.18)
        src = source("BEA, 2023 use table, final uses by commodity", size=13)
        with self.voiceover(
            "Each industry has its own customers. <bookmark mark='a'/> Health care, schools, shops, restaurants and "
            "hotels sell almost entirely to households. That includes care paid for by Medicare and Medicaid, which "
            "the statisticians count as households' spending, because households receive it. <bookmark mark='b'/> "
            "Factories sell half to households, a quarter as machinery and equipment that businesses invest in, and "
            "a fifth abroad. Business services sell more than half as investment, because software and research now "
            "count as investment. <bookmark mark='c'/> Builders sell almost nothing to households as consumption: "
            "houses, offices and factories are investment, roads and schools are the government's. Mines and oil "
            "fields sell more than half abroad. And the government is its own biggest customer. <bookmark mark='d'/> "
            "This matters when times turn. Households keep buying food, rent and health care through a recession. "
            "Investment is the buyer that cuts back first and most, so the industries that sell to it, the builders, the machine "
            "makers and the software houses, feel a downturn first and hardest. Part six is about that cycle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.15), FadeIn(note), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[4:7]], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[7:]], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("d")
            self.play(Indicate(VGroup(rows[6], rows[8]), color="#7EC8F5", scale_factor=1.03))
        self.clear_scene()
