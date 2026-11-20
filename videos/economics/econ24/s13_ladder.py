from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403

LADDER_SEED = 7   # one simulated career on the Island's ladder


class Ladder(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Job ladders and wage dispersion", r"Why do identical workers earn different wages, \ and "
             r"how do careers climb?", "Chapter eleven. Job ladders and wage dispersion.",
             lit={1992: r"Topel and Ward", 1998: r"Burdett and Mortensen", 2003: r"Manning"},
             scale=("person", "market"), horizon=("years",))
        self.careers()
        self.climb()
        self.dispersion()
        self.monopsony()

    def careers(self):
        rows = VGroup(
            label(r"Topel and Ward, \ 1992: \ about 10{,}000 young American men, \ followed from their first jobs",
                  font_size=23, color=GREY_A),
            label(r"a typical young man held seven jobs in his first ten years: \ about two-thirds of a career's "
                  r"total", font_size=24, color=WORKER),
            label(r"the raises at job changes: \ at least a third of early-career wage growth", font_size=24,
                  color=MATCH),
            label(r"so search does not stop at the first job: \ people keep looking, \ and climb", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.2)
        tag = published_tag(r"Topel and Ward, QJE 107(2) (1992): \ 439--479", corner=DR, font_size=12)
        with self.voiceover(
            "McCall's searcher stops for good at the first acceptable offer. Real careers do not. "
            "<bookmark mark='a'/> Robert Topel and Michael Ward followed about ten thousand young American men "
            "through the social security records of their employers. <bookmark mark='b'/> A typical young man held "
            "seven jobs in his first ten years at work, about two-thirds of all the jobs he would ever hold. "
            "<bookmark mark='c'/> And the raises he got when he changed jobs accounted for at least a third of his "
            "wage growth early in his career. <bookmark mark='d'/> Search does not end with the first job. People "
            "keep looking while they work, and climb."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def climb(self):
        lad = load("ladder")
        rng = np.random.default_rng(LADDER_SEED)
        ws, F = np.array(lad["w"]), np.array(lad["F"])
        lam, dlt = 0.1, 0.02
        months, w, path_ = 120, None, []
        for _ in range(months):
            if w is not None and rng.random() < dlt:
                w = None
            elif rng.random() < lam:
                offer = float(np.interp(rng.random(), F, ws))
                if w is None or offer > w:
                    w = offer
            path_.append(w)
        ax = plane([0, months], [0.35, 1.0], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[0, 24, 48, 72, 96, 120], yticks=[0.4, 0.6, 0.8, 1.0], xlabel=r"months",
                   ylabel=r"wage \ (output per worker $= 1$)", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=16)
        floor = seg(ax, 0, lad["w_lo"], months, lad["w_lo"], color=BENEFIT, width=2, dashed=True)
        floor_l = label(r"the benefit: \ unemployed", font_size=16, color=BENEFIT).next_to(
            ax.ax.c2p(months, lad["w_lo"]), UP, buff=0.08).shift(LEFT * 1.0)
        pts = [ax.ax.c2p(m, w_ if w_ is not None else lad["w_lo"]) for m, w_ in enumerate(path_)]
        career = VMobject(stroke_color=MATCH, stroke_width=4)
        stairs = []
        for k, p in enumerate(pts):
            if k:
                stairs.append(np.array([p[0], pts[k - 1][1], 0]))
            stairs.append(p)
        career.set_points_as_corners(stairs)
        side = VGroup(
            label(r"offers arrive while employed too \\ (here, \ one in ten months)", font_size=20, color=JOB),
            label(r"take any offer above \\ your current wage", font_size=20, color=MATCH),
            label(r"now and then the job ends: \\ back to the bottom", font_size=20, color=SEP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is one simulated career on the Island's job ladder. <bookmark mark='a'/> Offers arrive now and "
            "then, whether you are employed or not: about one month in ten. <bookmark mark='b'/> The rule is simple. "
            "If you are unemployed, take any offer, since every firm pays at least the benefit. If you are employed, "
            "take any offer that beats your current wage. Each move is a step up. <bookmark mark='c'/> And now and "
            "then the job ends, and you drop back to the bottom and start again. A career is a staircase with "
            "occasional falls."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(floor), FadeIn(floor_l), FadeIn(tag), run_time=0.8)
            self.play(Create(career), run_time=6, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def dispersion(self):
        lad = load("ladder")
        ax = plane([0.35, 1.0], [0, 32], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=5.0,
                   xticks=[0.4, 0.6, 0.8, 1.0], yticks=[0, 10, 20, 30], xlabel=r"wage", ylabel=r"density",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        fo = path(ax, lad["w"], lad["f"], color=JOB, width=4, yr=(0, 32))
        ge = path(ax, lad["w"], lad["g"], color=MATCH, width=4, yr=(0, 32))
        side = VGroup(
            label(r"identical workers, \\ identical firms", font_size=21, color=GREY_A),
            label(rf"the wages firms offer: \\ from {lad['w_lo']:.2f} to {lad['w_hi']:.2f}, \ mean {lad['mean_offer']:.2f}",
                  font_size=20, color=JOB),
            label(rf"the wages the employed earn: \\ mean {lad['mean_earned']:.2f}", font_size=20, color=MATCH),
            label(r"high-wage firms are big: \\ they recruit more and lose fewer", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Burdett and Mortensen, IER 39(2) (1998): \ 257--273", corner=DR, font_size=12)
        with self.voiceover(
            "Kenneth Burdett and Dale Mortensen asked what wages firms would choose to pay on such a ladder. "
            "<bookmark mark='a'/> Every worker is the same and every firm is the same, yet in equilibrium firms do "
            "not all pay the same wage. <bookmark mark='b'/> A firm that pays more makes less on each worker, but "
            "recruits more of them, and loses fewer to rivals. A firm that pays less keeps a fatter margin on a "
            "smaller, leakier workforce. Profits are equal along the whole range of wages. On the Island, offers "
            f"spread from {lad['w_lo']:.2f}, the benefit, up to {lad['w_hi']:.2f}. <bookmark mark='c'/> The wages "
            "people actually earn are higher than the wages offered, because workers keep climbing: on average "
            f"{lad['mean_earned']:.2f} against {lad['mean_offer']:.2f}. <bookmark mark='d'/> And firms that pay more "
            "are bigger: the link between wages and employer size that the data show everywhere."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(fo), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(fo, color=WHITE))
            vo.wait_until("c")
            self.play(Create(ge), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def monopsony(self):
        rows = VGroup(
            label(r"in a market without frictions, \ a firm that cut its wage by a cent would lose every worker",
                  font_size=23, color=GREY_A),
            label(r"on a ladder it loses some, \ slowly: \ each firm faces an upward-sloping supply of labour",
                  font_size=23, color=JOB),
            label(r"so every employer has some power over wages, \ even among many employers", font_size=24,
                  color=E.ACCENT),
            label(r"Alan Manning, \emph{Monopsony in Motion}, \ 2003; \ the evidence and the minimum wage: \ Part 38",
                  font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.2)
        tag = published_tag(r"Manning, \emph{Monopsony in Motion} (Princeton, 2003)", corner=DR, font_size=12)
        with self.voiceover(
            "There is a deeper lesson here. <bookmark mark='a'/> In a market without frictions, a firm that cut its "
            "wage by a cent would lose every worker at once. <bookmark mark='b'/> On a job ladder, it loses some, "
            "gradually, as they find better offers, and it recruits a little more slowly. Each firm faces a supply "
            "of labour that slopes upward. <bookmark mark='c'/> That is a kind of monopsony power, and it exists "
            "even with many employers, because finding them takes time. <bookmark mark='d'/> Alan Manning built "
            "a book around this idea in 2003. Its evidence, and what it implies for the minimum wage, are Part "
            "thirty-eight's."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
