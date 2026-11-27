from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

TIGHT, LOOSE = "#E8554E", "#7BD88F"


class Tariffs(VoiceoverScene):
    def construct(self):
        card(self, 11, "Tariffs and the reshuffling of the chain", "Did the tariffs move the factories?",
             "Chapter eleven. Tariffs and the reshuffling of the chain.", lit=("change",))
        self.timeline()
        self.shares("phones")
        self.units()
        self.shares("laptops")
        self.laptop_units()
        self.tvs()

    def timeline(self):
        T = R["tariffs"]
        sh = T["china_share"]
        x0, x1, t0, t1 = -6.2, 6.2, 2018.0, 2026.6

        def X(t):
            return x0 + (t - t0) / (t1 - t0) * (x1 - x0)
        axis = Line([x0, -0.2, 0], [x1, -0.2, 0], stroke_color=GREY_B, stroke_width=2.5)
        ticks = VGroup(*[tx(str(y), 14, GREY_B).move_to([X(y + 0.5), -0.5, 0]) for y in range(2018, 2027)])
        ev = [(2018.47, 1, "June 2018", f"{T['r2018']:.0f}% on a first list\nof Chinese goods", "83 FR 28710", True, "c"),
              (2019.63, 2, "August 2019", f"goods where China supplied\n{T['share_rule']:.0f}%+ of US imports: delayed\n"
               f"(phones {100 * sh['phones'][2018]:.0f}%, laptops {100 * sh['laptops'][2018]:.0f}% in 2018)", "84 FR 43304", True, "c"),
              (2019.96, 1, "December 2019", "that duty suspended\nbefore it began", "84 FR 69447", False, "c"),
              (2025.3, 2, "spring 2025", "new tariffs on imports from\nChina, India, Vietnam, Taiwan...", "Apple 10-K", True, "l"),
              (2026.04, 1, "January 2026", "chip investigation: no new\ntariffs on Apple's products", "Apple 10-K", False, "l"),
              (2026.14, 2, "20 February 2026", "Supreme Court strikes down\nthe emergency tariffs; refunds", "Apple 10-K", False, "r")]
        marks, labels = [], []
        for t, tier, when, what, cite, tight, side in ev:
            col = TIGHT if tight else LOOSE
            y = -0.2 + (0.95 * tier + 0.3 if tight else -0.95 * tier - 0.3)
            stem = Line([X(t), -0.2, 0], [X(t), y, 0], stroke_color=col, stroke_width=2)
            tri = Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale(0.09).move_to([X(t), -0.2, 0])
            if not tight:
                tri.rotate(PI)
            lab = VGroup(tx(when, 14, col, bold=True), *[tx(s_, 12, WHITE) for s_ in what.split("\n")], tx(cite, 11, GREY_B)).arrange(DOWN, buff=0.03)
            lab.next_to([X(t), y, 0], UP if tight else DOWN, buff=0.05)
            if side == "l":
                lab.align_to([X(t) - 0.08, 0, 0], RIGHT)
            elif side == "r":
                lab.align_to([X(t) + 0.08, 0, 0], LEFT)
            if lab.get_right()[0] > 6.9:
                lab.shift(LEFT * (lab.get_right()[0] - 6.9))
            if lab.get_left()[0] < -6.9:
                lab.shift(RIGHT * (-6.9 - lab.get_left()[0]))
            marks.append(VGroup(stem, tri))
            labels.append(lab)
        src = source("Federal Register: USTR Section 301 notices 83 FR 28710, 84 FR 43304, 84 FR 69447; Apple, Form 10-K FY2026; "
                     "UN Comtrade (China's shares)", size=12)
        groups = [(0,), (1, 2), (3,), (4, 5)]
        with self.voiceover(
            "Since 2018 America has tried to move this chain with tariffs. <bookmark mark='a'/> In June 2018 it put a 25 per "
            "cent duty on a first list of Chinese goods. <bookmark mark='b'/> In August 2019 it announced duties on most of "
            "the rest, but delayed those on goods where China supplied three-quarters or more of America's imports. Phones "
            f"and laptops were such goods: China supplied {100 * sh['phones'][2018]:.0f} and {100 * sh['laptops'][2018]:.0f} "
            "per cent of them in 2018. That December the delayed duty was suspended before it began. "
            "<bookmark mark='c'/> In the spring of 2025 came new tariffs on imports from almost everywhere, China, India and "
            "Vietnam included, as Apple's annual report records. <bookmark mark='d'/> In January 2026 an investigation into "
            "chips imposed nothing new on Apple's products, and on 20 February the Supreme Court struck down the tariffs "
            "imposed under emergency powers; Apple applied for refunds."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks), FadeIn(src), FadeIn(ghost(*marks, *labels, opacity=0.2)))
            for mk, grp in zip("abcd", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[AnimationGroup(Create(marks[i]), FadeIn(labels[i], shift=UP * 0.1)) for i in grp], lag_ratio=0.5),
                          run_time=1.0 + 0.4 * len(grp))
        self.clear_scene()

    def shares(self, key):
        T = R["tariffs"]
        D = T[key]
        ys = list(range(2015, 2026))
        order = ["China", "India", "Vietnam", "Thailand", "Mexico", "other"] if key == "laptops" else ["China", "India", "Vietnam", "other"]
        sc = 4.4 / 70
        base = -2.4
        cols = VGroup()
        for i, y in enumerate(ys):
            x = -5.6 + 0.95 * i
            parts = {p: D.get(p, {}).get(y, 0.0) for p in order[:-1]}
            parts["other"] = D["World"][y] - sum(parts.values())
            st, h0 = VGroup(), base
            for p in order:
                v = max(parts[p], 0)
                if v * sc < 0.004:
                    continue
                st.add(Rectangle(width=0.62, height=v * sc, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9).move_to([x, h0, 0], aligned_edge=DOWN))
                h0 += v * sc
            share = parts["China"] / D["World"][y]
            cols.add(VGroup(st, tx(str(y), 12, GREY_B).move_to([x, base - 0.22, 0]),
                            tx(f"{100 * share:.0f}%", 13, COUNTRY_COL["China"], bold=True).move_to([x, h0 + 0.18, 0])))
        key_ = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9), tx(p, 14, GREY_A)).arrange(RIGHT, buff=0.08)
                        for p in order]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.4, 0.4, 0])
        name = {"phones": "mobile phones", "laptops": "laptops"}[key]
        head = tx(f"US imports of {name}, by country (above each bar: China's share)", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        hs = "HS 851712 to 2021, 851713 from 2022" if key == "phones" else "HS 847130"
        src = source(f"UN Comtrade: US imports ({hs}), by partner, 2015-2025, as reported by the United States", size=13)
        c18, c25 = D["China"][2018], D["China"][2025]
        if key == "phones":
            other, ov = "India", D["India"][2025]
            text = (f"Here are America's imports of mobile phones. <bookmark mark='a'/> From 2015 to 2024, China supplied "
                    f"about three-quarters or more of them, tariffs or no tariffs. <bookmark mark='b'/> Then in 2025, the year "
                    f"of the new tariffs, China's phones fell to ${c25:.0f} billion, from ${D['China'][2024]:.0f} billion, and "
                    f"India's rose to ${ov:.0f} billion. India's share went from almost nothing in 2018 to "
                    f"{100 * ov / D['World'][2025]:.0f} per cent in seven years, most of it in the last two.")
        else:
            other, ov = "Vietnam", D["Vietnam"][2025]
            text = (f"And laptops. <bookmark mark='a'/> China supplied more than nine in every ten until 2022. "
                    f"<bookmark mark='b'/> Then they moved, fast: by 2025 China's share was "
                    f"{100 * c25 / D['World'][2025]:.0f} per cent, and Vietnam's ${ov:.0f} billion was the largest. The "
                    "tariffs of 2018 hardly moved the laptop; the years since 2023 did.")
        with self.voiceover(text) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key_), *[FadeIn(c[1]) for c in cols], FadeIn(ghost(*[c[0] for c in cols], opacity=0.2)))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(*[GrowFromEdge(r_, DOWN) for r_ in c[0]], FadeIn(c[2])) for c in cols[:-1]], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r_, DOWN) for r_ in cols[-1][0]], FadeIn(cols[-1][2]), run_time=1.5)
            self.play(Indicate(cols[-1][0], color=COUNTRY_COL[other], scale_factor=1.05))
        self.clear_scene()

    def units(self):
        U = R["tariffs"]["units"]["phones"]
        per = 5
        rows = VGroup()
        for i, p in enumerate(("China", "India", "Vietnam")):
            for j, y in enumerate((2024, 2025)):
                n = int(round(U[p][y] / per))
                g = VGroup(*[draw.phone(0.3, screen=COUNTRY_COL[p]) for _ in range(n)]).arrange(RIGHT, buff=0.04)
                lab = tx(f"{p}, {y}: {U[p][y]:.0f} million", 14, COUNTRY_COL[p] if y == 2025 else GREY_A, bold=y == 2025)
                y_ = 2.4 - 0.95 * (2 * i + j)
                lab.move_to([-6.6, y_, 0], aligned_edge=LEFT)
                g.next_to([-3.4, y_, 0], RIGHT, buff=0)
                if j == 0:
                    g.set_opacity(0.45)
                rows.add(VGroup(lab, g))
        key = tx(f"each phone: {per} million smartphones imported into the United States", 13, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("UN Comtrade: US imports of smartphones (HS 851713), units, by partner, 2024 and 2025", size=13)
        with self.voiceover(
            "Count the phones rather than the dollars. <bookmark mark='a'/> In 2024 about "
            f"{U['China'][2024]:.0f} million smartphones came to America from China; in 2025, about {U['China'][2025]:.0f} "
            f"million. <bookmark mark='b'/> From India, {U['India'][2024]:.0f} million, then {U['India'][2025]:.0f} million. "
            f"<bookmark mark='c'/> From Vietnam, {U['Vietnam'][2024]:.0f} million, then {U['Vietnam'][2025]:.0f} million. "
            "Tens of millions of phones a year changed country of assembly in twelve months."
        ) as vo:
            self.play(FadeIn(src), FadeIn(key), *[FadeIn(r_[0]) for r_ in rows], FadeIn(ghost(*[r_[1] for r_ in rows], opacity=0.15)))
            for mk, k in zip("abc", (0, 2, 4)):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(i_, shift=RIGHT * 0.1) for i_ in rows[k][1]], lag_ratio=0.02), run_time=1.0)
                self.play(LaggedStart(*[FadeIn(i_, shift=RIGHT * 0.1) for i_ in rows[k + 1][1]], lag_ratio=0.02), run_time=1.0)
        self.clear_scene()

    def tvs(self):
        T = R["tariffs"]["tvs"]
        ys = (2017, 2025)
        sc = 0.32
        cols = VGroup()
        for j, y in enumerate(ys):
            x = -3.6 + 3.4 * j
            st, h0 = VGroup(), -2.4
            for p in ("Mexico", "China", "Vietnam"):
                v = T[p][y]
                st.add(Rectangle(width=1.6, height=max(v * sc, 0.01), stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9).move_to([x, h0, 0], aligned_edge=DOWN))
                h0 += v * sc
            other = T["World"][y] - sum(T[p][y] for p in ("Mexico", "China", "Vietnam"))
            st.add(Rectangle(width=1.6, height=max(other * sc, 0.01), stroke_width=0, fill_color=COUNTRY_COL["other"], fill_opacity=0.9).move_to([x, h0, 0], aligned_edge=DOWN))
            cols.add(VGroup(st, tx(str(y), 16, GREY_A).next_to(st, DOWN, buff=0.1), tx(f"${T['World'][y]:.1f}bn", 16, WHITE, bold=True).next_to(st, UP, buff=0.1)))
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9), tx(p, 14, GREY_A)).arrange(RIGHT, buff=0.08)
                       for p in ("Mexico", "China", "Vietnam", "other")]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, 0.4, 0])
        head = tx("US imports of colour televisions, by country", 20, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("UN Comtrade: US imports of colour television receivers (HS 852872), by partner, 2017 and 2025", size=13)
        with self.voiceover(
            "Televisions show where a big, cheap, bulky box ends up. <bookmark mark='a'/> In 2017 America imported about "
            f"${T['World'][2017]:.0f} billion of them, ${T['Mexico'][2017]:.1f} billion from Mexico and "
            f"${T['China'][2017]:.1f} billion from China. <bookmark mark='b'/> In 2025, ${T['Mexico'][2025]:.1f} billion of "
            f"${T['World'][2025]:.0f} came from Mexico, and almost none from China. Most of America's televisions now cross "
            "a land border, close to the people who buy them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(key), *[FadeIn(c[1]) for c in cols], FadeIn(ghost(*[c[0] for c in cols], opacity=0.2)))
            for mk, c in zip("ab", cols):
                vo.wait_until(mk)
                self.play(*[GrowFromEdge(r_, DOWN) for r_ in c[0]], FadeIn(c[2]), run_time=1.5)
        self.clear_scene()

    def laptop_units(self):
        U = R["tariffs"]["units"]["laptops"]
        per = 5
        rows = VGroup()
        for i, p in enumerate(("China", "Vietnam", "Thailand", "Mexico")):
            for j, y in enumerate((2024, 2025)):
                n = max(int(round(U[p][y] / per)), 0)
                g = VGroup(*[draw.laptop(0.36, screen=COUNTRY_COL[p]) for _ in range(max(n, 1))]).arrange(RIGHT, buff=0.04)
                if n == 0:
                    g.set_opacity(0)
                lab = tx(f"{p}, {y}: {U[p][y]:.0f} million", 14, COUNTRY_COL[p] if y == 2025 else GREY_A, bold=y == 2025)
                y_ = 2.5 - 0.68 * (2 * i + j)
                lab.move_to([-6.6, y_, 0], aligned_edge=LEFT)
                g.next_to([-3.2, y_, 0], RIGHT, buff=0)
                if j == 0 and n:
                    g.set_opacity(0.45)
                rows.add(VGroup(lab, g))
        key = tx(f"each laptop: {per} million imported into the United States", 13, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("UN Comtrade: US imports of laptops (HS 847130), units, by partner, 2024 and 2025", size=13)
        with self.voiceover(
            "In units the laptop's move is starker still. <bookmark mark='a'/> From China, about "
            f"{U['China'][2024]:.0f} million laptops in 2024 and {U['China'][2025]:.0f} million in 2025. "
            f"<bookmark mark='b'/> From Vietnam, {U['Vietnam'][2024]:.0f} million, then {U['Vietnam'][2025]:.0f} million. "
            f"<bookmark mark='c'/> Thailand and Mexico, from almost none to {U['Thailand'][2025]:.0f} and "
            f"{U['Mexico'][2025]:.0f} million. America bought about as many laptops as ever; they simply came from somewhere "
            "else."
        ) as vo:
            self.play(FadeIn(src), FadeIn(key), *[FadeIn(r_[0]) for r_ in rows], FadeIn(ghost(*[r_[1] for r_ in rows], opacity=0.15)))
            for mk, ks in zip("abc", ((0, 1), (2, 3), (4, 5, 6, 7))):
                vo.wait_until(mk)
                self.play(*[LaggedStart(*[FadeIn(i_, shift=RIGHT * 0.1) for i_ in rows[k][1]], lag_ratio=0.03) for k in ks], run_time=1.5)
        self.clear_scene()
