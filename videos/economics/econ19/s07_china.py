from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

SHOW = ("GBR", "NLD", "ITA", "CHN", "JPN", "IND")


class China(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Why not China?", r"China led the world in many technologies for centuries. \ Why did the "
             r"escape not begin there?", "Chapter six. Why not China?",
             lit={1954: r"Needham's question", 2000: r"Pomeranz", 2018: r"Broadberry, Guan and Li"},
             scale=("nation", "world"), horizon=("a century",))
        self.needham()
        self.data()
        self.debate()

    def needham(self):
        rows = VGroup(
            label(r"printing, \ paper money, \ gunpowder, \ the compass, \ cast iron, \ a civil service by exam",
                  font_size=23, color=CN),
            label(r"Joseph Needham, \ from 1954: \ why did modern science and industry arise in Europe, \ not China?",
                  font_size=23),
            label(r"the Needham question, \ and its economic twin: \ why did the great divergence happen?",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.2)
        tag = published_tag(r"Needham, \emph{Science and Civilisation in China} (from 1954)", corner=DR, font_size=13)
        with self.voiceover(
            "For much of history the obvious place for an escape was China. <bookmark mark='a'/> Printing, paper "
            "money, gunpowder, the compass, cast iron and a civil service chosen by examination were all Chinese long "
            "before they were European. <bookmark mark='b'/> The biochemist Joseph Needham spent his life on the "
            "history of Chinese science, and asked why modern science and industry arose in Europe instead. "
            "<bookmark mark='c'/> Economists ask the same question about incomes: why did the great divergence "
            "between Europe and Asia happen?"
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def data(self):
        d = load("divergence")
        ax = plane([1000, 1860], [np.log10(600), np.log10(6000)], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.0,
                   y_length=5.2, xticks=[1000, 1200, 1400, 1600, 1800],
                   yticks=[np.log10(v) for v in (700, 1000, 2000, 4000)],
                   ylabel=r"GDP per head, \ 2011 dollars \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), font_size=16)
        curves, tags = {}, {}
        for c in SHOW:
            s = d["series"][c]
            name, col = COUNTRY[c]
            curves[c] = log_axis(ax, s["year"], s["gdppc"], col, width=3.5 if c in ("GBR", "CHN") else 2.5)
            tags[c] = label(name, font_size=18, color=col).next_to(
                ax.ax.c2p(s["year"][-1], np.log10(s["gdppc"][-1])), RIGHT, buff=0.1)
        a = d["at"]
        rows = VGroup(
            label(rf"1000: \ China {a['CHN']['1000']['gdppc']:,.0f}, \ Britain {a['GBR']['1000']['gdppc']:,.0f}"
                  .replace(",", "{,}"), font_size=19, color=GREY_A),
            label(rf"1700: \ China {a['CHN']['1700']['gdppc']:,.0f}, \ Britain {a['GBR']['1700']['gdppc']:,.0f}"
                  .replace(",", "{,}"), font_size=19, color=GREY_A),
            label(rf"1850: \ China {a['CHN']['1850']['gdppc']:,.0f}, \ Britain {a['GBR']['1850']['gdppc']:,.0f}"
                  .replace(",", "{,}"), font_size=19, color=E.ACCENT),
            label(r"the little divergence: \\ Holland and Britain pass Italy", font_size=19, color=NL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        src = data_tag(r"Maddison Project Database 2023 \ (Bolt and van Zanden)", corner=DR, font_size=12)
        g, c = a["GBR"], a["CHN"]
        with self.voiceover(
            "Here is what the Maddison Project's historians estimate, on a log scale, in dollars of 2011. "
            "<bookmark mark='a'/> Around the year 1000, China and England were about equally poor, near twelve "
            "hundred dollars a head. <bookmark mark='b'/> China's estimates rise and fall between about twelve and "
            "fifteen hundred dollars for seven centuries, then sink after 1700, while north-western Europe pulls ahead: first Holland, whose golden age peaks around 1600, then "
            "Britain. Italy, rich in the Middle Ages, stays where it was: the little divergence, inside Europe. "
            f"<bookmark mark='c'/> By 1700 Britain is at about {g['1700']['gdppc']:,.0f} dollars against China's "
            f"{c['1700']['gdppc']:,.0f}. <bookmark mark='d'/> By 1850, about {g['1850']['gdppc']:,.0f} against "
            f"{c['1850']['gdppc']:,.0f}: five to one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(curves["GBR"]), Create(curves["CHN"]), run_time=3)
            self.play(FadeIn(tags["GBR"]), FadeIn(tags["CHN"]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[Create(curves[k]) for k in ("NLD", "ITA", "JPN", "IND")], run_time=3)
            self.play(*[FadeIn(tags[k]) for k in ("NLD", "ITA", "JPN", "IND")], FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def debate(self):
        rows = VGroup(
            label(r"Kenneth Pomeranz, \ \emph{The Great Divergence}, \ 2000:", font_size=24, color=CN),
            label(r"as late as 1750, \ the Yangzi delta lived about as well as England", font_size=22),
            label(r"England's luck: \ coal near its people, \ and the New World's land \ (cotton, \ sugar, \ timber)",
                  font_size=22, color=WAGE),
            label(r"Broadberry, \ Guan and Li, \ 2018: \ China's national accounts rebuilt back to 980",
                  font_size=23, color=GDP),
            label(r"the Yangzi delta fell decisively behind Europe's richest region around 1700", font_size=22,
                  color=GREY_A),
            label(r"the debate is over the date, \ and with it the cause: \ a late accident, \ or a long lead?",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Pomeranz (2000); \ Broadberry, Guan and Li, JEH 78(4) (2018)", corner=DR, font_size=13)
        with self.voiceover(
            "How late the divergence came is the heart of the debate. <bookmark mark='a'/> In 2000 Kenneth "
            "Pomeranz argued <bookmark mark='b'/> that as late as 1750 the richest part of China, the Yangzi delta, "
            "lived about as well as England. <bookmark mark='c'/> What set England apart was luck: coal close to its "
            "people, and the land of the New World, which grew the cotton, sugar and timber that England could not. "
            "<bookmark mark='d'/> Stephen Broadberry, Hanhui Guan and David Daokui Li rebuilt China's national "
            "accounts from its own records, back to the year 980, <bookmark mark='e'/> and concluded that the Yangzi "
            "delta fell decisively behind the richest region of Europe around 1700: later than older writers "
            "assumed, but earlier than Pomeranz said. Their estimates are still being argued over. "
            "<bookmark mark='f'/> The debate is over the "
            "date, and with it the cause: a late accident of geography, or a long European lead."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcdef", [rows[0], *rows[1:]]):
                if mk == "a":
                    continue
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
