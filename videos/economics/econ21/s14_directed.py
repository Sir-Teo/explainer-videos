from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Directed(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Directed technical change", r"Why did the wage premium for college rise just as college "
             r"graduates became plentiful?", "Chapter twelve. Directed technical change.",
             lit={1992: r"Katz and Murphy", 2002: r"Acemoglu"}, scale=("market", "nation"), horizon=("decades",))
        self.puzzle()
        self.model()
        self.curves()

    def puzzle(self):
        rows = VGroup(
            label(r"in America, \ the share of workers with college degrees rose steeply after 1960", font_size=24,
                  color=SKILL),
            label(r"supply and demand: \ the premium they earn should have fallen", font_size=24, color=GREY_A),
            label(r"it rose, \ sharply, \ from about 1980", font_size=26, color=WEDGE),
            label(r"the usual answer: \ skill-biased technical change", font_size=24, color=E.ACCENT),
            label(r"the deeper question: \ why was technology biased toward skill?", font_size=24, color=IDEA),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Katz and Murphy, QJE 107(1) (1992); \ Acemoglu, REStud 69(4) (2002)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Ideas also have a direction. <bookmark mark='a'/> In America, the share of workers with college degrees "
            "rose steeply from the 1960s. <bookmark mark='b'/> More supply should have lowered the premium they "
            "earn. <bookmark mark='c'/> Instead it rose sharply from about 1980, as Lawrence Katz and Kevin Murphy "
            "documented. <bookmark mark='d'/> The usual answer is skill-biased technical change: new technologies "
            "raised the demand for skill faster than supply grew. <bookmark mark='e'/> Daron Acemoglu asked the "
            "deeper question: why did inventors aim their ideas at skilled workers?"
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def model(self):
        rows = VGroup(
            MathTex(r"\frac{w_H}{w_L} = \Big(\frac{N_H}{N_L}\Big)^{\frac{\sigma-1}{\sigma}}\Big(\frac{H}{L}\Big)^"
                    r"{-\frac{1}{\sigma}}", font_size=46),
            label(r"technology fixed: \ more skilled workers lower their premium", font_size=22, color=GREY_A),
            label(r"price effect: \ invent for the scarce factor, \ whose products are dear", font_size=22,
                  color=WEDGE),
            label(r"market-size effect: \ invent for the abundant factor, \ which has more users", font_size=22,
                  color=SKILL),
            MathTex(r"\frac{N_H}{N_L} \propto \Big(\frac{H}{L}\Big)^{\sigma-1} \;\Rightarrow\; \frac{w_H}{w_L} "
                    r"\propto \Big(\frac{H}{L}\Big)^{\sigma-2}", font_size=42, color=E.ACCENT),
            label(r"if $\sigma > 2$, \ the market-size effect wins: \ more skills, \ a higher premium, \ in the long run",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        with self.voiceover(
            "Acemoglu's model has two kinds of workers, skilled H and unskilled L, and two kinds of technology, "
            "N H and N L. <bookmark mark='a'/> The skill premium rises with the relative productivity of skilled "
            "work and falls with the relative number of skilled workers. With technology fixed, more skilled "
            "workers lower their premium. <bookmark mark='b'/> But technology is invented for profit, and two "
            "forces pull. The price effect: invent for the scarce factor, whose products are dear. "
            "<bookmark mark='c'/> The market-size effect: invent for the abundant factor, which has more users to "
            "sell to. <bookmark mark='d'/> When inventors respond, relative technology rises with relative supply "
            "to the power sigma minus one, and the premium moves with relative supply to the power sigma minus "
            "two. <bookmark mark='e'/> If the elasticity of substitution between the two kinds of work is above "
            "two, more skilled workers raise the premium in the long run: supply creates its own demand."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            for mk, r in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def curves(self):
        d = load("directed")
        ax = plane([np.log(0.5), np.log(2.0)], [np.log(0.4), np.log(2.5)], center=LEFT * 1.6 + DOWN * 0.4,
                   x_length=8.0, y_length=4.8, xticks=[np.log(v) for v in (0.5, 1, 2)],
                   yticks=[np.log(v) for v in (0.5, 1, 2)], xlabel=r"relative supply of skill, \ $H/L$ \ (log)",
                   ylabel=r"skill premium \ (log)", xfmt=lambda v: f"{np.exp(v):g}", yfmt=lambda v: f"{np.exp(v):g}",
                   font_size=16)
        lo, hi = d["1.4"], d["3"]
        x = np.log(lo["ratio"])
        s1 = path(ax, x, np.log(lo["short"]), color=GREY_B, width=3)
        l1 = path(ax, x, np.log(lo["long"]), color=SKILL, width=4)
        l3 = path(ax, x, np.log(hi["long"]), color=E.ACCENT, width=4)
        side = VGroup(
            label(r"technology fixed, \ $\sigma = 1.4$: \ slope $-0.71$", font_size=19, color=GREY_B),
            label(rf"technology responds, \ $\sigma = 1.4$: \ slope ${lo['long_slope']:+.1f}$", font_size=19,
                  color=SKILL),
            label(rf"technology responds, \ $\sigma = 3$: \ slope ${hi['long_slope']:+.1f}$", font_size=19,
                  color=E.ACCENT),
            label(r"estimates of $\sigma$ for college \\ and non-college work: \ about 1.4 \\ (Katz and Murphy)",
                  font_size=19, color=HOLD),
            label(r"so the simple model needs help: \\ the bias builds on itself over time", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Agora draws the three cases. <bookmark mark='a'/> With technology fixed and sigma at 1.4, the premium "
            "falls steeply as skills become more plentiful. <bookmark mark='b'/> Let technology respond, and it "
            "falls less steeply. <bookmark mark='c'/> With sigma at three, the curve turns up: more skill, a higher "
            "premium. <bookmark mark='d'/> But the best estimates of sigma for college and non-college workers, "
            "starting with Katz and Murphy's, are about 1.4. So in its simplest form the model cannot produce a "
            "rising premium. Acemoglu's richer versions let the bias build on itself, as each skill-biased idea "
            "makes the next one easier to find. The direction of invention, like its rate, responds to profit."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(s1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(l3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()
