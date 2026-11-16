from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Loop(SoundScene):
    def construct(self):
        chapter(self, 9, r"Popularity feeding on itself", r"What happens when a recommender learns from its own recommendations?")
        self.simulation()
        self.curve()
        self.lorenz()
        self.meaning()

    # ------------------------------------------------------------------
    def simulation(self):
        items = [
            (r"a service recommends each listener the five most played songs", WHITE),
            (r"listeners play a recommendation if it suits them \ (their true taste decides)", WHITE),
            (r"the plays feed the next round's ranking", WHITE),
            (r"beside it, \ a world without a recommender: \ listeners browse at random and play what suits them", WHITE),
            (r"Part 60's MusicLab, \ with the influence built by engineers", TUNE),
        ]
        rows_scene(self, r"a feedback loop", items,
                   "Recommenders change what they measure. Monochord runs a simple loop. <bookmark mark='b'/> A service recommends "
                   "each listener the five most played songs. <bookmark mark='c'/> Listeners play a recommendation if it suits them, "
                   "their true taste deciding. <bookmark mark='d'/> Those plays feed the next round's ranking. "
                   "<bookmark mark='e'/> Beside it runs a world without a recommender, where listeners browse at random and play "
                   "what suits them. <bookmark mark='f'/> It is Part 60's MusicLab, with the social influence built by engineers.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def curve(self):
        d = load("loop")
        g, ge, go = np.array(d["gini"]), np.array(d["gini_explore"]), np.array(d["gini_own"])
        r = np.arange(1, len(g) + 1)
        ax = frame_axes(width=8.4, height=3.2, xlo=1, xhi=len(g), ylo=0, yhi=1.0, center=DOWN * 0.4 + LEFT * 0.6)
        c1 = curve(r, g, ax.to, color=EAR, width=3.5)
        c2 = curve(r, ge, ax.to, color=BLUE, width=3)
        c3 = curve(r, go, ax.to, color=GREY_B, width=3)
        yt = VGroup(*[label(f"{v:g}", font_size=13, color=GREY_A).next_to(ax.to(1, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xl = label(r"rounds", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        key = VGroup(label(r"recommending the most played", font_size=15, color=EAR), label(r"the same, \ exploring 30\% of the time", font_size=15, color=BLUE),
                     label(r"no recommender", font_size=15, color=GREY_B)).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        note = label(rf"the top 1\% of songs' share of plays: \ {100 * d['top1']:.0f}\% with the loop, \ {100 * d['top1_explore']:.0f}\% exploring, \ {100 * d['top1_own']:.0f}\% without", font_size=16, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"inequality of plays \ (Gini), \ round by round", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the inequality of plays, round by round. <bookmark mark='a'/> Without a recommender, listeners spread "
            "their plays: the Gini stays low. <bookmark mark='b'/> With the loop, the first few songs to be played are "
            "recommended to everyone, played more, and recommended more: the Gini climbs toward one. <bookmark mark='c'/> "
            "Exploring thirty per cent of the time slows the runaway, because songs outside the top get a chance to be played. "
            f"<bookmark mark='d'/> At the end, the top one percent of songs hold {say(100 * d['top1'])} percent of all plays "
            f"with the loop, against {say(100 * d['top1_own'])} without a recommender."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(c3), FadeIn(key[2]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(c2), FadeIn(key[1]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"a recommender trained on its own outputs measures its own influence and calls it taste", WHITE),
            (r"real services mix popularity, \ personal taste, \ exploration and editors, \ and study the loop carefully", WHITE),
            (r"offline tests on logged plays inherit the loop: \ the logs reflect exposure, selection and other routes to discovery", WHITE),
            (r"the remedies: \ randomized exploration, \ reweighting by how likely each recommendation was \ (inverse propensity)", WHITE),
            (r"what people play is partly what they were shown", TUNE),
        ]
        rows_scene(self, r"what the loop means", items,
                   "What does it mean? <bookmark mark='b'/> A recommender trained on its own outputs measures its own influence and calls it taste. <bookmark mark='c'/> Real services mix popularity, personal taste, exploration and human editors, and study the loop carefully. <bookmark mark='d'/> Offline tests on logged plays inherit the loop, because the logs reflect exposure, selection and other routes to discovery. <bookmark mark='e'/> Possible remedies include randomized exploration and inverse-propensity weighting, when exposure probabilities and overlap are known well enough. <bookmark mark='f'/> What people play is partly what they were shown.", marks="bcdef")

    # ------------------------------------------------------------------
    def lorenz(self):
        d = load("lorenz")
        ax = frame_axes(width=4.6, height=4.6, xlo=0, xhi=1, ylo=0, yhi=1, center=DOWN * 0.3 + LEFT * 2.6)
        diag = DashedLine(ax.to(0, 0), ax.to(1, 1), color=GREY_D, stroke_width=1.5)
        def lc(v, col):
            v = np.array(v)
            return curve(np.linspace(0, 1, len(v)), v, ax.to, color=col, width=3)
        cs = VGroup(lc(d["own"], GREY_B), lc(d["explore"], BLUE), lc(d["rec"], EAR))
        t = d["top10"]
        key = VGroup(label(r"the most-played tenth of the clips gets:", font_size=17, color=GREY_A),
                     label(rf"listeners on their own: \ {100 * t['own']:.0f}\% of plays", font_size=18, color=GREY_B),
                     label(rf"popularity, \ exploring 30\%: \ {100 * t['explore']:.0f}\%", font_size=18, color=BLUE),
                     label(rf"popularity alone: \ {100 * t['rec']:.0f}\%", font_size=18, color=EAR)).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(RIGHT * 3.2 + DOWN * 0.2)
        xl = label(r"clips, \ least played first", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"share of all plays", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15)
        head = label(r"who gets the plays", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Another view of the same thirty rounds: a Lorenz curve, the clips lined up from least to most played, and the "
            "share of plays they hold together. Equal shares would be the diagonal. <bookmark mark='a'/> On their own, "
            f"listeners give the most-played tenth of the clips {say(round(100 * t['own']))} per cent of plays. "
            f"<bookmark mark='b'/> With the recommender exploring, {say(round(100 * t['explore']))} per cent. "
            f"<bookmark mark='c'/> With popularity alone, {say(round(100 * t['rec']))} per cent: nearly everything, and the "
            "curve hugs the floor until the very last clips."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(diag), FadeIn(xl), FadeIn(yl), FadeIn(key[0]))
            for mark, cv_, k in zip("abc", cs, key[1:]):
                vo.wait_until(mark)
                self.play(Create(cv_), FadeIn(k), run_time=1.0)
        self.wait(0.6)
        self.clear_scene()
