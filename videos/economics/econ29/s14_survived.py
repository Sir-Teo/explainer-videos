from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Survived(VoiceoverScene):
    def construct(self):
        card(self, 12, r"What survived", r"If the claim was wrong, \ why did the method win?", "Chapter twelve. What "
             "survived.", lit={2004: r"the Nobel", 2006: r"Beaudry and Portier", 2007: r"Chari, \ Kehoe, \ "
                                                                                     r"McGrattan"},
             scale=("nation",), horizon=("a quarter", "a decade"))
        self.method()
        self.wedges()
        self.labour_wedge()
        self.others()

    def method(self):
        rows = VGroup(
            label(r"what the real business cycle left behind", font_size=27, color=E.ACCENT),
            label(r"households and firms that optimize, \ looking ahead", font_size=22, color=VALUE),
            label(r"the whole economy in equilibrium at once, \ shocks and all", font_size=22, color=OUTPUT),
            label(r"solve it on a computer; \ simulate it; \ compare its moments and responses with the data",
                  font_size=22, color=TECH),
            label(r"add frictions where the data demand them: \ sticky prices, \ money, \ credit, \ search",
                  font_size=22, color=INVEST),
            label(r"the result has a name: \ dynamic stochastic general equilibrium, \ DSGE", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kydland and Prescott, \ Nobel Prize in Economic Sciences, \ 2004", corner=DR,
                            font_size=12)
        with self.voiceover(
            "So why did the method win? <bookmark mark='a'/> Because of what it left behind. "
            "<bookmark mark='b'/> Households and firms that optimize and look ahead, so that their behaviour does "
            "not change arbitrarily when policy does: Lucas's critique, answered. <bookmark mark='c'/> The whole "
            "economy solved at once, in equilibrium, with shocks inside. <bookmark mark='d'/> A computer to solve "
            "it, and the habit of comparing a model's simulated moments and impulse responses with the data's. "
            "<bookmark mark='e'/> And a place to put frictions when the data demand them: sticky prices, money, "
            "credit, search. <bookmark mark='f'/> The result is called a dynamic stochastic general equilibrium "
            "model, and every central bank runs one. Kydland and Prescott shared the Nobel Prize in 2004, for "
            "this and for their work on time consistency."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def wedges(self):
        items = VGroup(
            label(r"Chari, \ Kehoe and McGrattan, \ 2007: \ business cycle accounting", font_size=25,
                  color=E.ACCENT),
            label(r"keep the growth model; \ let four `wedges' absorb everything it gets wrong", font_size=22,
                  color=GREY_A),
            label(r"efficiency: \ output from inputs \ (the Solow residual)", font_size=22, color=TECH),
            label(r"labour: \ a gap between what an hour is worth to workers and to firms", font_size=22,
                  color=HOURS),
            label(r"investment: \ a gap between saving and the return on capital", font_size=22, color=INVEST),
            label(r"government: \ spending and net exports", font_size=22, color=GREY_B),
            label(r"then ask which wedge made each recession; \ each points to the friction a model needs",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Chari, \ Kehoe and McGrattan, \ \emph{Econometrica} 75(3) (2007)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The model also became a measuring instrument. <bookmark mark='a'/> In 2007, V. V. Chari, Patrick "
            "Kehoe and Ellen McGrattan proposed business cycle accounting. <bookmark mark='b'/> Keep the growth "
            "model, and let four wedges absorb everything it gets wrong. <bookmark mark='c'/> An efficiency wedge: "
            "how much output comes from given inputs. <bookmark mark='d'/> A labour wedge: a gap between what an "
            "hour is worth to the worker and to the firm, like a tax on work. <bookmark mark='e'/> An investment "
            "wedge: a gap between what savers want and what capital returns. <bookmark mark='f'/> And government "
            "spending. <bookmark mark='g'/> Measure the wedges from the data, feed them back one at a time, and see "
            "which one made each recession. Each wedge points to the kind of friction a better model needs."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(tag))
            for mk, r_ in zip("abcdefg", items[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def labour_wedge(self):
        W = load("wedges")
        t = np.array(W["t"])
        ax = plane([1947, 2020.5], [-6, 6], center=LEFT * 1.9 + DOWN * 0.45, x_length=8.8, y_length=4.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[-6, -3, 0, 3, 6], ylabel=r"\% from trend",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        rec = shade(ax, W["recessions"], -6, 6)
        zero = seg(ax, 1947, 0, 2020.5, 0, GREY_D, 1.5)
        y = path(ax, t, W["y"], OUTPUT, 2, smooth=False, yr=(-6, 6))
        lw = path(ax, t, W["labour"], HOURS, 2.5, smooth=False, yr=(-6, 6))
        eq = MathTex(r"1 - \tau_t = \frac{A\, c_t}{(1-\alpha)\, y_t / n_t}", font_size=30).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"the wage a worker would need \\ over what an hour produces", font_size=18, color=GREY_A),
            label(r"pink: \ the labour wedge $\tau$", font_size=19, color=HOURS),
            label(r"green: \ output", font_size=19, color=OUTPUT),
            label(rf"correlation {W['corr']:.2f}: \ in every \\ recession it is as if \\ a tax on work rose",
                  font_size=19, color=E.ACCENT),
            label(r"the friction is in the \\ labour market: \ Parts 24 \\ and 30 build candidates", font_size=19,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"BEA and BLS via FRED, \ this film's wedge; \ Shimer, \ \emph{AEJ: Macro} 1(1) (2009)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Here is the labour wedge, computed in this film from three American series. <bookmark mark='a'/> It "
            "compares what an hour is worth to a worker in this model, set by consumption, with what an hour "
            "produces. If labour markets worked as the model says, the two would be equal, and the wedge would be "
            "zero. <bookmark mark='b'/> In pink, the wedge's gap from trend. <bookmark mark='c'/> In green, "
            f"output's. <bookmark mark='d'/> They move against each other, with a correlation of "
            f"{say_num(W['corr'])}. In every recession it is as if a tax on work suddenly rose. Robert Shimer set "
            "it out in 2009 as a challenge for every theory of the labour market. <bookmark mark='e'/> Wherever "
            "that friction lives, in wages that do not adjust or in the slow search of Part twenty-four, the growth "
            "model alone does not have it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rec), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lw), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(y), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def others(self):
        cards = point_cards([
            (r"news shocks", r"Beaudry and Portier, \ 2006: \ stock prices \\ jump on news of future \\ "
                             r"technology, \ and spending \\ moves before it arrives", INVEST),
            (r"uncertainty shocks", r"Bloom, \ 2009: \ when uncertainty \\ jumps, \ firms pause hiring \\ and "
                                    r"investing, \ then rebound", TECH),
            (r"investment shocks", r"shocks to how cheaply \\ saving becomes capital: \\ in estimated models, "
                                   r"\\ a large share of the cycle", OUTPUT),
            (r"the lesson", r"many shocks, \ many frictions, \\ one framework to \\ put them in", E.ACCENT),
        ], width=12.8, cols=2, font_size=21).move_to(DOWN * 0.1)
        tag = published_tag(r"Beaudry and Portier, \ \emph{AER} 96(4) (2006); \ Bloom, \ \emph{Econometrica} 77(3) "
                            r"(2009); \ Justiniano, \ Primiceri and Tambalotti, \ \emph{JME} 57(2) (2010)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Other shocks joined technology. <bookmark mark='a'/> News: Paul Beaudry and Franck Portier showed in "
            "2006 that stock prices jump on news about technology years before it arrives, and spending moves at "
            "once, so a boom can begin on expectations alone. <bookmark mark='b'/> Uncertainty: Nicholas Bloom "
            "showed in 2009 that when uncertainty jumps, firms pause hiring and investing, then rebound once it "
            "passes. <bookmark mark='c'/> Investment shocks: changes in how cheaply saving turns into capital, "
            "which in estimated models account for a large share of the cycle. <bookmark mark='d'/> The lesson is "
            "not one shock but many, with frictions, inside the framework Kydland and Prescott built."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
