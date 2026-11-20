from __future__ import annotations

from videos.economics.econ38.common import *  # noqa: F403


class Roy(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Selection: \ Roy's model", r"What do the wages we see hide?",
             "Chapter eleven. Selection: Roy's model.", lit={1951: r"Roy", 1979: r"Heckman"}, scale=("person",),
             horizon=("a decade",))
        self.sorting()
        self.correction()

    def sorting(self):
        R = load("roy")
        w1, w2, sec = np.array(R["sample_w1"]), np.array(R["sample_w2"]), np.array(R["sample_second"], bool)
        ax = plane([1.4, 3.8], [1.0, 4.0], center=LEFT * 2.2 + DOWN * 0.4, x_length=5.4, y_length=5.0,
                   xticks=[1.5, 2, 2.5, 3, 3.5], yticks=[1.5, 2, 2.5, 3, 3.5], xlabel=r"log wage as a fisher",
                   ylabel=r"log wage at the boatyard", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        pts = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.03, color=BOAT if s else FISH, fill_opacity=0.8)
                       for a, b, s in zip(w1, w2, sec) if 1.4 < a < 3.8 and 1.0 < b < 4.0])
        diag = seg(ax, 1.4, 1.4, 3.8, 3.8, WHITE, 2, dashed=True)
        side = VGroup(
            label(r"each dot: \ one islander's \\ two possible wages", font_size=18, color=GREY_A),
            label(r"blue: \ fishes; \ gold: \\ the boatyard \ (net of \\ the cost of switching)", font_size=18,
                  color=WHITE),
            label(rf"fishers seen: \ {R['mean1_obs']:.2f}; \\ everyone as a fisher: \ {R['mean1_all']:.2f}",
                  font_size=18, color=FISH),
            label(rf"boatbuilders seen: \ {R['mean2_obs']:.2f}; \\ everyone at the boatyard: \ {R['mean2_all']:.2f}",
                  font_size=18, color=BOAT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        hc = history_card(1951, r"Andrew Roy", r"an economy of fishers and hunters: \ each person good at each to a "
                          r"different degree, \ each choosing the trade that pays them more", color=E.ACCENT,
                          width=5.0, font_size=20).move_to(ax.ax.c2p(2.6, 2.6))
        with self.voiceover(
            "Every wage we observe was chosen. In 1951 Andrew Roy imagined an economy of fishers and hunters, each "
            "person good at each to a different degree, each choosing the trade that paid them more. "
            "<bookmark mark='a'/> On the Island, each dot is a person and their two possible wages, as a fisher or at "
            "the boatyard. <bookmark mark='b'/> Each picks the larger, after the cost of switching. "
            "<bookmark mark='c'/> The fishers we see earn more as fishers than the average islander would: "
            f"{R['mean1_obs']:.2f} against {R['mean1_all']:.2f} in logs. <bookmark mark='d'/> The boatbuilders, even "
            f"more so: {R['mean2_obs']:.2f} against {R['mean2_all']:.2f}. Comparing the two trades' observed wages "
            "says little about what anyone would earn after a switch."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeOut(hc), run_time=0.5)
            self.play(FadeIn(pts, lag_ratio=0.002), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def correction(self):
        R = load("roy")
        rows = ((r"everyone, \ as fishers \ (the truth)", R["truth"], WHITE),
                (r"the fishers we see \ (naive)", R["naive"], LOSS),
                (r"Heckman's two steps", R["corrected"], WAGE))
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 1.2 - 1.0 * k
            r = Rectangle(width=(v - 2.3) * 14, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.4 + (v - 2.3) * 7, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(r, LEFT, buff=0.2).align_to(
                np.array([-0.5, 0, 0]), RIGHT), r, label(f"{v:.3f}", font_size=19, color=WHITE).next_to(r, RIGHT,
                                                                                                      buff=0.1)))
        eq = MathTex(r"E[\ln w_1 \mid \text{fishes}] = \mu_1 + \sigma_{1v}\,\lambda(Z\gamma), \quad "
                     r"\lambda = \phi/\Phi", font_size=32).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"the cost of switching moves people between trades without changing their skills: \ "
                             r"the excluded variable that makes the correction credible", 12.0, 19, GREY_A).to_edge(
            DOWN, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        steps = label(r"step 1: \ who fishes, \ by a probit on the cost of switching; \ \ step 2: \ fishers' wages, "
                      r"with $\lambda$ added", font_size=18, color=GREY_A).next_to(eq, DOWN, buff=0.3)
        from scipy.stats import norm
        lax = plane([-2.0, 2.0], [0, 2.5], center=DOWN * 0.7, x_length=5.6, y_length=2.8, xticks=[-2, -1, 0, 1, 2],
                    yticks=[0, 1, 2], xlabel=r"$Z\gamma$: \ how likely fishing was", ylabel=r"$\lambda$",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        cs = np.linspace(-2, 2, 81)
        lcur = path(lax, cs, norm.pdf(cs) / norm.cdf(cs), FISH, 3)
        lnote = label(r"the inverse Mills ratio: \ large for those \ who barely chose fishing", font_size=17,
                      color=FISH).next_to(lax.ax, RIGHT, buff=0.4)
        with self.voiceover(
            "In 1979 James Heckman showed how to undo the selection. <bookmark mark='a'/> First, model who chooses "
            "which trade; then add to the wage regression a term, the inverse Mills ratio, that measures how selected "
            "each person is. <bookmark mark='b'/> On the Island, the truth, the average fishing wage across everyone, "
            f"is {R['truth']:.3f}. <bookmark mark='c'/> The fishers we see average {R['naive']:.3f}. "
            f"<bookmark mark='d'/> Heckman's two steps give {R['corrected']:.3f}. <bookmark mark='e'/> The correction "
            "works because something, here the cost of switching, moves people between trades without changing what "
            "they could earn in either. Without such a variable the method leans on the normal distribution. Part "
            "thirty-nine meets selection again in the gender gap, where who works shapes the wages we see."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(steps, shift=DOWN * 0.1))
            self.play(FadeIn(lax), Create(lcur), FadeIn(lnote), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(lax), FadeOut(lcur), FadeOut(lnote), run_time=0.5)
            for mk, b_ in zip("bcd", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
