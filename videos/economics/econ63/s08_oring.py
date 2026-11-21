from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


def team(qs, color=PEOPLE, w=1.5, h=1.1):
    """Four task boxes with each worker's chance of getting it right."""
    g = VGroup()
    for k, q in enumerate(qs):
        c = SHOCK if q < 0.9 else color
        r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=c, stroke_width=2.2, fill_color=c,
                             fill_opacity=0.14)
        t = VGroup(label(rf"task {k + 1}", font_size=16, color=GREY_A), label(f"{q:.2f}", font_size=26,
                                                                              color=c)).arrange(DOWN, buff=0.1)
        g.add(VGroup(r, t.move_to(r)))
    times = VGroup(*[label(r"$\times$", font_size=28) for _ in range(len(qs) - 1)])
    row = VGroup()
    for k, b in enumerate(g):
        row.add(b)
        if k < len(times):
            row.add(times[k])
    return row.arrange(RIGHT, buff=0.25)


class ORing(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The O-ring", r"Why can one weak link sink a team, \ and what does that do to who works "
             r"with whom?", "Chapter seven. The O-ring.", lit={1986: r"Challenger", 1993: r"Kremer"},
             scale=("person", "firm"), horizon=("a day",))
        self.weak()
        self.sorting()
        self.wages()

    def weak(self):
        hc = history_card(1986, r"28 January, \ the Challenger", r"the space shuttle breaks apart 73 seconds after "
                          r"launch: \ a rubber seal, \ an O-ring, \ fails in the cold", color=SHOCK, width=11.4,
                          font_size=21).to_edge(UP, buff=0.4)
        good = team([0.99, 0.99, 0.99, 0.99])
        bad = team([0.99, 0.99, 0.60, 0.99])
        eq_g = label(rf"$= {0.99 ** 4:.2f}$", font_size=30, color=PEOPLE)
        eq_b = label(rf"$= {0.99 ** 3 * 0.6:.2f}$", font_size=30, color=SHOCK)
        r1 = VGroup(good, eq_g).arrange(RIGHT, buff=0.3)
        r2 = VGroup(bad, eq_b).arrange(RIGHT, buff=0.3)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.45).next_to(hc, DOWN, buff=0.5)
        if rows.width > 12.4:
            rows.width = 12.4
        note_ = label(r"output $= B \cdot q_1 q_2 q_3 q_4$: \ one weak link costs two fifths; \ averaged, \ it would "
                      r"cost a tenth", font_size=21, color=E.ACCENT).next_to(rows, DOWN, buff=0.4)
        tag = published_tag(r"Kremer, \ Quarterly Journal of Economics 108(3) (1993)", corner=DL, font_size=12)
        with self.voiceover(
            "On the twenty-eighth of January 1986 the space shuttle Challenger broke apart seventy-three seconds "
            "after launch, because a rubber seal, an O-ring, failed in the cold. Thousands of parts worked; one did "
            "not. <bookmark mark='a'/> Michael Kremer built a theory of production on it. A product needs several "
            "tasks done right, and its value is the product of the chances that each is done right. Four workers "
            f"who each get their task right ninety-nine times in a hundred make {0.99 ** 4:.2f} of the perfect "
            "output. <bookmark mark='b'/> Swap one of them for a worker who gets it right sixty percent of the "
            f"time, and output falls to {0.99 ** 3 * 0.6:.2f}. <bookmark mark='c'/> One weak link costs two "
            "fifths of everything. If output were the average of the four, it would cost a tenth."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(r1))
            vo.wait_until("b")
            self.play(FadeIn(r2))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def sorting(self):
        O = load("oring")
        hist = np.array(O["q_hist"], float)
        edges = np.linspace(0.4, 1.0, len(hist) + 1)
        mids = (edges[:-1] + edges[1:]) / 2
        ax = plane([0.38, 1.02], [0, 100], center=LEFT * 3.2 + DOWN * 0.4, x_length=5.6, y_length=4.2,
                   xticks=[0.4, 0.6, 0.8, 1.0], yticks=[0, 50, 100], xlabel=r"chance of doing a task right",
                   ylabel=r"workers", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        hb = bars(ax, mids, hist, [PEOPLE] * len(hist), width=0.045)
        side = VGroup(
            label(r"400 workers, \ 100 teams of four", font_size=20, color=WHITE),
            label(rf"teams drawn at random: \ output {O['mixed']:.1f}", font_size=20, color=GREY_B),
            label(rf"the best with the best: \ output {O['sorted']:.1f}, \ +{100 * O['gain']:.0f}\%", font_size=20,
                  color=GAIN),
            label(r"skills are complements: \\ firms, \ cities and countries sort", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"the Island: \ agora.network.oring", corner=DL, font_size=12)
        with self.voiceover(
            "Multiplication has a consequence for who works with whom. <bookmark mark='a'/> Take four hundred of "
            "the Island's workers, with skills spread like this, and form a hundred teams of four. <bookmark "
            f"mark='b'/> Teams drawn at random produce {O['mixed']:.1f} units. <bookmark mark='c'/> Put the best "
            f"with the best and the worst with the worst, and they produce {O['sorted']:.1f}: "
            f"{100 * O['gain']:.0f} percent more from the same people, because a skilled worker's care is wasted "
            "beside a careless one. <bookmark mark='d'/> So skills are complements, and firms, cities and whole "
            "countries sort: the best engineers work together, and a country with a few weak links in its "
            "infrastructure or its courts drags down the value of everyone's skill."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b, DOWN) for b in hb], FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def wages(self):
        O = load("oring")
        g, w = np.array(O["grid"]), np.array(O["wage"])
        w = w / w[-1]
        ax = plane([0.8, 1.0], [0.3, 1.05], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.2, y_length=4.6,
                   xticks=[0.8, 0.85, 0.9, 0.95, 1.0], yticks=[0.4, 0.6, 0.8, 1.0], xlabel=r"skill $q$",
                   ylabel=r"wage, \ best worker = 1", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        cv = path(ax, g, w, GDP, 3.4)
        ln = path(ax, g, g / g[-1], GREY_B, 2.4, smooth=False)
        r90 = (0.9 / 0.999) ** O["team"]
        side = VGroup(
            label(r"grey: \ pay in proportion to skill", font_size=20, color=GREY_B),
            label(rf"gold: \ Kremer's wages, \ $w \propto q^{O['team']}$", font_size=20, color=GDP),
            label(rf"a worker 10\% less careful earns {100 * (1 - r90):.0f}\% less", font_size=20, color=E.ACCENT),
            label(r"small differences in skill, \\ large differences in pay", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.5)
        tag = island_tag(r"computed: \ sorted teams of four", corner=DL, font_size=12)
        with self.voiceover(
            "And pay. <bookmark mark='a'/> If output added up skills, a worker ten percent less careful would earn "
            "ten percent less. <bookmark mark='b'/> In Kremer's sorted economy, wages rise with skill to the power "
            "of the team's size. <bookmark mark='c'/> A worker ten percent less careful earns about "
            f"{100 * (1 - r90):.0f} percent less. <bookmark mark='d'/> Small differences in skill become large "
            "differences in pay, within countries and between them. The network here is the smallest possible: "
            "four people at one bench. But it already shows the theme of this part. When everyone depends on "
            "everyone, the weakest link sets the pace."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
