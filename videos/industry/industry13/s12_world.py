from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403

NAMES = {"China": ("China", "#E8554E"), "United States": ("United States", "#7EC8F5"), "European Union (27)": ("European Union", "#B58CFF"),
         "India": ("India", "#F6C453"), "Japan": ("Japan", "#E8EAED"), "Brazil": ("Brazil", "#7BD88F"), "Russia": ("Russia", "#8C929B"),
         "World": ("World", "#C9D3E0")}


class World(VoiceoverScene):
    def construct(self):
        card(self, 10, "Around the world", "Who makes the world's electricity, and from what?",
             "Chapter ten. Around the world.", lit=("map", "change"))
        self.growth()
        self.per_person()
        self.mix()

    def growth(self):
        W = R["world"]["gen"]
        keys = ["China", "United States", "European Union (27)", "India"]
        ys = list(range(2000, 2026))
        pa = viz.plot_axes([2000, 2025], [0, 11500], x_length=9.0, y_length=4.6, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[2500, 5000, 7500, 10000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}",
                           ylabel="electricity generated, TWh a year", size=14).move_to([-1.6, -0.4, 0])
        lines, labs = VGroup(), VGroup()
        for k in keys:
            n, col = NAMES[k]
            pts = [(y, W[k][y]) for y in ys if y in W[k]]
            lines.add(poly(pa, pts, col, 4))
            labs.add(tx(f"{n}: {W[k][2025]:,.0f}", 15, col, bold=True).next_to(pa.ax.c2p(2025, W[k][2025]), RIGHT, buff=0.12))
        labs[2].shift(UP * 0.12)
        labs[3].shift(DOWN * 0.22)
        notes = VGroup(tx(f"China, 2000 to 2025: x{W['China'][2025] / W['China'][2000]:.1f}", 17, NAMES["China"][1], bold=True),
                       tx(f"more than America and the EU together", 15, GREY_A),
                       tx(f"the world: {W['World'][2000]:,.0f} to {W['World'][2025]:,.0f} TWh", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([-3.7, 1.1, 0])
        src = source("Ember and the Energy Institute, via Our World in Data (electricity generation)", size=13)
        with self.voiceover(
            "Step back to the whole world. <bookmark mark='a'/> In 2000, America made more electricity than anyone, about "
            f"{W['United States'][2000]:,.0f} terawatt-hours. It still makes about {W['United States'][2025]:,.0f}. "
            "<bookmark mark='b'/> Europe, flat. <bookmark mark='c'/> India has more than tripled. <bookmark mark='d'/> And "
            f"China went from about {W['China'][2000]:,.0f} to about {W['China'][2025]:,.0f}, nearly eight times as much: "
            "more than America and the European Union put together. Most of the world's new electricity this century "
            "has been Chinese."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            for m_, i in zip("abcd", (1, 2, 3, 0)):
                vo.wait_until(m_)
                self.play(Create(lines[i]), FadeIn(labs[i]), run_time=2.0)
            self.play(FadeIn(notes))
        self.clear_scene()

    def per_person(self):
        P = R["world"]["per"]
        keys = sorted(["United States", "Japan", "Russia", "China", "European Union (27)", "World", "Brazil", "India"], key=lambda k: -P[k][2025])
        bars = VGroup()
        for i, k in enumerate(keys):
            n, col = NAMES[k]
            v = P[k][2025]
            y = 2.3 - 0.62 * i
            b = Rectangle(width=v / 13500 * 8.0, height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-2.4, y, 0], aligned_edge=LEFT)
            bars.add(VGroup(tx(n, 17, WHITE).next_to([-2.55, y, 0], LEFT, buff=0.0), b, tx(f"{v:,.0f} kWh", 16, col, bold=True).next_to(b, RIGHT, buff=0.12)))
        head = tx("Electricity generated per person, 2025", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Ember and the Energy Institute, via Our World in Data (per capita electricity generation)", size=13)
        with self.voiceover(
            "Per person, the order changes. <bookmark mark='a'/> An American's share of the country's electricity was "
            f"about {P['United States'][2025]:,.0f} kilowatt-hours in 2025. <bookmark mark='b'/> A Chinese person's, about "
            f"{P['China'][2025]:,.0f}, now more than a European's. <bookmark mark='c'/> An Indian's, about "
            f"{P['India'][2025]:,.0f}: a ninth of an American's. Hundreds of millions of people are still at the bottom of "
            "Insull's curve, with their peak still ahead of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(b_[0]) for b_ in bars])
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2])) for b_ in bars[1:-1]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[-1][1], LEFT), FadeIn(bars[-1][2]))
        self.clear_scene()

    def mix(self):
        Wd = R["world"]
        keys = ["India", "China", "World", "Japan", "United States", "European Union (27)", "Brazil"]
        rows = VGroup()
        for i, k in enumerate(keys):
            n, col = NAMES[k]
            y = 2.2 - 0.7 * i
            c = Wd["coal"][k][2025]
            r = Wd["solar"][k][2025] + Wd["wind"][k][2025]
            cb = Rectangle(width=c / 100 * 4.0, height=0.4, stroke_width=0, fill_color=COAL, fill_opacity=0.9).move_to([-1.0, y, 0], aligned_edge=RIGHT)
            rb = Rectangle(width=r / 100 * 4.0, height=0.4, stroke_width=0, fill_color=SUN, fill_opacity=0.9).move_to([1.0, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(tx(n, 16, col, bold=True).move_to([0, y, 0]), cb, tx(f"{c:.0f}%", 14, COAL).next_to(cb, LEFT, buff=0.08), rb,
                            tx(f"{r:.0f}%", 14, SUN).next_to(rb, RIGHT, buff=0.08)))
        heads = VGroup(tx("coal's share of electricity", 17, COAL, bold=True).move_to([-3.2, 2.95, 0]),
                       tx("wind and solar's share", 17, SUN, bold=True).move_to([3.2, 2.95, 0]))
        src = source("Ember and the Energy Institute, via Our World in Data (shares of electricity from coal, solar and wind), 2025", size=13)
        with self.voiceover(
            "And the fuel. <bookmark mark='a'/> On the left, coal's share of each place's electricity in 2025; on the "
            f"right, wind and solar's. India still makes about {Wd['coal']['India'][2025]:.0f} per cent of its power from "
            f"coal, and China about {Wd['coal']['China'][2025]:.0f}. <bookmark mark='b'/> America, about "
            f"{Wd['coal']['United States'][2025]:.0f}, and the European Union about {Wd['coal']['European Union (27)'][2025]:.0f}. "
            "<bookmark mark='c'/> Wind and sun now make about a sixth of the world's electricity, nearly a third of "
            f"Europe's, and about {Wd['solar']['China'][2025] + Wd['wind']['China'][2025]:.0f} per cent of China's, which, "
            "because China is so large, makes it by far the biggest producer of both."
        ) as vo:
            self.play(FadeIn(heads), FadeIn(src), *[FadeIn(r_[0]) for r_ in rows])
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[1], RIGHT), FadeIn(r_[2])) for r_ in rows[:2]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[1], RIGHT), FadeIn(r_[2])) for r_ in rows[2:]], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r_[3], LEFT), FadeIn(r_[4])) for r_ in rows], lag_ratio=0.15), run_time=2.0)
        self.clear_scene()
