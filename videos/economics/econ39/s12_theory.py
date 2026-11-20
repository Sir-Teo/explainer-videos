from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Theory(VoiceoverScene):
    def construct(self):
        card(self, 10, r"Discrimination in theory", r"Can a competitive market sustain a pay gap?",
             "Chapter ten. Discrimination in theory.",
             lit={1957: r"Becker", 1972: r"Phelps", 1973: r"Arrow"}, scale=("firm", "market"),
             horizon=("a year", "a decade"))
        self.taste()
        self.marginal()
        self.statistical()

    def taste(self):
        T = load("theory")
        ex = T["example"]
        ds = np.array(ex["d_sorted"])
        n = len(ds)
        ax = plane([0, 1], [0, 0.6], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.2, 0.4, 0.6],
                   xlabel=r"employers, \ from least to most prejudiced", ylabel=r"taste for discrimination, \ $d$",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        xs = (np.arange(n) + 0.5) / n
        curve = path(ax, xs, ds, LOSS, 3.2, yr=(0, 0.6), smooth=False)
        cut = vline(ax, T["share_minority"], 0, 0.6, BLACK_N)
        cl = label(rf"minority workers: \\ {100 * T['share_minority']:.1f}\% of jobs", font_size=16,
                   color=BLACK_N).next_to(ax.ax.c2p(T["share_minority"], 0.6), RIGHT, buff=0.1)
        gp = dot(ax, T["share_minority"], ex["gap"], E.ACCENT, 0.09)
        side = VGroup(
            label(r"an employer with taste $d$ \\ acts as if a minority \\ worker cost $w_m(1+d)$", font_size=18,
                  color=WHITE),
            label(r"minority workers are hired \\ first by the least prejudiced", font_size=18, color=BLACK_N),
            label(rf"the market gap is the taste \\ of the marginal employer: \\ {100 * ex['gap']:.1f}\%",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1957 Gary Becker gave discrimination an economic model. Suppose some employers dislike hiring a "
            "minority group. <bookmark mark='a'/> An employer with a taste for discrimination d behaves as if a "
            "minority worker cost the wage times one plus d. <bookmark mark='b'/> Line up the Island's employers from "
            f"the least prejudiced to the most: here, only {say_pct(0.05, 0)} have no prejudice at all. "
            "<bookmark mark='c'/> Minority workers, an eighth of the labour force, are hired first by the least "
            "prejudiced employers, until all have jobs. <bookmark mark='d'/> The market wage gap is set by the last "
            "employer needed to hire them: the marginal employer's taste, here "
            f"{say_pct(ex['gap'], 1)}. The most prejudiced employers simply hire no minority workers at all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(curve), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Indicate(curve, color=WHITE))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(cl), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(gp, scale=1.5), FadeIn(side[2]))
        self.clear_scene()

    def marginal(self):
        T = load("theory")
        sh, gp = np.array(T["shares"]), np.array(T["gaps"])
        ax = plane([0, 0.3], [0, 0.025], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.01, 0.02],
                   xlabel=r"share of employers with no prejudice", ylabel=r"market wage gap",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, sh, gp, E.ACCENT, 3.4, smooth=False)
        cut = vline(ax, T["share_minority"], 0, 0.025, BLACK_N)
        side = VGroup(
            label(rf"once unprejudiced employers \\ can hire every minority \\ worker ({100 * T['share_minority']:.1f}"
                  r"\%), \ the gap is zero", font_size=18, color=WHITE),
            label(r"and prejudice costs profit: \\ competition should \\ erode it", font_size=18, color=GAIN),
            label(r"unless the taste is \\ customers' or co-workers', \\ or employers have \\ market power",
                  font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Becker's model makes a striking prediction. <bookmark mark='a'/> Raise the share of employers with no "
            "prejudice, and the market gap shrinks, <bookmark mark='b'/> reaching zero once the unprejudiced alone "
            "can hire every minority worker. The average employer's tastes do not matter; the marginal employer's "
            "do. <bookmark mark='c'/> Prejudice also costs the prejudiced: they pay more for the same work, so "
            "competition should let fair employers grow and push the others out. <bookmark mark='d'/> Discrimination "
            "can persist if the taste belongs to customers or co-workers, whom firms must please, or if employers "
            "have the wage-setting power of Part thirty-eight, which lets them pay groups differently without losing "
            "them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def statistical(self):
        T = load("theory")
        s = np.array(T["signal"])
        ax = plane([-3, 3], [-3, 3], center=LEFT * 2.2 + DOWN * 0.4, x_length=6.0, y_length=4.8,
                   xticks=[-2, 0, 2], yticks=[-2, 0, 2], xlabel=r"test score", ylabel=r"pay: \ expected productivity",
                   xfmt=lambda v: f"{v:+.0f}", yfmt=lambda v: f"{v:+.0f}", font_size=14)
        l0 = path(ax, s, T["pay0"], WHITE_N, 3.2, smooth=False)
        l1 = path(ax, s, T["pay1"], BLACK_N, 3.2, smooth=False)
        d45 = seg(ax, -3, -3, 3, 3, GREY_D, 1.5, dashed=True)
        p0, p1 = dot(ax, 2, T["pay0"][50], WHITE_N, 0.09), dot(ax, 2, T["pay1"][50], BLACK_N, 0.09)
        eq = MathTex(r"E[q \mid s] = (1-\lambda)\,\mu + \lambda\,s, \quad \lambda = "
                     r"\frac{\sigma_q^2}{\sigma_q^2 + \sigma_e^2}", font_size=30).to_edge(UP, buff=0.45)
        side = VGroup(
            label(rf"group A: \ a precise score, \ $\lambda$ = {T['lam0']:.1f}", font_size=18, color=WHITE_N),
            label(rf"group B: \ a noisier score, \ $\lambda$ = {T['lam1']:.1f}", font_size=18, color=BLACK_N),
            label(r"equal average ability; \\ at a high score, \\ B is paid less", font_size=18, color=WHITE),
            label(r"Arrow: \ if B expects this, \\ it pays B less to invest \\ in skills: \ beliefs \\ "
                  r"can fulfil themselves", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "A second theory needs no prejudice at all. In 1972 Edmund Phelps imagined an employer who cannot see "
            "productivity, only a noisy signal, such as a test score or an interview, and pays what the worker is "
            "expected to produce. <bookmark mark='a'/> The best guess shrinks the score towards the group's average, "
            "by more when the score is noisier. <bookmark mark='b'/> For a group whose scores the employer reads "
            "precisely, pay follows the score closely. <bookmark mark='c'/> For a group whose scores are noisier to "
            "this employer, perhaps because the interviewers share less background with them, pay is flatter. "
            "<bookmark mark='d'/> The two groups have the same average ability, yet a high scorer from the second "
            "group is paid less: equal scores, unequal pay, from statistics alone. <bookmark mark='e'/> Kenneth Arrow "
            "added the sting: if workers from a group expect their skills to be read poorly, investing in skills pays "
            "them less, so they may invest less, and the employer's belief comes true."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(d45), Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(eq, color=E.ACCENT, scale_factor=1.03))
            vo.wait_until("b")
            self.play(Create(l0), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(l1), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(p0, scale=1.5), FadeIn(p1, scale=1.5), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
