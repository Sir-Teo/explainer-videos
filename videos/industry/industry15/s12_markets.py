from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

PROD = [("logic", "Logic", "chips that compute: accelerators, custom chips, network chips", "#7EC8F5"),
        ("memory", "Memory", "DRAM and flash: where data is kept", "#F2A65A"),
        ("discretes, opto, sensors", "Discretes, opto, sensors", "single transistors, LEDs, lasers, sensors", "#9AA3B2"),
        ("analog", "Analog", "power and signals", "#7BD88F"),
        ("micro", "Micro", "microprocessors, microcontrollers", "#B58CFF")]
PLAT = [("hpc", "high-performance computing", "#7EC8F5"), ("phone", "smartphones", "#7BD88F"), ("iot", "internet of things", "#B58CFF"),
        ("auto", "cars", "#F2A65A"), ("dce", "consumer electronics", "#F6C453"), ("other", "other", "#5C6472")]


class Markets(VoiceoverScene):
    def construct(self):
        card(self, 10, "Where the chips go", "Who buys eight hundred billion dollars of chips?",
             "Chapter ten. Where the chips go.", lit=("sold", "change"))
        self.products()
        self.platforms()
        self.forecast()

    def products(self):
        M = R["markets"]
        P, tot = M["products"], M["total25"]
        W, H, cx, cy = 11.0, 4.4, 0.0, -0.5
        left = cx - W / 2
        tiles, labels = VGroup(), VGroup()
        # slice and dice: logic, memory as columns; the three small ones stacked in the last column
        wl, wm = W * P["logic"] / tot, W * P["memory"] / tot
        rest = tot - P["logic"] - P["memory"]
        boxes = {"logic": (left, cy - H / 2, wl, H), "memory": (left + wl, cy - H / 2, wm, H)}
        y = cy + H / 2
        for k in ("discretes, opto, sensors", "analog", "micro"):
            h = H * P[k] / rest
            boxes[k] = (left + wl + wm, y - h, W - wl - wm, h)
            y -= h
        for k, name, what, col in PROD:
            x0, y0, w, h = boxes[k]
            t = Rectangle(width=w - 0.06, height=h - 0.06, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x0 + w / 2, y0 + h / 2, 0])
            tiles.add(t)
            big = h > 2
            lab = VGroup(tx(name, 20 if big else 16, "#0E1117", bold=True), tx(f"${P[k]:.0f}bn", 26 if big else 18, "#0E1117", bold=True),
                         tx(what, 14 if big else 12, "#1B2230")).arrange(DOWN, buff=0.05)
            if lab.width > w - 0.2:
                lab.scale_to_fit_width(w - 0.2)
            labels.add(lab.move_to(t))
        whole = Rectangle(width=W, height=H, stroke_width=0, fill_color=SILICON, fill_opacity=0.5).move_to([cx, cy, 0])
        tv = ValueTracker(0)
        num = draw.number(lambda: tv.get_value(), prefix="\\$", suffix=" billion", size=34, color=WHITE).move_to(whole)
        head = tx("World semiconductor sales, 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("World Semiconductor Trade Statistics (WSTS), Spring 2026 forecast: 2025 sales by product", size=13)
        with self.voiceover(
            "Where do all these chips go? Start with what they are. <bookmark mark='a'/> In 2025 the world bought about "
            f"${tot:.0f} billion of semiconductors, by the count of WSTS, the industry's own statisticians. "
            f"<bookmark mark='b'/> The biggest slice, about ${P['logic']:.0f} billion, was logic: chips that compute, from "
            "the accelerators in AI servers to the chips that run networks. <bookmark mark='c'/> Next came memory, about "
            f"${P['memory']:.0f} billion: the business of booms and busts we met in chapter eight. <bookmark mark='d'/> "
            f"Then three slices of about ${min(P[k] for k in ('analog', 'micro', 'discretes, opto, sensors')):.0f} to "
            f"${max(P[k] for k in ('analog', 'micro', 'discretes, opto, sensors')):.0f} billion each: the analog chips "
            "that handle power and signals, the microprocessors and microcontrollers, and a mixed bag of single "
            "transistors, light-emitting chips and sensors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(tiles)))
            vo.wait_until("a")
            self.add(num)
            self.play(FadeIn(whole), tv.animate.set_value(tot), run_time=2.0)
            vo.wait_until("b")
            self.remove(num)
            self.play(FadeOut(whole), GrowFromEdge(tiles[0], LEFT), FadeIn(labels[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(tiles[1], LEFT), FadeIn(labels[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(tiles[i], UP), FadeIn(labels[i])) for i in (2, 3, 4)], lag_ratio=0.3),
                      run_time=2.0)
        self.clear_scene()

    def platforms(self):
        M = R["markets"]
        PY = M["plat_years"]
        cols = list(PY)
        H, base = 4.4, -2.6
        xs = [-4.6, -2.7, -0.8, 1.1]
        stacks, pct = [], []
        for x, c in zip(xs, cols):
            st, lab = VGroup(), VGroup()
            y = base
            for k, name, col in PLAT:
                h = H * PY[c][k] / 100
                seg = Rectangle(width=1.25, height=max(h - 0.03, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.88).move_to([x, y + h / 2, 0])
                st.add(seg)
                if PY[c][k] >= 15:
                    lab.add(tx(f"{PY[c][k]:.0f}%", 18, "#0E1117", bold=True).move_to(seg))
                y += h
            stacks.append(st)
            pct.append(lab)
        years = VGroup(*[tx(c, 16, WHITE, bold=True).move_to([x, base - 0.3, 0]) for x, c in zip(xs, cols)])
        # the boundary between computing and phones
        line = VMobject(stroke_color=WHITE, stroke_width=2.5).set_points_as_corners(
            [[x + d, base + H * PY[c]["hpc"] / 100, 0] for x, c in zip(xs, cols) for d in (-0.62, 0.62)])
        icons = {"hpc": draw.server_rack(0.6), "phone": draw.phone(0.5), "auto": draw.car(0.8, PLAT[3][2])}
        key = VGroup()
        for k, name, col in PLAT:
            row = VGroup(Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.9), tx(name, 15, GREY_A)).arrange(RIGHT, buff=0.12)
            key.add(row)
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([4.95, -0.4, 0])
        for k, ic in icons.items():
            i = [p[0] for p in PLAT].index(k)
            ic.next_to(key[i], LEFT, buff=0.2)
        key_icons = VGroup(*icons.values())
        head = tx("TSMC's revenue, by what its chips go into", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        hpc = M["hpc_twd"]
        src = source("TSMC, Form 20-F 2025 (net revenue by platform, 2023-2025); 3Q26 earnings conference presentation", size=13)
        with self.voiceover(
            "And who buys them? TSMC reports its revenue by the kind of product its chips end up in. "
            "<bookmark mark='a'/> In 2023, high-performance computing, its name for the processors and accelerators in "
            f"computers and servers, brought in {PY['2023']['hpc']:.0f} per cent, and smartphones "
            f"{PY['2023']['phone']:.0f} per cent. <bookmark mark='b'/> Then computing pulled ahead: "
            f"{PY['2024']['hpc']:.0f} per cent in 2024, {PY['2025']['hpc']:.0f} in 2025. <bookmark mark='c'/> In the "
            f"third quarter of 2026, {PY['3Q 2026']['hpc']:.0f} per cent, against {PY['3Q 2026']['phone']:.0f} for "
            f"smartphones. <bookmark mark='d'/> In 2025 computing alone brought TSMC about NT${hpc[2025] / 1000:.1f} "
            f"trillion, {hpc[2025] / hpc[2023]:.1f} times as much as two years before. Cars, for all the trouble of the "
            f"shortage, were about {PY['2025']['auto']:.0f} per cent. The phone built the modern chip industry; "
            "computing now pays most of its bills."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(key_icons), FadeIn(years), FadeIn(ghost(*stacks)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in stacks[0]], lag_ratio=0.15), run_time=1.5)
            self.play(FadeIn(pct[0]))
            vo.wait_until("b")
            for i in (1, 2):
                self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in stacks[i]], lag_ratio=0.1), FadeIn(pct[i]), run_time=1.2)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(s, DOWN) for s in stacks[3]], lag_ratio=0.1), FadeIn(pct[3]), run_time=1.2)
            self.play(Create(line), run_time=1.5)
            vo.wait_until("d")
            self.play(Indicate(icons["hpc"], color=PLAT[0][2]), *[Indicate(s[0], color=WHITE, scale_factor=1.03) for s in stacks])
            self.play(Indicate(icons["auto"], color=PLAT[3][2]))
        self.clear_scene()

    def forecast(self):
        F = R["markets"]["forecast"]
        (t0, t1), (m0, m1) = F["total"], F["memory"]
        sc = 6.6 / 1600
        y1, y2 = 1.0, -1.0
        def stack(y, total, mem, op):
            other = Rectangle(width=(total - mem) * sc, height=0.8, stroke_width=0, fill_color="#7EC8F5", fill_opacity=op).move_to([-5.0, y, 0], aligned_edge=LEFT)
            memr = Rectangle(width=mem * sc, height=0.8, stroke_width=0, fill_color="#F2A65A", fill_opacity=op).next_to(other, RIGHT, buff=0.03)
            return VGroup(other, memr)
        s25, s26 = stack(y1, t0, m0, 0.9), stack(y2, t1, m1, 0.9)
        l25 = tx(f"2025: ${t0:.0f}bn", 17, WHITE, bold=True).next_to(s25, UP, buff=0.1).align_to(s25, LEFT)
        l26 = tx(f"2026, forecast in May 2026: ${t1:,.0f}bn", 17, WHITE, bold=True).next_to(s26, UP, buff=0.1).align_to(s26, LEFT)
        m25 = tx(f"memory ${m0:.0f}bn", 12, "#0E1117", bold=True).move_to(s25[1])
        m26 = tx(f"memory ${m1:.0f}bn", 15, "#0E1117", bold=True).move_to(s26[1])
        o26 = tx(f"everything else ${t1 - m1:.0f}bn", 15, "#0E1117", bold=True).move_to(s26[0])
        o25 = tx(f"everything else ${t0 - m0:.0f}bn", 13, "#0E1117", bold=True).move_to(s25[0])
        inc, minc = t1 - t0, m1 - m0
        verdict = VGroup(tx(f"forecast increase: ${inc:.0f}bn", 18, WHITE, bold=True),
                         tx(f"of which memory: ${minc:.0f}bn, {100 * minc / inc:.0f}%", 20, "#F2A65A", bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.6, -2.6, 0])
        head = tx("Where 2026's growth comes from", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("WSTS, Spring 2026 forecast (May 2026): 2025 sales and the 2026 forecast, total and memory", size=13)
        with self.voiceover(
            "One more split, and it explains this year. <bookmark mark='a'/> In 2025 the world bought about "
            f"${t0:.0f} billion of chips, ${m0:.0f} billion of it memory. <bookmark mark='b'/> For 2026, WSTS's forecast of "
            f"May was about ${t1:,.0f} billion, with memory at ${m1:.0f} billion. <bookmark mark='c'/> Of the forecast "
            f"increase of ${inc:.0f} billion, about ${minc:.0f} billion, {100 * minc / inc:.0f} per cent, is memory. The "
            "boom of 2026 is, more than anything, a boom in the price of memory, the most cyclical chip of all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(ghost(s25, s26, opacity=0.2)))
            vo.wait_until("a")
            self.play(GrowFromEdge(s25[0], LEFT), GrowFromEdge(s25[1], LEFT), FadeIn(l25), run_time=1.5)
            self.play(FadeIn(m25), FadeIn(o25))
            vo.wait_until("b")
            self.play(GrowFromEdge(s26[0], LEFT), FadeIn(l26), run_time=1.2)
            self.play(GrowFromEdge(s26[1], LEFT), FadeIn(o26), FadeIn(m26), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(verdict, shift=UP * 0.1), Indicate(s26[1], color="#F2A65A", scale_factor=1.03))
        self.clear_scene()
