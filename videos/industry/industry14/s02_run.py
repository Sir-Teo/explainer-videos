from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

PLANS = ("fill", "ceiling", "expand")


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: the last landfill in the valley", "What is a hole in the ground worth?",
             "Chapter one. Run it: the last landfill in the valley.", lit=("unit", "moat"))
        self.valley()
        self.plans()
        self.play15()
        self.play5()
        self.curve()

    def valley(self):
        P = R["run"]["params"]
        hills = VGroup(
            Polygon([-7.2, -2.2, 0], [-4.8, 0.4, 0], [-2.6, -2.2, 0], stroke_width=0, fill_color="#2B3A2E", fill_opacity=1),
            Polygon([1.8, -2.2, 0], [4.6, 0.7, 0], [7.2, -0.6, 0], [7.2, -2.2, 0], stroke_width=0, fill_color="#2B3A2E", fill_opacity=1))
        ground = Rectangle(width=14.4, height=1.4, stroke_width=0, fill_color="#1F2A22", fill_opacity=1).move_to([0, -2.9, 0])
        town = VGroup(*[draw.house(0.45, c).move_to([x, -2.0, 0]) for x, c in
                        zip((-6.4, -5.8, -5.2, -4.6, -4.0, -3.4), ("#B9B2A3", "#C9D3E0", "#B9B2A3", "#C9D3E0", "#B9B2A3", "#C9D3E0"))])
        town_l = tx(f"the valley: {P['region']:.1f} million tons a year", 15, WHITE).next_to(town, UP, buff=0.15)
        fill = draw.landfill_section(2.6, 1.1, fill=0.55).move_to([-0.6, -2.15, 0])
        fill.cap.set_opacity(0)
        fill_l = VGroup(tx("Valley landfill", 18, PRICE, bold=True),
                        tx(f"{P['airspace']:.0f} million tons of airspace left", 14, GREY_A),
                        tx(f"costs ${P['cost']:.0f} a ton to run", 14, GREY_A)).arrange(DOWN, buff=0.04).next_to(fill, UP, buff=0.2)
        nb = VGroup(*[draw.house(0.4, "#9AA3B2").move_to([x, -2.05, 0]) for x in (4.7, 5.2, 5.7, 6.2)])
        nb_l = VGroup(tx(f"neighbours: {P['neighbours']:.1f} million tons", 14, GREY_A),
                      tx(f"come if the fee is ${P['rival_fee']:.0f} or less", 14, GREY_A)).arrange(DOWN, buff=0.03).next_to(nb, UP, buff=0.15)
        far = VGroup(tx("the next landfill, over the hills", 15, WHITE, bold=True),
                     tx(f"its fee ${P['rival_fee']:.0f} + the haul ${P['ceiling'] - P['rival_fee']:.0f}", 14, GREY_A),
                     tx(f"= ${P['ceiling']:.0f}: the valley's ceiling", 15, PRICE, bold=True)).arrange(DOWN, buff=0.04).move_to([4.6, 2.2, 0])
        arrow = CurvedArrow([3.0, 1.6, 0], [0.4, -0.7, 0], angle=0.5, color=GREY_B, stroke_width=2)
        rival = VGroup(Rectangle(width=1.4, height=0.55, stroke_color=BAD, stroke_width=2, fill_color="#1B2230", fill_opacity=1),
                       tx("rival site:", 12, BAD, bold=True), tx("permit applied for", 11, GREY_A)).move_to([2.3, -1.7, 0])
        rival[1].move_to(rival[0].get_center() + UP * 0.1)
        rival[2].move_to(rival[0].get_center() + DOWN * 0.12)
        post = Line([2.3, -1.98, 0], [2.3, -2.3, 0], stroke_color=GREY_B, stroke_width=3)
        tag = estimate_tag("the Works' model: an illustration, not a real landfill", corner=DR, size=12)
        with self.voiceover(
            "You own the only landfill in a valley. <bookmark mark='a'/> It has room for another "
            f"{P['airspace']:.0f} million tons of rubbish, and every ton costs you about ${P['cost']:.0f} to bury: the "
            "compacting, the daily soil cover, the leachate and gas systems, and money set aside for closing it. "
            f"<bookmark mark='b'/> The valley's own towns make {P['region']:.1f} million tons a year. <bookmark mark='c'/> "
            f"The next landfill is over the hills. It charges ${P['rival_fee']:.0f} a ton, and hauling a ton there costs "
            f"another ${P['ceiling'] - P['rival_fee']:.0f}, so the valley will pay you up to ${P['ceiling']:.0f} before it "
            "starts trucking its rubbish away. <bookmark mark='d'/> The towns on the other side would bring you another "
            f"million tons a year, but only at ${P['rival_fee']:.0f}. <bookmark mark='e'/> And someone has applied for a "
            "permit to open a rival landfill in the valley. When it opens, you will both charge "
            f"${P['rival_fee']:.0f} and split the rubbish."
        ) as vo:
            self.play(FadeIn(ground), FadeIn(hills), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(fill), FadeIn(fill_l, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in town], lag_ratio=0.08), FadeIn(town_l))
            lorries = VGroup(*[draw.bin_lorry(0.7).move_to([-5.6 + 0.9 * k, -2.25, 0]) for k in range(2)])
            self.play(FadeIn(lorries))
            self.play(lorries.animate.shift(RIGHT * 3.2), run_time=2.2, rate_func=smooth)
            self.play(FadeOut(lorries, shift=DOWN * 0.15), fill.cells[4].animate.set_opacity(1), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(far), Create(arrow))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in nb], lag_ratio=0.08), FadeIn(nb_l))
            vo.wait_until("e")
            self.play(Create(post), FadeIn(rival, shift=DOWN * 0.1))
            self.play(Indicate(rival, color=BAD))
        self.clear_scene()

    def plans(self):
        P = R["run"]["params"]
        descs = {"fill": [f"charge ${P['rival_fee']:.0f} from day one", f"take {P['region'] + P['neighbours']:.1f} million tons a year",
                          "everyone's rubbish, valley and neighbours"],
                 "ceiling": [f"charge ${P['ceiling']:.0f} until the rival opens", f"take the valley's {P['region']:.1f} million tons",
                             "the neighbours go elsewhere"],
                 "expand": ["charge the ceiling, as plan 2", f"and spend ${P['expansion_cost']:.0f}m now applying to expand",
                            f"+{P['expansion']:.0f} million tons of airspace in year {P['expansion_year']}"]}
        cards = VGroup()
        for i, p in enumerate(PLANS):
            col = PLAN_COL[p]
            box = RoundedRectangle(corner_radius=0.12, width=3.9, height=2.5, stroke_color=col, stroke_width=3,
                                   fill_color="#151A23", fill_opacity=1)
            t = VGroup(tx(f"{i + 1}. {PLAN_NAME[p]}", 21, col, bold=True), *[tx(d, 15, GREY_A) for d in descs[p]]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12)
            t.move_to(box.get_center())
            cards.add(VGroup(box, t))
        cards.arrange(RIGHT, buff=0.3).move_to([0, 0.2, 0])
        head = tx("Three plans. Which is worth most?", 26, WHITE, bold=True).to_edge(UP, buff=0.5)
        foot = tx(f"value = each year's (fee - ${P['cost']:.0f}) x tons, discounted at {100 * P['rate']:.0f}% a year", 17, GREY_B).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "You have three plans. <bookmark mark='a'/> One: fill it fast. Charge the same as the landfill over the "
            "hills, take everybody's rubbish, the valley's and the neighbours', and turn your airspace into cash as "
            "quickly as you can. <bookmark mark='b'/> Two: charge the ceiling. Take only the valley's rubbish, at "
            f"${P['ceiling']:.0f} a ton, until the rival opens. <bookmark mark='c'/> Three: charge the ceiling, and also "
            f"spend ${P['expansion_cost']:.0f} million now on applying to expand, which adds "
            f"{P['expansion']:.0f} million tons of room in year {P['expansion_year']}. <bookmark mark='d'/> We score each "
            f"plan the way an owner would: the cash each year, discounted at {100 * P['rate']:.0f} per cent a year back to "
            "today. Pick one before we run it."
        ) as vo:
            self.play(FadeIn(head))
            for m_, c in zip("abc", cards):
                vo.wait_until(m_)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
            self.wait(1.5)
        self.clear_scene()

    def _bars(self, rival_year: int, x0: float = -5.6):
        G = R["run"]["games"]
        P = R["run"]["params"]
        top = P["airspace"] + P["expansion"]
        sc = 3.4 / top
        out = []
        for i, p in enumerate(PLANS):
            g = G[f"{p}|{rival_year}"]
            x = x0 + 1.25 * i
            frame = Rectangle(width=0.8, height=P["airspace"] * sc, stroke_color=PLAN_COL[p], stroke_width=2).move_to(
                [x, -2.4, 0], aligned_edge=DOWN)
            out.append(dict(p=p, g=g, x=x, frame=frame, sc=sc))
        return out

    def _run(self, rival_year: int, vo_marks, say: str):
        P = R["run"]["params"]
        G = R["run"]["games"]
        bars = self._bars(rival_year)
        t = ValueTracker(0)
        years = 36

        def left_at(g, yr):
            k = int(np.floor(yr))
            lst = g["left"]
            if k <= 0:
                return P["airspace"]
            prev = lst[min(k, len(lst)) - 1]
            nxt = lst[min(k, len(lst) - 1)]
            return prev + (nxt - prev) * (yr - k)

        def pv_at(g, yr):
            v = -P["expansion_cost"] if g is G[f"expand|{rival_year}"] else 0.0
            for j in range(int(np.floor(yr))):
                v += (g["fee"][j] - P["cost"]) * g["tons"][j] / (1 + P["rate"]) ** (j + 1) if j < len(g["fee"]) else 0.0
            return v
        fills, labels, pvs = VGroup(), VGroup(), VGroup()
        for b in bars:
            g, sc = b["g"], b["sc"]
            fl = always_redraw(lambda g=g, b=b: Rectangle(width=0.8, height=max(left_at(g, t.get_value()), 1e-3) * b["sc"],
                                                          stroke_width=0, fill_color=PLAN_COL[b["p"]], fill_opacity=0.75).move_to(
                [b["x"], -2.4, 0], aligned_edge=DOWN))
            fills.add(fl)
            labels.add(tx(PLAN_NAME[b["p"]].replace(", and ", ",\nand "), 13, PLAN_COL[b["p"]], bold=True).next_to(b["frame"], DOWN, buff=0.12))
        head_l = tx("airspace left (million tons)", 14, GREY_B).move_to([-4.35, 1.55, 0])
        # value counters
        for i, b in enumerate(bars):
            n = draw.number(lambda b=b: pv_at(b["g"], t.get_value()), 0, prefix="$", suffix="m", size=34, color=PLAN_COL[b["p"]])
            n.add_updater(lambda m, i=i: m.move_to([3.6, 1.3 - 1.0 * i, 0], aligned_edge=RIGHT))
            pvs.add(n)
        names = VGroup(*[tx(PLAN_NAME[p], 17, PLAN_COL[p], bold=True).move_to([0.2, 1.3 - 1.0 * i, 0], aligned_edge=LEFT)
                         for i, p in enumerate(PLANS)])
        vhead = tx("value today, so far", 16, GREY_B).move_to([2.0, 2.05, 0])
        yr_n = draw.number(lambda: t.get_value(), 0, size=30, color=WHITE)
        yr_n.add_updater(lambda m: m.move_to([-4.0, 2.4, 0], aligned_edge=LEFT))
        yr = VGroup(tx("year", 26, WHITE, bold=True).move_to([-4.15, 2.4, 0], aligned_edge=RIGHT), yr_n)
        pvs.update()
        yr_n.update()
        rival_note = tx(f"the rival opens in year {rival_year}", 16, BAD, bold=True).move_to([1.9, -2.2, 0])
        fulls = VGroup(*[tx(f"full in year {b['g']['full']}", 13, GREY_A).next_to(b["frame"], UP, buff=0.08) for b in bars])
        tag = estimate_tag("the Works' model: an illustration, not a real landfill", corner=DR, size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(tag), FadeIn(head_l), *[FadeIn(b["frame"]) for b in bars], FadeIn(labels), FadeIn(names), FadeIn(vhead))
            self.add(fills, pvs, yr)
            vo.wait_until(vo_marks[0])
            self.play(t.animate.set_value(rival_year), run_time=5.0 if rival_year > 8 else 2.5, rate_func=linear)
            self.play(FadeIn(rival_note, shift=UP * 0.1), Flash(rival_note, color=BAD))
            vo.wait_until(vo_marks[1])
            self.play(t.animate.set_value(years), run_time=5.0, rate_func=linear)
            self.play(FadeIn(fulls))
            vo.wait_until(vo_marks[2])
            final = [G[f"{p}|{rival_year}"]["pv"] for p in PLANS]
            best = int(np.argmax(final))
            self.play(Indicate(pvs[best], color=PLAN_COL[PLANS[best]], scale_factor=1.2), Indicate(names[best], scale_factor=1.1))
        for m in list(pvs) + [yr_n]:
            m.clear_updaters()
        self.clear_scene()

    def play15(self):
        G = R["run"]["games"]
        P = R["run"]["params"]
        f, c, e = (G[f"{p}|15"] for p in PLANS)
        self._run(15, "abc",
                  "Run it, with the rival's permit taking fifteen years. <bookmark mark='a'/> Plan one empties fastest: "
                  f"{P['region'] + P['neighbours']:.1f} million tons a year at a modest margin. Plans two and three fill slowly, at "
                  f"${P['ceiling'] - P['cost']:.0f} of margin on every ton. <bookmark mark='b'/> Then the rival opens, the fee "
                  f"falls to ${P['rival_fee']:.0f}, and the volume is shared. Plan one is already full, in year "
                  f"{f['full']}. <bookmark mark='c'/> The scores: filling fast is worth about ${f['pv']:,.0f} million today. "
                  f"Charging the ceiling, about ${c['pv']:,.0f} million. And charging the ceiling while you expand, about "
                  f"${e['pv']:,.0f} million. The slow, expensive landfill is worth half as much again as the fast, cheap one.")

    def play5(self):
        G = R["run"]["games"]
        c15, c5 = G["ceiling|15"], G["ceiling|5"]
        f5, e5 = G["fill|5"], G["expand|5"]
        rows = VGroup()
        for i, p in enumerate(PLANS):
            a, b = G[f"{p}|15"]["pv"], G[f"{p}|5"]["pv"]
            y = 1.2 - 0.95 * i
            rows.add(VGroup(tx(PLAN_NAME[p], 19, PLAN_COL[p], bold=True).move_to([-4.6, y, 0], aligned_edge=LEFT),
                            tx(f"${a:,.0f}m", 24, WHITE, bold=True).move_to([0.6, y, 0]),
                            tx(f"${b:,.0f}m", 24, PRICE, bold=True).move_to([3.6, y, 0])))
        heads = VGroup(tx("rival in 15 years", 17, GREY_A).move_to([0.6, 2.0, 0]), tx("rival in 5 years", 17, PRICE).move_to([3.6, 2.0, 0]))
        gap = VGroup(tx(f"ten more years of the rival's permitting: worth ${R['run']['permit_worth']:,.0f}m to you", 20, GOOD, bold=True)).move_to([0, -2.0, 0])
        head = tx("The same plans, a faster permit", 24, WHITE, bold=True).to_edge(UP, buff=0.4)
        tag = estimate_tag("the Works' model: an illustration, not a real landfill", corner=DR, size=12)
        with self.voiceover(
            "Now change one thing. Suppose the rival's permit takes five years instead of fifteen. <bookmark mark='a'/> "
            f"Every plan is worth less. Charging the ceiling falls from about ${c15['pv']:,.0f} million to "
            f"${c5['pv']:,.0f} million, because the ceiling only lasts five years. <bookmark mark='b'/> The gap between the "
            f"plans shrinks too: filling fast is worth ${f5['pv']:,.0f} million, expanding ${e5['pv']:,.0f}. "
            "<bookmark mark='c'/> So the most valuable thing you own is not the hole. It is the time it takes anyone "
            f"else to get permission to dig another: in this valley, ten years of it are worth about "
            f"${R['run']['permit_worth']:,.0f} million."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads), FadeIn(tag), *[FadeIn(r_[0]) for r_ in rows], *[FadeIn(r_[1]) for r_ in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[2], shift=LEFT * 0.2) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(gap, shift=UP * 0.1))
        self.clear_scene()

    def curve(self):
        C = R["run"]["curve"]
        G = R["run"]["games"]
        P = R["run"]["params"]
        Ts = sorted(int(k) for k in C)
        top = max(max(v.values()) for v in C.values())
        pa = viz.plot_axes([0, 25], [0, 750], x_length=7.0, y_length=4.4, xticks=[0, 5, 10, 15, 20, 25],
                           yticks=[200, 400, 600], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}m",
                           ylabel="value of the landfill today", size=13).move_to([-2.3, -0.3, 0])
        xl = tx("years until the rival's permit is granted", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        lines = VGroup(*[poly(pa, [(T, C[T][p] if T in C else C[str(T)][p]) for T in Ts], PLAN_COL[p], 4) for p in PLANS])
        labs = VGroup(*[tx(PLAN_NAME[p], 15, PLAN_COL[p], bold=True).next_to(pa.ax.c2p(25, C[25][p]), RIGHT, buff=0.1) for p in PLANS])
        per = G["ceiling|15"]["per_ton"]
        box = VGroup(tx("A ton of airspace", 18, WHITE, bold=True),
                     tx(f"worth about ${per:.0f} in the ground (plan 2, 15 years)", 15, PRICE),
                     tx(f"Waste Management's books: ${R['run']['depletion']:.2f} a ton", 15, GREY_A),
                     tx("(what it cost to build, not what it is worth)", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.5, -1.6, 0])
        tag = estimate_tag("the Works' model: an illustration, not a real landfill", corner=DR, size=12)
        src = source("Waste Management, Form 10-K 2025 (average landfill airspace depletion expense per ton)", size=13)
        with self.voiceover(
            "Draw it for every permit time. <bookmark mark='a'/> If the rival could open tomorrow, the first two plans "
            f"are worth exactly the same, about ${C[0]['fill']:,.0f} million: airspace with competition next door is just "
            "a place to put rubbish. <bookmark mark='b'/> The longer the rival waits, the more the patient plans are worth, and "
            "filling fast stops gaining once you would be full before the rival arrives. <bookmark mark='c'/> Divide by "
            f"the tons, and a ton of room in the ground is worth about ${per:.0f} today. Waste Management's accounts "
            f"carry its airspace at about ${R['run']['depletion']:.2f} a ton, because accounts record what it cost to "
            "build, not what scarcity makes it worth. Hold on to that gap; it is the whole business."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(tag), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(labs[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines[1]), Create(lines[2]), FadeIn(labs[1]), FadeIn(labs[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(box, shift=LEFT * 0.1))
        self.clear_scene()
