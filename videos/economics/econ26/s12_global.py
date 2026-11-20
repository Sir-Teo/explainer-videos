from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Global(VoiceoverScene):
    def construct(self):
        card(self, 10, r"One equilibrium after all: \ global games", r"Can the model say when a run will happen?",
             "Chapter ten. One equilibrium after all: global games.",
             lit={1998: r"Morris and Shin", 2005: r"Goldstein and Pauzner"}, scale=("market",), horizon=("a day",))
        self.problem()
        self.picture()
        self.marginal()
        self.tradeoff()

    def problem(self):
        rows = VGroup(
            label(r"two equilibria: \ the model says a run \emph{can} happen, \ not when", font_size=25,
                  color=GREY_A),
            label(r"Morris and Shin, \ 1998: \ give each player a slightly different view of the fundamentals",
                  font_size=23, color=E.ACCENT),
            label(r"the bank's strength $\theta$: \ it fails if the share withdrawing reaches $\theta$", font_size=23,
                  color=STAY),
            label(r"each depositor sees $x = \theta + \sigma\varepsilon$: \ the truth, \ plus a little private noise",
                  font_size=23, color=DEPOSIT),
            label(r"then there is only one equilibrium: \ withdraw if and only if your signal is below $x^*$",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Morris and Shin, \ AER 88(3) (1998): \ 587--597", corner=DR, font_size=12)
        with self.voiceover(
            "Diamond and Dybvig leave a hole. <bookmark mark='a'/> With two equilibria, the model says a run can "
            "happen, but not when, or how likely it is. <bookmark mark='b'/> In 1998, Stephen Morris and Hyun Song "
            "Shin found a way to close it, first for currency attacks. Give each player a slightly different view of "
            "the fundamentals. <bookmark mark='c'/> Say the bank has a strength theta, and fails if the share of "
            "depositors withdrawing reaches theta. <bookmark mark='d'/> Each depositor sees theta plus a little "
            "private noise. Nobody knows exactly what the others see. <bookmark mark='e'/> Then, however small the "
            "noise, there is only one equilibrium: withdraw if and only if your signal is below a cutoff."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def picture(self):
        g = load("gg")
        b = g["base"]
        ax = plane([0, 1], [0, 1.05], center=LEFT * 2.3 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1],
                   xlabel=r"the bank's strength $\theta$", ylabel=r"share of depositors withdrawing",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        diag = seg(ax, 0, 0, 1, 1, color=GREY_B, width=2, dashed=True)
        share = path(ax, b["theta"], b["share"], color=RUN, width=4, smooth=False)
        ts = b["theta_star"]
        zone = Polygon(ax.ax.c2p(0, 0), ax.ax.c2p(ts, 0), ax.ax.c2p(ts, 1.05), ax.ax.c2p(0, 1.05), stroke_width=0,
                       fill_color=RUN, fill_opacity=0.12)
        vline = seg(ax, ts, 0, ts, 1.05, color=STAY, width=3)
        side = VGroup(
            label(r"dashed: \ share $= \theta$; \\ above it, \ the bank fails", font_size=20, color=GREY_B),
            label(rf"withdraw $c = {g['c']:.0f}$; \\ stay: \ $R = {g['R']:.0f}$ if it survives, \ 0 if not",
                  font_size=20, color=GREY_A),
            label(rf"red: \ the share withdrawing \\ in the unique equilibrium, \\ {g['n']:,} depositors, \ "
                  rf"$\sigma = {g['sigma']}$", font_size=20, color=RUN),
            label(rf"it fails exactly when \\ $\theta < \theta^* = c/R = {ts:.2f}$", font_size=22, color=STAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the Island's version. Across the bottom, the bank's strength. Up the side, the share of "
            "depositors who withdraw. <bookmark mark='a'/> The dashed line is where the share withdrawing equals "
            "the strength: above it, the bank fails. <bookmark mark='b'/> A depositor who withdraws gets "
            f"{g['c']:.0f}. One who stays gets {g['R']:.0f} if the bank survives and nothing if it fails. "
            f"<bookmark mark='c'/> In red, the share withdrawing in the unique equilibrium, simulated with "
            f"{g['n']:,} depositors. When the bank is weak, almost everyone runs; when it is strong, almost nobody "
            f"does; the switch is sharp. <bookmark mark='d'/> And the bank fails exactly when its strength is below "
            f"{ts:.1f}, the ratio of what withdrawing pays to what staying pays. A bank that would have survived if "
            "everyone stayed still fails, if it is weak enough: the run is real, but it is now predictable."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(diag), run_time=1)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(share), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(zone), Create(vline), FadeIn(side[3]))
        self.clear_scene()

    def marginal(self):
        g = load("gg")
        rows = VGroup(
            label(r"why $\theta^* = c/R$: \ think like the depositor at the cutoff", font_size=26, color=E.ACCENT),
            MathTex(r"R \cdot \Pr(\text{survive} \mid x^*) = c", font_size=40, color=WHITE),
            label(r"at the cutoff, \ you have no idea whether you are high or low in the crowd: \ every share of "
                  r"others below you is equally likely", font_size=21, color=GREY_A),
            MathTex(r"\Pr(\text{survive} \mid x^*) = \theta^* \;\Rightarrow\; \theta^* = \frac{c}{R} = "
                    rf"\frac{{{g['c']:.0f}}}{{{g['R']:.0f}}}", font_size=40, color=STAY),
            label(r"the noise only has to exist: \ its size $\sigma$ drops out", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        with self.voiceover(
            "Why that ratio? <bookmark mark='a'/> Put yourself at the cutoff. You are indifferent: staying pays R "
            "times the chance the bank survives, and that must equal c. <bookmark mark='b'/> At the cutoff you "
            "cannot tell whether your signal is high or low compared with everyone else's, so every share of "
            "depositors below you is equally likely. Morris and Shin call this belief Laplacian. "
            "<bookmark mark='c'/> The bank survives if its strength exceeds the share withdrawing, so your chance "
            "of survival is theta star itself, and theta star is c over R. <bookmark mark='d'/> The noise only "
            "has to be there; how large it is drops out of the answer."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            for mk, r_ in zip("bcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def tradeoff(self):
        g = load("gg")
        b, gen = g["base"], g["generous"]
        ax = plane([0, 1], [0, 1.05], center=LEFT * 2.3 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1],
                   xlabel=r"the bank's strength $\theta$", ylabel=r"share of depositors withdrawing",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=16)
        diag = seg(ax, 0, 0, 1, 1, color=GREY_B, width=2, dashed=True)
        s0 = path(ax, b["theta"], b["share"], color=RUN, width=4, smooth=False)
        s1 = path(ax, gen["theta"], gen["share"], color=STAY, width=4, smooth=False)
        band = Polygon(ax.ax.c2p(b["theta_star"], 0), ax.ax.c2p(gen["theta_star"], 0),
                       ax.ax.c2p(gen["theta_star"], 1.05), ax.ax.c2p(b["theta_star"], 1.05), stroke_width=0,
                       fill_color=STAY, fill_opacity=0.18)
        side = VGroup(
            label(rf"a deposit paying {g['c']:.0f} on demand: \\ fails below {b['theta_star']:.1f}", font_size=20,
                  color=RUN),
            label(rf"a more generous deposit, \ {g['c_generous']:.1f}: \\ fails below {gen['theta_star']:.1f}",
                  font_size=20, color=STAY),
            label(r"more insurance for the impatient \\ means more runs", font_size=21, color=E.ACCENT),
            label(r"Goldstein and Pauzner, \ 2005: \\ the best contract weighs the two", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Goldstein and Pauzner, \ J.\ Finance 60(3) (2005): \ 1293--1327", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The unique equilibrium lets us ask a question the old model could not. <bookmark mark='a'/> With a "
            f"deposit that pays {g['c']:.0f} on demand, the bank fails when its strength is below "
            f"{b['theta_star']:.1f}. <bookmark mark='b'/> Make the deposit more generous to people who withdraw "
            f"early, {g['c_generous']:.1f} instead of {g['c']:.0f}, and it fails below {gen['theta_star']:.1f}. "
            "The yellow band is the extra failures. <bookmark mark='c'/> Better insurance for the impatient makes "
            "running more attractive, so runs become more likely. <bookmark mark='d'/> Itay Goldstein and Ady "
            "Pauzner worked this out for Diamond and Dybvig's bank in 2005: the best deposit contract trades risk "
            "sharing against the probability of a run, and it offers less than the contract that ignores runs."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(diag), Create(s0), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(s1), FadeIn(band), FadeIn(side[1]), run_time=1.5)
            for mk, r_ in zip("cd", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
