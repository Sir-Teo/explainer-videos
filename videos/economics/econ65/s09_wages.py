from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403

ORDER = ("business as usual", "every task in 20 years", "every task in 5 years")


class Wages(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Wages and labour's share", r"If machines can do every task, \ what is a person's work worth?",
             "Chapter seven. Wages and labour's share.", lit={2024: "Korinek and Suh"}, scale=("nation",),
             horizon=("a decade", "a century"))
        self.share()
        self.race()
        self.floor()

    def share(self):
        N = load("nordhaus")
        C = N["capital"]
        yrs = np.array(C["year"])
        ls = 100 * (1 - np.array(C["capital_share"]))
        ax = plane([1948, 2026], [50, 68], center=LEFT * 1.4 + DOWN * 0.3, x_length=8.8, y_length=4.6,
                   xticks=[1950, 1970, 1990, 2010], yticks=[52, 56, 60, 64, 68],
                   ylabel=r"labour's share of GDP, \ United States, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = path(ax, yrs, ls, WORK, 3.0, smooth=False)
        side = VGroup(
            label(rf"{C['year'][0]}: \ {ls[0]:.1f}\%", font_size=18, color=WORK),
            label(rf"{C['year'][-1]}: \ {ls[-1]:.1f}\%", font_size=18, color=WORK),
            label(r"the fall since 2000: \ automation, \\ superstar firms, \ trade \ (Part 39)", font_size=16,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax.ax, RIGHT, buff=0.35)
        tag = data_tag(r"Penn World Table 11.0: \ labsh, \ United States", corner=DL, font_size=12)
        with self.voiceover(
            "The task model's warning is about labour's share of income. <bookmark mark='a'/> In the United "
            f"States it was about {ls[0]:.0f} percent of GDP in {C['year'][0]}, by the Penn World Table's measure. "
            f"<bookmark mark='b'/> By {C['year'][-1]} it was about {ls[-1]:.0f} percent, most of the fall since "
            "2000. <bookmark mark='c'/> Part thirty-nine weighed the suspects: automation, superstar firms that "
            "make a lot with few workers, and trade. Six points of GDP is a great deal of money. But it is not the "
            "end of work. The question is what happens if machines can do every task."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def race(self):
        R = load("race")
        axl = plane([0, 60], [0.8, 2.8], center=LEFT * 3.5 + DOWN * 0.2, x_length=5.6, y_length=4.4,
                    xticks=[0, 20, 40, 60], yticks=[1.0, 1.5, 2.0, 2.5], xlabel=r"years", ylabel=r"the wage",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        axr = plane([0, 60], [0, 0.8], center=RIGHT * 3.3 + DOWN * 0.2, x_length=5.6, y_length=4.4,
                    xticks=[0, 20, 40, 60], yticks=[0, 0.2, 0.4, 0.6, 0.8], xlabel=r"years",
                    ylabel=r"labour's share of output", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=13)
        floor = seg(axl, 0, 1.0, 60, 1.0, GREY_B, 2.0, dashed=True)
        flab = label(r"what a machine doing the work costs", font_size=13, color=GREY_B).next_to(
            axl.ax.c2p(30, 1.0), DOWN, buff=0.1)
        wl = {k: path(axl, R[k]["year"], R[k]["w"], SCEN[k], 3.0, smooth=False) for k in ORDER}
        sl = {k: path(axr, R[k]["year"], R[k]["labour_share"], SCEN[k], 3.0, smooth=False) for k in ORDER}
        key = legend_rows([(SCEN[k], k) for k in ORDER], font_size=15).to_edge(UP, buff=0.35)
        key.arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.35)
        tag = island_tag(r"a model: \ tasks with capital that accumulates \ (after Korinek and Suh); \ "
                         r"agora.automation.race", corner=DL, font_size=12)
        bau, f20 = R["business as usual"], R["every task in 20 years"]
        with self.voiceover(
            "Take the task model and let capital accumulate, year by year, as people save. Anton Korinek and "
            "Donghyun Suh asked what happens to wages under different paths for the automation frontier. "
            "<bookmark mark='a'/> In grey, business as usual: the frontier creeps forward, but the hardest tasks "
            "keep receding ahead of it. Capital piles up, and the wage rises, from "
            f"{bau['w'][0]:.2f} to {bau['w'][-1]:.2f} in sixty years. <bookmark mark='b'/> In orange, every task "
            "becomes automatable within twenty years. For a couple of years the wage edges up; then it falls, "
            f"and from year {[k for k, w in enumerate(f20['w']) if abs(w - 1.0) < 1e-3][0]} it sits at one. "
            "<bookmark mark='c'/> In red, every task in five years: the wage falls almost at once, to the same "
            "level. <bookmark mark='d'/> Labour's share collapses in both, from "
            f"{100 * f20['labour_share'][0]:.0f} percent to {100 * f20['labour_share'][-1]:.0f}. And output? In "
            f"sixty years it grows {f20['Y'][-1] / f20['Y'][0]:.0f}-fold when every task is automated, "
            f"{bau['Y'][-1] / bau['Y'][0]:.1f}-fold under business as usual. A far richer economy, in which work "
            "earns almost none of the income."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(floor), FadeIn(flab), FadeIn(tag))
            for mk, k in zip("abc", ORDER):
                vo.wait_until(mk)
                self.play(Create(wl[k]), FadeIn(key[ORDER.index(k)]), run_time=1.8)
            vo.wait_until("d")
            self.play(*[Create(sl[k]) for k in ORDER], run_time=2.2)
        self.clear_scene()

    def floor(self):
        eq = MathTex(r"\frac{w}{A_L} \;\geq\; \frac{r}{A_K}", font_size=46).to_edge(UP, buff=0.6)
        cards = point_cards([
            (r"why one", r"once a machine can do any task, \ a person is worth what the machine doing the same "
             r"work would cost: \ $w = A_L\,r/A_K$", MACH),
            (r"why not zero", r"people still produce what they did; \ but the wage stops growing with the "
             r"economy, \ however rich it gets", WORK),
            (r"why it can rise", r"if some tasks stay human, \ and they are essential, \ their scarcity raises their "
             r"pay: \ Baumol again", NEWT),
            (r"who gets the income", r"whoever owns the machines: \ the distribution of capital becomes the "
             r"distribution of income \ (Part 40)", GDP),
        ], width=12.6, cols=2, font_size=19).next_to(eq, DOWN, buff=0.5)
        tag = published_tag(r"Korinek and Suh, \ \emph{Scenarios for the Transition to AGI}, \ NBER WP 32255 "
                            r"(2024)", corner=DL, font_size=12)
        with self.voiceover(
            "Why does the wage stop at one, in this model? <bookmark mark='a'/> Because a firm will automate a task "
            "whenever a machine is cheaper per unit of work, the wage per unit of a person's work can never stay "
            "above the cost of a machine's for long, once machines can do everything. A person is worth what the "
            "machine that could replace them costs. <bookmark mark='b'/> That is not zero: people still produce "
            "what they did. But the wage stops growing with the economy, however rich the economy gets. <bookmark "
            "mark='c'/> If some essential tasks "
            "stay human, the opposite happens: their scarcity raises their pay, the same bottleneck as in the "
            "Play-it. Korinek and Suh show that whether wages collapse or keep rising depends on whether the list "
            "of tasks only people can do runs out. <bookmark mark='d'/> Either way, more of the income goes to "
            "whoever owns the machines. The distribution of capital becomes the distribution of income, and Part "
            "forty's questions become the central ones."
        ) as vo:
            self.play(Write(eq), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
