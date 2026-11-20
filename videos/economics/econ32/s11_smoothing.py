from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Smoothing(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Tax smoothing: \ why debt should absorb wars", r"How should a government pay for a war?",
             "Chapter nine. Tax smoothing: why debt should absorb wars.", lit={1979: r"Barro"}, scale=("nation",),
             horizon=("a year", "decades"))
        self.model()
        self.history()

    def model(self):
        W = load("war")
        t = np.array(W["t"])
        ax = plane([0, 50], [0, 0.6], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"years",
                   ylabel=r"share of output", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        ax2 = plane([0, 50], [-0.5, 1.0], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[0, 10, 20, 30, 40, 50], yticks=[-0.5, 0, 0.5, 1.0], xlabel=r"years",
                    ylabel=r"debt, \ share of output", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                    font_size=14)
        g = path(ax, t, W["g"], SPEND, 3.5, smooth=False)
        tau = seg(ax, 0, W["tau_smooth"], 50, W["tau_smooth"], TAX, 3.5)
        debt = path(ax2, list(range(len(W["debt"]))), W["debt"], DEBT, 3.5, smooth=False)
        zero2 = seg(ax2, 0, 0, 50, 0, GREY_C, 1.2)
        harm = MathTex(r"\text{harm} \propto \tau^{2}", font_size=34, color=TAX).move_to(ax.ax.c2p(33, 0.48))
        head = label(r"Barro, \ 1979: \ a tax's harm rises with the square of its rate", font_size=22,
                     color=E.ACCENT).to_edge(UP, buff=0.4)
        foot = label(rf"pay as you go: \ {100 * (W['ratio'] - 1):.0f}\% more deadweight loss than the smooth tax of "
                     rf"{100 * W['tau_smooth']:.1f}\%", font_size=20, color=WHITE).to_edge(DOWN, buff=0.45)
        k1 = label(r"teal: \ spending, \ a five-year war", font_size=16, color=SPEND).next_to(ax, UP, buff=0.1)
        k2 = label(r"gold: \ the smooth tax rate", font_size=16, color=TAX).next_to(k1, DOWN, buff=0.06)
        k3 = label(r"purple: \ the debt that absorbs the war", font_size=16, color=DEBT).next_to(ax2, UP, buff=0.1)
        tag = published_tag(r"Barro, \ \emph{JPE} 87(5) (1979); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "How should a government pay for a war? <bookmark mark='a'/> Robert Barro's answer, in 1979, starts "
            "from one fact of public finance: the harm a tax does, by discouraging work and saving, rises with the "
            "square of its rate. <bookmark mark='b'/> So suppose spending jumps from twenty to fifty percent of "
            "output for five years. Raising taxes to fifty percent for those years would be very costly. "
            f"<bookmark mark='c'/> Better to set a tax rate of {100 * W['tau_smooth']:.1f} percent, now and for "
            "ever, <bookmark mark='d'/> and let debt absorb the war and be paid down slowly afterwards. "
            "<bookmark mark='e'/> Paying as you go would cost the Island "
            f"{100 * (W['ratio'] - 1):.0f} percent more in lost output from taxes. Debt is a shock absorber."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ax), FadeIn(ax2), FadeIn(zero2), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(harm, scale=1.1))
            vo.wait_until("b")
            self.play(Create(g), FadeIn(k1), harm.animate.set_opacity(0.4), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(tau), FadeIn(k2))
            vo.wait_until("d")
            self.play(Create(debt), FadeIn(k3), run_time=1.8)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def history(self):
        W = load("war")
        t = np.array(W["us_t"])
        ax = plane([1910, 1961], [0, 125], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1910, 1920, 1930, 1940, 1950, 1960], yticks=[0, 25, 50, 75, 100, 125],
                   ylabel=r"federal debt held by the public, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        wars = shade(ax, [(1917.25, 1918.9), (1941.9, 1945.7)], 0, 125, INFL, 0.12)
        line = path(ax, t, W["us_debt"], DEBT, 3.2, smooth=False)
        side = VGroup(
            label(r"shaded: \ the United States at war", font_size=18, color=INFL),
            label(rf"1941: \ {W['d1941']:.0f}\%; \ 1946: \ {W['d1946']:.0f}\%", font_size=18, color=DEBT),
            label(rf"1960: \ {W['d1960']:.0f}\%, \\ with modest surpluses and fast growth", font_size=18,
                  color=OUTPUT),
            label(r"Britain financed the Napoleonic wars \\ the same way", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Ramey and Zubairy, \ replication data", corner=DR, font_size=12)
        with self.voiceover(
            "That is roughly how wars have been paid for. <bookmark mark='a'/> American debt rose in both World "
            f"Wars, <bookmark mark='b'/> from {W['d1941']:.0f} percent of GDP in 1941 to {W['d1946']:.0f} in 1946, "
            "<bookmark mark='c'/> and then fell for decades as the economy outgrew it, to "
            f"{W['d1960']:.0f} percent by 1960. <bookmark mark='d'/> Britain financed its wars against Napoleon the "
            "same way. Smoothing does not mean debt never matters; it means the time to reduce it is in "
            "peacetime and in good years."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(wars), run_time=0.6)
            self.play(Create(line), run_time=2.0)
            for mk, s_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()
