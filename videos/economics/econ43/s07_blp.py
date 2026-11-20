from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class BLP(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Random coefficients, \ derived", r"How do you let different buyers want different things?",
             "Chapter six. Random coefficients, derived.", lit={1995: r"Berry, \ Levinsohn and Pakes"},
             scale=("market",), horizon=("a year",))
        self.idea()
        self.integral()
        self.contraction()
        self.moments()
        self.instruments()

    def idea(self):
        eq = MathTex(r"u_{ij} \;=\; \delta_j \;+\;", r"\sigma\,\nu_i\, p_j", r"\;+\; \varepsilon_{ij}, \qquad",
                     r"\delta_j = x_j\beta - \alpha p_j + \xi_j", font_size=42).move_to(UP * 1.9)
        eq[1].set_color(BLP_C)
        eq[3].set_color(GREY_A)
        T = TRUTH["cars"]
        al = T["alpha"]
        sg = T["sigma"]
        ax = plane([0.0, 1.2], [0, 1.0], center=DOWN * 1.2 + LEFT * 2.0, x_length=6.4, y_length=2.6,
                   xticks=[0, 0.3, 0.6, 0.9, 1.2], yticks=[0, 0.5, 1.0], xlabel=r"price sensitivity, \ $\alpha_i$",
                   ylabel=r"share of buyers", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        xs = np.linspace(0.0, 1.2, 120)
        dens = np.exp(-0.5 * ((xs - al) / sg) ** 2)
        curve = path(ax, xs, dens, BLP_C, 3.0)
        mean = vline(ax, al, 0, 1.0, PRICE)
        side = VGroup(
            label(r"each buyer $i$ has \\ their own price sensitivity: \\ $\alpha_i = \alpha - \sigma\nu_i$",
                  font_size=19, color=BLP_C),
            label(rf"on the Island: \ mean {al}, \\ spread {sg}", font_size=19, color=PRICE),
            label(r"in BLP's cars: \ random \\ tastes for size, \ power, \\ air conditioning \ldots", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.8)
        tag = published_tag(tables.BLP_1995.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1995 Berry, Levinsohn and Pakes let different buyers want different things. "
            "<bookmark mark='a'/> Add to each buyer's utility a term that varies across buyers: here, a buyer's own "
            "sensitivity to price, the average alpha less sigma times a random draw nu for that buyer. "
            f"<bookmark mark='b'/> On the Island's car market, sensitivity averages {al} with a spread of {sg}. "
            "<bookmark mark='c'/> In their own study of cars, buyers also differ in how much they value size, power "
            "and air conditioning. The consequence is the point of the whole method. A buyer who chose an expensive "
            "car is, on average, a buyer who does not mind high prices, so when its price rises that buyer moves to "
            "another expensive car, not to the cheapest. Substitution follows similarity, without the economist "
            "drawing any nests."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(ax), Create(curve), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def integral(self):
        eq = MathTex(r"s_j(\delta, \sigma) \;=\; \int \frac{e^{\delta_j + \sigma \nu p_j}}"
                     r"{1 + \sum_k e^{\delta_k + \sigma \nu p_k}}\; dF(\nu) \;\approx\; \frac{1}{R}\sum_{r=1}^{R} "
                     r"s_{rj}", font_size=38, color=E.ACCENT).to_edge(UP, buff=0.7)
        cols = (DEMAND, PRICE, IV_C, GAIN)
        rows = VGroup()
        probs = []
        quality = np.array([0.5, 1.2, 1.9, 2.6])     # dearer cars are better
        price = np.array([1.0, 2.0, 3.0, 4.0])
        for r in range(5):
            u = quality - (0.3 + 0.35 * r) * price     # buyer 1 cares least about price, buyer 5 most
            e = np.exp(u)
            p = e / (1 + e.sum())
            probs.append(p)
            bars = VGroup(*[Rectangle(width=max(p[k] * 7, 0.02), height=0.3, stroke_width=0, fill_color=cols[k],
                                      fill_opacity=0.85) for k in range(4)]).arrange(RIGHT, buff=0.0)
            bars.move_to(np.array([0, 1.2 - 0.55 * r, 0]), aligned_edge=LEFT).shift(LEFT * 1.5)
            rows.add(VGroup(label(rf"buyer {r + 1}", font_size=17, color=GREY_A).next_to(bars, LEFT, buff=0.25),
                            bars))
        avg = np.mean(probs, axis=0)
        mb = VGroup(*[Rectangle(width=max(avg[k] * 7, 0.02), height=0.36, stroke_width=0, fill_color=cols[k],
                                fill_opacity=1.0) for k in range(4)]).arrange(RIGHT, buff=0.0)
        mb.move_to(np.array([0, -1.75, 0]), aligned_edge=LEFT).shift(LEFT * 1.5)
        ml = label(r"the market", font_size=18, color=WHITE).next_to(mb, LEFT, buff=0.25)
        key = VGroup(*[label(t, font_size=16, color=c) for t, c in zip((r"car 1 \ (cheap)", r"car 2", r"car 3",
                                                                        r"car 4 \ (dear)"), cols)]).arrange(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.45)
        line = Line(LEFT * 3.5, RIGHT * 5.5, stroke_width=1.2, color=GREY_B).move_to(DOWN * 1.3)
        foot = label(r"no closed form: \ draw $R$ buyers, \ compute each one's logit, \ average", font_size=20,
                     color=GREY_A).next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "What does this do to market shares? <bookmark mark='a'/> Each buyer still makes a logit choice, but "
            "with their own sensitivity, so each has their own probabilities of buying each car. "
            "<bookmark mark='b'/> Here are five buyers, from the least sensitive to price at the top to the most "
            "sensitive at the bottom: the first leans to the dear car, the last to the cheap one, or to buying "
            "nothing, the empty end of each bar. "
            "<bookmark mark='c'/> The market's share of each car is the average over all buyers: an integral over "
            "the distribution of tastes. It has no formula, so it is computed by simulation: draw a few hundred "
            "buyers, compute each one's logit probabilities, and average."
        ) as vo:
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(key), FadeIn(foot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(line), FadeIn(ml), *[TransformFromCopy(VGroup(*[r_[1][k] for r_ in rows]), mb[k])
                                                  for k in range(4)], run_time=1.6)
        self.clear_scene()

    def contraction(self):
        Cn = load("contraction")
        steps = np.log10(np.maximum(np.array(Cn["steps"]), 1e-16))
        it = np.arange(1, len(steps) + 1)
        ax = plane([0, 30], [-16, 1], center=LEFT * 1.8 + DOWN * 0.5, x_length=8.0, y_length=4.4,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, -4, -8, -12, -16], xlabel=r"iteration",
                   ylabel=r"largest change in $\delta$ \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"10^{{{v:.0f}}}", font_size=14)
        keep = it <= 30
        ln = path(ax, it[keep], steps[keep], BLP_C, 3.2, smooth=False)
        dts = VGroup(*[dot(ax, x, y, BLP_C, 0.05) for x, y in zip(it[keep], steps[keep])])
        eq = MathTex(r"\delta^{\,t+1} \;=\; \delta^{\,t} \;+\; \ln s^{\text{data}} \;-\; \ln s(\delta^{\,t}, \sigma)",
                     font_size=38, color=E.ACCENT).to_edge(UP, buff=0.45)
        side = VGroup(
            label(r"start: \ the plain logit's \\ answer, \ $\ln s_j - \ln s_0$", font_size=18, color=GREY_A),
            label(r"each step shrinks \\ the error by a \\ constant factor", font_size=18, color=BLP_C),
            label(rf"error against the \\ planted $\delta$: \ {Cn['err_start']:.1f} \\ $\to$ "
                  r"less than $10^{-14}$", font_size=18, color=TRUTH_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the hard part. The plain logit could be inverted by taking logs. With random coefficients, for any "
            "guess of sigma we need the mean utilities, delta, that make the predicted shares equal the observed "
            "ones, for every product at once. <bookmark mark='a'/> Berry proved that a simple rule finds them: add "
            "to each delta the log of its observed share minus the log of the share the current deltas predict, "
            "and repeat. The rule is a contraction, so it converges from any start. <bookmark mark='b'/> In one "
            "year of the Island's car market, starting from the plain logit's answer, each step shrinks the error "
            "by about the same factor. <bookmark mark='c'/> After thirty steps the deltas match the ones planted in "
            "the simulation to the last digit a computer keeps."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.5)
            self.play(Create(ln), LaggedStart(*[FadeIn(d) for d in dts], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("a")
            self.play(Indicate(eq, color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def moments(self):
        steps = flow_chain([(r"guess $\sigma$", BLP_C), (r"invert shares", E.ACCENT), (r"linear IV", IV_C),
                            (r"check moments", PRICE)],
                           notes=[r"how much \\ tastes differ", r"the contraction \\ gives $\delta(\sigma)$",
                                  r"$\delta = x\beta - \alpha p + \xi$ \\ gives $\xi(\sigma)$",
                                  r"$\frac{1}{N}\sum_j z_j\,\xi_j(\sigma) \approx 0$?"],
                           box_w=2.7, font_size=20, note_size=16).move_to(UP * 0.8)
        loop = CurvedArrow(steps.boxes[3].get_bottom() + DOWN * 1.05, steps.boxes[0].get_bottom() + DOWN * 1.05,
                           angle=-TAU / 6, color=GREY_B, stroke_width=2.2)
        lab = label(r"not yet: \ a new $\sigma$, \ and again", font_size=18, color=GREY_B).next_to(loop, DOWN,
                                                                                                  buff=0.1)
        eq = MathTex(r"\hat\sigma = \arg\min_\sigma\; \xi(\sigma)'\,Z\,W\,Z'\,\xi(\sigma)", font_size=38,
                     color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.BLP_1995.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The whole estimator is a loop. <bookmark mark='a'/> Guess how much tastes differ, sigma. "
            "<bookmark mark='b'/> Invert the observed shares by the contraction, which gives the mean utilities "
            "for that sigma. <bookmark mark='c'/> Because the mean utilities are linear in price and "
            "characteristics, a linear instrumental-variables regression gives alpha and beta, and what is left "
            "over is the unseen quality, xi. <bookmark mark='d'/> Then check the moment conditions: the unseen "
            "quality should be uncorrelated with the instruments. <bookmark mark='e'/> If it is not, try another "
            "sigma. <bookmark mark='f'/> The estimate is the sigma that makes the moments closest to zero, the "
            "generalized method of moments. On a modern computer each pass through the loop takes a fraction of a "
            "second."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(3), "bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("e")
            self.play(Create(loop), FadeIn(lab))
            vo.wait_until("f")
            self.play(Write(eq))
        self.clear_scene()

    def instruments(self):
        cards = point_cards([
            (r"rivals' characteristics", r"a car with many close \\ rivals must be priced \\ low; \ their features "
                                         r"\\ are set years ahead", DEMAND),
            (r"the firm's other cars", r"a firm prices each car \\ knowing it competes \\ with its own others",
             PRICE),
            (r"cost shifters", r"input prices that move \\ cost but not quality", GAIN),
            (r"differentiation", r"how crowded a \\ product's neighbourhood \\ is \ (Gandhi and Houde)", BLP_C),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.1)
        head = label(r"instruments: \ what moves price but not unseen quality?", font_size=27,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"the assumption: \ characteristics are chosen before the unseen quality is known", font_size=20,
                     color=HOLD).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.BLP_1995.tag + r"; \ " + tables.FRONTIER43.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Which instruments? <bookmark mark='a'/> Berry, Levinsohn and Pakes used the characteristics of rival "
            "products. A car surrounded by close rivals must be priced lower, and its rivals' features were fixed "
            "years before, when the models were designed. <bookmark mark='b'/> They also used the characteristics "
            "of the firm's own other models, which it takes into account when pricing each one. "
            "<bookmark mark='c'/> Cost shifters, such as the price of inputs, move price without touching quality. "
            "<bookmark mark='d'/> And Amit Gandhi and Jean-François Houde later showed that measures of how crowded "
            "a product's neighbourhood is in characteristics space are stronger still. <bookmark mark='e'/> All of "
            "them rest on one assumption: that characteristics are chosen before the unseen quality shocks are "
            "known."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
