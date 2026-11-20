from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class China(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The China shock", r"What did a generation of imports do to American towns?",
             "Chapter nine. The China shock.", lit={2001: r"China joins the WTO", 2013: r"Autor, \ Dorn and Hanson"},
             scale=("city", "nation"), horizon=("a decade",))
        self.aggregate()
        self.design()
        self.island()

    def aggregate(self):
        C = load("china")
        ax = plane([1985, 2026], [0, 600], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.4,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 200, 400, 600], ylabel=r"\$ billion a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        imp = path(ax, C["years"], C["imp_bn"], CHINA, 3.2, smooth=False)
        ax2 = plane([1985, 2026], [10, 20], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.4,
                    xticks=[], yticks=[], font_size=14)
        man = path(ax2, C["man_y"], C["man"], WHITE, 2.4, xr=(1985, 2026), smooth=False)
        side = VGroup(
            label(rf"red: \ imports from China, \\ \${C['imp1991']:.0f}bn (1991) $\to$ \${C['imp2007']:.0f}bn (2007)",
                  font_size=17, color=CHINA),
            label(rf"white: \ US manufacturing jobs \\ (scale 10 to 20 million): \\ {C['man2000']:.1f}m (2000) "
                  rf"$\to$ {C['man2010']:.1f}m (2010)", font_size=17, color=WHITE),
            label(r"which caused which? \\ automation, \ the 2008 \\ recession, \ and trade \\ all hit at once",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"US Census Bureau and BLS, \ via FRED: \ IMPCH, \ MANEMP", corner=DR, font_size=12)
        with self.voiceover(
            "Now the evidence that changed the profession's mind. <bookmark mark='a'/> China joined the World Trade "
            f"Organization in December 2001. America's imports from China rose from {C['imp1991']:.0f} billion "
            f"dollars in 1991 to {C['imp2007']:.0f} billion in 2007. <bookmark mark='b'/> Over the same years "
            f"American manufacturing employment fell, from {C['man2000']:.1f} million in 2000 to "
            f"{C['man2010']:.1f} million in 2010. <bookmark mark='c'/> But many things hit manufacturing at once: "
            "automation, the recession of 2008, and trade. A national time series cannot separate them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(imp), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(man), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def design(self):
        C = load("china")
        cards = point_cards([
            (r"the units", r"722 commuting zones: \\ local labour markets", WHITE),
            (r"the exposure", r"each zone's industry mix \\ times the national \\ rise in imports per worker",
             CHINA),
            (r"the instrument", r"the same, \ using China's \\ exports to eight other \\ rich countries", ARCH),
            (r"the answer", rf"\$1,000 per worker \\ $\to$ manufacturing \\ employment {C['adh_beta']:.3f} points",
             GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"Autor, \ Dorn and Hanson (2013)", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(rf"exposure rose \${C['adh_exposure_90s']:,} per worker in the 1990s and "
                     rf"\${C['adh_exposure_00s']:,} in 2000--07: \ about a quarter of the fall in manufacturing",
                     font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.ADH_2013.tag, corner=DR, font_size=12)
        with self.voiceover(
            "David Autor, David Dorn and Gordon Hanson found a way to separate them. <bookmark mark='a'/> They "
            "studied seven hundred and twenty-two local labour markets, commuting zones. <bookmark mark='b'/> Each "
            "zone's exposure to China depended on what it happened to make in 1990: furniture towns, toy towns and "
            "textile towns were hit; others were not. <bookmark mark='c'/> To keep American demand shocks out of "
            "the measure, they built it again from China's exports to eight other rich countries, which reflect "
            "China's own rise. <bookmark mark='d'/> The result: a thousand dollars more of imports per worker over "
            "a decade cut a zone's manufacturing employment, as a share of its adults, by "
            f"{abs(C['adh_beta']):.2f} percentage points, with unemployment, disability claims and lower wages "
            "following. Across the country, conservatively, about a quarter of the decline in manufacturing "
            "employment from 1990 to 2007."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()

    def island(self):
        C = load("china")
        x, y = np.array(C["sim_x"]), np.array(C["sim_y"])
        ax = plane([float(x.min()), float(x.max())], [float(y.min()), float(y.max())], center=LEFT * 1.8 + DOWN * 0.4,
                   x_length=8.4, y_length=4.4, xticks=[], yticks=[], xlabel=r"a zone's import exposure",
                   ylabel=r"change in its manufacturing share", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.03, color=CHINA) for a, b in zip(x, y)])
        side = VGroup(
            label(rf"the Island's 400 zones: \\ the planted effect {C['sim_beta']:.2f}", font_size=18, color=WHITE),
            label(rf"least squares: \ {C['sim_ols']:.2f} \\ (demand shocks raise \\ imports and jobs together)",
                  font_size=18, color=TARIFF),
            label(rf"with the instrument: \ {C['sim_iv']:.2f}", font_size=18, color=GAIN),
            label(r"the modern reading: \\ shift-share designs \\ need many independent \\ industry shocks",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Why the instrument? <bookmark mark='a'/> On the Island's four hundred zones, with an effect planted at "
            f"{C['sim_beta']:.1f}, <bookmark mark='b'/> least squares finds {C['sim_ols']:.2f}: industries where "
            "Islanders' own demand rose import more and employ more, which hides part of the damage. "
            f"<bookmark mark='c'/> Using exposure built from other countries' imports recovers {C['sim_iv']:.2f}. "
            "<bookmark mark='d'/> Recent work, by Borusyak, Hull and Jaravel and by Goldsmith-Pinkham, Sorkin and "
            "Swift, shows what such shift-share designs rest on: many industry shocks that are as good as random. "
            "The China shock's estimates have held up when re-examined this way."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.003), run_time=2.0)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
