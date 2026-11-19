from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

FERT = (("Sweden", "#F2C14E"), ("World", WHITE), ("South Korea", "#F7D154"), ("India", IN), ("Nigeria", "#7FD1B9"))


class Transition(VoiceoverScene):
    def construct(self):
        card(self, 8, r"The demographic transition", r"Richer people should have had more children. \ Why did they "
             r"have fewer?", "Chapter eight. The demographic transition.",
             lit={1891: r"Sweden's fertility", 1973: r"Becker and Lewis"}, scale=("household", "nation", "world"),
             horizon=("a lifetime", "a century"))
        self.deaths()
        self.births()
        self.why()

    def deaths(self):
        tr = load("transition")
        ax = plane([1540, 2030], [20, 90], center=LEFT * 1.6 + DOWN * 0.4, x_length=9.2, y_length=5.0,
                   xticks=[1600, 1700, 1800, 1900, 2000], yticks=[20, 40, 60, 80], ylabel=r"life expectancy at birth, "
                   r"\ years", xfmt=lambda v: f"{v:.0f}", font_size=17)
        lines = {}
        for e, c in (("United Kingdom", UK), ("Sweden", "#F2C14E"), ("World", WHITE)):
            d = tr["life"][e]
            lines[e] = path(ax, d["year"], d["value"], color=c, width=3 if e != "World" else 4, smooth=False)
        k = tr["key"]
        rows = VGroup(
            label(rf"England, \ 1543: \ {k['uk_le_1543']:.0f} years; \ 1850: \ {k['uk_le_1850']:.0f}", font_size=20,
                  color=UK),
            label(rf"Sweden, \ 1800: \ {k['se_le_1800']:.0f}; \ 1900: \ {k['se_le_1900']:.0f}", font_size=20,
                  color="#F2C14E"),
            label(rf"the world, \ 1800: \ {k['world_le_1800']:.0f}; \ 2023: \ {k['world_le_2023']:.0f}", font_size=20,
                  color=WHITE),
            label(r"most of the old deaths were children's", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        src = data_tag(data.cite("longrun"), corner=DR, font_size=12)
        with self.voiceover(
            "The escape had a second half, and it began with death. <bookmark mark='a'/> In England in 1543, life "
            f"expectancy at birth was about {k['uk_le_1543']:.0f} years; in 1850, still only about "
            f"{k['uk_le_1850']:.0f}. <bookmark mark='b'/> In Sweden, whose national records go back furthest, it rose from "
            f"about {k['se_le_1800']:.0f} in 1800 to about {k['se_le_1900']:.0f} by 1900. <bookmark mark='c'/> For the "
            f"world as a whole it was about {k['world_le_1800']:.0f} in 1800, and {k['world_le_2023']:.0f} in 2023. "
            "<bookmark mark='d'/> Those low averages were not because adults died at thirty: most of the deaths "
            "were of children. Cleaner water, better food and, later, vaccines brought them down first."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines["United Kingdom"]), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(lines["Sweden"]), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines["World"]), FadeIn(rows[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def births(self):
        tr = load("transition")
        ax = plane([1885, 2030], [0, 7], center=LEFT * 1.6 + DOWN * 0.4, x_length=9.2, y_length=5.0,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2025], yticks=[0, 1, 2, 3, 4, 5, 6, 7],
                   ylabel=r"children per woman", xfmt=lambda v: f"{v:.0f}", font_size=17)
        lines, tags = [], []
        for e, c in FERT:
            d = tr["fert"][e]
            lines.append(path(ax, d["year"], d["value"], color=c, width=3.5 if e in ("Sweden", "World") else 2.5,
                              smooth=False))
            tags.append(label(e if e != "World" else r"the world", font_size=17, color=c).next_to(
                ax.ax.c2p(d["year"][-1], d["value"][-1]), RIGHT, buff=0.08))
        repl = VGroup(DashedLine(ax.ax.c2p(1885, 2.1), ax.ax.c2p(2030, 2.1), color=GREY_C, stroke_width=1.5),
                      label(r"replacement, \ about 2.1", font_size=16, color=GREY_B).next_to(ax.ax.c2p(1890, 2.1), UP,
                                                                                             buff=0.05,
                                                                                             aligned_edge=LEFT))
        k = tr["key"]
        rows = VGroup(
            label(rf"Sweden: \ {k['se_tfr_1891']:.1f} in 1891, \ {k['se_tfr_1935']:.1f} in 1935", font_size=20,
                  color="#F2C14E"),
            label(rf"the world: \ {k['world_tfr_1950']:.1f} in 1950, \ {k['world_tfr_2023']:.1f} in 2023",
                  font_size=20),
            label(rf"South Korea: \ {k['kor_tfr_1950']:.1f} to {k['kor_tfr_2023']:.2f}", font_size=20,
                  color="#F7D154"),
            label(rf"Nigeria, \ 2023: \ {k['nga_tfr_2023']:.1f}", font_size=20, color="#7FD1B9"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 1.2)
        src = data_tag(data.cite("longrun"), corner=DR, font_size=12)
        with self.voiceover(
            "Then births. <bookmark mark='a'/> Swedish women had about four children each in 1891; by 1935, fewer "
            "than two. <bookmark mark='b'/> For the whole world, the figure fell from almost five in 1950 to about "
            f"{k['world_tfr_2023']:.1f} today, close to the replacement level of about two. <bookmark mark='c'/> "
            f"South Korea went from six to {say_num(k['kor_tfr_2023'], 2)}, the lowest in the world. "
            "<bookmark mark='d'/> And Nigeria, still at about four and a half, is where the transition is now under "
            "way. First deaths fell, so for a while populations grew fast; then births followed. That is the "
            "demographic transition."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(repl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(tags[0]), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(tags[1]), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines[2]), Create(lines[3]), FadeIn(tags[2]), FadeIn(tags[3]), FadeIn(rows[2]),
                      run_time=2)
            vo.wait_until("d")
            self.play(Create(lines[4]), FadeIn(tags[4]), FadeIn(rows[3]), run_time=2)
        self.clear_scene()

    def why(self):
        u = load("unified")
        qq = u["qq"]
        ax = plane([0, 0.85], [0, 1.5], center=LEFT * 2.6 + DOWN * 0.45, x_length=6.4, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0, 0.5, 1.0, 1.5],
                   xlabel=r"pace of technological change \ $g$", font_size=17)
        gs = [q["g"] for q in qq]
        cn = path(ax, gs, [q["n"] for q in qq], color=POP, width=4)
        ce = path(ax, gs, [5 * q["e"] for q in qq], color=EDU, width=4)
        ln = label(r"children per adult", font_size=18, color=POP).move_to(ax.ax.c2p(0.45, 1.12), aligned_edge=LEFT)
        le = label(r"schooling per child \ ($\times 5$)", font_size=18, color=EDU).move_to(ax.ax.c2p(0.42, 0.3),
                                                                                        aligned_edge=LEFT)
        rows = VGroup(
            label(r"Gary Becker and H.\ Gregg Lewis, \ 1973: \ quantity against quality", font_size=21),
            label(r"each child costs time; \ an educated child costs more", font_size=21, color=GREY_A),
            label(r"when change makes schooling pay, \ parents buy more of it, \\ and so fewer children",
                  font_size=21, color=EDU),
            label(r"also: \ fewer child deaths, \ women's wages, \ pensions, \ contraception", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(UP * 0.4)
        for r in rows:
            if r.width > 5.8:
                r.width = 5.8
        tag = published_tag(r"Becker and Lewis, JPE 81(2) (1973); \ Galor and Weil, AER 90(4) (2000)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Why would richer people choose fewer children? <bookmark mark='a'/> Gary Becker and H. Gregg Lewis "
            "proposed in 1973 that parents choose between the quantity of children and their quality. "
            "<bookmark mark='b'/> Every child costs time and money, and an educated child costs more. "
            "<bookmark mark='c'/> Agora runs the version Oded Galor and David Weil built: when technology changes "
            "faster, schooling pays more, because it helps a child cope with change. Above a threshold, parents "
            "start to educate, and since each child now costs more, they have fewer. <bookmark mark='d'/> Falling "
            "child deaths, women's rising wages, pensions and contraception all pushed the same way."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cn), Create(ce), FadeIn(ln), FadeIn(le), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
