from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403

HT = (("United Kingdom", UK, 4.0), ("Netherlands", NL, 2.5), ("United States", "#9FB8F2", 2.5), ("Sweden", "#7BD88F",
                                                                                                  2.5))


class Good(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Was it good?", r"Incomes rose. \ Did lives get better, \ and for whom?",
             "Chapter ten. Was it good?", lit={1845: r"Engels", 2000: r"Voth's hours"},
             scale=("person", "nation"), horizon=("a lifetime",))
        self.heights()
        self.debate()

    def heights(self):
        h = load("heights")
        ax = plane([1700, 1985], [160, 185], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.8, y_length=5.0,
                   xticks=[1700, 1750, 1800, 1850, 1900, 1950], yticks=[160, 165, 170, 175, 180, 185],
                   xlabel=r"decade of birth", ylabel=r"men's average height, \ cm", xfmt=lambda v: f"{v:.0f}",
                   font_size=17)
        lines, tags = [], []
        for e, c, w in HT:
            d = h["series"][e]
            pts = [(y, v) for y, v in zip(d["year"], d["value"]) if 1700 <= y <= 1985]
            lines.append(path(ax, [p[0] for p in pts], [p[1] for p in pts], color=c, width=w, smooth=False))
            tags.append(label(e if e != "United Kingdom" else r"Britain", font_size=17, color=c).next_to(
                ax.ax.c2p(pts[-1][0], pts[-1][1]), RIGHT, buff=0.08))
        uk = h["uk"]
        rows = VGroup(
            label(rf"British men born in the 1760s: \ {uk['1760']:.1f} cm", font_size=20, color=UK),
            label(rf"born in the 1850s: \ {uk['1850']:.1f} cm", font_size=20, color=DEATH),
            label(rf"born in the 1960s: \ {uk['1960']:.1f} cm", font_size=20, color=GDP),
            label(r"height records childhood nutrition and disease: \\ a measure income misses", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 1.0)
        src = data_tag(data.cite("longrun"), corner=DR, font_size=12)
        with self.voiceover(
            "Incomes rose; did lives get better? One answer is written in bones. <bookmark mark='a'/> A grown "
            "man's height records how well he was fed, and how much disease he fought, as a child. British men born "
            f"in the 1760s averaged about {uk['1760']:.0f} centimetres. <bookmark mark='b'/> Men born in the 1850s, in "
            f"the crowded industrial towns, averaged about {uk['1850']:.1f}: shorter, while income per head rose. "
            "Dutch and American men shrank too. <bookmark mark='c'/> Only for those born after the 1850s did "
            f"heights climb, to about {uk['1960']:.0f} centimetres by the 1960s. <bookmark mark='d'/> Height catches "
            "what income misses: the cost of the early industrial city."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(tags[0]), FadeIn(rows[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[Create(l_) for l_ in lines[1:]], *[FadeIn(t) for t in tags[1:]], run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def debate(self):
        cards = point_cards([
            (r"the optimists", r"more goods, \ cheaper cloth; \\ wages rise after 1840", GDP),
            (r"the pessimists", r"crowded towns, \ child labour, \\ shorter, \ sicker lives", DEATH),
            (r"longer hours", r"fewer holidays, \ longer years \\ (Voth; \ de Vries)", WAGE),
            (r"in the long run", r"life expectancy from 30 \\ to over 70, \ worldwide", LIFE),
        ], width=12.6, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"the standard-of-living debate", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"for the first generations, \ a hard bargain; \ for their great-grandchildren, \ the escape",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Voth, \emph{Time and Work in England 1750--1830} (2000); \ de Vries, JEH 54(2) (1994)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Historians have argued about this for a century and a half. <bookmark mark='a'/> The optimists point "
            "to more goods, far cheaper cloth, and wages that rose after 1840. The pessimists point to crowded towns, "
            "child labour, and shorter, sicker lives. <bookmark mark='b'/> Hans-Joachim Voth found that the English "
            "also worked longer years, with fewer holidays, and Jan de Vries argued that households worked harder to "
            "buy the new goods: an industrious revolution before the industrial one. <bookmark mark='c'/> In the "
            "long run there is no contest: life expectancy has risen from about thirty to over seventy, across the "
            "world. <bookmark mark='d'/> For the first generations the escape was a hard bargain. For their "
            "great-grandchildren, it was the escape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards.cards[2], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards.cards[3], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
