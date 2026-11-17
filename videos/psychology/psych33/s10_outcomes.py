from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Outcomes(VoiceoverScene):
    def construct(self):
        self.card()
        self.power()
        self.replication()
        self.small()

    def card(self):
        card = chapter_card(9, r"What traits predict", r"Do personality scores matter for a life?",
                            lit={2007: r"Roberts et al.", 2019: r"Soto"}, part=PART, scale=("person", "society"),
                            marr=("what",))
        with self.voiceover("Chapter nine. What traits predict."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def power(self):
        head = heading(r"The power of personality")
        grid = VGroup()
        cols = [(r"personality traits", PERSON), (r"socioeconomic status", SITUATION), (r"cognitive ability", O_)]
        outs = [r"how long people live", r"whether marriages last", r"how far people go in education and work"]
        hdr = VGroup(*[label(c, font_size=20, color=col) for c, col in cols]).arrange(RIGHT, buff=0.9)
        hdr.move_to([2.6, 1.6, 0])
        for i, o in enumerate(outs):
            y = 0.8 - 0.75 * i
            grid.add(label(o, font_size=20, color=WHITE).move_to([-5.6, y, 0], aligned_edge=LEFT))
            for j in range(3):
                grid.add(Dot([hdr[j].get_center()[0], y, 0], radius=0.12, color=cols[j][1]))
        rows = rows_of([
            (r"Brent Roberts, \ Nathan Kuncel, \ Rebecca Shiner, \ Avshalom Caspi and Lewis Goldberg, \ 2007: \ "
             r"prospective studies of three outcomes", WHITE),
            (r"traits measured years earlier predicted all three, \ about as well as socioeconomic status and "
             r"cognitive ability, \ and on top of them", PERSON),
            (r"the point of the comparison: \ personality's effects are modest, \ and so are those of the "
             r"predictors nobody calls small", C_),
        ], 12.4, 22, 0.36).move_to([0, -2.1, 0])
        tag = published_tag(r"Roberts et al.\ (2007)")
        with self.voiceover(
            "Whatever traits are, do they matter? <bookmark mark='a'/> In 2007 Brent Roberts, Nathan Kuncel, Rebecca "
            "Shiner, Avshalom Caspi and Lewis Goldberg reviewed prospective studies of three outcomes: how long "
            "people live, whether their marriages last, and how far they go in education and work. "
            "<bookmark mark='b'/> Traits measured years earlier predicted all three, about as well as socioeconomic "
            "status and cognitive ability did, and on top of them. <bookmark mark='c'/> That was the point of the "
            "comparison. Personality's effects are modest, and so are the effects of the predictors nobody calls "
            "small."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hdr), FadeIn(grid[0::4]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_, scale=0.5) for k, g_ in enumerate(grid) if k % 4], lag_ratio=0.1),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def replication(self):
        head = heading(r"Seventy-eight links, \ tested again")
        A = axes([0, 100], [0, 1], x_length=5.4, y_length=1.0, xticks=[0, 25, 50, 75, 100], yticks=None,
                 xfmt=lambda v: f"{v:.0f}\\%", center=[-3.2, 1.1, 0], font_size=14)
        rep = Rectangle(width=A.ax.c2p(87, 0)[0] - A.ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=GOOD,
                        fill_opacity=0.85).move_to(A.ax.c2p(0, 0.5), aligned_edge=LEFT)
        rep_l = label(r"87\% replicated", font_size=20, color=GOOD).next_to(rep, UP, buff=0.12)
        B = axes([0, 100], [0, 1], x_length=5.4, y_length=1.0, xticks=[0, 25, 50, 75, 100], yticks=None,
                 xfmt=lambda v: f"{v:.0f}\\%", center=[-3.2, -1.4, 0], font_size=14)
        size = Rectangle(width=B.ax.c2p(77, 0)[0] - B.ax.c2p(0, 0)[0], height=0.5, stroke_width=0, fill_color=YOU,
                         fill_opacity=0.85).move_to(B.ax.c2p(0, 0.5), aligned_edge=LEFT)
        size_l = label(r"effects 77\% as large as the originals", font_size=20, color=YOU).next_to(size, UP, buff=0.12)
        rows = rows_of([
            (r"Christopher Soto, \ 2019: \ the Life Outcomes of Personality Replication project", WHITE),
            (r"78 published links between the five traits and outcomes, \ from health to relationships to work, \ "
             r"each tested again with a preregistered plan and a median of 1{,}504 people", GREY_A),
            (r"87\% of the replications came out significant in the predicted direction", GOOD),
            (r"the effects were typically 77\% as large as first reported: \ real, \ and smaller", YOU),
        ], 5.6, 21, 0.38).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Soto (2019)")
        with self.voiceover(
            "And do those links replicate? <bookmark mark='a'/> In 2019 Christopher Soto ran the Life Outcomes of "
            "Personality Replication project. <bookmark mark='b'/> He took seventy-eight published links between the "
            "five traits and outcomes, from health to relationships to work, and tested each again with a "
            "preregistered plan and a median of one thousand five hundred and four people. <bookmark mark='c'/> "
            "Eighty-seven percent of the replications came out significant in the predicted direction. "
            "<bookmark mark='d'/> And the effects were typically seventy-seven percent as large as first reported: "
            "real, and smaller. By the standards of Part 4, that's a good record."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(A), GrowFromEdge(rep, LEFT), FadeIn(rep_l), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(B), GrowFromEdge(size, LEFT), FadeIn(size_l), FadeIn(rows[3]))
        self.clear_scene()

    def small(self):
        d = load("outcomes")
        head = heading(r"What a small correlation means")
        A = axes([-0.6, 2.6], [0, 1.0], x_length=5.6, y_length=3.8, xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share with the good outcome", center=[-3.0, -0.4, 0], font_size=15)
        hi = bars(A.ax, np.arange(3) - 0.18, d["hi"], GOOD, width=0.32)
        lo = bars(A.ax, np.arange(3) + 0.18, d["lo"], LOST, width=0.32)
        names = VGroup(*[label(rf"$r = {r:.1f}$", font_size=18, color=GREY_A).next_to(A.ax.c2p(i, 0), DOWN, buff=0.2)
                         for i, r in enumerate(d["r"])])
        key = legend([(GOOD, r"above the median on the trait"), (LOST, r"below")], font_size=16)
        key.move_to(A.ax.c2p(1.0, 0.92))
        rows = rows_of([
            (r"Robert Rosenthal and Donald Rubin's display: \ split people at the median of the trait and of the "
             r"outcome", WHITE),
            (r"a correlation $r$ becomes success rates of $50 + 50r$ and $50 - 50r$ percent", MODEL),
            (rf"so $r = 0.2$, \ which explains 4\% of the variance, \ means {pct(d['hi'][1])} against "
             rf"{pct(d['lo'][1])}", GOOD),
            (r"across a life, \ or a population, \ small correlations add up", YOU),
        ], 5.6, 21, 0.38).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.besd}")
        with self.voiceover(
            "Correlations like these are modest. Are they small? <bookmark mark='a'/> "
            "Robert Rosenthal and Donald Rubin proposed a way to see them: split people at the middle of the trait "
            "and at the middle of the outcome. <bookmark mark='b'/> A correlation r becomes success rates of fifty "
            "plus fifty r, and fifty minus fifty r, percent. <bookmark mark='c'/> So a correlation of point two, "
            f"which explains just four percent of the variance, means {spct(d['hi'][1])} against "
            f"{spct(d['lo'][1])}. <bookmark mark='d'/> Across a life, or a population, small correlations add up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hi), FadeIn(lo), FadeIn(key), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
