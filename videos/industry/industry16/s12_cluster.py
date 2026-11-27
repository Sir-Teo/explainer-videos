from __future__ import annotations

from videos.industry.industry16.common import *  # noqa: F403

# circles sit near each country, nudged apart so they do not cover one another
PLACES = {"cn": ("China", (103.0, 37.0)), "vn": ("Vietnam", (108.0, 8.0)), "in": ("India", (76.0, 20.0)),
          "us": ("USA", (-98.0, 41.0)), "mx": ("Mexico", (-104.0, 21.0)), "tw": ("Taiwan", (128.0, 22.0))}


class Cluster(VoiceoverScene):
    def construct(self):
        card(self, 10, "The cluster, and the move", "Why is assembly so slow to leave the places where it started?",
             "Chapter ten. The cluster, and the move.", lit=("make", "change"))
        self.assets()
        self.mexico()
        self.jobs()

    def assets(self):
        N = R["cluster"]["nca"]
        wm = draw.world_map(12.4, lon=(-130, 150), lat=(-5, 58)).move_to([0, 0.5, 0])

        def circ(k, year):
            v = N[k][year]
            r_ = 0.038 * np.sqrt(v)
            name = PLACES[k][0]
            col = COUNTRY_COL.get(name, "#9AA3B2") if name not in ("USA",) else "#C9D3E0"
            return Circle(radius=r_, stroke_color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.45).move_to(wm.p(*PLACES[k][1])).set_z_index(3)
        c24 = {k: circ(k, 0) for k in PLACES}
        c25 = {k: circ(k, 1) for k in PLACES}
        labs = {}
        for k in PLACES:
            a, b = N[k]
            name = PLACES[k][0]
            lab = VGroup(tx(name, 14, WHITE, bold=True), tx(f"NT${b:.0f}bn ({'+' if b >= a else ''}{100 * (b / a - 1):.0f}%)", 13, GOOD if b >= a else BAD, bold=True)).arrange(
                DOWN, buff=0.02).set_z_index(4)
            side = {"cn": UP, "vn": DOWN, "in": LEFT, "us": UP, "mx": DOWN, "tw": RIGHT}[k]
            lab.next_to(c25[k], side, buff=0.08)
            labs[k] = lab
        labs["cn"].shift(LEFT * 0.4)
        head = tx("Hon Hai's plants and equipment by country (non-current assets), end of 2024 and 2025", 18, WHITE, bold=True).to_edge(UP, buff=0.3)
        key = tx("circle area: non-current assets", 13, GREY_B).to_edge(DOWN, buff=0.75)
        src = source("Hon Hai, audited consolidated statements 2025, note 14 (5): non-current assets by country", size=13)
        a_cn, b_cn = N["cn"]
        with self.voiceover(
            "Where are the assembly plants? Hon Hai's accounts list its plants, equipment and other long-lived assets by "
            f"country. <bookmark mark='a'/> At the end of 2024, by far the most were in China: about NT${a_cn:.0f} billion. "
            "<bookmark mark='b'/> A year later China's had shrunk a little, while Vietnam's rose by half, America's by "
            f"{100 * (N['us'][1] / N['us'][0] - 1):.0f} per cent, Mexico's by {100 * (N['mx'][1] / N['mx'][0] - 1):.0f}, and "
            f"India's by {100 * (N['in'][1] / N['in'][0] - 1):.0f}. <bookmark mark='c'/> Even so, China still held more "
            "than Vietnam, America and India put together. Assembly does move, but one plant and one product at a time."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(head), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(c24[k]) for k in PLACES], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Transform(c24[k], c25[k]) for k in PLACES], run_time=2.0)
            self.play(LaggedStart(*[FadeIn(labs[k]) for k in PLACES], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(c24["cn"], color=COUNTRY_COL["China"], scale_factor=1.05))
        self.clear_scene()

    def jobs(self):
        J = R["cluster"]["jobs"]
        ys = sorted(y for y in J if y <= 2025)
        pa = viz.plot_axes([1989.5, 2025.5], [0, 2000], x_length=9.4, y_length=4.4, xticks=[1990, 2000, 2010, 2020, 2025],
                           yticks=[500, 1000, 1500, 2000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v / 1000:.1f}m",
                           ylabel="US jobs making computers and electronic products", size=13).move_to([-0.8, -0.4, 0])
        line = poly(pa, [(y, J[y]) for y in ys], PARTS, 4)
        y0, y1 = ys[0], ys[-1]
        a = Dot(pa.ax.c2p(y0, J[y0]), radius=0.08, color=WHITE)
        b = Dot(pa.ax.c2p(y1, J[y1]), radius=0.08, color=WHITE)
        la = tx(f"{y0}: {J[y0] / 1000:.2f} million", 16, WHITE, bold=True).next_to(a, UP + RIGHT, buff=0.1)
        lb = tx(f"{y1}: {J[y1] / 1000:.2f} million", 16, WHITE, bold=True).next_to(b, UP, buff=0.15).shift(LEFT * 0.6)
        src = source("BLS, Current Employment Statistics: all employees, computer and electronic products manufacturing (CEU3133400001), via FRED, annual averages", size=12)
        with self.voiceover(
            "And America's own electronics factories? <bookmark mark='a'/> In 1990 about "
            f"{J[y0] / 1e3:.1f} million Americans worked making computers and electronic products. "
            f"<bookmark mark='b'/> In 2025, about {J[y1] / 1e3:.1f} million: roughly half, while the country bought more "
            "electronics than ever. The assembly happens elsewhere, as the trade figures in the next chapter show."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(line, opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromCenter(a), FadeIn(la))
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(GrowFromCenter(b), FadeIn(lb))
        self.clear_scene()

    def mexico(self):
        M = R["cluster"]["mexico"]
        N = R["cluster"]["nca"]["mx"]
        items = [("servers", "servers and processing units"), ("tvs", "televisions"), ("laptops", "laptops")]
        sc = 0.045
        rows = VGroup()
        for i, (k, name) in enumerate(items):
            a, b = M[k]
            y = 1.6 - 1.5 * i
            lab = tx(name, 16, WHITE, bold=True).move_to([-6.4, y + 0.42, 0], aligned_edge=LEFT)
            ba = Rectangle(width=max(a * sc, 0.02), height=0.32, stroke_width=0, fill_color=COUNTRY_COL["Mexico"], fill_opacity=0.4).move_to([-6.4, y + 0.05, 0], aligned_edge=LEFT)
            bb = Rectangle(width=max(b * sc, 0.02), height=0.32, stroke_width=0, fill_color=COUNTRY_COL["Mexico"], fill_opacity=0.95).move_to([-6.4, y - 0.32, 0], aligned_edge=LEFT)
            va = tx(f"2017: ${a:.1f}bn", 12, GREY_A).next_to(ba, RIGHT, buff=0.1)
            vb = tx(f"2025: ${b:.1f}bn", 14, COUNTRY_COL["Mexico"], bold=True).next_to(bb, RIGHT, buff=0.1)
            rows.add(VGroup(lab, ba, va, bb, vb))
        side = VGroup(tx("Hon Hai's assets in Mexico", 15, GREY_A), tx(f"NT${N[0]:.0f}bn -> NT${N[1]:.0f}bn", 18, COUNTRY_COL["Mexico"], bold=True),
                      tx("end of 2024 -> end of 2025", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([4.4, 1.8, 0])
        head = tx("US imports from Mexico", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("UN Comtrade: US imports from Mexico (HS 847150, 852872, 847130), 2017 and 2025; Hon Hai, audited statements 2025", size=13)
        with self.voiceover(
            "One country stands out for the American market: Mexico, across a land border. <bookmark mark='a'/> America's "
            f"imports of servers and processing units from Mexico went from ${M['servers'][0]:.0f} billion in 2017 to "
            f"${M['servers'][1]:.0f} billion in 2025. <bookmark mark='b'/> Its televisions held at about "
            f"${M['tvs'][1]:.0f} billion, most of America's. <bookmark mark='c'/> Its laptops, from almost nothing to "
            f"${M['laptops'][1]:.1f} billion. And Hon Hai's own assets in Mexico grew by a third in a single year."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(r_[0]) for r_ in rows], FadeIn(ghost(*[r_[3] for r_ in rows], opacity=0.2)))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(GrowFromEdge(r_[1], LEFT), FadeIn(r_[2]), GrowFromEdge(r_[3], LEFT), FadeIn(r_[4]), run_time=1.2)
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()
