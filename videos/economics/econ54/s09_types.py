from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Types(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Dynamic choices and hidden types", r"Is it habit, or is it who they are?",
             "Chapter seven. Dynamic choices and hidden types.",
             lit={1981: r"Heckman", 1984: r"Heckman and Singer", 1987: r"Rust", 1997: r"Keane and Wolpin"},
             scale=("person",), horizon=("a decade",))
        self.dynamic()
        self.panel()
        self.table()

    def dynamic(self):
        steps = flow_chain(steps=[(r"a guess at the parameters", EST),
                                  (r"solve the dynamic problem: values of each choice", MODEL),
                                  (r"choice probabilities, state by state", MODEL),
                                  (r"the likelihood of what people did", DATA)],
                           box_w=2.9, box_h=1.2, font_size=19, buff=0.4).move_to(UP * 1.3)
        notes = VGroup(
            label(r"Rust's buses (Part 44): \ the model solved inside every evaluation of the likelihood", font_size=20,
                  color=WHITE),
            label(r"Hotz and Miller: \ read the values off observed choice frequencies instead", font_size=20,
                  color=THEORY),
            label(r"Keane and Wolpin: \ careers as dynamic choices, \ with a few hidden types of person",
                  font_size=20, color=CAUTION),
        ).arrange(DOWN, buff=0.3).next_to(steps, DOWN, buff=0.7)
        tag = published_tag(r"Rust, \ Econometrica (1987); \ Hotz and Miller, \ REStud (1993); \ Keane and Wolpin, "
                            r"\ JPE (1997)", corner=DR, font_size=12)
        with self.voiceover(
            "When today's choice changes tomorrow's options, the model has to look ahead, and so does the "
            "estimator. <bookmark mark='a'/> For each guess at the parameters, <bookmark mark='b'/> solve the "
            "dynamic problem for the value of each choice in each state, <bookmark mark='c'/> turn the values into "
            "choice probabilities, <bookmark mark='d'/> and evaluate the likelihood of what people did. <bookmark "
            "mark='e'/> That is John Rust's nested fixed point, which estimated the bus engines of Part forty-four. "
            "<bookmark mark='f'/> Joseph Hotz and Robert Miller found a shortcut: read the values off the "
            "observed frequency of each choice, and skip most of the solving. <bookmark mark='g'/> And Michael "
            "Keane and Kenneth Wolpin estimated young men's careers this way, with one more ingredient that "
            "turns out to matter enormously: a few hidden types of person."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            for mk, n_ in zip("efg", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_, shift=UP * 0.1))
        self.clear_scene()

    def panel(self):
        T = load("types")
        n = T["T"] + 1
        hist, low = np.array(T["rate_hist"]), np.array(T["rate_low"])
        ax = plane([-0.5, n - 0.5], [0, 180], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=list(range(n)), yticks=[0, 50, 100, 150], xlabel=rf"weeks by bus, \ out of {T['T']}",
                   ylabel=r"people", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for k in range(n):
            g = VGroup()
            for lo, hi, col in ((0, low[k], CAUTION), (low[k], hist[k], PATIENCE)):
                if hi - lo <= 0:
                    continue
                p0, p1 = ax.ax.c2p(k - 0.38, lo), ax.ax.c2p(k + 0.38, hi)
                g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.8,
                                stroke_width=0).move_to((p0 + p1) / 2))
            bars.add(g)
        side = VGroup(
            label(rf"{T['people']} commuters, \ {T['T']} weeks", font_size=19, color=WHITE),
            label(r"each week: \ bus or not, \\ depending on how the trip \\ looks that week", font_size=19,
                  color=GREY_A),
            label(rf"hidden: \ {100 * T['truth']['share_low']:.0f}\% dislike the bus \\ (pink), \ the rest like it "
                  r"\\ (green)", font_size=19, color=CAUTION),
            label(r"no habit at all: \\ last week's choice \\ changes nothing", font_size=19, color=TRUTHC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"simulated: \ the Island's commuters", corner=DR, font_size=13)
        with self.voiceover(
            f"Here is why. The Island follows {T['people']} commuters for {T['T']} weeks. <bookmark mark='a'/> Each "
            "week each of them takes the bus or not, depending on how the trip looks that week. <bookmark "
            "mark='b'/> The bars count people by how many weeks they took the bus. <bookmark mark='c'/> We "
            f"planted two kinds of people: {100 * T['truth']['share_low']:.0f} percent who dislike the bus, in "
            "pink, and the rest, who like it, in green. The data do not say who is which. <bookmark mark='d'/> "
            "And we planted no habit at all: last week's choice has no effect on this week's."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), *[Indicate(b, color=WHITE, scale_factor=1.0) for b in bars])
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def table(self):
        T = load("types")
        head = VGroup(label(r"", font_size=20), label(r"truth", font_size=20, color=TRUTHC),
                      label(r"ignore the types", font_size=20, color=ERR),
                      label(r"two hidden types, \ by EM", font_size=20, color=EST))
        r1 = VGroup(label(r"how the trip looks", font_size=20, color=WHITE),
                    label(f"{T['truth']['b']:.2f}", font_size=21, color=TRUTHC),
                    label(f"{T['pooled_b']:.2f}", font_size=21, color=ERR),
                    label(f"{T['mix_b']:.2f}", font_size=21, color=EST))
        r2 = VGroup(label(r"habit: \ last week's choice", font_size=20, color=WHITE),
                    label(r"0", font_size=21, color=TRUTHC),
                    label(f"{T['pooled_lag']:.2f} \\ ({T['pooled_lag_se']:.2f})", font_size=21, color=ERR),
                    label(f"{T['mix_lag']:.2f}", font_size=21, color=EST))
        r3 = VGroup(label(r"share who dislike the bus", font_size=20, color=WHITE),
                    label(f"{T['truth']['share_low']:.2f}", font_size=21, color=TRUTHC),
                    label(r"--", font_size=21, color=ERR), label(f"{T['mix_share']:.2f}", font_size=21, color=EST))
        grid = VGroup(*head, *r1, *r2, *r3).arrange_in_grid(rows=4, cols=4, buff=(0.6, 0.35),
                                                             col_alignments="lccc").move_to(UP * 1.2)
        notes = VGroup(
            label(r"spurious state dependence: \ who people are, \ mistaken for what they did last week",
                  font_size=21, color=ERR),
            label(r"the mixture asks, \ person by person, \ how likely each type is, \ then refits: \ the EM "
                  r"algorithm", font_size=21, color=EST),
            label(r"habit and heterogeneity call for opposite policies: \ a free week builds a habit, \ or does "
                  r"nothing", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(grid, DOWN, buff=0.6)
        tag = published_tag(r"Heckman (1981); \ Heckman and Singer, \ Econometrica 52(2) (1984)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now estimate. <bookmark mark='a'/> Ignore the types, and fit one logit to everybody. The response to "
            f"how the trip looks comes out at {T['pooled_b']:.2f}, too small: the hidden differences between people "
            "add noise that flattens it. <bookmark mark='b'/> Worse, add last week's choice as a regressor, and "
            f"it comes out at {T['pooled_lag']:.2f}, more than twenty standard errors from zero: a strong habit "
            "that does not exist. People who took the bus last week are mostly the people who like the bus. James "
            "Heckman called this spurious state dependence. <bookmark mark='c'/> Now let there be two hidden "
            "types, and estimate their share and their constants along with everything else. The EM algorithm "
            "asks, person by person, how likely each type is given everything they did, refits, and repeats. "
            f"It finds the response, {T['mix_b']:.2f}, the share of bus-haters, {T['mix_share']:.2f}, and a habit "
            f"of {T['mix_lag']:.2f}: about zero. <bookmark mark='d'/> The difference matters. If riding builds a "
            "habit, a free week of buses is a good investment; if it does not, it is a gift to people who would "
            "have ridden anyway."
        ) as vo:
            self.play(FadeIn(VGroup(*head)), FadeIn(VGroup(*r1[:2], *r2[:2], *r3[:2])), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(r1[2]), FadeIn(r3[2]))
            vo.wait_until("b")
            self.play(FadeIn(r2[2]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(r1[3]), FadeIn(r2[3]), FadeIn(r3[3]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
