from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Lucas(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The Lucas tree and the stochastic discount factor", r"Where do the 0.8 and the 1.2 come from?",
             "Chapter six. The Lucas tree and the stochastic discount factor.", lit={1978: r"Lucas"},
             scale=("market", "nation"), horizon=("a year",))
        self.tree()
        self.sdf()
        self.riskfree()

    def tree(self):
        rows = VGroup(
            history_card(1978, r"Robert Lucas", r"\emph{Asset Prices in an Exchange Economy}, \ Econometrica",
                         color=STOCK, width=10.6, font_size=22),
            label(r"an economy of identical households and fruit trees; \ the fruit cannot be stored", font_size=24,
                  color=GREY_A),
            label(r"so in equilibrium everyone eats the fruit: \ consumption equals dividends", font_size=24,
                  color=CONS),
            label(r"prices must make people content to hold the trees, \ neither buying nor selling", font_size=24,
                  color=WHITE),
            label(r"that is the Euler equation of Part 7, \ applied to a share of a tree", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Lucas, Econometrica 46(6) (1978): \ 1429--1445", corner=DR, font_size=12)
        with self.voiceover(
            "In 1978 Robert Lucas built the economy that asset pricing still starts from. <bookmark mark='a'/> "
            "Identical households own fruit trees. The fruit falls each period, in a random amount, and cannot be "
            "stored. <bookmark mark='b'/> So in equilibrium everyone eats exactly what falls: consumption equals "
            "dividends. <bookmark mark='c'/> Prices cannot change what is eaten. They must instead make every "
            "household content to hold the trees it has, neither buying nor selling. <bookmark mark='d'/> That "
            "condition is Part seven's Euler equation, applied to a share in a tree."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def sdf(self):
        rows = VGroup(
            MathTex(r"p_t\,u'(c_t) \;=\; \beta\,\mathbb{E}_t\Big[u'(c_{t+1})\,\big(p_{t+1} + d_{t+1}\big)\Big]",
                    font_size=42),
            label(r"give up a share's price in marginal utility today; \ get its price and fruit tomorrow", font_size=22,
                  color=GREY_A),
            MathTex(r"p_t \;=\; \mathbb{E}_t\big[m_{t+1}\,x_{t+1}\big], \qquad m_{t+1} \;=\; \beta\,\frac{u'(c_{t+1})}"
                    r"{u'(c_t)}", font_size=44, color=SDF),
            label(r"$m$: \ the stochastic discount factor, \ high in bad times, \ low in good", font_size=24,
                  color=SDF),
            label(r"one formula prices every asset: \ trees, \ bonds, \ insurance, \ options", font_size=24,
                  color=E.ACCENT),
            label(r"the Island's 0.8 and 1.2 were $m$ in a good year and a bad one", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "Write it down. <bookmark mark='a'/> Buying a share costs its price, valued at today's marginal utility. "
            "It returns tomorrow's price plus the fruit, valued at tomorrow's marginal utility, discounted by beta. "
            "At the right price the two sides balance. <bookmark mark='b'/> Rearranged: today's price is the "
            "expected value of what the asset pays tomorrow, x, times a number m. <bookmark mark='c'/> m is the "
            "stochastic discount factor: beta times the ratio of marginal utilities. It is high in bad times, when "
            "consumption is low and an extra coconut is precious, and low in good times. <bookmark mark='d'/> This "
            "one formula prices every asset there is: trees, bonds, insurance, options. Only the payoff x changes. "
            "<bookmark mark='e'/> The Island's 0.8 and 1.2 in the game were m in a good year and in a bad one."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def riskfree(self):
        rows = VGroup(
            label(r"two consequences", font_size=28, color=E.ACCENT),
            MathTex(r"1 \;=\; \mathbb{E}[m]\,R_f \quad\Longrightarrow\quad R_f \;=\; \frac{1}{\mathbb{E}[m]}",
                    font_size=44, color=BILL),
            label(r"the safe rate is set by patience and expected growth", font_size=23, color=BILL),
            MathTex(r"\mathbb{E}[R] - R_f \;=\; -R_f\,\operatorname{cov}(m, R)", font_size=44, color=STOCK),
            label(r"an asset that pays when $m$ is low, \ in good times, \ must offer a premium; \ insurance pays "
                  r"less than safe", font_size=23, color=STOCK),
            label(r"risk is priced by its covariance with bad times, \ not by its variance", font_size=26,
                  color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Two consequences follow in a line each. <bookmark mark='a'/> A safe asset pays the same in every state, "
            "so its gross return is one over the expected discount factor. <bookmark mark='b'/> The safe rate is set "
            "by patience and by how fast consumption is expected to grow. <bookmark mark='c'/> For a risky asset, "
            "its expected excess return equals minus the safe return times the covariance of m with the asset's "
            "return. <bookmark mark='d'/> An asset that pays well when m is low, in good times, must offer a premium "
            "to be held. Insurance, which pays in bad times, can return less than a safe bond and still be bought. "
            "<bookmark mark='e'/> Risk is priced by its covariance with bad times, not by its variance. A share whose "
            "price jumps around for reasons unrelated to the economy carries no premium at all."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
