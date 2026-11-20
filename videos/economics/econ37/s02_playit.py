from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403

CHIP = ("#7FD1B9", "#F2C14E", "#E8A0B4", "#C9A0FF")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ Schelling's rule", r"How mixed does the board stay?",
             "Chapter one. Play it: Schelling's rule.", lit={1971: r"Schelling"}, scale=("household", "city"),
             horizon=("a decade",))
        self.choose()
        self.reveal()
        self.sweep()

    def choose(self):
        S = load("schelling")
        cards = point_cards([
            (r"A: \ about half", r"the board \\ stays mixed", CHIP[0]),
            (r"B: \ about 60\%", r"a little \\ clustering", CHIP[1]),
            (r"C: \ about 75\%", r"large blocks \\ of one kind", CHIP[2]),
            (r"D: \ over 90\%", r"almost complete \\ separation", CHIP[3]),
        ], width=12.6, cols=4, font_size=21).move_to(UP * 0.1)
        q = wrapped_label(r"every coin is content with a third of its neighbours like it: \ when the board settles, "
                          r"what share of a coin's neighbours are its own kind?", 12.0, 26, E.ACCENT).to_edge(
            UP, buff=0.6)
        ring = countdown().scale(0.7).next_to(cards, DOWN, buff=0.5)
        start = label(rf"at the start: \ {100 * S['start']:.0f}\%", font_size=20, color=GREY_A).to_corner(DL,
                                                                                                       buff=0.6)
        with self.voiceover(
            "Your turn. Every coin is content as long as a third of its neighbours are its own kind. At the start "
            f"the average coin's neighbours are {100 * S['start']:.0f} percent its own kind. When the board "
            "settles, what will that share be? <bookmark mark='a'/> About half, because such tolerant coins hardly "
            "need to move; about sixty percent; about three quarters; or over ninety percent. Pause, and choose."
        ) as vo:
            self.play(FadeIn(q), FadeIn(start))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards.cards], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        S = load("schelling")
        ax = plane([0, S["rounds"]], [0.4, 1.0], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=list(range(0, S["rounds"] + 1)), yticks=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                   xlabel=r"round", ylabel=r"share of a coin's neighbours of its own kind", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, list(range(len(S["like"]))), S["like"], CHIP[2], 3.4, smooth=False)
        dots_ = VGroup(*[dot(ax, k, v, CHIP[2], 0.06) for k, v in enumerate(S["like"])])
        mini = board(S["frames"][-1], size=2.6).to_edge(RIGHT, buff=0.6).shift(UP * 0.6)
        side = VGroup(
            label(rf"C: \ {100 * S['final']:.0f}\% \ after {S['rounds']} rounds", font_size=24, color=CHIP[2]),
            label(rf"content with half alike: \ {100 * S['half_final']:.0f}\%", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(mini, DOWN, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The answer is C. <bookmark mark='a'/> The share climbs from {100 * S['start']:.0f} percent to "
            f"{100 * S['final']:.0f} in {S['rounds']} rounds, and the board ends in large blocks of one kind. "
            "<bookmark mark='b'/> Coins content with half their neighbours alike end at "
            f"{100 * S['half_final']:.0f} percent. Each move by one discontented coin leaves its old neighbours a "
            "little less content, and the movements cascade."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(mini, lag_ratio=0.002), Create(ln), FadeIn(dots_),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def sweep(self):
        S = load("schelling")
        sw = S["sweep"]
        th, lk, st = np.array(sw["thresholds"]), np.array(sw["like"]), np.array(sw["settled"])
        ax = plane([0, 0.8], [0.4, 1.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=[0.4, 0.6, 0.8, 1.0],
                   xlabel=r"the share of like neighbours each coin wants", ylabel=r"like neighbours when it ends",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ok = st > 0.5
        ln = path(ax, th[ok], lk[ok], E.ACCENT, 3.4, smooth=False)
        pts = VGroup(*[dot(ax, x, y, E.ACCENT if s > 0.5 else LOSS, 0.07) for x, y, s in zip(th, lk, st)])
        churn = shade(ax, [(float(th[~ok].min()) - 0.025, 0.8)], 0.4, 1.0, color=RECESS, opacity=0.6)
        side = VGroup(
            label(r"a small taste for \\ like neighbours \\ makes a lot of sorting", font_size=19, color=E.ACCENT),
            label(r"grey: \ the board \\ never settles", font_size=19, color=LOSS),
            label(r"a possibility, \\ not a diagnosis: \\ prices, \ policy and \\ discrimination sort too",
                  font_size=19, color=WHITE),
            label(r"James Sakoda had \\ a similar model \\ in 1949", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.SCHELLING_1971.tag + r"; \ played by Agora", corner=DR, font_size=11)
        with self.voiceover(
            "Now play it for every tolerance. Each point is the share of like neighbours when the board stops, "
            "against the share each coin wants. <bookmark mark='a'/> The curve rises far above the line of what "
            "anyone asked for: coins wanting a quarter alike end with well over half, coins wanting a half end "
            "near ninety percent. <bookmark mark='b'/> Past about two thirds the board never settles: someone is "
            "always discontented, and the churn keeps it mixed. <bookmark mark='c'/> The model shows that mild "
            "preferences can produce stark segregation. It does not show that real segregation comes from mild "
            "preferences: prices, laws, lending and discrimination sort people too, and Part thirty-nine returns to "
            "them. <bookmark mark='d'/> Credit where it is due: the sociologist James Sakoda had a similar "
            "checkerboard model in his dissertation of 1949."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(seg(ax, 0.4, 0.4, 0.8, 0.8, GREY_B, 1.5, dashed=True)))
            vo.wait_until("b")
            self.play(FadeIn(churn), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
