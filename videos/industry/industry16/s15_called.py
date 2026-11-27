from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 13, "Called it?", "Will the screws come to America?", "Chapter thirteen. Called it?", lit=("change",))
        self.theirs()
        self.ours()
        self.arithmetic()

    def theirs(self):
        C = R["called"]
        P = C["phones"]
        quote = VGroup(tx("'...the army of millions and millions of human beings", 17, WHITE),
                       tx("screwing in little- little screws to make iPhones,", 17, WHITE),
                       tx("that kind of thing is going to come to America.", 17, WHITE),
                       tx("It's going to be automated...'", 17, WHITE),
                       tx("Howard Lutnick, US Commerce Secretary, CBS, Face the Nation, 6 April 2025", 13, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).to_corner(UL, buff=0.45)
        sc = 0.055
        def bar(x, y):
            st, h0 = VGroup(), -2.6
            for p in ("China", "India", "Vietnam"):
                v = P[p][y]
                st.add(Rectangle(width=1.0, height=v * sc, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9).move_to([x, h0, 0], aligned_edge=DOWN))
                h0 += v * sc
            other = P["World"][y] - sum(P[p][y] for p in ("China", "India", "Vietnam"))
            st.add(Rectangle(width=1.0, height=max(other, 0) * sc, stroke_width=0, fill_color=COUNTRY_COL["other"], fill_opacity=0.9).move_to([x, h0, 0], aligned_edge=DOWN))
            return VGroup(st, tx(str(y), 15, GREY_A).next_to(st, DOWN, buff=0.1), tx(f"${P['World'][y]:.1f}bn", 15, WHITE, bold=True).next_to(st, UP, buff=0.08))
        b24, b25 = bar(-4.6, 2024), bar(-2.8, 2025)
        key = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=COUNTRY_COL[p], fill_opacity=0.9), tx(p, 13, GREY_A)).arrange(RIGHT, buff=0.08)
                       for p in ("China", "India", "Vietnam", "other")]).arrange(RIGHT, buff=0.3).move_to([-3.7, -3.25, 0])
        facts = VGroup(tx("US imports of smartphones, 2025:", 16, GREY_A),
                       tx(f"${P['World'][2025]:.1f}bn, against ${P['World'][2024]:.1f}bn in 2024", 17, WHITE, bold=True),
                       tx(f"from China ${P['China'][2025]:.1f}bn, from India ${P['India'][2025]:.1f}bn", 17, WHITE, bold=True),
                       tx("US jobs making computers and electronics:", 16, GREY_A),
                       tx(f"{C['jobs24'] / 1000:.2f}m (2024), {C['jobs25'] / 1000:.2f}m (2025)", 17, WHITE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07).move_to([3.4, -1.2, 0])
        verdict = tx("Called it? Not so far: the screws moved to India, not to America.", 19, PRICE, bold=True).to_edge(DOWN, buff=0.45).shift(RIGHT * 2.2)
        src = source("CBS News transcript, 6 April 2025; UN Comtrade (US imports, HS 851713); BLS via FRED (CEU3133400001)", size=12)
        with self.voiceover(
            "Two forecasts. The first was made on television in April 2025, the week of the new tariffs. "
            "<bookmark mark='a'/> America's Commerce Secretary said that 'the army of millions and millions of human beings "
            "screwing in little screws to make iPhones, that kind of thing is going to come to America', automated. "
            f"<bookmark mark='b'/> What happened? In 2025 America imported ${P['World'][2025]:.0f} billion of smartphones, "
            f"about the same as the year before. <bookmark mark='c'/> But from China, ${P['China'][2025]:.0f} billion, down "
            f"from ${P['China'][2024]:.0f}; from India, ${P['India'][2025]:.0f} billion. And American jobs making computers "
            "and electronics did not rise. <bookmark mark='d'/> Called it? Not so far. The screws moved, but to India, not "
            "to America."
        ) as vo:
            self.play(FadeIn(src), FadeIn(quote[-1]), FadeIn(ghost(b24, b25, opacity=0.35)), FadeIn(ghost(quote[:-1], opacity=0.4)), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(quote[:-1], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(r_, DOWN) for r_ in b24[0]], FadeIn(b24[1:]), run_time=1.2)
            self.play(*[GrowFromEdge(r_, DOWN) for r_ in b25[0]], FadeIn(b25[1:]), FadeIn(facts[:2]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(facts[2:], shift=UP * 0.1), Indicate(b25[0][1], color=COUNTRY_COL["India"]))
            vo.wait_until("d")
            self.play(FadeIn(verdict, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        M = C["monthly"]
        months = sorted(m for m in M["World"] if M["World"][m] > 0)
        xs = list(range(len(months)))
        share = [M["India"].get(m, 0) / M["World"][m] for m in months]
        pa = viz.plot_axes([-0.5, 23.5], [0, 0.8], x_length=7.2, y_length=4.0, xticks=[0, 6, 12, 18],
                           yticks=[0, 0.2, 0.4, 0.5, 0.6, 0.8], xfmt=lambda v: {0: "Jan 2025", 6: "Jul 2025", 12: "Jan 2026", 18: "Jul 2026"}[int(v)],
                           yfmt=lambda v: f"{100 * v:.0f}%", ylabel="India's share of US smartphone imports, each month", size=12).move_to([-2.9, 0.4, 0])
        half = DashedLine(pa.ax.c2p(-0.5, 0.5), pa.ax.c2p(23.5, 0.5), stroke_color=PRICE, stroke_width=2, dash_length=0.08)
        hl = tx("half", 13, PRICE, bold=True).next_to(pa.ax.c2p(23.5, 0.5), RIGHT, buff=0.08)
        dots = VGroup(*[Dot(pa.ax.c2p(x, s_), radius=0.06, color=COUNTRY_COL["India"]) for x, s_ in zip(xs, share)])
        line = poly(pa, list(zip(xs, share)), COUNTRY_COL["India"], 3)
        launch = Rectangle(width=pa.ax.c2p(11.5, 0)[0] - pa.ax.c2p(7.5, 0)[0], height=4.0, stroke_width=0, fill_color=COUNTRY_COL["China"], fill_opacity=0.1).move_to(
            [(pa.ax.c2p(7.5, 0)[0] + pa.ax.c2p(11.5, 0)[0]) / 2, pa.get_center()[1], 0])
        ll = VGroup(tx("Sep-Dec 2025:", 12, COUNTRY_COL["China"]), tx("China's months", 12, COUNTRY_COL["China"])).arrange(DOWN, buff=0.02).move_to(
            [launch.get_center()[0], pa.ax.c2p(0, 0.74)[1], 0])
        y, pr = C["ytd"], C["proj"]
        card_ = VGroup(tx("Our call", 28, PRICE, bold=True),
                       tx("In 2026, India will supply more than half", 16, WHITE),
                       tx("of America's smartphone imports, by value.", 16, WHITE, bold=True),
                       tx(f"Probability: {100 * C['prob']:.0f}%", 26, PRICE, bold=True),
                       tx("Checked against UN Comtrade's 2026 figures", 13, GREY_A), tx("for US imports (HS 851713), mid-2027", 13, GREY_A)).arrange(
            DOWN, buff=0.1).move_to([4.4, 1.3, 0])
        why = VGroup(tx(f"January-{_mon(C['months26'][-1])} 2026: India {100 * C['ytd_share']:.0f}%", 14, GOOD),
                     tx(f"if Sep-Dec repeats 2025: {100 * C['proj_share']:.1f}%", 14, PRICE),
                     tx("against: a new phone's launch months, made in China", 14, BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.2, -1.7, 0])
        src = source("UN Comtrade: US imports of smartphones (HS 851713) from the world and from India, monthly, as reported by the United States", size=12)
        with self.voiceover(
            "Now our own call, written down so you can check it. <bookmark mark='a'/> Here is India's share of America's "
            "smartphone imports, month by month since January 2025. It passed half in the spring of 2025. "
            "<bookmark mark='b'/> Then from September to December it fell back, as China supplied the launch months of "
            "the new phones. <bookmark mark='c'/> In 2026 India has been above half every month so far: "
            f"{100 * C['ytd_share']:.0f} per cent from January to {_mon(C['months26'][-1])}. If the last four months of "
            f"2026 look like the last four of 2025, the year ends at {100 * C['proj_share']:.1f} per cent: a coin toss "
            "around one half. <bookmark mark='d'/> India's shipments this year have run well above last year's, and we "
            f"think that tips it. We give it {100 * C['prob']:.0f} per cent, and we will check it against the 2026 trade figures, right or "
            "wrong."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), Create(half), FadeIn(hl), FadeIn(card_[0]), FadeIn(ghost(line, dots, opacity=0.25)))
            vo.wait_until("a")
            self.play(Create(VMobject().set_points_as_corners(line.get_points()[: len(line.get_points()) * 8 // len(xs)]).set_stroke(COUNTRY_COL["India"], 3)),
                      LaggedStart(*[GrowFromCenter(d) for d in dots[:8]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(launch), FadeIn(ll), LaggedStart(*[GrowFromCenter(d) for d in dots[8:12]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(line), LaggedStart(*[GrowFromCenter(d) for d in dots[12:]], lag_ratio=0.15), FadeIn(why[:2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(card_[1:], shift=UP * 0.1), FadeIn(why[2]))
        self.clear_scene()


    def arithmetic(self):
        C = R["called"]
        cv = C["curve"]
        xs = sorted(cv)
        pa = viz.plot_axes([0.1, 0.7], [0.35, 0.65], x_length=8.0, y_length=4.2, xticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                           yticks=[0.4, 0.45, 0.5, 0.55, 0.6], xfmt=lambda v: f"{100 * v:.0f}%", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="India's share of the whole year, 2026", size=13).move_to([-1.2, -0.3, 0])
        xl = tx("India's share of September-December 2026", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        line = poly(pa, [(x, cv[x]) for x in xs], COUNTRY_COL["India"], 4)
        half = DashedLine(pa.ax.c2p(0.1, 0.5), pa.ax.c2p(0.7, 0.5), stroke_color=PRICE, stroke_width=2, dash_length=0.08)
        need = C["need"]
        nm = DashedLine(pa.ax.c2p(need, 0.35), pa.ax.c2p(need, 0.5), stroke_color=WHITE, stroke_width=2, dash_length=0.06)
        nl = tx(f"needed: {100 * need:.1f}%", 15, WHITE, bold=True).next_to(pa.ax.c2p(need, 0.36), RIGHT, buff=0.1)
        la = tx(f"last autumn: {100 * C['last_autumn']:.1f}%", 15, PRICE, bold=True).move_to([4.6, 0.6, 0])
        note = VGroup(tx("assuming September-December 2026", 13, GREY_A), tx("is as large as September-December 2025", 13, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03).move_to([4.6, -0.2, 0])
        src = source("UN Comtrade: US imports of smartphones (HS 851713), monthly, January 2025 to August 2026", size=12)
        with self.voiceover(
            "Here is the arithmetic behind the call. <bookmark mark='a'/> Across: India's share of America's smartphone "
            "imports in the last four months of 2026. Up: its share of the whole year. <bookmark mark='b'/> To end the "
            f"year above half, India needs about {100 * need:.0f} per cent of those last four months. "
            f"<bookmark mark='c'/> In the same months of 2025 it had {100 * C['last_autumn']:.0f} per cent. So the call "
            "comes down to whether India supplies more of this autumn's new phones than it did last year's."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(src), Create(half), FadeIn(note), FadeIn(ghost(line, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(nm), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(la, shift=LEFT * 0.1))
        self.clear_scene()


def _mon(m: str) -> str:
    return ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
            "December"][int(m[5:7]) - 1]
