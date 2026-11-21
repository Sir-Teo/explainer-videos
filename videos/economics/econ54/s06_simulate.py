from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Simulate(VoiceoverScene):
    def construct(self):
        card(self, 5, r"When the likelihood has no formula", r"How do you fit a model you can only simulate?",
             "Chapter five. When the likelihood has no formula.",
             lit={1989: r"McFadden; \ Pakes and Pollard", 1993: r"Gouri\'eroux, Monfort and Renault"},
             scale=("person", "market"), horizon=("a year",))
        self.why()
        self.indirect()
        self.many()

    def why(self):
        loop = flow_chain(steps=[(r"a guess at the parameters", EST), (r"simulate S data sets with fixed draws",
                                                                       MODEL),
                                 (r"their moments", MODEL), (r"compare with the data's moments", DATA)],
                          box_w=2.9, box_h=1.15, font_size=19, buff=0.4).move_to(UP * 1.2)
        back = CurvedArrow(loop.boxes[3].get_bottom() + DOWN * 0.1, loop.boxes[0].get_bottom() + DOWN * 0.1,
                           angle=-PI / 3, color=GREY_B, stroke_width=2.5)
        back_l = label(r"adjust, \ and repeat", font_size=18, color=GREY_A).next_to(back, DOWN, buff=0.1)
        notes = VGroup(
            label(r"the same random draws at every guess: \ otherwise the objective jumps, \ and no optimizer can "
                  r"climb it", font_size=20, color=WHITE),
            label(r"the price of simulating: \ the variance grows by a factor $1 + 1/S$", font_size=20,
                  color=THEORY),
            label(r"used for random-coefficient demand (Part 43), \ dynamic choice (Part 44), \ life cycles "
                  r"(next chapter)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.28).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"McFadden, \ Econometrica 57(5) (1989); \ Pakes and Pollard, \ ibid.", corner=DR,
                            font_size=12)
        integ = VGroup(
            MathTex(r"\Pr(i \text{ chooses } j) = \int \frac{e^{V_{ij}(\beta)}}{\sum_k e^{V_{ik}(\beta)}}\, "
                    r"f(\beta)\, d\beta", font_size=44, color=THEORY),
            label(r"tastes that vary from person to person: \ an integral with no formula", font_size=22,
                  color=GREY_A),
            label(r"but one draw of $\beta$ at a time, \ the model is easy to simulate", font_size=22, color=MODEL),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.3)
        with self.voiceover(
            "The logit had a formula for each choice's probability. Most realistic models do not. Let tastes vary "
            "from person to person, or let today's choice depend on expectations about tomorrow, and the "
            "probability of what someone did becomes an integral nobody can write down. <bookmark mark='z'/> But you "
            "can still simulate the model. In 1989 Daniel McFadden, and separately Ariel Pakes and David Pollard, "
            "showed how to estimate with simulations. <bookmark mark='a'/> Guess the parameters. <bookmark mark='b'/> "
            "Simulate the model several times, S data sets as large as the real one. <bookmark mark='c'/> Compute "
            "their moments, <bookmark mark='d'/> compare them with the data's, and adjust the guess until they "
            "match: the method of simulated moments. <bookmark mark='e'/> Two rules. Use the same random draws at "
            "every guess, or the objective jumps about and no optimizer can climb it. <bookmark mark='f'/> And "
            "pay for the simulation in precision: with S simulated data sets, the variance of the estimate is "
            "multiplied by one plus one over S. <bookmark mark='g'/> This is the workhorse behind random-coefficient "
            "demand in Part forty-three, dynamic choice in Part forty-four, and the life cycle in the next chapter."
        ) as vo:
            self.play(FadeIn(tag), Write(integ[0]), FadeIn(integ[1]), run_time=1.5)
            vo.wait_until("z")
            self.play(FadeIn(integ[2]))
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(integ))
                an = [FadeIn(loop.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(loop.arrows[k - 1]))
                self.play(*an)
            self.play(Create(back), FadeIn(back_l))
            for mk, n_ in zip("efg", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_, shift=UP * 0.1))
        self.clear_scene()

    def indirect(self):
        M = load("ma1")
        y = np.array(M["example"])
        ax = plane([0, len(y)], [-3.5, 3.5], center=UP * 1.7 + LEFT * 0.2, x_length=11.0, y_length=2.4,
                   xticks=[0, 20, 40, 60, 80], yticks=[-3, 0, 3], xlabel=r"period", ylabel=r"",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=13)
        ser = path(ax, np.arange(len(y)), y, DATA, 2.0, smooth=False)
        eq = MathTex(r"y_t = e_t + \theta\, e_{t-1}", r"\qquad \text{lens: } y_t = a_1 y_{t-1} + a_2 y_{t-2} + "
                     r"a_3 y_{t-3} + u_t", font_size=34, color=THEORY).next_to(ax, DOWN, buff=0.55)
        rows = VGroup(
            label(r"the model is easy to simulate, \ its likelihood awkward", font_size=21, color=MODEL),
            label(rf"fit the lens to the data: \ $a = ({M['aux'][0]:.2f},\ {M['aux'][1]:.2f},\ "
                  rf"{M['aux'][2]:.2f})$".replace("-", "{-}"), font_size=21, color=DATA),
            label(r"choose $\theta$ so the lens, \ fitted to simulated data, \ sees the same", font_size=21,
                  color=EST),
            label(rf"this sample: \ indirect inference {M['one_ii']:.2f}; \ from the first autocorrelation alone "
                  rf"{M['one_naive']:.2f}; \ truth {M['theta']:.1f}", font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(eq, DOWN, buff=0.5)
        tag = published_tag(r"Gouri\'eroux, \ Monfort and Renault, \ J. Applied Econometrics 8 (1993); \ Smith "
                            r"(1993)", corner=DR, font_size=12)
        with self.voiceover(
            "Indirect inference, from Christian Gouriéroux, Alain Monfort and Éric Renault, and from Anthony Smith, "
            "goes one step further. <bookmark mark='a'/> Take a moving average: each period's value is a fresh "
            "shock plus theta times the last one. It is trivial to simulate, but its likelihood is awkward to "
            "write. <bookmark mark='b'/> So look at the data through a lens that is easy to fit: a regression of "
            "each value on its three predecessors, by least squares. The lens is the wrong model, and that does "
            "not matter. <bookmark mark='c'/> Choose theta so that the same lens, fitted to data simulated from the "
            f"model, sees the same coefficients. <bookmark mark='d'/> In this sample of {M['n']} periods, indirect "
            f"inference gives {M['one_ii']:.2f}; the simplest method, inverting the first autocorrelation, gives "
            f"{M['one_naive']:.2f}. The truth is {M['theta']:.1f}."
        ) as vo:
            self.play(FadeIn(ax), Create(ser), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(Write(eq[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eq[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def many(self):
        M = load("ma1")
        bins = np.array(M["bins"])
        top = max(max(M["naive"]["hist"]), max(M["ii"]["hist"]))
        ax = plane([bins[0], bins[-1]], [0, top * 1.1], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8,
                   y_length=4.6, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 20, 40, 60, 80],
                   xlabel=r"estimate of $\theta$", ylabel=rf"samples, \ of {M['reps']}", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)

        def hist(h, color, op):
            g = VGroup()
            for k, c in enumerate(h):
                if c == 0:
                    continue
                p0, p1 = ax.ax.c2p(bins[k], 0), ax.ax.c2p(bins[k + 1], c)
                g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=color, fill_opacity=op,
                                stroke_color=color, stroke_width=1.2).move_to((p0 + p1) / 2))
            return g

        hn = hist(M["naive"]["hist"], GRID, 0.35)
        hi = hist(M["ii"]["hist"], EST, 0.55)
        tl = vline(ax, M["theta"], 0, top * 1.05, TRUTHC, 2.0)
        side = VGroup(
            label(rf"{M['reps']} samples of {M['n']} periods, \\ $\theta = {M['theta']:.1f}$", font_size=19,
                  color=TRUTHC),
            label(rf"grey: \ the first autocorrelation \\ error {M['naive']['rmse']:.3f}", font_size=19, color=GRID),
            label(rf"gold: \ indirect inference \\ error {M['ii']['rmse']:.3f}", font_size=19, color=EST),
            label(r"the lens used more of the \\ data's shape, \ so it learned more", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"One sample proves nothing, so repeat it {M['reps']} times. <bookmark mark='a'/> Here is the spread "
            "of the simple estimate across samples: centred on the truth, but wide, with a typical error of "
            f"{M['naive']['rmse']:.2f}. <bookmark mark='b'/> And indirect inference: centred on the truth too, and "
            f"about half as wide, a typical error of {M['ii']['rmse']:.2f}. <bookmark mark='c'/> The first "
            "autocorrelation uses one feature of the data; the lens uses three, and the simulations translate "
            "them back into the parameter. Choosing a good lens is choosing which features of the data the "
            "estimate listens to, the same question the Play it asked."
        ) as vo:
            self.play(FadeIn(ax), Create(tl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(hn), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(hi), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
