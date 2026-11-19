from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403

HAWK = "#F25F5C"
DOVE = "#7EC8F5"
RPS = ("#F2A65A", "#7BD88F", "#C9A0FF")


class Evolution(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Evolution and learning", r"Can players who never reason about each other still reach an "
             r"equilibrium?", "Chapter eleven. Evolution and learning.", lit={1973: r"Maynard Smith and Price"},
             scale=("person", "market"), horizon=("a year", "a century"))
        self.hawkdove()
        self.cycle()
        self.learning()

    def hawkdove(self):
        e = load("evolution")
        A = np.array(e["A"])
        mat = matrix(A, A.T, [r"hawk", r"dove"], [r"hawk", r"dove"], row_name=r"one animal", col_name=r"another",
                     cell_w=1.7, cell_h=0.85, font_size=24, labels_size=18, row_color=HAWK, col_color=DOVE
                     ).scale(0.95).to_corner(UL, buff=0.5).shift(RIGHT * 0.6)
        ax = plane([0, 25], [0, 1], center=RIGHT * 2.4 + DOWN * 0.4, x_length=6.0, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20, 25], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"time",
                   ylabel=r"share of hawks", font_size=16)
        t = np.array(e["t"])
        curves = VGroup(*[path(ax, t, np.array(p), color=HAWK, width=3) for p in e["paths"]])
        ess = DashedLine(ax.ax.c2p(0, e["ess"]), ax.ax.c2p(25, e["ess"]), color=EQ, stroke_width=2)
        el = label(rf"$V/C = {e['ess']:.1f}$", font_size=18, color=EQ).next_to(ax.ax.c2p(25, e["ess"]), UP, buff=0.08)
        side = VGroup(
            label(rf"a prize worth {e['V']:.0f}; \ a fight costs {e['C']:.0f}", font_size=21),
            label(r"hawks fight; \ doves share, \ or back down", font_size=21, color=GREY_A),
            label(r"no reasoning: \ strategies that earn more \\ simply become more common", font_size=21,
                  color=DOVE),
            label(r"the replicator dynamic: \ from any start, \\ hawks settle at half the population", font_size=21,
                  color=HAWK),
            label(r"an evolutionarily stable strategy: \\ no rare mutant can invade it", font_size=22, color=EQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(mat, DOWN, buff=0.45).align_to(mat, LEFT)
        tag = published_tag(r"Maynard Smith and Price, Nature 246 (1973)", corner=DR, font_size=13)
        with self.voiceover(
            "Equilibrium can also be reached without anyone reasoning at all. <bookmark mark='a'/> In 1973 John "
            "Maynard Smith and George Price applied game theory to animals contesting a prize worth two, where a "
            "fight costs four. <bookmark mark='b'/> Hawks always fight; doves share with other doves and back down "
            "before hawks. <bookmark mark='c'/> No animal thinks. Strategies that earn more just leave more "
            "offspring, and become more common. <bookmark mark='d'/> Follow that rule, the replicator dynamic, and "
            "from any starting mixture the population settles at half hawks and half doves, the share where both "
            "earn the same. <bookmark mark='e'/> Maynard Smith and Price called it an evolutionarily stable strategy: "
            "a population playing it cannot be invaded by a rare mutant. It is a Nash equilibrium, reached by "
            "selection instead of thought."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(ax), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2), Create(ess), FadeIn(el),
                      FadeIn(side[3]), run_time=3)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def cycle(self):
        e = load("evolution")
        rps = np.array(e["rps"])
        R = 2.4
        c0 = LEFT * 3.2 + DOWN * 0.4
        V = [c0 + R * np.array([np.cos(PI / 2 + 2 * PI * k / 3), np.sin(PI / 2 + 2 * PI * k / 3), 0])
             for k in range(3)]
        tri = Polygon(*V, stroke_color=GREY_B, stroke_width=2)
        names = VGroup(*[label(n, font_size=20, color=col).next_to(v, d, buff=0.12) for n, col, v, d in
                         zip((r"all rock", r"all paper", r"all scissors"), RPS, V, (UP, DL, DR))])

        def pt(x):
            return x[0] * V[0] + x[1] * V[1] + x[2] * V[2]

        orbit = VMobject(stroke_color=EQ, stroke_width=3).set_points_smoothly([pt(x) for x in rps[::10]])
        mid = Dot(pt([1 / 3, 1 / 3, 1 / 3]), radius=0.08, color=WHITE)
        side = VGroup(
            label(r"rock, \ paper, \ scissors: \ each strategy beats one \\ and loses to another", font_size=22),
            label(r"the only equilibrium: \ a third each", font_size=22, color=GREY_A),
            label(r"under the replicator, \ the population never settles: \\ rock spreads, \ then paper, \ then "
                  r"scissors, \ round and round", font_size=22, color=EQ),
            label(r"side-blotched lizards cycle like this \\ through three mating strategies \\ (Sinervo and Lively, "
                  r"1996)", font_size=21, color=GREY_A),
            label(r"evolution can find an equilibrium, \\ or circle it for ever", font_size=23, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = published_tag(r"Sinervo and Lively, Nature 380 (1996)", corner=DR, font_size=13)
        with self.voiceover(
            "Selection doesn't always settle. <bookmark mark='a'/> In rock, paper, scissors each strategy beats one "
            "and loses to another. <bookmark mark='b'/> Its only equilibrium is a third of each. "
            "<bookmark mark='c'/> But under the replicator dynamic a population that starts anywhere else never gets "
            "there: rock spreads until paper is profitable, paper spreads until scissors is, and so round and round, "
            "a closed orbit about the equilibrium. <bookmark mark='d'/> Barry Sinervo and Curt Lively found male "
            "side-blotched lizards in California cycling like this, through three mating strategies, over the years. "
            "<bookmark mark='e'/> Evolution can find an equilibrium, or circle it for ever, as Scarf's prices did in "
            "Part nine."
        ) as vo:
            self.play(Create(tri), FadeIn(names), FadeIn(mid), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(mid, color=EQ))
            vo.wait_until("c")
            self.play(Create(orbit), FadeIn(side[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def learning(self):
        e = load("evolution")
        fp = np.array(e["fp_row"])
        rounds = np.arange(1, len(fp) + 1)
        ax = plane([0, 3.2], [0, 1], center=LEFT * 2.9 + DOWN * 0.3, x_length=6.0, y_length=4.6,
                   xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1], xlabel=r"rounds played",
                   ylabel=r"share of heads so far", font_size=16,
                   xfmt=lambda v: {0: "1", 1: "10", 2: "100", 3: "1000"}.get(int(round(v)), ""))
        curve = path(ax, np.log10(rounds), fp, color=ANA, width=3, smooth=False)
        half = DashedLine(ax.ax.c2p(0, 0.5), ax.ax.c2p(3.2, 0.5), color=EQ, stroke_width=2)
        side = VGroup(
            label(r"fictitious play (Brown, 1951): \\ each round, \ best-respond to how often \\ the other has played "
                  r"each move so far", font_size=21),
            label(r"matching pennies: \ the frequencies swing, \\ and narrow onto a half", font_size=22, color=ANA),
            label(r"Julia Robinson (1951): \ in two-player \\ zero-sum games, \ it always converges", font_size=21,
                  color=EQ),
            label(r"Shapley (1964): \ a three-strategy game \\ where it cycles for ever", font_size=21, color=HOLD),
            label(r"learning rules that do converge, \\ and how fast: \ chapter 16", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "People learn, too. <bookmark mark='a'/> In 1951 George Brown proposed fictitious play: in each round, "
            "each player plays the best response to how often the other has played each move so far. "
            "<bookmark mark='b'/> In matching pennies, where one player wants to match and the other to mismatch, the "
            "running frequencies swing back and forth, and narrow onto a half each, the mixed equilibrium. "
            "<bookmark mark='c'/> The same year Julia Robinson proved that in any two-player game of pure conflict, "
            "fictitious play converges. <bookmark mark='d'/> But in 1964 Lloyd Shapley found a game with three "
            "strategies where it cycles for ever. <bookmark mark='e'/> Which learning rules do reach equilibrium, and "
            "how quickly, turned out to matter far beyond economics, as the frontier chapter shows."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curve), Create(half), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
