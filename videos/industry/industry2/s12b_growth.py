from __future__ import annotations

from videos.industry.industry2.common import *  # noqa: F403

SHOW = [("Data processing, internet publishing, and other information services", "Web search, cloud, internet services"),
        ("Computer systems design and related services", "Computer systems design"),
        ("Publishing industries, except internet (includes software)", "Software publishing"),
        ("Transit and ground passenger transportation", "Taxis, ride-hailing, buses"),
        ("Professional, scientific, and technical services", "Professional services"),
        ("Oil and gas extraction", "Oil and gas"),
        ("Warehousing and storage", "Warehousing"),
        ("Ambulatory health care services", "Doctors' offices, clinics"),
        ("Manufacturing", "All manufacturing"),
        ("Construction", "Construction"),
        ("Farms", "Farms"),
        ("Food and beverage stores", "Grocery stores"),
        ("Paper products", "Paper"),
        ("Furniture and related products", "Furniture"),
        ("Rail transportation", "Railways"),
        ("Printing and related support activities", "Printing")]


class Growth(VoiceoverScene):
    def construct(self):
        card(self, 14, "Who is growing", "Which industries are getting bigger, and which are shrinking?",
             "Chapter fourteen. Who is growing.", lit=("change",))
        G = R["growth"]
        ch = G["change"]
        gdp = ch["Gross domestic product"]
        sc = 1.3  # screen units per 100%
        x0 = -0.2
        bars = VGroup()
        for k, (key, name) in enumerate(SHOW):
            v = ch[key]
            y = 2.3 - k * 0.335
            col = "#B58CFF" if v > 1.0 else ("#7BD88F" if v > gdp else ("#8B95A7" if v > 0 else "#F2A65A"))
            r = Rectangle(width=max(abs(v) * sc, 0.02), height=0.24, fill_color=col, fill_opacity=0.9,
                          stroke_width=0).move_to(np.array([x0, y, 0]), aligned_edge=LEFT if v >= 0 else RIGHT)
            val = T(f"{100 * v:+.0f}%", 14, col).next_to(r, RIGHT if v >= 0 else LEFT, buff=0.08)
            if 0 <= v < ch["Gross domestic product"]:  # keep short bars' labels clear of the economy's line
                val.move_to(np.array([x0 + ch["Gross domestic product"] * sc + 0.12, y, 0]), aligned_edge=LEFT)
            nm = T(name, 15, I.TEXT)
            if v >= 0:
                nm.move_to(np.array([x0 - 0.12, y, 0]), aligned_edge=RIGHT)
            else:
                nm.next_to(val, LEFT, buff=0.12)
            bars.add(VGroup(nm, r, val))
        bottom = 2.3 - (len(SHOW) - 1) * 0.335 - 0.25
        axis = Line(np.array([x0, 2.55, 0]), np.array([x0, bottom, 0]), color=I.EDGE, stroke_width=1.5)
        gx = x0 + gdp * sc
        mark = DashedLine(np.array([gx, 2.6, 0]), np.array([gx, bottom, 0]), color=I.ACCENT, stroke_width=2)
        mlab = TB(f"the whole economy {100 * gdp:+.0f}%", 16, I.ACCENT).next_to(mark, UP, buff=0.05)
        head = T(f"Growth in real value added, {G['y0']} to {G['y1']} (adjusted for prices)", 22, I.TEXT).to_corner(
            UL, buff=0.35)
        src = source("BEA, chain-type quantity indexes of value added by industry (TVA103), published September 2026",
                     size=13)
        with self.voiceover(
            f"Size is one thing; growth is another. <bookmark mark='a'/> Between {G['y0']} and {G['y1']}, America's "
            f"output, adjusted for prices, grew by {say_pct(gdp)}. <bookmark mark='b'/> The fastest-growing "
            "industries are almost all about computers. Web search, cloud computing and the other internet "
            f"services grew {say_pct(ch[SHOW[0][0]])}: about four times as big. The firms that design and run other "
            "companies' computer systems, and the software publishers, nearly tripled. <bookmark mark='c'/> Taxis "
            "and ride-hailing more than doubled, as the apps turned spare cars into a transport industry. Warehousing "
            "grew with online shopping, oil and gas with the shale fields, doctors' offices and clinics with an "
            "ageing population. <bookmark mark='d'/> Manufacturing as a whole grew "
            f"{say_pct(ch['Manufacturing'])}, slower than the economy, which is why its share keeps falling even as "
            "it makes more. <bookmark mark='e'/> And some industries shrank outright: furniture, paper and the "
            f"railways by about a sixth, printing by {say_pct(-ch['Printing and related support activities'])}, as "
            "screens replaced paper. Growth is the Board's ninth row. An industry that grows faster than the "
            "economy takes a bigger share of it every year; one that shrinks is managed for cash, consolidated or "
            "closed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(axis))
            vo.wait_until("a")
            self.play(Create(mark), FadeIn(mlab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[:3]], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[3:8]], lag_ratio=0.2), run_time=1.8)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[8:12]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.1) for b in bars[12:]], lag_ratio=0.2), run_time=1.5)
            self.play(Indicate(bars[-1], color="#F2A65A", scale_factor=1.04))
        self.clear_scene()
        assert ch[SHOW[0][0]] > 2.5 and ch["Printing and related support activities"] < -0.2
