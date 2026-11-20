from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403

SHOWN = ("1", "2", "5", "10", "30", "100")


class VFI(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Value function iteration", r"How does a computer find the unknown function?",
             "Chapter four. Value function iteration.", lit={1965: r"Blackwell"}, scale=("person",),
             horizon=("a day", "for ever"))
        self.iterate()
        self.contraction()
        self.policy()

    def _axes(self):
        return plane([0, 1], [-70, 0], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.9,
                     xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[-60, -40, -20, 0], xlabel=r"cake $w$",
                     ylabel=r"value $V_n(w)$", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.0f}", font_size=15)

    def iterate(self):
        K = load("cake")
        w = np.array(K["w"])
        keep = w >= 0.05
        ax = self._axes()
        cols = [interpolate_color(ManimColor(GREY_B), ManimColor(VALUE), k / (len(SHOWN) - 1))
                for k in range(len(SHOWN))]
        curves = [path(ax, w[keep], np.array(K["kept"][s])[keep], c, 3, yr=(-70, 0)) for s, c in zip(SHOWN, cols)]
        zero = path(ax, w[keep], np.zeros(keep.sum()), GREY_C, 3)
        exact = DashedVMobject(path(ax, w[keep], np.array(K["V_exact"])[keep], WHITE, 2, yr=(-70, 0)),
                               num_dashes=40)
        names = VGroup(*[label(rf"$V_{{{s}}}$", font_size=18, color=c).next_to(
            ax.ax.c2p(1.0, float(np.array(K["kept"][s])[-1])), RIGHT, buff=0.1) for s, c in zip(SHOWN, cols)])
        z_name = label(r"$V_0 = 0$", font_size=18, color=GREY_C).next_to(ax.ax.c2p(1.0, 0), RIGHT, buff=0.1)
        y_prev = z_name.get_y()
        for n_ in names:                                   # spread the labels so that none overlap
            if n_.get_y() > y_prev - 0.3:
                n_.set_y(y_prev - 0.3)
            y_prev = n_.get_y()
        rec = MathTex(r"V_{n+1}(w) = \max_{c} \big\{ \log c + \beta\, V_n(w-c) \big\}", font_size=30,
                      color=VALUE).to_edge(UP, buff=0.3).shift(RIGHT * 2.2)
        side = VGroup(
            label(rf"a grid of {K['n']:,} cake sizes".replace(",", "{,}"), font_size=19, color=GREY_A),
            label(r"$V_n$: \ the best you can do \\ if the world ends after $n$ days", font_size=19, color=VALUE),
            label(r"$V_1$: \ eat it all today", font_size=19, color=GREY_B),
            label(r"by $V_{100}$, \ nothing moves", font_size=19, color=VALUE),
            label(r"dashed: \ the exact answer \\ from chapter three", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A computer cannot guess the shape of V. It does something simpler. <bookmark mark='a'/> Put the cake "
            f"sizes on a grid, here {K['n']:,} of them, and start from any guess at all, say V is zero everywhere. "
            "<bookmark mark='b'/> Then apply the Bellman equation as a recipe: today's best choice, valued with "
            "yesterday's guess, gives a new guess. <bookmark mark='c'/> The guesses have a meaning. V n is the best "
            "you can do if the world ends after n days. <bookmark mark='d'/> V one: eat everything today. "
            "<bookmark mark='e'/> V two, V five, V ten: each is lower, because the cake must stretch over more days. "
            "<bookmark mark='f'/> By V one hundred, nothing moves any more. <bookmark mark='g'/> And the dashed line "
            "is the exact answer found by hand. The iterations land on it, except at the smallest cakes, where a "
            "grid of thousandths is too coarse to cut."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(zero), FadeIn(z_name), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(rec))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(curves[0]), FadeIn(names[0]), FadeIn(side[2]))
            vo.wait_until("e")
            for c, n_ in zip(curves[1:4], names[1:4]):
                self.play(Create(c), FadeIn(n_), run_time=0.8)
            vo.wait_until("f")
            self.play(Create(curves[4]), FadeIn(names[4]), run_time=0.8)
            self.play(Create(curves[5]), FadeIn(names[5]), FadeIn(side[3]), run_time=0.8)
            vo.wait_until("g")
            self.play(Create(exact), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def contraction(self):
        K = load("cake")
        g = np.array(K["gaps"])
        it = np.arange(1, len(g) + 1)
        ax = plane([0, 250], [-11, 1], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 50, 100, 150, 200, 250], yticks=[-10, -8, -6, -4, -2, 0], xlabel=r"iteration $n$",
                   ylabel=r"$\| V_{n} - V_{n-1} \|$, \ largest gap \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: rf"10^{{{v:.0f}}}", font_size=15)
        dots = VGroup(*[Dot(ax.ax.c2p(x, np.log10(y)), radius=0.03, color=VALUE) for x, y in zip(it, g) if y > 0])
        side = VGroup(
            MathTex(r"\| TV - TW \| \le \beta\, \| V - W \|", font_size=32, color=E.ACCENT),
            label(rf"each step shrinks the gap by $\beta = {K['beta']}$: \\ a straight line on a log scale \\ "
                  rf"(measured ratio {K['ratio']:.3f})", font_size=19, color=VALUE),
            label(r"Blackwell, \ 1965: \ more tomorrow is never worse, \\ and the future is discounted, \\ so the "
                  r"recipe is a contraction", font_size=19, color=GREY_A),
            label(r"one fixed point, \ reached from any start", font_size=20, color=E.ACCENT),
            label(rf"here: \ {K['iterations']} steps to $10^{{-10}}$", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Blackwell, \ \emph{Annals of Mathematical Statistics} 36(1) (1965); \ Stokey, \ Lucas "
                            r"and Prescott (1989), \ ch.\ 3", corner=DR, font_size=12)
        with self.voiceover(
            "Why must this work? <bookmark mark='a'/> Call the recipe T: it takes a guess V and returns a new "
            "one. Take any two guesses. After one application of T, the largest distance between them has shrunk by "
            "at least the factor beta. <bookmark mark='b'/> Here is the distance between successive guesses for the "
            f"cake, on a log scale. It falls on a straight line, by a factor of {K['ratio']:.2f} at each step, "
            "which is beta exactly. <bookmark mark='c'/> David Blackwell showed in 1965 that two plain properties "
            "are enough for this: more cake tomorrow is never worse, and the future is discounted. "
            "<bookmark mark='d'/> A map that shrinks distances like this is a contraction, and a contraction has "
            "exactly one fixed point, which the iterations reach from any starting guess. <bookmark mark='e'/> Here "
            f"it takes {K['iterations']} steps to agree to ten decimal places. That guarantee is why economists "
            "can solve problems with no pencil-and-paper answer at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Write(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def policy(self):
        K = load("cake")
        w = np.array(K["w"])
        keep = w >= 0.02
        ax = plane([0, 1], [0, 0.12], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.04, 0.08, 0.12], xlabel=r"cake $w$",
                   ylabel=r"eaten today, \ $c(w)$", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=15)
        grid_c = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.035, color=POLICY) for x, y in zip(w[keep],
                                                                                       np.array(K["c"])[keep])])
        exact = path(ax, [0, 1], [0, 1 - K["beta"]], WHITE, 2.5, smooth=False)
        side = VGroup(
            label(r"dots: \ the computer's policy, \\ read off the grid", font_size=19, color=POLICY),
            label(r"line: \ $c = (1 - \beta) w$", font_size=19, color=WHITE),
            label(rf"on average it eats {100 * K['share']:.1f}\% \\ instead of {100 * (1 - K['beta']):.0f}\%: "
                  r"\\ the grid can only cut thousandths", font_size=19, color=HOLD),
            label(r"finer grids, \ or smarter methods, \\ close the gap", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The value function is only a means. What you want is the policy: how much to eat with each size of "
            "cake. <bookmark mark='a'/> The dots are the computer's policy, read off the grid as the best choice "
            "at each point. <bookmark mark='b'/> The line is the exact rule, one minus beta of the cake. "
            f"<bookmark mark='c'/> On average the computer eats {100 * K['share']:.1f} percent instead of ten, "
            "because on this grid the cake can only be cut in thousandths. <bookmark mark='d'/> Finer grids, "
            "interpolation between grid points, or smarter methods close the gap. Value function iteration is slow "
            "but almost impossible to break, and it is the method the rest of this part builds on."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in grid_c], lag_ratio=0.02), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(exact), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
