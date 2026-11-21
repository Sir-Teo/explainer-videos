from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403

CURVES = (("at random", GREY_B), ("highest risk", NAIVE), ("largest effect (estimated)", ALGO),
          ("largest effect (truth)", TRUTHC))


class Forests(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Heterogeneous effects and policy learning", r"Who gains most from a programme, \ and how "
             r"should places be allocated?", "Chapter six. Heterogeneous effects and policy learning.",
             lit={2018: r"Wager and Athey", 2021: r"Athey and Wager"}, scale=("person", "nation"),
             horizon=("a year",))
        self.forest()
        self.policy()

    def forest(self):
        T = load("targeting")
        x = np.array(T["risk_bins"])
        ax = plane([0, 1], [0, 0.35], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.1, 0.2, 0.3],
                   xlabel=r"chance of still being out of work, \ without the programme",
                   ylabel=r"the programme's effect", xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        tru = path(ax, x, T["effect_by_risk"], TRUTHC, 3.2)
        est = path(ax, x, T["estimate_by_risk"], ALGO, 3.2)
        side = VGroup(
            label(rf"a randomized trial of {T['trial']:,} people".replace(",", "{,}"), font_size=20, color=WHITE),
            label(r"a causal forest: \ trees that split \\ where the effect differs, \ not the outcome", font_size=20,
                  color=ALGO),
            label(r"honesty: \ one half chooses the splits, \\ the other estimates the effects", font_size=20,
                  color=ALGO),
            label(r"gold: \ the truth; \ blue: \ the forest's estimate, \\ by risk", font_size=20, color=TRUTHC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Wager and Athey, \ JASA 113(523) (2018); \ the Island: \ agora.learn.targeting",
                            corner=DL, font_size=12)
        with self.voiceover(
            "To target by effects, you have to estimate them, person by person, and they are never observed: "
            "nobody is both treated and untreated. In gold, the effect the Island knows, by risk. <bookmark "
            "mark='a'/> Start from a randomized trial: on the "
            f"Island, {T['trial']:,} unemployed people, half given a place at random. <bookmark mark='b'/> Stefan "
            "Wager and Susan Athey's causal forest grows trees that split where the effect differs, not where the "
            "outcome does. <bookmark mark='c'/> And it is honest: one half of each tree's sample chooses the splits "
            "and the other half estimates the effect in each leaf, so the forest cannot fit its own noise. "
            "<bookmark mark='d'/> Averaged by risk, the forest's estimates follow the true hump, flattened at the "
            "edges where data are thin."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(tru), run_time=1.5)
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(side[k], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(Create(est), FadeIn(side[3]), run_time=1.8)
        self.clear_scene()

    def policy(self):
        T = load("targeting")
        sh = np.array(T["shares"])
        A = T["averted"]
        top = max(max(v) for v in A.values()) * 1.1
        ax = plane([0, 0.62], [0, top], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6], yticks=None, xlabel=r"share of the unemployed given a place",
                   ylabel=r"unemployment averted, \ per 100 unemployed", xfmt=lambda v: rf"{100 * v:.0f}\%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        ls = VGroup(*[path(ax, sh, A[k], c, 3.2) for k, c in CURVES])
        side = VGroup(*[label(k, font_size=19, color=c) for k, c in CURVES],
                      label(r"policy learning: \ choose the rule \\ that maximizes the estimated gain, \\ and bound "
                            r"its regret", font_size=19, color=E.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side.to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Athey and Wager, \ Econometrica 89(1) (2021); \ Kitagawa and Tetenov, \ Econometrica "
                            r"86(2) (2018)", corner=DL, font_size=12)
        with self.voiceover(
            "Now the allocation, for every size of programme. <bookmark mark='a'/> Places at random: the gain "
            "grows in proportion. <bookmark mark='b'/> By risk: less than at random until a third of the "
            "unemployed have places. <bookmark mark='c'/> By the forest's estimated effect: close to the best "
            "possible, <bookmark mark='d'/> which uses the true effects. <bookmark mark='e'/> Choosing a rule "
            "this way is policy learning, after Toru Kitagawa and Aleksey Tetenov and after Athey and Wager: "
            "pick, from a class of simple rules, the one with the largest estimated gain, and bound how much "
            "worse than the best it can be. Simple rules matter: a programme officer has to be able to apply "
            "them, and a citizen to understand them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(Create(ls[k]), FadeIn(side[k]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
