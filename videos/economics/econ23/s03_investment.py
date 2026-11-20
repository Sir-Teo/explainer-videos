from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Investment(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Investment: \ the user cost and Tobin's q", r"How much should a firm invest, \ and how fast?",
             "Chapter two. Investment: the user cost and Tobin's q.",
             lit={1963: r"Jorgenson", 1969: r"Tobin", 1982: r"Hayashi"}, scale=("firm", "nation"),
             horizon=("a year", "decades"))
        self.user_cost()
        self.q()
        self.path()

    def user_cost(self):
        f = load("firm")
        rows = VGroup(
            label(r"Dale Jorgenson, \ 1963: \ what does it cost to use a machine for a year?", font_size=25,
                  color=E.ACCENT),
            MathTex(r"c \;=\; p_K\,\big(r + \delta - \pi_K\big)\,\frac{1 - \tau z}{1 - \tau}", font_size=48,
                    color=FIRM),
            label(r"interest forgone, \ wear and tear, \ less any rise in the machine's price; \ adjusted for tax",
                  font_size=22, color=GREY_A),
            label(r"invest until the marginal product of capital equals its user cost", font_size=24, color=WHITE),
            label(rf"the island's firm: \ $r = {pc(f['r'], 0)}$, \ $\delta = {pc(f['delta'], 0)}$: \ "
                  rf"$c = {f['user_cost']:.2f}$ a year per unit", font_size=22, color=FIRM),
            label(r"a lower interest rate or a tax break lowers $c$, \ and raises the capital a firm wants", font_size=23,
                  color=STOCK),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Jorgenson, AER 53(2) (1963); \ Hall and Jorgenson, AER 57(3) (1967)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Now the firm, and what gets built. <bookmark mark='a'/> In 1963 Dale Jorgenson asked what it costs to use "
            "a machine for a year, even if you own it. <bookmark mark='b'/> The interest you could have earned on "
            "its price, plus the wear and tear, less any rise in what the machine will sell for; and the tax code "
            "changes all three. <bookmark mark='c'/> A firm should add capital until one more unit adds as much to "
            "output as it costs to use. <bookmark mark='d'/> On the Island, with interest at five percent and "
            f"depreciation at eight, a unit of capital costs {f['user_cost']:.2f} a year. <bookmark mark='e'/> Lower "
            "the interest rate, or give the firm a tax break, and the user cost falls and the capital it wants rises. "
            "This is the channel through which interest rates move investment."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def q(self):
        rows = VGroup(
            label(r"James Tobin, \ 1969: \ compare what the market pays for capital with what it costs to build",
                  font_size=24, color=E.ACCENT),
            MathTex(r"q \;=\; \frac{\text{market value of the firm}}{\text{replacement cost of its capital}}",
                    font_size=44, color=FIRM),
            label(r"$q > 1$: \ building adds more value than it costs, \ so build; \ $q < 1$: \ do not", font_size=24,
                  color=WHITE),
            label(r"but building in a hurry costs extra: \ installing, \ training, \ disruption", font_size=23,
                  color=GREY_A),
            MathTex(r"\text{cost of } I \;=\; I + \frac{\phi}{2}\,\frac{I^2}{K} \quad\Longrightarrow\quad "
                    r"\frac{I}{K} = \frac{q - 1}{\phi}", font_size=40, color=STOCK),
            label(r"Fumio Hayashi, \ 1982: \ with constant returns, \ the $q$ that matters equals the $q$ one can "
                  r"measure", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Tobin, JMCB 1(1) (1969); \ Hayashi, Econometrica 50(1) (1982)", corner=DR, font_size=12)
        with self.voiceover(
            "James Tobin gave the same idea a market price. <bookmark mark='a'/> Divide what the stock market says a "
            "firm is worth by what it would cost to rebuild its capital. Call that q. <bookmark mark='b'/> If q is "
            "above one, a new machine adds more to the firm's value than it costs, so build. Below one, do not. "
            "<bookmark mark='c'/> Firms do not jump straight to the capital they want, because building fast is "
            "expensive: installation, training, disruption. <bookmark mark='d'/> If those adjustment costs rise "
            "with the square of investment, the investment rate is q minus one over phi: proportional to how far q "
            "is above one. <bookmark mark='e'/> And Fumio Hayashi showed in 1982 that under constant returns, the "
            "q that matters for the next machine equals the average q that a stock market reveals."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def path(self):
        f = load("firm")
        t = np.array(f["t"])
        a1 = plane([0, 40], [2.8, 4.1], center=LEFT * 3.3 + DOWN * 0.5, x_length=5.6, y_length=4.2,
                   xticks=[0, 10, 20, 30, 40], yticks=[3.0, 3.5, 4.0], xlabel=r"years", ylabel=r"capital $K$",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=15)
        a2 = plane([0, 40], [0.9, 1.6], center=RIGHT * 3.2 + DOWN * 0.5, x_length=5.6, y_length=4.2,
                   xticks=[0, 10, 20, 30, 40], yticks=[1.0, 1.2, 1.4, 1.6], xlabel=r"years", ylabel=r"Tobin's $q$",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=15)
        kline = path(a1, t, f["K"], color=FIRM, width=4)
        old = seg(a1, 0, f["K_old"], 40, f["K_old"], color=GREY_B, width=2, dashed=True)
        new = seg(a1, 0, f["K_new"], 40, f["K_new"], color=TRUTH_C, width=2, dashed=True)
        qline = path(a2, t, f["q"], color=STOCK, width=4)
        qss = seg(a2, 0, f["q_new"], 40, f["q_new"], color=GREY_B, width=2, dashed=True)
        head = label(rf"the island's firm: \ productivity rises {100 * (f['A1'] / f['A0'] - 1):.0f}\% \ "
                     rf"(adjustment cost $\phi = {f['phi']:g}$)", font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        notes = VGroup(
            label(rf"$q$ jumps to {f['q0']:.2f}", font_size=19, color=STOCK).next_to(a2.ax.c2p(2, f["q0"]), RIGHT,
                                                                                buff=0.1),
            label(rf"investment {pc(f['ik'][0], 0)} of capital \\ against {pc(f['delta'], 0)} wearing out",
                  font_size=17, color=FIRM).next_to(a1.ax.c2p(12, 3.2), RIGHT, buff=0.05),
            label(rf"capital climbs from {f['K_old']:.2f} to {f['K_new']:.2f}", font_size=17, color=TRUTH_C).next_to(
                a1.ax.c2p(10, f["K_new"]), DOWN, buff=0.12),
        )
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Agora runs Hayashi's firm on the Island. <bookmark mark='a'/> Productivity rises by a fifth for good, "
            "which is the same, for the firm, as a fall in the user cost. <bookmark mark='b'/> The stock market sees "
            f"it at once: q jumps to {f['q0']:.2f}. <bookmark mark='c'/> The firm invests "
            f"{100 * f['ik'][0]:.0f} percent of its capital in the first year, against the "
            f"{100 * f['delta']:.0f} percent that wears out. <bookmark mark='d'/> Capital climbs from "
            f"{f['K_old']:.2f} toward {f['K_new']:.2f} over the next decades, and as it does, q falls back toward "
            "its steady value. Investment is a flow toward a target, and q is the market's measure of how far "
            "there is to go."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(a2), FadeIn(old), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(new), FadeIn(qss))
            vo.wait_until("b")
            self.play(Create(qline), FadeIn(notes[0]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Create(kline), FadeIn(notes[2]), run_time=2.5)
        self.clear_scene()
